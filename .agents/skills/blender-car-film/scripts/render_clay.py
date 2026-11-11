# One-off "Blender breakdown" render: white clay on everything, no textures, EEVEE. Does NOT save the .blend.
import bpy, os, math
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"; sc.eevee.taa_render_samples = 16
clay = bpy.data.materials.new("ClayWhite"); clay.use_nodes = True
b = clay.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.82, 0.82, 0.82, 1); b.inputs["Roughness"].default_value = 0.55
sc.view_layers[0].material_override = clay
for L in bpy.data.objects:
    if L.type == "LIGHT": L.hide_render = True
for o in bpy.data.collections["Set"].objects:   # trees/poles: no shadows, so the car is lit
    if o.instance_collection and o.instance_collection.name in ("pine_tree_01", "fir_tree_01", "modular_electricity_poles"): o.visible_shadow = False
for cn in ("pine_tree_01", "fir_tree_01", "modular_electricity_poles"):
    for o in bpy.data.collections[cn].all_objects: o.visible_shadow = False
if "FogVolume" in bpy.data.objects: bpy.data.objects["FogVolume"].hide_render = True
sun = bpy.data.objects.new("ClaySun", bpy.data.lights.new("ClaySun", "SUN")); sc.collection.objects.link(sun)
sun.data.energy = 5.0; sun.data.angle = math.radians(8); sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(200))
w = bpy.data.worlds.new("ClaySky"); w.use_nodes = True; sc.world = w
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.3, 0.32, 0.36, 1); w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.5
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
if sc.animation_data: sc.animation_data_clear()
sc.view_settings.exposure = 0
sc.render.use_compositing = False; sc.render.use_motion_blur = True
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_depth = "8"
sc.render.use_overwrite = False; sc.render.use_placeholder = True
sc.render.filepath = os.path.expanduser("~/blender-car-film/frames_clay4/c_####")
for c in bpy.data.cameras: c.dof.use_dof = False
sc.render.use_motion_blur = False; sc.eevee.taa_render_samples = 8; sc.render.resolution_percentage = 50
for n in ("SnowFall", "SnowFlake"): bpy.data.objects[n].hide_render = True
print("CLAY SETUP OK", sc.render.engine)
