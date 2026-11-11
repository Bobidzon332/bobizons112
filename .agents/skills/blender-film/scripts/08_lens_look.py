# Lens look (no colour grade): soft bloom around bright lights (fog glow), very slight barrel distortion + dispersion.
# Blender 5.x compositor = a node group assigned to scene.compositing_node_group.
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
sc = bpy.context.scene
ng = bpy.data.node_groups.get("Lens Look")
if ng: bpy.data.node_groups.remove(ng)
ng = bpy.data.node_groups.new("Lens Look", "CompositorNodeTree")
ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
n = ng.nodes; l = ng.links
rl = n.new("CompositorNodeRLayers"); rl.location = (-600, 0); rl.scene = sc
gl = n.new("CompositorNodeGlare"); gl.location = (-300, 0)
gl.inputs["Type"].default_value = "Bloom"
gl.inputs["Quality"].default_value = "High"
gl.inputs["Threshold"].default_value = 1.2
gl.inputs["Smoothness"].default_value = 0.4
gl.inputs["Strength"].default_value = 0.35
gl.inputs["Size"].default_value = 0.55
ld = n.new("CompositorNodeLensdist"); ld.location = (0, 0)
ld.inputs["Distortion"].default_value = -0.012
ld.inputs["Dispersion"].default_value = 0.006
ld.inputs["Fit"].default_value = True
out = n.new("NodeGroupOutput"); out.location = (300, 0)
l.new(rl.outputs["Image"], gl.inputs["Image"]); l.new(gl.outputs["Image"], ld.inputs["Image"]); l.new(ld.outputs["Image"], out.inputs[0])
sc.compositing_node_group = ng
sc.render.use_compositing = True
save()
print("compositor:", [x.bl_idname for x in n])
