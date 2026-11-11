"""Phase 05a: UVs. Every LOW part is unwrapped (body: seams on R15-part x front/back chart borders,
angle-based; hard-surface gear: smart project), then everything is joined into one delivery mesh
CH_StarPlatinum_LOD0 in EXPORT with a single shared atlas: islands averaged to one texel density,
the face chart scaled up for detail, packed with a 4 px (2k) margin. The int face attributes r15_part
and region ride along for the painter (05c) and the R15 split (06).

blender --background --python build/05a_uv.py -- [--master ...]
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Vector
import bt
import sp_lib as L
import sp_r15 as R

L.setup("05a_uv")
FACE_SCALE = 1.8        # extra linear texel density for the face chart
MARGIN = 0.0015         # UV units (3 px at 2048, 1.5 px at the 1024 Roblox maps)


def edit_ops(ob, fn):
    vl = bpy.context.view_layer
    vl.objects.active = ob
    for o in vl.objects:
        o.select_set(o == ob)
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob],
                                   selected_editable_objects=[ob]):
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        fn()
        bpy.ops.object.mode_set(mode="OBJECT")


def body_charts(ob):
    """chart id per face = part * 2 + side (0 front, 1 back) relative to the part's bone axis."""
    segs = R.segments()
    parts = [0] * len(ob.data.polygons)
    ob.data.attributes["r15_part"].data.foreach_get("value", parts)
    charts = []
    for p, part in zip(ob.data.polygons, parts):
        a, b, _ = segs[R.R15_PARTS[part]]
        c = ob.matrix_world @ p.center
        _, t = R.seg_dist(c, a, b)
        axis_pt = a + (b - a) * t
        charts.append(part * 2 + (0 if c.y < axis_pt.y else 1))
    return charts


def mark_chart_seams(ob, charts):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    for e in bm.edges:
        lf = e.link_faces
        e.seam = len(lf) == 2 and charts[lf[0].index] != charts[lf[1].index]
    bm.to_mesh(ob.data)
    bm.free()


def main():
    a = L.args()
    bt.open_master(a.master)
    bt.clear_owned()
    lows = [o for o in bt.col("LOW").objects if o.type == "MESH"]
    face_charts = {}
    for o in lows:
        if not o.data.uv_layers:
            o.data.uv_layers.new(name="UVMap")
        if R.base_of(o.name) == "Body":
            ch = body_charts(o)
            mark_chart_seams(o, ch)
            face_charts[o.name] = ch
            edit_ops(o, lambda: bpy.ops.uv.unwrap(method="ANGLE_BASED", margin=0.001))
        else:
            edit_ops(o, lambda: bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.001,
                                                         scale_to_bounds=False))
    # flag the face chart before joining: Head part, front side, skin
    for o in lows:
        me = o.data
        flag = me.attributes.get("uv_face") or me.attributes.new("uv_face", "INT", "FACE")
        vals = [0] * len(me.polygons)
        if o.name in face_charts:
            head_front = R.PART_INDEX["Head"] * 2
            vals = [1 if c == head_front else 0 for c in face_charts[o.name]]
        flag.data.foreach_set("value", vals)
    out = bt.join_meshes(L.name("LOD0", "tmp"), lows, "EXPORT")
    out.name = "CH_StarPlatinum_LOD0"
    out.data.name = "CH_StarPlatinum_LOD0"
    edit_ops(out, lambda: bpy.ops.uv.average_islands_scale())
    # enlarge the face chart about its own centre
    me = out.data
    uv = me.uv_layers["UVMap"].data
    flags = [0] * len(me.polygons)
    me.attributes["uv_face"].data.foreach_get("value", flags)
    loops = [li for p in me.polygons if flags[p.index] for li in p.loop_indices]
    if loops:
        c = sum((uv[li].uv for li in loops), Vector((0, 0))) / len(loops)
        for li in loops:
            uv[li].uv = c + (uv[li].uv - c) * FACE_SCALE
    edit_ops(out, lambda: bpy.ops.uv.pack_islands(rotate=True, margin=MARGIN, scale=True, margin_method="FRACTION",
                                                   shape_method="CONCAVE", rotate_method="ANY"))
    me.attributes.remove(me.attributes["uv_face"])
    mat = bpy.data.materials.get("MAT_StarPlatinum") or bpy.data.materials.new("MAT_StarPlatinum")
    me.materials.clear()
    me.materials.append(mat)
    bt.shade_smooth(out, math.radians(180))
    tris = sum(len(p.vertices) - 2 for p in me.polygons)
    bt.log("delivery mesh", out.name, "tris", tris, "uv layers", [l.name for l in me.uv_layers])
    bt.save_master(a.master)


main()
