"""Render-settings benchmark: same frames, different Cycles settings, timed per frame.

  BENCH='{"samples":128,"denoiser":"OPENIMAGEDENOISE"}' blender -b scene/forest.blend \
      --python scripts/look.py --python scripts/bench.py -- <out_dir> <frame> [frame ...]
Prints BENCH <frame> <seconds>. Always 2560x1440, full textures, persistent data.
"""
import bpy, sys, os, json, time, ctypes

argv = sys.argv[sys.argv.index("--") + 1:]
out_dir, frames = argv[0], [int(f) for f in argv[1:]]
cfg = json.loads(os.environ.get("BENCH", "{}"))
try:
    k = ctypes.windll.kernel32
    k.SetPriorityClass(k.GetCurrentProcess(), 0x00004000)
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
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 2560, 1440, 100
sc.render.use_simplify = False
sc.render.use_persistent_data = True
sc.render.image_settings.file_format = "PNG"

cy.samples = cfg.get("samples", 256)
cy.use_adaptive_sampling = True
cy.adaptive_threshold = cfg.get("threshold", 0.01)
cy.use_denoising = True
cy.denoiser = cfg.get("denoiser", "OPTIX")
if cy.denoiser == "OPENIMAGEDENOISE":
    try:
        cy.denoising_use_gpu = True
        cy.denoising_prefilter = "ACCURATE"
        cy.denoising_quality = "HIGH"
    except AttributeError:
        pass
for key in ("max_bounces", "diffuse_bounces", "glossy_bounces", "transmission_bounces",
            "transparent_max_bounces", "volume_bounces"):
    if key in cfg:
        setattr(cy, key, cfg[key])
if "seed" in cfg:
    cy.seed = cfg["seed"]
if "clamp_indirect" in cfg:
    cy.sample_clamp_indirect = cfg["clamp_indirect"]
if "caustics" in cfg:
    cy.caustics_reflective = cy.caustics_refractive = cfg["caustics"]
if "filter_glossy" in cfg:
    cy.blur_glossy = cfg["filter_glossy"]
print("BENCH cfg", json.dumps(cfg), "| bounces", cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces,
      cy.transmission_bounces, cy.transparent_max_bounces, "| clamp", cy.sample_clamp_indirect)

os.makedirs(out_dir, exist_ok=True)
markers = sorted((m for m in sc.timeline_markers if m.camera), key=lambda m: m.frame)
for f in frames:
    sc.frame_set(f)
    cams = [m.camera for m in markers if m.frame <= f]
    if cams:
        sc.camera = cams[-1]
    sc.render.filepath = os.path.join(out_dir, f"r{f:04d}.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print(f"BENCH {f} {time.time() - t:.1f}")
