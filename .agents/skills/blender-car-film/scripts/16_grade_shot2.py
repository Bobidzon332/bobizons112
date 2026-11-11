import bpy
sc = bpy.context.scene; cy = sc.cycles
ng = bpy.data.node_groups["CineComp"]; cb = ng.nodes["Grade"]
# the grade the user liked (first version), used ONLY on shot 2 (frames 73-120)
cb.inputs[4].default_value = (0.97, 0.99, 1.07, 1); cb.inputs[8].default_value = (1.06, 1.0, 0.93, 1)
if ng.animation_data: ng.animation_data_clear()
fac = cb.inputs["Factor"]
for f, v in [(1, 0.0), (72, 0.0), (73, 1.0), (120, 1.0), (121, 0.0), (480, 0.0)]:
    fac.default_value = v; fac.keyframe_insert("default_value", frame=f)
# undo the purple sources: original fog colour, neutral warm dash light, smaller exposure lift in shot 5
bpy.data.materials["Fog"].node_tree.nodes["Principled Volume"].inputs["Color"].default_value = (0.75, 0.82, 1.0, 1)
d = bpy.data.lights["DashGlow"]; d.color = (1.0, 0.86, 0.72); d.energy = 3
vs = sc.view_settings
if sc.animation_data: sc.animation_data_clear()
for f, e in [(1, 0), (264, 0), (265, 0.9), (348, 0.9), (349, 0)]:
    vs.exposure = e; vs.keyframe_insert("exposure", frame=f)
# fewer samples: denoiser does the cleaning
cy.samples = 48; cy.adaptive_min_samples = 12; cy.adaptive_threshold = 0.05
print("grade on shot 2 only; samples", cy.samples)
