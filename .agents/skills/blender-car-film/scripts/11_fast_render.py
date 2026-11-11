import bpy
sc = bpy.context.scene; cy = sc.cycles
# GPU: OptiX on the RTX 5070, GPU only
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"; prefs.refresh_devices()
for d in prefs.devices: d.use = (d.type == "OPTIX")
bpy.ops.wm.save_userpref()
sc.render.engine = "CYCLES"; cy.device = "GPU"
# 1) adaptive sampling + AI denoise: fewer samples, same look
cy.samples = 160; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.03; cy.adaptive_min_samples = 32
cy.use_denoising = True; cy.denoiser = "OPTIX"; cy.denoising_input_passes = "RGB_ALBEDO_NORMAL"; cy.denoising_prefilter = "ACCURATE"
cy.denoising_use_gpu = True
# 2) light tree: many lights (streetlights, headlights, porch) sampled smartly
cy.use_light_tree = True
# 3) light paths: cut bounces nobody can see at night
cy.max_bounces = 6; cy.diffuse_bounces = 2; cy.glossy_bounces = 3; cy.transmission_bounces = 6
cy.volume_bounces = 0; cy.transparent_max_bounces = 16
cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 1.0
cy.sample_clamp_direct = 0; cy.sample_clamp_indirect = 8          # kills fireflies -> denoiser works less
# 4) volumes (the fog is the slowest part): bigger step, fewer steps
cy.volume_step_rate = 4.0; cy.volume_preview_step_rate = 4.0; cy.volume_max_steps = 256
# 5) persistent data: keep scene in VRAM between frames (big win for animation)
sc.render.use_persistent_data = True
# 6) tiles off for GPU, render texture limit 2k (4k car textures halved; not visible at 1080p)
cy.use_auto_tile = False
sc.render.use_simplify = True; cy.texture_limit_render = "2048"; cy.texture_limit = "1024"
# 7) motion blur kept (it is cheap in Cycles), shorter shutter
sc.render.motion_blur_shutter = 0.5
# film: 1080p, 16-bit PNG frames, resumable
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_depth = "16"
sc.render.use_overwrite = False; sc.render.use_placeholder = True
print("fast render settings ok |", [d.name for d in prefs.devices if d.use])
