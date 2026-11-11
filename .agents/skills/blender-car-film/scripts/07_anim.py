import bpy, math, random
from mathutils import Vector
sc = bpy.context.scene; FPS = 24; random.seed(3)
rig = bpy.data.objects["CarRig"]; rig.animation_data_clear(); rig.rotation_euler = (0, 0, 0)
for n in ("SnowBank-1", "SnowBank1"):
    o = bpy.data.objects[n]; o.scale = (1.4, 1, 0.3); o.location.z = -0.05
# speed profile (m/s) by time
def v(t):
    if t < 5.3: return 0
    if t < 8.0: return 12.5 * ((t - 5.3) / 2.7) ** 1.3
    if t < 11.0: return 12.5 + 1.4 * (t - 8) / 3
    if t < 13.5: return 13.9
    if t < 16.0: return 13.9 * (1 - (t - 13.5) / 2.5) ** 1.15
    return 0
X0 = 1.9; s = 0.0; prev_v = 0; dist = {}
for f in range(1, 481):
    t = (f - 1) / FPS; vv = v(t); s += vv / FPS; acc = (vv - prev_v) * FPS; prev_v = vv; dist[f] = s
    sc.frame_set(f) if False else None
    rig.location = (X0, s, 0.0 + (0.012 * math.sin(t * 9.1) + 0.008 * math.sin(t * 15.7)) * min(vv / 8, 1) + (0.004 * math.sin(t * 60) if 3.6 < t < 16.5 else 0))
    pitch = max(min(acc * 0.004, 0.03), -0.035)  # brake -> nose dips (-), accel -> squat (+)
    rig.rotation_euler = (pitch, 0.006 * math.sin(t * 2.3) * min(vv / 8, 1), 0)
    rig.keyframe_insert("location", frame=f); rig.keyframe_insert("rotation_euler", frame=f)
print("stop at y", round(s, 2))
# wheels: roll about world -X, angle = distance / radius
R = 0.332
for n in ("wheel_003_tire_DefaultMaterial_0", "wheel_004_tire_DefaultMaterial_0"):
    o = bpy.data.objects[n]; o.animation_data_clear(); o.rotation_mode = "XYZ"
    bpy.context.view_layer.update()
    M = o.parent.matrix_world.to_3x3().normalized(); a = M.inverted() @ Vector((-1, 0, 0))
    i = max(range(3), key=lambda k: abs(a[k])); sign = 1 if a[i] > 0 else -1
    base = o.rotation_euler.copy()
    for f in range(1, 481):
        e = base.copy(); e[i] += sign * dist[f] / R; o.rotation_euler = e; o.keyframe_insert("rotation_euler", frame=f)
    for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, "fcurves") else []:
        for k in fc.keyframe_points: k.interpolation = "LINEAR"
# headlights + tail lights (parented, set at frame 1 where rig is at start)
sc.frame_set(1); bpy.context.view_layer.update()
for n in [o.name for o in bpy.data.objects if o.name.startswith(("HeadL", "TailL", "HeadGlow"))]: bpy.data.objects.remove(bpy.data.objects[n])
def keyed_light(name, typ, loc, rot, color, onoff, power, size=0.06, spot=None):
    L = bpy.data.lights.new(name, typ); L.color = color; L.shadow_soft_size = size
    if spot: L.spot_size = spot; L.spot_blend = 0.35
    o = bpy.data.objects.new(name, L); bpy.data.collections["Car"].objects.link(o)
    o.matrix_world = __import__("mathutils").Matrix.LocRotScale(Vector(loc), __import__("mathutils").Euler(rot), None)
    mw = o.matrix_world.copy(); o.parent = rig; o.matrix_world = mw
    for f, on in onoff: L.energy = power if on else 0; L.keyframe_insert("energy", frame=f)
    return o
HEAD = [(1, 0), (82, 0), (84, 1), (391, 1), (393, 0)]
for sx in (-0.58, 0.58):
    keyed_light(f"HeadL{sx}", "SPOT", (X0 + sx, 2.15, 0.72), (math.radians(86), 0, 0), (1.0, 0.93, 0.78), HEAD, 900, 0.05, math.radians(55))
    keyed_light(f"HeadGlow{sx}", "POINT", (X0 + sx, 2.3, 0.72), (0, 0, 0), (1.0, 0.93, 0.78), HEAD, 30, 0.04)
    keyed_light(f"TailL{sx}", "POINT", (X0 + sx * 1.05, -2.35, 0.8), (0, 0, 0), (1.0, 0.05, 0.02), [(1, 0), (82, 0), (84, 1), (360, 1), (362, 1), (391, 1), (393, 0)], 4, 0.05)
# porch light on at 17.5 s
pl = bpy.data.lights["PorchLight"]; bm = bpy.data.materials["PorchBulb"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
for f, on in [(1, 0), (420, 0), (421, 1)]:
    pl.energy = 80 if on else 0; pl.keyframe_insert("energy", frame=f)
    bm.default_value = 40 if on else 0; bm.keyframe_insert("default_value", frame=f)
print("anim ok")
