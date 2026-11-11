import bpy, math
from mathutils import Vector
sc = bpy.context.scene; cy = sc.cycles; X0 = 1.9
# ---- SPEED ----
cy.volume_biased = True; cy.volume_step_rate = 2.0; cy.volume_max_steps = 256
sc.render.use_simplify = True; cy.use_camera_cull = True; cy.camera_cull_margin = 0.15
cy.use_distance_cull = True; cy.distance_cull_margin = 60
for o in bpy.data.collections["Set"].objects:
    if o.instance_collection and o.instance_collection.name in ("pine_tree_01", "fir_tree_01", "modular_electricity_poles"):
        o.cycles.use_camera_cull = True; o.cycles.use_distance_cull = True
sf = bpy.data.objects["SnowFall"]; sf.cycles.use_camera_cull = True; sf.cycles.use_distance_cull = True
sf.scale = (24, 170, 1); sf.particle_systems[0].settings.count = 230000
cy.use_fast_gi = True; cy.fast_gi_method = "REPLACE"; cy.ao_bounces_render = 2; cy.ao_bounces = 1
sc.world.light_settings.distance = 12
# ---- CINEMATIC ----
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 2560, 1072, 100
def look(c, t): c.rotation_euler = (Vector(t) - c.location).to_track_quat("-Z", "Y").to_euler()
sc.frame_set(1); bpy.context.view_layer.update()
# keep all cameras on the car's left side (180-degree rule)
c2 = bpy.data.objects["Cam2_Headlight"]; c2.location = (X0 - 1.7, 4.6, 0.95); look(c2, (X0 - 0.45, 2.2, 0.72))
ht = bpy.data.objects["T_headlight"]; rig = bpy.data.objects["CarRig"]
ht.parent = None; ht.location = (X0 - 0.45, 2.1, 0.7); bpy.context.view_layer.update()
mw = ht.matrix_world.copy(); ht.parent = rig; ht.matrix_parent_inverse = rig.matrix_world.inverted(); ht.matrix_world = mw
c3 = bpy.data.objects["Cam3_Wheel"]; c3.location = (X0 - 1.55, -3.1, 0.22); look(c3, (X0 - 0.7, -1.0, 0.35))
# stronger DOF on wides
bpy.data.cameras["Cam1_Wide"].dof.aperture_fstop = 2.0
c6 = bpy.data.objects["Cam6_House"]; c6.data.dof.aperture_fstop = 2.8; c6.animation_data_clear()
for f, p in [(349, (-1.6, 89.5, 1.45)), (480, (-0.9, 91.3, 1.38))]:
    c6.location = p; look(c6, (7.0, 109.5, 1.6)); c6.keyframe_insert("location", frame=f); c6.keyframe_insert("rotation_euler", frame=f)
# moonlight rim from behind (cold, faint)
L = bpy.data.lights.get("MoonRim") or bpy.data.lights.new("MoonRim", "SUN")
L.energy = 0.12; L.color = (0.55, 0.68, 1.0); L.angle = math.radians(2)
mo = bpy.data.objects.get("MoonRim") or bpy.data.objects.new("MoonRim", L)
if mo.name not in sc.collection.objects: sc.collection.objects.link(mo)
mo.rotation_euler = (math.radians(70), 0, math.radians(180))  # light travels toward -Y: from far down the road
print("speed+cine ok", sc.render.resolution_x, sc.render.resolution_y)
