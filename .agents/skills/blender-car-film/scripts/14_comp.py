import bpy
sc = bpy.context.scene
ng = bpy.data.node_groups.get("CineComp") or bpy.data.node_groups.new("CineComp", "CompositorNodeTree")
sc.compositing_node_group = ng
ng.nodes.clear()
if not ng.interface.items_tree:
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
N = ng.nodes.new; Lk = ng.links.new
rl = N("CompositorNodeRLayers"); out = N("NodeGroupOutput")
def setin(n, name, v):
    s = n.inputs.get(name)
    if s is not None: s.default_value = v; return True
    return False
g1 = N("CompositorNodeGlare")   # soft bloom
g2 = N("CompositorNodeGlare")   # anamorphic streaks
for n, kind in ((g1, "Fog Glow"), (g2, "Streaks")):
    if not setin(n, "Type", kind):
        n.glare_type = kind.upper().replace(" ", "_")
setin(g1, "Threshold", 1.0); setin(g1, "Strength", 0.35); setin(g1, "Size", 0.6)
setin(g2, "Threshold", 2.0); setin(g2, "Strength", 0.25); setin(g2, "Streaks", 2); setin(g2, "Streaks Angle", 0.0); setin(g2, "Fade", 0.92)
ld = N("CompositorNodeLensdist"); setin(ld, "Dispersion", 0.012); setin(ld, "Distortion", -0.01)
# colour grade removed at user request (looked pinkish)
cb = None  # N("CompositorNodeColorBalance")
# cb.inputs[4].default_value = (0.97, 0.99, 1.07, 1)   # lift: cool shadows
# cb.inputs[8].default_value = (1.06, 1.0, 0.93, 1)   # gain: warm highlights
Lk(rl.outputs["Image"], g1.inputs["Image"]); Lk(g1.outputs[0], g2.inputs["Image"])
Lk(g2.outputs[0], ld.inputs["Image"]); Lk(ld.outputs[0], out.inputs[0])
print("comp ok", [ (n.bl_idname, [i.name for i in n.inputs][:8]) for n in (g1, ld)])
