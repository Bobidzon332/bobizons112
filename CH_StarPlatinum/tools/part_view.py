"""Debug render: colour each face of the delivery mesh by its r15_part attribute (front + back, workbench)."""
import bpy, sys, colorsys, math
from mathutils import Vector
blend, out = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.open_mainfile(filepath=blend)
ob = bpy.data.objects["CH_StarPlatinum_LOD0"]
me = ob.data
parts = [0] * len(me.polygons)
me.attributes["r15_part"].data.foreach_get("value", parts)
ca = me.color_attributes.new("partcol", "BYTE_COLOR", "CORNER")
for p in me.polygons:
    h = (parts[p.index] * 0.37) % 1.0
    c = colorsys.hsv_to_rgb(h, 0.75, 0.95)
    for li in p.loop_indices:
        ca.data[li].color = (*c, 1)
me.color_attributes.active_color = ca
for o in bpy.data.objects:
    o.hide_render = o is not ob and o.type == "MESH"
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "FLAT"
sc.display.shading.color_type = "VERTEX"
sc.render.resolution_x, sc.render.resolution_y = 500, 1000
cam_d = bpy.data.cameras.new("dbgcam")
cam_d.type = "ORTHO"
cam_d.ortho_scale = 2.3
cam = bpy.data.objects.new("dbgcam", cam_d)
sc.collection.objects.link(cam)
sc.camera = cam
for nm, loc, rot in (("front", (0, -5, 1.07), (math.radians(90), 0, 0)), ("back", (0, 5, 1.07), (math.radians(90), 0, math.pi))):
    cam.location = loc
    cam.rotation_euler = rot
    sc.render.filepath = f"{out}/parts_{nm}.png"
    bpy.ops.render.render(write_still=True)
