"""Fast animation preview: whole clip, low quality, to check motion/timing/cuts.

  blender -b scene/forest.blend --python scripts/look.py --python scripts/preview.py -- <out_dir>
Writes <out_dir>/p####.png (skips frames already rendered, so it resumes after a power cut).
"""
import bpy, sys, os, ctypes

out_dir = sys.argv[sys.argv.index("--") + 1]
try:
    k = ctypes.windll.kernel32
    k.SetPriorityClass(k.GetCurrentProcess(), 0x00004000)  # below normal
except Exception:
    pass

sc = bpy.context.scene
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "OPTIX"
cy = sc.cycles
cy.device = "GPU"
cy.samples = 4
cy.use_adaptive_sampling = False
cy.use_denoising = True
cy.denoiser = "OPTIX"
cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces = 3, 1, 1
cy.transmission_bounces, cy.transparent_max_bounces = 2, 4
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 960, 540, 100
sc.render.use_simplify = True
cy.texture_limit_render = "256"
sc.render.use_motion_blur = False
sc.render.use_persistent_data = True
sc.render.image_settings.file_format = "PNG"
sc.render.use_overwrite = False          # resume: keep frames already on disk
sc.render.use_placeholder = True
os.makedirs(out_dir, exist_ok=True)
sc.render.filepath = os.path.join(out_dir, "p####")
bpy.ops.render.render(animation=True)    # timeline markers switch the shot cameras
print("PREVIEW DONE", sc.frame_start, sc.frame_end)
