"""Render chosen frames of the shot timeline (look-dev / checks). Does not save the .blend.

  blender -b scene/forest.blend --python scripts/look.py --python scripts/render_frames.py -- <out_dir> <samples> <width> <frame> [frame ...]
Writes <out_dir>/r####.png (#### = timeline frame).
"""
import bpy, sys, os, ctypes

argv = sys.argv[sys.argv.index("--") + 1:]
out_dir, samples, width = argv[0], int(argv[1]), int(argv[2])
frames = [int(f) for f in argv[3:]]

try:
    k = ctypes.windll.kernel32
    k.SetPriorityClass(k.GetCurrentProcess(), 0x00004000)  # below normal: PC stays usable
except Exception:
    pass

sc = bpy.context.scene
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "OPTIX"
sc.cycles.device = "GPU"
sc.cycles.samples = samples
sc.render.resolution_x, sc.render.resolution_y = width, round(width * 9 / 16)
sc.render.resolution_percentage = 100
if os.environ.get("FULL") == "1":          # final quality: full-res textures
    sc.render.use_simplify = False
else:
    sc.render.use_simplify = True
    sc.cycles.texture_limit_render = "2048"
sc.cycles.use_denoising = True
sc.cycles.denoiser = "OPTIX"
sc.render.image_settings.file_format = "PNG"
# Keep the static forest (730k instances, BVH, textures) on the GPU between frames instead of
# rebuilding it on the CPU for every frame - that rebuild was most of the render time.
sc.render.use_persistent_data = True
os.makedirs(out_dir, exist_ok=True)

markers = sorted((m for m in sc.timeline_markers if m.camera), key=lambda m: m.frame)
for f in frames:
    sc.frame_set(f)
    cams = [m.camera for m in markers if m.frame <= f]
    if cams:
        sc.camera = cams[-1]
    sc.render.filepath = os.path.join(out_dir, f"r{f:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("FRAME", f, sc.camera.name, sc.render.filepath)
