"""Stage D: gravel path + gravel pad in front of the cabins.

His method was boolean(curve, duplicated terrain). We build the same surface directly:
a ribbon that follows the smoothed path and hugs the terrain (raycast), plus a pad
whose outline is snapped to a smooth rounded box. Both get a 'middle' colour attribute
(1 = centre, 0 = edges) that mixes his two gravel textures, exactly like his setup.

Run:  blender -b scene/forest.blend --python scripts/build_path.py
"""
import bpy, bmesh, math, os, sys, ctypes
import numpy as np
from mathutils import Vector, noise

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

ROOT = os.path.join(os.path.expanduser("~"), "blender-forest")
LIB_BLEND = os.path.join(ROOT, "assets", "Plant models", "assets", "AE_15th Assets.blend")

try:
    k = ctypes.windll.kernel32
    k.SetPriorityClass(k.GetCurrentProcess(), 0x00004000)
except Exception:
    pass

STEP = 0.12          # metres between cross sections / grid cells
COLS = 16            # vertices across the path
EDGE_FADE = 0.8      # metres over which gravel thins out into the soil
LIFT_MID, LIFT_EDGE = L.LIFT_MID, L.LIFT_EDGE   # height above terrain (no z-fighting)


def n1(x, seed):
    return noise.noise(Vector((x, seed * 13.1, seed * 7.7)))


def ground_z(terrain, x, y):
    hit, loc, *_ = terrain.ray_cast(Vector((x, y, 80.0)), Vector((0, 0, -1)))
    return loc.z if hit else 0.0


def build_ribbon(bm, terrain, mid_layer, uv_layer):
    pts = L.path_spline(STEP)
    seg = np.diff(pts, axis=0)
    tang = np.vstack([seg, seg[-1:]])
    tang /= np.linalg.norm(tang, axis=1)[:, None]
    side = np.stack([-tang[:, 1], tang[:, 0]], axis=1)
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(seg, axis=1))])
    rows = []
    for i, (p, sd, d) in enumerate(zip(pts, side, s)):
        wl = L.PATH_HALF_WIDTH * (1.0 + 0.10 * n1(d * 0.35, 1) + 0.04 * n1(d * 2.1, 2))
        wr = L.PATH_HALF_WIDTH * (1.0 + 0.10 * n1(d * 0.35, 3) + 0.04 * n1(d * 2.1, 4))
        row = []
        for j in range(COLS):
            u = -1.0 + 2.0 * j / (COLS - 1)          # -1 left edge .. +1 right edge
            w = wl if u < 0 else wr
            x, y = p + sd * (u * w)
            crown = 1.0 - u * u
            z = ground_z(terrain, x, y) + LIFT_EDGE + (LIFT_MID - LIFT_EDGE) * crown
            v = bm.verts.new((x, y, z))
            # 'middle' mask: wobbly centre band of cleaner gravel.
            mval = np.clip(crown * 1.4 - 0.25 + 0.35 * n1(d * 0.5, 5), 0.0, 1.0)
            edge = float(np.clip((1.0 - abs(u)) * w / EDGE_FADE, 0.0, 1.0))
            row.append((v, mval, edge))
        rows.append(row)
    for r0, r1 in zip(rows[:-1], rows[1:]):
        for j in range(COLS - 1):
            f = bm.faces.new((r0[j][0], r0[j + 1][0], r1[j + 1][0], r1[j][0]))
            for loop in f.loops:
                val, edge = next((m, e) for vv, m, e in (r0[j], r0[j + 1], r1[j + 1], r1[j])
                                 if vv is loop.vert)
                loop[mid_layer] = (val, edge, 0.0, 1.0)
                loop[uv_layer].uv = (loop.vert.co.x, loop.vert.co.y)
    print(f"ribbon: {len(rows)} sections, length {s[-1]:.1f} m")


def build_pad(bm, terrain, mid_layer, uv_layer):
    cx, cy = L.PAD_CENTER
    hx, hy = L.PAD_HALF
    xs = np.arange(cx - hx - 0.5, cx + hx + 0.5 + STEP, STEP)
    ys = np.arange(cy - hy - 0.5, cy + hy + 0.5 + STEP, STEP)
    gx, gy = np.meshgrid(xs, ys)
    xy = np.stack([gx.ravel(), gy.ravel()], axis=1)

    def sdf(q):
        wob = np.array([0.12 * n1(a * 0.6 + b * 0.4, 9) for a, b in q])
        return L.dist_to_pad(q) + wob

    d = sdf(xy).reshape(gy.shape)
    inside = d < 0
    keep = inside[:-1, :-1] | inside[1:, :-1] | inside[:-1, 1:] | inside[1:, 1:]
    used = np.zeros_like(inside)
    used[:-1, :-1] |= keep; used[1:, :-1] |= keep; used[:-1, 1:] |= keep; used[1:, 1:] |= keep
    verts = {}
    e = 0.02
    for (iy, ix) in zip(*np.nonzero(used)):
        p = np.array([gx[iy, ix], gy[iy, ix]])
        dv = d[iy, ix]
        if dv > 0:  # pull outside corners onto the smooth outline
            g = np.array([sdf(np.array([p + [e, 0]]))[0] - sdf(np.array([p - [e, 0]]))[0],
                          sdf(np.array([p + [0, e]]))[0] - sdf(np.array([p - [0, e]]))[0]]) / (2 * e)
            p = p - g / max(np.linalg.norm(g), 1e-6) * dv
        depth = max(-dv, 0.0)
        lift = LIFT_EDGE + (LIFT_MID - LIFT_EDGE) * min(depth / 0.6, 1.0)
        z = ground_z(terrain, p[0], p[1]) + lift
        mval = float(np.clip(0.55 + 0.3 * n1(p[0] * 0.4 + p[1] * 0.3, 11), 0, 1)) * min(depth / 0.8, 1.0)
        edge = min(depth / EDGE_FADE, 1.0)
        verts[(iy, ix)] = (bm.verts.new((p[0], p[1], z + 0.003)), mval, edge)  # just above the ribbon
    for (iy, ix) in zip(*np.nonzero(keep)):
        quad = [verts[(iy, ix)], verts[(iy, ix + 1)], verts[(iy + 1, ix + 1)], verts[(iy + 1, ix)]]
        f = bm.faces.new([q[0] for q in quad])
        for loop, (_, m, e) in zip(f.loops, quad):
            loop[mid_layer] = (m, e, 0.0, 1.0)
            loop[uv_layer].uv = (loop.vert.co.x, loop.vert.co.y)
    print(f"pad: {int(keep.sum())} quads")


def gravel_material():
    with bpy.data.libraries.load(LIB_BLEND, link=False) as (src, dst):
        dst.materials = ["AE_15th_Gravel"]
    mat = dst.materials[0]
    nt = mat.node_tree
    nodes = {n.name: n for n in nt.nodes}
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.5, 0.5, 0.5)   # UVs are metres -> one tile per 2 m
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
    for n in nt.nodes:
        if n.type == "TEX_IMAGE":
            nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
    # His two-texture mix: clean gravel ('gravel soils') in the middle, gravel+soil at edges.
    attr = nt.nodes.new("ShaderNodeVertexColor")
    attr.layer_name = "middle"
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    edge_tex, mid_tex = nodes["Image Texture.002"], nodes["Image Texture"]

    def s(sockets, name, kind):
        return next(x for x in sockets if x.name == name and x.type == kind and x.enabled)

    # 'middle' colour: R = centre band (texture mix), G = distance-from-edge (fade).
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(attr.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs[0], s(mix.inputs, "Factor", "VALUE"))
    nt.links.new(edge_tex.outputs["Color"], s(mix.inputs, "A", "RGBA"))
    nt.links.new(mid_tex.outputs["Color"], s(mix.inputs, "B", "RGBA"))
    # Lift the dark 4k scans a little (his path reads light beige in the sun).
    hsv = nt.nodes.new("ShaderNodeHueSaturation")
    hsv.inputs["Value"].default_value = 1.35
    nt.links.new(s(mix.outputs, "Result", "RGBA"), hsv.inputs["Color"])
    nt.links.new(hsv.outputs["Color"], bsdf.inputs["Base Color"])
    nodes["Image Texture.001"].image.colorspace_settings.name = "Non-Color"  # height map
    # Edge fade: gravel breaks up into the soil instead of a hard slab edge.
    noi = nt.nodes.new("ShaderNodeTexNoise")
    noi.inputs["Scale"].default_value = 3.0
    noi.inputs["Detail"].default_value = 6.0
    nt.links.new(mp.outputs["Vector"], noi.inputs["Vector"])
    add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"
    nt.links.new(sep.outputs[1], add.inputs[0])
    sub = nt.nodes.new("ShaderNodeMath"); sub.operation = "SUBTRACT"
    nt.links.new(noi.outputs["Fac"], sub.inputs[0]); sub.inputs[1].default_value = 0.5
    sc = nt.nodes.new("ShaderNodeMath"); sc.operation = "MULTIPLY"
    nt.links.new(sub.outputs[0], sc.inputs[0]); sc.inputs[1].default_value = 0.8
    nt.links.new(sc.outputs[0], add.inputs[1])
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs["From Min"].default_value = 0.25
    ramp.inputs["From Max"].default_value = 0.65
    nt.links.new(add.outputs[0], ramp.inputs["Value"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    ms = nt.nodes.new("ShaderNodeMixShader")
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    nt.links.new(ramp.outputs["Result"], ms.inputs["Fac"])
    nt.links.new(tr.outputs[0], ms.inputs[1])
    nt.links.new(bsdf.outputs[0], ms.inputs[2])
    nt.links.new(ms.outputs[0], out.inputs["Surface"])
    # Stronger pebble relief.
    for n in nt.nodes:
        if n.type == "BUMP":
            n.inputs["Strength"].default_value = 0.35
    mat.displacement_method = "BOTH"
    return mat


def main():
    for name in ("Path",):
        o = bpy.data.objects.get(name)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    terrain = bpy.data.objects["Terrain"]
    bm = bmesh.new()
    mid = bm.loops.layers.color.new("middle")
    uv = bm.loops.layers.uv.new("UVMap")
    build_ribbon(bm, terrain, mid, uv)
    if L.USE_CABINS:
        build_pad(bm, terrain, mid, uv)
    me = bpy.data.meshes.new("Path")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("Path", me)
    col = bpy.data.collections.get("Terrain")
    col.objects.link(ob)
    me.materials.append(gravel_material())
    bpy.ops.wm.save_mainfile(relative_remap=True)
    print("SAVED", bpy.data.filepath, "path verts", len(me.vertices))


main()
