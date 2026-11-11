"""Place a look-dev camera from env CAM="x,y,height,yaw_deg,pitch_deg,lens" (height above ground)."""
import bpy, os, math
from mathutils import Vector
x, y, h, yaw, pitch, lens = [float(v) for v in os.environ["CAM"].split(",")]
sc = bpy.context.scene
dg = bpy.context.evaluated_depsgraph_get()
t = bpy.data.objects["Terrain"]
hit, loc, *_ = t.ray_cast(Vector((x, y, 60)), Vector((0, 0, -1)))
d = bpy.data.cameras.new("TestCam"); d.lens = lens; d.clip_start = 0.05; d.clip_end = 400
c = bpy.data.objects.new("TestCam", d); sc.collection.objects.link(c)
c.location = (x, y, (loc.z if hit else 0) + h)
c.rotation_euler = (math.radians(pitch), 0, math.radians(yaw))
sc.camera = c
