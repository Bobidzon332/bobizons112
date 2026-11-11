"""His Porsche 992 GT3 RS + our own car rig (no Rig-A-Car add-on).

His file already splits the car onto 9 empties (mycar_body, mycar_wheel.Ft/Bk.L/R,
mycar_wheelbrake.*). We append those empties with everything under them, drop his armature,
camera, light and road, and drive the car ourselves, baked per frame from scripts/car.json:
  * follows the gravel road spline (layout.path_spline) at the keyed speeds
  * height / pitch / roll from the ground under the four tyres (raycast road + terrain)
  * small gravel bob on the body
  * wheels spin from distance travelled (s / radius), front wheels + brakes steer from curvature

  blender -b scene/forest.blend --python scripts/build_car.py        (saves the .blend)
"""
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix, Euler, noise

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import layout as L

ROOT = os.path.dirname(HERE)
CAR_BLEND = os.path.join(ROOT, "quarantine", "Porsche Gtr_Rigged", "Porsche Gtr_Rigged.blend")
C = json.load(open(os.path.join(HERE, "car.json"), encoding="utf-8"))
sc = bpy.context.scene
RIG = ["mycar_body"] + [f"mycar_{k}.{a}.{s}" for k in ("wheel", "wheelbrake") for a in ("Ft", "Bk") for s in ("L", "R")]


def clear_previous():
    col = bpy.data.collections.get("Car")
    if col:
        for o in list(col.all_objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(col)


def descendants(o):
    out = [o]
    for c in o.children:
        out += descendants(c)
    return out


def import_car():
    with bpy.data.libraries.load(CAR_BLEND, link=False) as (src, dst):
        dst.objects = list(src.objects)
    col = bpy.data.collections.new("Car")
    sc.collection.children.link(col)
    for o in dst.objects:
        if o is not None:
            col.objects.link(o)
    bpy.context.view_layer.update()
    keep = set()
    for n in RIG:
        keep.update(descendants(bpy.data.objects[n]))
    # Freeze each rig empty where his rig had it, then cut it loose from his armature.
    world = {n: bpy.data.objects[n].matrix_world.copy() for n in RIG}
    for n in RIG:
        o = bpy.data.objects[n]
        o.constraints.clear()
        o.animation_data_clear()
        o.parent = None
        o.matrix_world = world[n]
    dropped = [o for o in col.objects if o not in keep]
    print(f"car: keep {len(keep)} objects, drop {len(dropped)}:",
          sorted({o.type for o in dropped}), [o.name for o in dropped][:12])
    for o in dropped:
        bpy.data.objects.remove(o, do_unlink=True)
    return col


def car_frame():
    P = {n: bpy.data.objects[n].matrix_world.translation.copy() for n in RIG}
    front = (P["mycar_wheel.Ft.L"] + P["mycar_wheel.Ft.R"]) / 2
    back = (P["mycar_wheel.Bk.L"] + P["mycar_wheel.Bk.R"]) / 2
    fwd = (front - back); fwd.z = 0; fwd.normalize()
    wb = (front - back).length
    track = (P["mycar_wheel.Ft.L"] - P["mycar_wheel.Ft.R"]).length
    # Tyre radius from the wheel's own meshes.
    w = bpy.data.objects["mycar_wheel.Ft.L"]
    zs = [(m.matrix_world @ Vector(c)).z for m in descendants(w) if m.type == "MESH" for c in m.bound_box]
    radius = (max(zs) - min(zs)) / 2
    ground = min(zs)
    mid = (front + back) / 2
    print(f"car: wheelbase {wb:.2f} m, track {track:.2f} m, tyre radius {radius:.3f} m")
    return mid, fwd, wb, track, radius, ground


def build_root(mid, fwd, ground):
    root = bpy.data.objects.new("CarRoot", None)
    root.empty_display_size = 2
    bpy.data.collections["Car"].objects.link(root)
    yaw = math.atan2(fwd.y, fwd.x) - math.pi / 2          # root +Y = car forward
    root.matrix_world = Matrix.Translation((mid.x, mid.y, ground)) @ Matrix.Rotation(yaw, 4, "Z")
    bpy.context.view_layer.update()
    inv = root.matrix_world.inverted()
    rest = {}
    for n in RIG:
        o = bpy.data.objects[n]
        mw = o.matrix_world.copy()
        o.parent = root
        o.matrix_parent_inverse = Matrix.Identity(4)
        o.matrix_basis = inv @ mw
        rest[n] = o.matrix_basis.copy()
    return root, rest


def road():
    pts = L.path_spline(0.05)
    seg = np.diff(pts, axis=0)
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(seg, axis=1))])
    if C["direction"] < 0:
        pts = pts[::-1]
        s = s[-1] - s[::-1]

    def at(d):
        d = float(np.clip(d, 0.0, s[-1] - 0.01))
        i = int(np.searchsorted(s, d) - 1)
        i = max(0, min(i, len(pts) - 2))
        t = (d - s[i]) / max(s[i + 1] - s[i], 1e-9)
        p = pts[i] + (pts[i + 1] - pts[i]) * t
        tg = pts[i + 1] - pts[i]
        tg = tg / np.linalg.norm(tg)
        return p, tg
    return at, s[-1]


def ground_z(x, y):
    best = None
    for name in ("Path", "Terrain"):
        ob = bpy.data.objects.get(name)
        hit, loc, *_ = ob.ray_cast(Vector((x, y, 60.0)), Vector((0, 0, -1)))
        if hit:
            z = (ob.matrix_world @ loc).z
            best = z if best is None else max(best, z)
    return best if best is not None else 0.0


def distance_curve():
    f0, f1 = C["frames"]
    keys = C["speed"]
    fr = np.arange(f0, f1 + 1)
    v = np.interp(fr, [k[0] for k in keys], [k[1] for k in keys])
    d = C["s0"] + np.concatenate([[0.0], np.cumsum(v[:-1] / sc.render.fps)])
    return fr, d


def animate(root, rest, wb, track, radius):
    at, length = road()
    fr, dist = distance_curve()
    lat = C.get("lateral", 0.0)
    bob = C.get("bob_mm", 6.0) / 1000.0
    prev_heading = None
    for f, d in zip(fr, dist):
        p, tg = at(d)
        side = np.array([tg[1], -tg[0]])                     # right of travel
        centre = p + side * lat
        heading = math.atan2(tg[1], tg[0])
        # Four tyre contacts on the ground.
        pf, tf = at(d + wb / 2)
        pr, tr = at(d - wb / 2)
        sf, sr = np.array([tf[1], -tf[0]]), np.array([tr[1], -tr[0]])
        zfl = ground_z(*(pf + sf * (lat - track / 2)))
        zfr = ground_z(*(pf + sf * (lat + track / 2)))
        zrl = ground_z(*(pr + sr * (lat - track / 2)))
        zrr = ground_z(*(pr + sr * (lat + track / 2)))
        pitch = math.atan2(((zfl + zfr) - (zrl + zrr)) / 2, wb)
        roll = math.atan2(((zfr + zrr) - (zfl + zrl)) / 2, track)
        t = f / sc.render.fps
        z = (zfl + zfr + zrl + zrr) / 4 + bob * noise.noise(Vector((t * 7.0, 0.3, 0.0)))
        pitch += 0.004 * noise.noise(Vector((t * 5.0, 1.7, 0.0)))
        roll += 0.003 * noise.noise(Vector((t * 4.0, 3.1, 0.0)))
        root.location = (centre[0], centre[1], z)
        root.rotation_mode = "YXZ"                       # R = Rz(yaw) Rx(pitch) Ry(roll)
        yaw = heading - math.pi / 2
        if prev_heading is not None:                     # unwrap yaw too
            yaw = prev_heading + ((yaw - prev_heading + math.pi) % (2 * math.pi) - math.pi)
        prev_heading = yaw
        root.rotation_euler = (pitch, -roll, yaw)
        root.keyframe_insert("location", frame=int(f))
        root.keyframe_insert("rotation_euler", frame=int(f))
        # Steering from road curvature (bicycle model), clamped.
        p2, t2 = at(d + 1.0)
        dh = math.atan2(t2[1], t2[0]) - heading
        dh = (dh + math.pi) % (2 * math.pi) - math.pi
        steer = max(-0.5, min(0.5, math.atan(wb * dh / 1.0)))
        spin = (d - C["s0"]) / radius
        for n in RIG[1:]:
            o = bpy.data.objects[n]
            r = rest[n]
            loc = r.to_translation()
            rot = r.to_3x3().to_4x4()
            m = Matrix.Translation(loc)
            if ".Ft." in n:
                m = m @ Matrix.Rotation(steer, 4, "Z")
            if "wheelbrake" not in n:
                m = m @ Matrix.Rotation(-spin, 4, "X")
            prev = o.rotation_euler.copy()
            o.matrix_basis = m @ rot
            # Keep Euler angles continuous frame to frame (no +180 -> -180 wrap), otherwise
            # motion blur interpolates a backwards near-full turn and smears the tyre.
            o.rotation_euler = o.rotation_euler.to_matrix().to_euler(o.rotation_mode, prev)
            o.keyframe_insert("location", frame=int(f))
            o.keyframe_insert("rotation_euler", frame=int(f))
    print(f"car: drove {dist[-1] - dist[0]:.1f} m over {len(fr)} frames (road {length:.0f} m)")


def main():
    clear_previous()
    import_car()
    mid, fwd, wb, track, radius, ground = car_frame()
    root, rest = build_root(mid, fwd, ground)
    # His model is oversized; scale to the real 992 GT3 RS wheelbase (2.46 m).
    k = C.get("real_wheelbase", 2.46) / wb
    root.scale = (k, k, k)
    wb, track, radius = wb * k, track * k, radius * k
    print(f"car: scaled x{k:.3f} -> wheelbase {wb:.2f}, track {track:.2f}, tyre r {radius:.3f}")
    animate(root, rest, wb, track, radius)
    sc.frame_set(C["frames"][0])
    bpy.ops.wm.save_mainfile(relative_remap=True)
    print("SAVED", bpy.data.filepath)


main()
