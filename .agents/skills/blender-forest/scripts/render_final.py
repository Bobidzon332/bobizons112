"""Final render of the 19-32 s clip: 2560x1440, 128 samples + OpenImageDenoise (benchmarked:
no visible difference vs 256 samples, ~45% faster), motion blur on, PNG sequence.
Resumes after a power cut (frames already on disk are skipped).

  blender -b scene/forest.blend --python scripts/look.py --python scripts/render_final.py
"""
import bpy, os, ctypes

ROOT = os.path.join(os.path.expanduser("~"), "blender-forest")
OUT = os.path.join(ROOT, "render", "final_2k")
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
cy = sc.cycles
cy.device = "GPU"
cy.samples = 128
cy.use_adaptive_sampling = True
cy.adaptive_threshold = 0.01
cy.use_denoising = True
cy.denoiser = "OPENIMAGEDENOISE"
try:
    cy.denoising_use_gpu = True
    cy.denoising_prefilter = "ACCURATE"
    cy.denoising_quality = "HIGH"
except AttributeError:
    pass
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 2560, 1440, 100
sc.render.use_simplify = False
sc.render.use_motion_blur = True
sc.render.use_persistent_data = True
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_depth = "16"
sc.render.use_overwrite = False
sc.render.use_placeholder = True
os.makedirs(OUT, exist_ok=True)
sc.render.filepath = os.path.join(OUT, "f####")
print("FINAL start", sc.frame_start, sc.frame_end, "->", OUT)
bpy.ops.render.render(animation=True)
print("FINAL DONE")
