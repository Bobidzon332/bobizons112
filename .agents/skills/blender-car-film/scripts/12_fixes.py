import bpy, math
from mathutils import Vector
sc = bpy.context.scene; cy = sc.cycles
# 1) SNOW: emitters must stay camera-visible (flakes inherit it); hide only the emitter mesh itself
for o in bpy.data.collections["FX"].objects:
    if o.particle_systems:
        o.visible_camera = True; o.visible_shadow = True; o.show_instancer_for_render = False; o.show_instancer_for_viewport = False
sf = bpy.data.objects["SnowFall"]; ps = sf.particle_systems[0].settings
sf.location = (0, 60, 11); sf.scale = (34, 170, 1)
ps.count = 320000; ps.frame_start = -260; ps.frame_end = 480; ps.lifetime = 260
ps.object_align_factor = (0, 0, -1.1); ps.factor_random = 0.25; ps.effector_weights.gravity = 0.01; ps.brownian_factor = 0.35
ps.particle_size = 1.0; ps.size_random = 0.6; ps.display_percentage = 2
bpy.data.objects["SnowFlake"].scale = (1.4, 1.4, 1.4)
# 2) FOG BANDING: finer volume steps + film dither
cy.volume_step_rate = 2.0; sc.render.dither_intensity = 2.0
# 3) SHOT 5 inside too dark: exposure lift only during that shot, brighter dash + headlight reach
vs = sc.view_settings
for f, e in [(1, 0), (264, 0), (265, 1.4), (348, 1.4), (349, 0)]:
    vs.exposure = e; vs.keyframe_insert("exposure", frame=f)
fc = sc.animation_data.action.fcurves if sc.animation_data and hasattr(sc.animation_data.action, "fcurves") else []
bpy.data.lights["DashGlow"].energy = 5
# 4) SHOT 6 house: camera off the lamp/pole line, clear blockers, remove tube snowbanks
for n in ("SnowBank-1", "SnowBank1"):
    if n in bpy.data.objects: bpy.data.objects.remove(bpy.data.objects[n])
c6 = bpy.data.objects["Cam6_House"]
c6.location = (-1.6, 89.5, 1.45)
c6.rotation_euler = (Vector((7.0, 109.5, 1.6)) - c6.location).to_track_quat("-Z", "Y").to_euler()
c6.data.lens = 30
for n in ("street_lamp_01.004", "modular_electricity_poles.003", "pine_tree_01.081"):
    if n in bpy.data.objects: bpy.data.objects.remove(bpy.data.objects[n])
lamp4 = bpy.data.objects.get("StreetLight3")
if lamp4: bpy.data.objects.remove(lamp4)
# 5) one hydrant: drop the 'aged' variant from the library model
for o in list(bpy.data.collections["fire_hydrant"].objects):
    if o.name.endswith("_aged"): bpy.data.objects.remove(o)
# 6) ground: road reads as packed snow, not gravel
m = bpy.data.materials["RoadSnow"]; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
src = b.inputs["Base Color"].links[0].from_socket
mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.inputs["Factor"].default_value = 0.55
mx.inputs[7].default_value = (0.78, 0.82, 0.88, 1)
nt.links.new(src, mx.inputs[6]); nt.links.new(mx.outputs[2], b.inputs["Base Color"])
for n in nt.nodes:
    if n.type == "DISPLACEMENT": n.inputs["Scale"].default_value = 0.012
print("fixes ok")
