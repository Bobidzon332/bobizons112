import bpy, os
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_depth = "16"
sc.render.use_overwrite = False; sc.render.use_placeholder = True   # resumable after power cut
sc.render.filepath = os.path.expanduser("~/blender-car-film/frames/f_####")
