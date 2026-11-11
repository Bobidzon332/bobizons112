"""Grey clay (Workbench, Solid shading) version of the 19-32 s car clip, for the tutorial's fake Blender viewport.
1280x720 PNG sequence in render/clay, resumable. Pass --test to time a single frame (frame 200) instead.

  blender -b --disable-autoexec scene/forest.blend --python scripts/render_clay.py [-- --test]
"""
import bpy, os, sys, time

ROOT = os.path.join(os.path.expanduser("~"), "blender-forest")
OUT = os.path.join(ROOT, "render", "clay")
test = "--test" in sys.argv

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "STUDIO"
sh.color_type = "SINGLE"
sh.single_color = (0.8, 0.8, 0.8)
sh.show_cavity = False
sh.show_shadows = False
sh.shadow_intensity = 0.45
sh.show_object_outline = False
sc.display.render_aa = "OFF"
sc.render.film_transparent = False
w = sc.world
if w:  # Workbench uses the world viewport colour as the background
    w.color = (0.24, 0.24, 0.24)
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 960, 540, 100
sc.render.use_motion_blur = False
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_depth = "8"
sc.render.use_overwrite = False
sc.render.use_placeholder = True
os.makedirs(OUT, exist_ok=True)
print("CLAY settings ok", flush=True)
if test:
    sc.frame_set(200)
    sc.render.filepath = os.path.join(OUT, "test_f0200.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print(f"CLAY TEST frame 200: {time.time() - t:.1f} s  (frames {sc.frame_start}-{sc.frame_end})")
else:
    sc.render.filepath = os.path.join(OUT, "c####")
    print("CLAY start", sc.frame_start, sc.frame_end, "->", OUT)
    bpy.ops.render.render(animation=True)
    print("CLAY DONE")
