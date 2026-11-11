import bpy
p = bpy.context.preferences
p.filepaths.use_auto_save_temporary_files = True; p.filepaths.auto_save_time = 2; p.filepaths.save_version = 2
p.system.gl_texture_limit = "CLAMP_1024"
bpy.ops.wm.save_userpref()
sc = bpy.context.scene
sc.render.use_simplify = True; sc.render.simplify_subdivision = 0; sc.render.simplify_child_particles = 0.1
sc.render.simplify_subdivision_render = 6; sc.render.simplify_child_particles_render = 1.0
for o in bpy.data.collections["Set"].objects:
    if o.instance_collection and o.instance_collection.name in ("pine_tree_01", "fir_tree_01"): o.display_type = "BOUNDS"
for a in bpy.context.screen.areas:
    if a.type == "VIEW_3D":
        for s in a.spaces:
            if s.type == "VIEW_3D": s.shading.type = "SOLID"; s.clip_end = 400
print("viewport light, autosave 2 min")
