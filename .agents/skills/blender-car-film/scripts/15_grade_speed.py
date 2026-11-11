import bpy
sc = bpy.context.scene; cy = sc.cycles
# grade: no green. shadows = neutral-blue (G lowest), highlights warm
cb = bpy.data.node_groups["CineComp"].nodes["Grade"]
cb.inputs[4].default_value = (0.99, 0.965, 1.04, 1)   # lift
cb.inputs[8].default_value = (1.05, 0.97, 0.92, 1)    # gain
# remove green sources in the scene itself
bpy.data.lights["DashGlow"].color = (1.0, 0.62, 0.3)          # amber dash, not teal
fog = bpy.data.materials["Fog"].node_tree.nodes["Principled Volume"]
fog.inputs["Color"].default_value = (0.8, 0.8, 0.9, 1)        # neutral-cool fog, less cyan
# speed: fewer samples (denoiser does the rest), coarser fog steps
cy.samples = 64; cy.adaptive_threshold = 0.05; cy.adaptive_min_samples = 16
cy.volume_step_rate = 3.0
# bake snow / steam / spray particles to disk once -> no re-simulation per frame or per process
for o in bpy.data.collections["FX"].objects:
    for p in o.particle_systems:
        pc = p.point_cache; pc.use_disk_cache = True; pc.frame_start = int(min(p.settings.frame_start, 1)); pc.frame_end = 480
with bpy.context.temp_override(scene=sc):
    bpy.ops.ptcache.bake_all(bake=True)
print("grade+speed ok")
