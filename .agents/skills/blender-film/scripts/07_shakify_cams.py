# Shakify (real recorded camera motion) on every shot camera, replacing the procedural noise curves.
# + CAM_LOW: street-level close-up, lens 0.45 m above the wet asphalt, the quad dives down the block straight at it,
#   flares hard and hangs right in front of the lens.
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
import json
from mathutils import Vector
sc = bpy.context.scene
dp = json.load(open(os.path.join(ROOT, "research", "drone_path.json")))
F = dp["frames"]; n = len(F); P = [Vector(f["p"]) for f in F]
emp = bpy.data.objects["Drone Empty"]
w, a = win_area(); reg = [r for r in a.regions if r.type == "WINDOW"][0]

# ---- CAM_LOW ----
o = bpy.data.objects.get("CAM_LOW")
if o: bpy.data.objects.remove(o)
cd = bpy.data.cameras.new("CAM_LOW"); cd.lens = 50; cd.sensor_width = 36; cd.clip_start = 0.02; cd.clip_end = 3000
cd.dof.use_dof = True; cd.dof.focus_object = emp; cd.dof.aperture_fstop = 2.0
low = bpy.data.objects.new("CAM_LOW", cd); coll("ANIMATION").objects.link(low); low.rotation_mode = "XYZ"
H = P[dp["hover"] - 1]
base = Vector((H.x + 2.3, 0.0, 0.42))          # on the double yellow line: traffic lanes are at y = +-1.9
prev = None
for f in range(400, n + 1):
    p = base + Vector((0.004 * (f - 400) * -1, 0, 0))
    aim = P[f - 1] + Vector((0, 0, 0.02))
    low.location = p; low.keyframe_insert("location", frame=f)
    q = (aim - p).normalized().to_track_quat("-Z", "Y")
    e = q.to_euler("XYZ", prev) if prev else q.to_euler("XYZ"); prev = e
    low.rotation_euler = e; low.keyframe_insert("rotation_euler", frame=f)
set_interp(low, "LINEAR")

# ---- shakes ----
PLAN = {   # camera: (shake type, influence, speed)
    "Camera":   ("INVESTIGATION", 0.55, 1.15),   # another pilot / operator chasing: hand-held energy
    "CAM_ROOF": ("THE_CLOSEUP", 0.45, 1.0),
    "CAM_HERO": ("THE_CLOSEUP", 0.6, 0.9),
    "CAM_LOW":  ("INVESTIGATION", 0.35, 1.0),
}
for name, (kind, infl, speed) in PLAN.items():
    cam = bpy.data.objects[name]
    for fc in fcurves(cam):                       # drop my old procedural noise
        for m in list(fc.modifiers): fc.modifiers.remove(m)
    for o in bpy.context.view_layer.objects: o.select_set(False)
    bpy.context.view_layer.objects.active = cam; cam.select_set(True)
    with bpy.context.temp_override(window=w, area=a, region=reg, active_object=cam, object=cam, selected_objects=[cam]):
        while len(cam.camera_shakes):
            bpy.ops.object.camera_shake_remove()
        bpy.ops.object.camera_shake_add()
    s = cam.camera_shakes[0]
    s.shake_type = kind; s.influence = infl; s.speed = speed; s.scale = 1.0
save()
print({k: (bpy.data.objects[k].camera_shakes[0].shake_type, round(bpy.data.objects[k].camera_shakes[0].influence, 2)) for k in PLAN})
