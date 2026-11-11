"""Stage F: the 5 shots of his first 16 s, driven by scripts/shots.json.

Per shot: an animated camera (start -> end pose, linear or eased, optional handheld noise),
lens + depth of field, its own sun angle/strength (switched on the cut, so every shot can match
his lighting), and optional hand-placed hero props (fallen log, rocks...) from his library.
Timeline markers switch cameras on the cuts. Frame 1 = 0.0 s, 30 fps.

  blender -b scene/forest.blend --python scripts/build_shots.py          (saves the .blend)

Pose format: {"pos": [x, y, h], "yaw": deg, "pitch": deg, "roll": deg}
  h = height above the ground at (x, y); yaw 0 = looking +Y; pitch 90 = level, <90 = looking down.
"""
import bpy, json, math, os, sys
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIB_BLEND = os.path.join(ROOT, "assets", "Plant models", "assets", "AE_15th Assets.blend")
S = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
sc = bpy.context.scene
terrain = bpy.data.objects["Terrain"]


def ground(x, y):
    """Highest surface under (x, y): deck, path or terrain (so cameras on the deck sit right)."""
    best = None
    for name in ("Deck", "Path", "Terrain"):           # walkable surfaces only (never tree tops)
        ob = bpy.data.objects.get(name)
        if not ob:
            continue
        hit, loc, *_ = ob.ray_cast(Vector((x, y, 60.0)), Vector((0, 0, -1)))
        if hit:
            z = (ob.matrix_world @ loc).z
            best = z if best is None else max(best, z)
    return best if best is not None else 0.0


def fcurves(obj):
    """All F-curves of an object's action (Blender 5 layered actions, or legacy)."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    try:
        out = []
        for layer in act.layers:
            for strip in layer.strips:
                bag = strip.channelbag(ad.action_slot)
                if bag:
                    out.extend(bag.fcurves)
        return out
    except AttributeError:
        return list(act.fcurves)


def clear_previous():
    for o in list(bpy.data.objects):
        if o.name.startswith("CAM_") or o.name.startswith("HERO_"):
            bpy.data.objects.remove(o, do_unlink=True)
    sc.timeline_markers.clear()
    sun = bpy.data.objects.get("Sun")
    if sun and sun.animation_data:
        sun.animation_data_clear()
        sun.data.animation_data_clear()


def pose(obj, p, frame):
    x, y, h = p["pos"]
    # Parented cameras (e.g. bolted to the car) use plain local coordinates.
    obj.location = (x, y, h) if obj.parent else (x, y, ground(x, y) + h)
    obj.rotation_euler = (math.radians(p["pitch"]), math.radians(p.get("roll", 0.0)), math.radians(p["yaw"]))
    obj.keyframe_insert("location", frame=frame)
    obj.keyframe_insert("rotation_euler", frame=frame)


def make_camera(shot):
    d = bpy.data.cameras.new("CAM_" + shot["name"])
    d.lens = shot.get("lens", 24)
    d.sensor_width = 36
    d.clip_start, d.clip_end = 0.05, 400
    cam = bpy.data.objects.new("CAM_" + shot["name"], d)
    sc.collection.objects.link(cam)
    cam["shot"] = shot["name"]
    if shot.get("parent"):
        cam.parent = bpy.data.objects[shot["parent"]]
        cam.matrix_parent_inverse = Matrix.Identity(4)
    pano = shot.get("pano")
    if pano:                                    # his car shot: panoramic fisheye (FOV 200, lens 23)
        d.type = "PANO"
        try:
            d.panorama_type = pano.get("type", "FISHEYE_EQUISOLID")
            d.fisheye_fov = math.radians(pano.get("fov", 200))
            d.fisheye_lens = pano.get("lens", 23)
        except AttributeError:
            d.cycles.panorama_type = pano.get("type", "FISHEYE_EQUISOLID")
            d.cycles.fisheye_fov = math.radians(pano.get("fov", 200))
            d.cycles.fisheye_lens = pano.get("lens", 23)
    pose(cam, shot["cam_start"], shot["start"])
    pose(cam, shot["cam_end"], shot["end"])
    ease = shot.get("ease", "linear")
    for fc in fcurves(cam):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR" if ease == "linear" else "BEZIER"
            if ease != "linear":
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
        shake = shot.get("shake", 0.0)
        if shake > 0:
            m = fc.modifiers.new("NOISE")
            is_rot = fc.data_path == "rotation_euler"
            m.strength = shake * (0.02 if is_rot else 1.0)      # metres / radians
            m.scale = 18.0
            m.phase = 13.0 * fc.array_index + (5 if is_rot else 0)
    # Depth of field: focus on the frame centre at the shot's middle pose (or a fixed distance).
    d.dof.use_dof = shot.get("fstop", 0) > 0
    if d.dof.use_dof:
        d.dof.aperture_fstop = shot["fstop"]
        f = shot.get("focus", "auto")
        if f == "auto":
            sc.frame_set((shot["start"] + shot["end"]) // 2)
            dg = bpy.context.evaluated_depsgraph_get()
            fwd = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
            hit, loc, *_ = sc.ray_cast(dg, cam.matrix_world.translation, fwd)
            d.dof.focus_distance = (loc - cam.matrix_world.translation).length if hit else 10.0
        else:
            d.dof.focus_distance = float(f)
    m = sc.timeline_markers.new(shot["name"], frame=shot["start"])
    m.camera = cam
    return cam


def key_sun(shot):
    sun = bpy.data.objects["Sun"]
    s = shot.get("sun")
    if not s:
        return
    az, el = math.radians(s["azimuth"]), math.radians(s["elevation"])
    to_sun = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    sun.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()
    sun.keyframe_insert("rotation_euler", frame=shot["start"])
    if "energy" in s:
        sun.data.energy = s["energy"]
        sun.data.keyframe_insert("energy", frame=shot["start"])


_PROP_COLS = {}


def hero(p, i):
    name = p["name"]
    if name not in _PROP_COLS:
        col = bpy.data.collections.get("PROP_" + name)
        if not col:
            with bpy.data.libraries.load(LIB_BLEND, link=True) as (src, dst):
                dst.objects = [name]
            src_ob = dst.objects[0]
            col = bpy.data.collections.new("PROP_" + name)
            props = bpy.data.collections.get("PROPS")
            if not props:                       # hidden holder for linked library props
                props = bpy.data.collections.new("PROPS")
                sc.collection.children.link(props)
                bpy.context.view_layer.layer_collection.children["PROPS"].exclude = True
            props.children.link(col)
            col.objects.link(src_ob)
            mw = src_ob.matrix_basis
            bb = [mw @ Vector(c) for c in src_ob.bound_box]
            col.instance_offset = (sum(v.x for v in bb) / 8, sum(v.y for v in bb) / 8, min(v.z for v in bb))
        _PROP_COLS[name] = col
    e = bpy.data.objects.new(f"HERO_{i}_{name}", None)
    e.instance_type = "COLLECTION"
    e.instance_collection = _PROP_COLS[name]
    col = bpy.data.collections.get("Hero") or bpy.data.collections.new("Hero")
    if col.name not in sc.collection.children:
        sc.collection.children.link(col)
    col.objects.link(e)
    x, y = p["pos"][:2]
    e.location = (x, y, ground(x, y) + p.get("z", 0.0))
    e.rotation_euler = (0, 0, math.radians(p.get("rot", 0.0)))
    e.scale = (p.get("scale", 1.0),) * 3


def main():
    clear_previous()
    sc.render.fps = S.get("fps", 30)
    for i, shot in enumerate(S["shots"]):
        make_camera(shot)
        key_sun(shot)
        for j, p in enumerate(shot.get("props", [])):
            hero(p, f"{i}{j}")
    sun = bpy.data.objects["Sun"]
    for ob in (sun, sun.data):
        if ob.animation_data and ob.animation_data.action:
            for fc in fcurves(ob):
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"          # sun jumps on the cut
    sc.frame_start = S["shots"][0]["start"]
    sc.frame_end = S.get("frame_end", S["shots"][-1]["end"])
    sc.frame_set(sc.frame_start)
    sc.camera = bpy.data.objects["CAM_" + S["shots"][0]["name"]]
    bpy.ops.wm.save_mainfile(relative_remap=True)
    print("SHOTS built:", [s["name"] for s in S["shots"]], "frames", sc.frame_start, sc.frame_end)


main()
