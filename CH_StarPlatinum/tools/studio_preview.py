"""Pack the Roblox R15 FBX for an in-Studio preview without uploads (roblox-3d-model "5 and 6" route,
extended: 15 parts at their assembled positions, per-corner normals, four SurfaceAppearance maps).

    blender --background --python tools/studio_preview.py -- <fbx> <textures dir> <serve dir>

Writes <serve>/parts.json, <serve>/<Part>.mesh.bin and <serve>/{BC,N,R,M}.tex.bin.
mesh.bin v2 (little endian): "RMSH" u32 2, nV, nUV, nN, nT, f32 pos[nV*3] (studs, Roblox axes, relative to the
part centre), f32 uv[nUV*2], f32 nrm[nN*3], u32 tri[nT*3], u32 triUV[nT*3], u32 triN[nT*3].
Axes: Blender (Z up, faces -Y) -> Roblox (Y up, faces -Z) is (x, y, z) -> (-x, z, y): a rotation (det +1),
so winding is kept (skill trap); the skill's (x, z, -y) would leave a character facing +Z.
Texture rows are written as Blender stores them (the two bottom/top conventions cancel, skill trap).
"""
import bpy, sys, os, json, struct
import numpy as np

fbx, texdir, serve = sys.argv[sys.argv.index("--") + 1:][:3]
os.makedirs(serve, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.unit_settings.scale_length = 0.01      # 1 imported unit = 1 stud
bpy.ops.import_scene.fbx(filepath=fbx, use_custom_normals=True)
parts = {}
for ob in bpy.data.objects:
    if ob.type != "MESH" or not ob.name.endswith("_Geo"):
        continue
    me = ob.data
    me.calc_loop_triangles()
    mw = np.array(ob.matrix_world)
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3) @ mw[:3, :3].T + mw[:3, 3]
    pos = np.stack([-co[:, 0], co[:, 2], co[:, 1]], 1)
    lo, hi = pos.min(0), pos.max(0)
    centre = (lo + hi) / 2
    pos = pos - centre
    nl = len(me.loops)
    uv = np.empty(nl * 2)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    cn = np.empty(nl * 3)
    me.corner_normals.foreach_get("vector", cn)
    cn = cn.reshape(-1, 3) @ mw[:3, :3].T
    cn = np.stack([-cn[:, 0], cn[:, 2], cn[:, 1]], 1)
    cn /= np.maximum(np.linalg.norm(cn, axis=1, keepdims=True), 1e-9)
    nt = len(me.loop_triangles)
    tv = np.empty(nt * 3, np.int64)
    tl = np.empty(nt * 3, np.int64)
    me.loop_triangles.foreach_get("vertices", tv)
    me.loop_triangles.foreach_get("loops", tl)
    _, fu, iu = np.unique(np.round(uv * 65535).astype(np.int64), axis=0, return_index=True, return_inverse=True)
    _, fn, inn = np.unique(np.round(cn * 32767).astype(np.int64), axis=0, return_index=True, return_inverse=True)
    iu, inn = iu.ravel(), inn.ravel()
    blob = bytearray(struct.pack("<4sIIIII", b"RMSH", 2, len(pos), len(fu), len(fn), nt))
    blob += pos.astype("<f4").tobytes() + uv[fu].astype("<f4").tobytes() + cn[fn].astype("<f4").tobytes()
    blob += tv.astype("<u4").tobytes() + iu[tl].astype("<u4").tobytes() + inn[tl].astype("<u4").tobytes()
    name = ob.name[:-4]
    open(os.path.join(serve, name + ".mesh.bin"), "wb").write(blob)
    parts[name] = {"centre": [round(float(c), 5) for c in centre], "size": [round(float(c), 4) for c in hi - lo],
                   "tris": nt}
for key in ("BC", "N", "R", "M"):
    im = bpy.data.images.load(os.path.join(texdir, f"T_StarPlatinum_{key}.png"))
    im.colorspace_settings.name = "sRGB" if key == "BC" else "Non-Color"
    n = im.size[0]
    px = np.empty(n * n * 4, np.float32)
    im.pixels.foreach_get(px)
    rgba = (np.clip(px, 0, 1) * 255).round().astype(np.uint8)
    open(os.path.join(serve, key + ".tex.bin"), "wb").write(struct.pack("<4sI", b"RTEX", n) + rgba.tobytes())
json.dump({"parts": parts, "maps": ["BC", "N", "R", "M"]}, open(os.path.join(serve, "parts.json"), "w"))
print("STUDIO_PACK", len(parts), "parts", sum(p["tris"] for p in parts.values()), "tris")
