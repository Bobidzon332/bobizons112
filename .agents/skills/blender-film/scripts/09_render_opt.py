# Render optimisation without visual loss:
#  * trees: the Poly Haven file stacks a complete tree (LOD0) + a separate trunk + leaf-clump sources + a 2nd demo tree
#    5 m away into the instanced collection -> keep LOD0 only; trees > 30 m from every shot camera use LOD1 (same tree,
#    1/3 of the faces; at that distance + DOF there is no visible difference)
#  * OIDN denoising on the GPU (same denoiser, runs on the RTX instead of the CPU)
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
from mathutils import Vector
sc = bpy.context.scene
SHOTS = [("CAM_ROOF", 2, 22), ("Camera", 23, 62), ("Camera", 145, 180), ("Camera", 300, 372), ("CAM_LOW", 438, 462), ("CAM_HERO", 476, 525)]
lib = bpy.data.collections["PROP_tree_small_02"]
lod0 = bpy.data.objects["tree_small_02_LOD0"]
for o in list(lib.objects):
    if o is not lod0:
        bpy.data.objects.remove(o)
pl = bpy.data.collections["PROP LIBRARY"]
c1 = bpy.data.collections.get("PROP_tree_small_02_LOD1") or bpy.data.collections.new("PROP_tree_small_02_LOD1")
if c1.name not in pl.children: pl.children.link(c1)
for o in list(c1.objects): bpy.data.objects.remove(o)
lod1 = bpy.data.objects.get("tree_small_02_LOD1")
if lod1 is None:
    p = os.path.join(ROOT, "downloads", "polyhaven", "tree_small_02", "tree_small_02_1k.blend")
    with bpy.data.libraries.load(p, link=False) as (df, dt):
        dt.objects = ["tree_small_02_LOD1"]
    lod1 = dt.objects[0]
for uc in list(lod1.users_collection): uc.objects.unlink(lod1)
c1.objects.link(lod1)
lod1.location = lod0.location.copy(); lod1.rotation_euler = lod0.rotation_euler.copy(); lod1.scale = lod0.scale.copy()
for o in [o for o in bpy.data.objects if o.name.startswith("tree_small_02_leaves_") and o.name.endswith("LOD1") and not o.users_collection]:
    bpy.data.objects.remove(o)

cams = []
for cn, f0, f1 in SHOTS:
    cam = bpy.data.objects[cn]
    for f in range(f0, f1 + 1, 2):
        sc.frame_set(f); cams.append(cam.matrix_world.translation.copy())
near = far = 0
for o in bpy.data.collections["STREET"].objects:
    if not o.name.startswith("tree"): continue
    p = o.matrix_world.translation + Vector((0, 0, 3.0))
    d = min((p - c).length for c in cams)
    if d > 30:
        o.instance_collection = c1; far += 1
    else:
        o.instance_collection = lib; near += 1
sc.cycles.denoising_use_gpu = True
sc.frame_set(1)
save()
dg = bpy.context.evaluated_depsgraph_get()
faces = sum(len(i.object.data.polygons) for i in dg.object_instances if i.object.type == "MESH")
print("trees near (full)", near, "far (LOD1)", far, "scene faces now %.1f M" % (faces / 1e6))
