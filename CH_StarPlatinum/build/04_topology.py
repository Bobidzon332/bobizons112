"""Phase 04: topology. Builds the LOW delivery meshes over the approved forms:
  * body: QuadriFlow retopology (X-symmetric quads) of the HIGH sculpt, shrinkwrapped back onto it
  * gear: the same builders at LOW segment counts (separate objects, rigid attachments)
  * coverage cuts: body faces hidden under rigid gear on the same R15 part are removed
  * every face gets int attributes r15_part and region (painter colour role)
  * delivery triangulation is locked here, before UVs and baking
Removes the phase-02 blockout from LOW.

blender --background --python build/04_topology.py -- [--master ...]
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import bt
import sp_lib as L
import sp_gear as G
import sp_r15 as R

L.setup("04_topology")
BODY_VOXEL = 0.019           # ~7.5k quads before coverage cuts (budget: body <= 12k tris)
CULL_BY = ("Hair", "Scarf", "Bracer", "WristRing", "Glove", "BootShaft", "BootFoot", "BootHeel", "AnkleRing")


def quadriflow(ob, faces):
    vl = bpy.context.view_layer
    vl.objects.active = ob
    for o in vl.objects:
        o.select_set(o == ob)
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob],
                                   selected_editable_objects=[ob]):
        bpy.ops.object.quadriflow_remesh(target_faces=faces, use_mesh_symmetry=True, use_preserve_sharp=False,
                                         use_preserve_boundary=False, seed=7, mode="FACES")


def set_face_attr(ob, attr, values):
    me = ob.data
    a = me.attributes.get(attr) or me.attributes.new(attr, "INT", "FACE")
    a.data.foreach_set("value", values)


def triangulate(ob):
    t = ob.modifiers.new("Triangulate", "TRIANGULATE")
    t.quad_method = "BEAUTY"
    t.ngon_method = "BEAUTY"
    t.keep_custom_normals = True
    L.apply_mods(ob)


def main():
    a = L.args()
    bt.open_master(a.master)
    bt.clear_owned()
    bt.clear_owned("phase:02_blockout")
    high = bpy.data.objects[L.name("Body", "HIGH")]

    # body retopology: coarse voxel remesh gives an even all-quad shell (QuadriFlow refuses this mesh in
    # Blender 5.2 even though it is manifold), relaxed and shrinkwrapped back onto the sculpt
    body = bt.duplicate(high, L.name("Body", "LOD0"), "LOW")
    r = body.modifiers.new("Remesh", "REMESH")
    r.mode = "VOXEL"
    r.voxel_size = BODY_VOXEL
    L.apply_mods(body)
    for _ in range(2):
        sm = body.modifiers.new("Relax", "SMOOTH")
        sm.factor = 0.5
        sm.iterations = 4
        sw = body.modifiers.new("Shrinkwrap", "SHRINKWRAP")
        sw.target = high
        sw.wrap_method = "NEAREST_SURFACEPOINT"
        L.apply_mods(body)
    bt.shade_smooth(body, 3.2)

    # gear
    gear = G.build_all_gear(seg=1.0, collection="LOW")
    for o in gear:
        if "BootShaft" in o.name:
            s = o.modifiers.new("Solidify", "SOLIDIFY")
            s.thickness = 0.006
            s.offset = -1.0
            s.use_even_offset = True
            L.apply_mods(o)

    # coverage cuts: a body face is hidden when a ray along its normal leaves a rigid gear shell within 5 cm
    occ = bt.join_meshes("_occluders", [o for o in gear if any(k in o.name for k in CULL_BY)], "LOW")
    obm = bmesh.new()
    obm.from_mesh(occ.data)          # joined in world space, identity transform
    tree = BVHTree.FromBMesh(obm)
    obm.free()
    bm = bmesh.new()
    bm.from_mesh(body.data)
    bm.normal_update()
    dead = []
    segs0 = R.segments()
    for f in bm.faces:
        c, n = f.calc_center_median(), f.normal
        # everything inside the boots goes: the shin and foot under the shell can poke through it
        if c.z < G.BOOT_TOP.z - 0.012 and R.nearest_part(c, segs0) in (
                "RightLowerLeg", "LeftLowerLeg", "RightFoot", "LeftFoot"):
            dead.append(f)
            continue
        origin, travelled = c + n * 0.001, 0.0
        for _ in range(4):
            hit, hn, idx, dist = tree.ray_cast(origin, n, 0.05 - travelled)
            if hit is None:
                break
            if hn.dot(n) > 0.2:
                dead.append(f)
                break
            travelled += dist + 0.0005
            origin = hit + n * 0.0005
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bm.to_mesh(body.data)
    bm.free()
    L.remove_object(occ)
    bt.log("coverage cut faces", len(dead))

    # attributes + triangulation
    segs = R.segments()
    lows = [o for o in bt.col("LOW").objects if o.type == "MESH"]
    for o in lows:
        triangulate(o)
        base = R.base_of(o.name)
        if base == "Body":
            parts, regs = [], []
            for p in o.data.polygons:
                parts.append(R.PART_INDEX[R.nearest_part(o.matrix_world @ p.center, segs)])
                regs.append(R.REGION_INDEX["skin"])
        else:
            n = len(o.data.polygons)
            parts = [R.PART_INDEX[R.GEAR_PART[base]]] * n
            regs = [R.REGION_INDEX[R.GEAR_REGION[base]]] * n
        set_face_attr(o, "r15_part", parts)
        set_face_attr(o, "region", regs)
    report = {}
    for o in lows:
        report[R.base_of(o.name)] = len(o.data.polygons)
    total = sum(report.values())
    bt.log("LOW tris", total, sorted(report.items(), key=lambda kv: -kv[1])[:8])
    bt.save_master(a.master)


main()
