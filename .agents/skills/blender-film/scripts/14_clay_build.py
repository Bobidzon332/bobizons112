# CLAY BUILD-UP (recreation of the "CINEMATIC CITY" build: white clay, the city drops out of the sky piece by piece).
# Re-run on a FRESH copy of spidey.blend (keys are added, not replaced).
# Runs on a COPY of the scene (scene/clay_build.blend) so the finished shot is untouched.
#  * camera = CAM_AERIAL frozen at the pose of scene frame 348 (the frame the wipe lands on)
#  * white clay override, daylight sun + sky, no fog / night lights / drone / trees (leaf cards turn into white squares)
#  * timeline 1-168 (7 s): ground is there from frame 1; cars -> buildings (nearest first) -> far city -> street props
#    each drops from above with an accelerating fall, a small impact dip and motion blur
import bpy, os, math, random
from mathutils import Vector, Matrix
random.seed(3)
sc = bpy.context.scene
LAND_FRAME = 348
sc.frame_set(LAND_FRAME)
vl = bpy.context.view_layer

# ---------- camera frozen at the landing pose ----------
cam = bpy.data.objects["CAM_AERIAL"]
mw = cam.matrix_world.copy()
cam.animation_data_clear()
for c in list(cam.constraints): cam.constraints.remove(c)
cam.matrix_world = mw
sc.camera = cam

# ---------- moving traffic frozen where it is at the landing frame ----------
street = bpy.data.collections["STREET"]
for o in street.objects:
    if o.animation_data:
        m = o.matrix_world.copy(); o.animation_data_clear(); o.matrix_world = m
    if o.instance_collection and o.instance_collection.name.startswith("CARON_"):
        o.instance_collection = bpy.data.collections["CAR_" + o.instance_collection.name[6:]]

# ---------- hide what clay should not show ----------
def find_lc(lc, name):
    if lc.name == name: return lc
    for ch in lc.children:
        r = find_lc(ch, name)
        if r: return r
for cname in ("NIGHT LIGHTS", "DRONE", "WEBS", "LANDING FX", "Spidey+Rig", "TMP LINEUP"):
    lc = find_lc(vl.layer_collection, cname)
    if lc: lc.exclude = True
for n in ("Atmosphere", "Drone Path", "Camera Path", "Spider-Man Path"):
    o = bpy.data.objects.get(n)
    if o: o.hide_render = True; o.hide_viewport = True
for o in street.objects:
    if o.name.startswith("tree"):
        o.hide_render = True; o.hide_viewport = True

# ---------- clay look ----------
clay = bpy.data.materials.get("CLAY") or bpy.data.materials.new("CLAY")
clay.use_nodes = True
b = next(x for x in clay.node_tree.nodes if x.type == "BSDF_PRINCIPLED")
b.inputs["Base Color"].default_value = (0.80, 0.80, 0.80, 1); b.inputs["Roughness"].default_value = 0.55
b.inputs["Emission Strength"].default_value = 0.0
vl.material_override = clay
day = sc.world                                          # night sky gradient turned up = soft fill
for n in day.node_tree.nodes if day else []:
    if n.type == "BACKGROUND": n.inputs["Strength"].default_value = 1.0
sun = bpy.data.objects.get("Clay Sun")
if sun is None:
    sun = bpy.data.objects.new("Clay Sun", bpy.data.lights.new("Clay Sun", "SUN")); sc.collection.objects.link(sun)
sun.data.energy = 5.0; sun.data.angle = math.radians(2.5); sun.data.color = (1.0, 0.97, 0.92)
sun.rotation_euler = (math.radians(42), 0, math.radians(150 + 90 + 25))
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Base Contrast"; sc.view_settings.exposure = -0.15
sc.render.use_compositing = False
sc.cycles.volume_bounces = 0

# ---------- drop-in animation ----------
sc.frame_start, sc.frame_end = 1, 168
cam_p = cam.matrix_world.translation
def drop(o, start, dur, height, dip):
    # hidden until its drop starts (no shadows from pieces waiting in the sky), then falls in from above the lens
    o.hide_render = True; o.keyframe_insert("hide_render", frame=1)
    o.hide_render = False; o.keyframe_insert("hide_render", frame=start)
    L = o.location.copy()
    o.location = L + Vector((0, 0, height)); o.keyframe_insert("location", index=2, frame=start)
    o.location = L - Vector((0, 0, dip)); o.keyframe_insert("location", index=2, frame=start + dur)
    o.location = L; o.keyframe_insert("location", index=2, frame=start + dur + 3)
    from bpy_extras import anim_utils
    fc = next(f for f in anim_utils.action_get_channelbag_for_slot(o.animation_data.action, o.animation_data.action_slot).fcurves
              if f.data_path == "location")
    k = fc.keyframe_points
    k[0].interpolation = "QUAD"; k[0].easing = "EASE_IN"           # accelerating fall
    k[1].interpolation = "SINE"; k[1].easing = "EASE_OUT"          # impact dip recovers

def by_distance(objs):
    return sorted(objs, key=lambda o: (o.matrix_world.translation - cam_p).length + random.uniform(-6, 6))

cars = by_distance([o for o in street.objects if o.name.startswith(("parked", "moving", "stopped", "cross"))])
props = by_distance([o for o in street.objects if o.name.startswith(("hydrant", "trash", "lamp", "signal"))])
city = by_distance(list(bpy.data.collections["CITY"].objects))
far = by_distance(list(bpy.data.collections["FAR CITY"].objects))
def spread(objs, f0, f1):
    n = max(1, len(objs) - 1)
    return [(o, int(round(f0 + (f1 - f0) * (i / n) ** 0.85 + random.uniform(-2, 2)))) for i, o in enumerate(objs)]
for o, s in spread(cars, 10, 46): drop(o, max(2, s), random.randint(8, 10), random.uniform(55, 70), 0.12)
for o, s in spread(city, 44, 96): drop(o, s, random.randint(10, 13), random.uniform(80, 110), 0.6)
for o, s in spread(far, 84, 116): drop(o, s, random.randint(12, 15), random.uniform(120, 160), 0.8)
for o, s in spread(props, 108, 148): drop(o, s, random.randint(8, 10), random.uniform(50, 60), 0.05)
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print("clay build:", len(cars), "cars,", len(city), "buildings,", len(far), "far,", len(props), "props; saved", bpy.data.filepath)
