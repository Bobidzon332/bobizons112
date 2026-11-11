# usage via send: PREVIEW = dict(cam="name" or None, loc=(..), look=(..), lens=35, frame=1, out="x.png", pct=50)
import bpy, os
from mathutils import Vector
sc = bpy.context.scene; P = globals().get("PREVIEW", {})
if P.get("frame"): sc.frame_set(P["frame"])
cam = bpy.data.objects.get(P.get("cam") or "")
if cam is None:
    cd = bpy.data.cameras.get("_prev") or bpy.data.cameras.new("_prev")
    cam = bpy.data.objects.get("_prevcam") or bpy.data.objects.new("_prevcam", cd)
    if cam.name not in sc.collection.objects: sc.collection.objects.link(cam)
    cam.location = P["loc"]; cd.lens = P.get("lens", 35)
    cam.rotation_euler = (Vector(P["look"]) - Vector(P["loc"])).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam
sc.render.resolution_percentage = P.get("pct", 25)
sc.eevee.taa_render_samples = P.get("samples", 8)
out = os.path.expanduser("~/blender-car-film/previews/" + P.get("out", "prev.png"))
os.makedirs(os.path.dirname(out), exist_ok=True)
sc.render.filepath = out; bpy.ops.render.render(write_still=True)
sc.render.resolution_percentage = 100
print("preview", out)
