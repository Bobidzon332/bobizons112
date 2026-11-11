import bpy, math
from mathutils import Vector
sc = bpy.context.scene
cc = bpy.data.collections.get("Cameras") or bpy.data.collections.new("Cameras")
if cc.name not in sc.collection.children: sc.collection.children.link(cc)
for o in list(cc.objects): bpy.data.objects.remove(o)
sc.timeline_markers.clear()
rig = bpy.data.objects["CarRig"]
def look(cam, target):
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
def make(name, lens, f0, focus=None, fstop=2.8):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36; cd.clip_start = 0.02
    if focus: cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop; cd.dof.focus_object = focus
    o = bpy.data.objects.new(name, cd); cc.objects.link(o)
    m = sc.timeline_markers.new(name, frame=f0); m.camera = o; return o
def shake(cam, kind, scale, speed=1.0):
    bpy.ops.object.select_all(action="DESELECT"); bpy.context.view_layer.objects.active = cam; cam.select_set(True)
    bpy.ops.object.camera_shake_add(); s = cam.camera_shakes[-1]
    s.shake_type = kind; s.scale = scale; s.speed = speed
def target(name, loc, parent=None):
    t = bpy.data.objects.new(name, None); t.location = loc; cc.objects.link(t)
    if parent: mw = t.matrix_world.copy(); t.parent = parent; t.matrix_world = mw
    return t
sc.frame_set(1); bpy.context.view_layer.update()
X0 = 1.9
carT = target("T_carbody", (X0, 0.2, 0.75), rig)      # follows car
headT = target("T_headlight", (X0 + 0.58, 2.2, 0.72), rig)
# remove trees that would block close camera views
for o in list(bpy.data.collections["Set"].objects):
    if o.instance_collection and o.instance_collection.name in ("pine_tree_01", "fir_tree_01") and abs(o.location.x) < 11 and o.location.y < 8:
        bpy.data.objects.remove(o)
# 1  0-3 s  wide low push-in
c = make("Cam1_Wide", 26, 1, carT, 4)
for f, p in [(1, (-4.2, -10.5, 0.75)), (73, (-3.4, -8.3, 0.85))]:
    c.location = p; look(c, (X0, 0.5, 0.9)); c.keyframe_insert("location", frame=f); c.keyframe_insert("rotation_euler", frame=f)
shake(c, "INVESTIGATION", 0.15)
# 2  3-5 s  headlight macro
c = make("Cam2_Headlight", 85, 73, headT, 2.0)
c.location = (X0 + 1.05, 3.15, 0.8); look(c, (X0 + 0.58, 2.2, 0.72))
shake(c, "INVESTIGATION", 0.1)
# 3  5-7 s  ground cam at rear wheel, static
c = make("Cam3_Wheel", 24, 121, None)
c.location = (X0 + 1.55, -3.1, 0.22); look(c, (X0 + 0.7, -1.0, 0.35))
shake(c, "INVESTIGATION", 0.08, 2.5)
# 4  7-11 s  tracking 3/4 front-left, ahead of the car, same speed
c = make("Cam4_Track", 30, 169, carT, 4)
for f in range(160, 270):
    sc.frame_set(f); y = rig.location.y
    c.location = (X0 - 3.6, y + 6.2, 1.05); look(c, (X0, y + 0.6, 0.75))
    c.keyframe_insert("location", frame=f); c.keyframe_insert("rotation_euler", frame=f)
shake(c, "OUT_CAR_WINDOW", 0.4)
# 5  11-14.5 s  inside, behind seats, through the windscreen (rides with the car)
sc.frame_set(1); bpy.context.view_layer.update()
c = make("Cam5_Inside", 22, 265, None)
c.location = (X0 + 0.05, -0.9, 1.22); look(c, (X0 - 0.05, 8, 0.9))
mw = c.matrix_world.copy(); c.parent = rig; c.matrix_world = mw
shake(c, "OUT_CAR_WINDOW", 0.6)
# 6  14.5-20 s  wide at the house, static
c = make("Cam6_House", 32, 349, carT, 5.6)
c.location = (-5.5, 93.5, 1.6); look(c, (6.5, 109, 1.4))
shake(c, "INVESTIGATION", 0.12)
sc.frame_set(1)
print("cams ok", [m.name for m in sc.timeline_markers])
