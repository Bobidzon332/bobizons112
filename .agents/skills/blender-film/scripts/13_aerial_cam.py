# Aerial establishing camera for the clay build-up shot (his "CINEMATIC CITY" look: high, steep, slow drift).
# Ahead of the intersection, looking back down the avenue; the quad punches up through the crossing toward the lens.
# Keyed on scene frames 290-420 (parts A and C use 300-347 and 348-411).
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
from mathutils import Vector
sc = bpy.context.scene
o = bpy.data.objects.get("CAM_AERIAL")
if o: bpy.data.objects.remove(o)
cd = bpy.data.cameras.new("CAM_AERIAL"); cd.lens = 24; cd.sensor_width = 36; cd.clip_start = 0.1; cd.clip_end = 3000
cd.dof.use_dof = False
cam = bpy.data.objects.new("CAM_AERIAL", cd); coll("ANIMATION").objects.link(cam); cam.rotation_mode = "XYZ"
F0, F1 = 290, 420
P0, P1 = Vector((241.0, -2.5, 50.0)), Vector((236.0, 1.0, 47.5))        # above the avenue centre line, slow drift + slight descent
T0, T1 = Vector((166.0, -1.0, 1.0)), Vector((171.0, 0.0, 2.0))        # aim back down the avenue at the crossing
prev = None
for f in range(F0, F1 + 1):
    s = (f - F0) / (F1 - F0); s = s * s * (3 - 2 * s)
    p = P0.lerp(P1, s); t = T0.lerp(T1, s)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    q = (t - p).normalized().to_track_quat("-Z", "Y")
    e = q.to_euler("XYZ", prev) if prev else q.to_euler("XYZ"); prev = e
    cam.rotation_euler = e; cam.keyframe_insert("rotation_euler", frame=f)
set_interp(cam, "LINEAR")
save()
print("CAM_AERIAL keyed", F0, F1)
