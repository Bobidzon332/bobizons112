import bpy, math
from mathutils import Vector, Matrix
sc = bpy.context.scene; sc.frame_set(1); bpy.context.view_layer.update()
rig = bpy.data.objects["CarRig"]; X0 = 1.9
def reparent(o, world_loc, world_rot=None):
    o.parent = None
    o.matrix_world = Matrix.LocRotScale(Vector(world_loc), world_rot, None) if world_rot else Matrix.Translation(Vector(world_loc))
    bpy.context.view_layer.update()
    mw = o.matrix_world.copy(); o.parent = rig; o.matrix_parent_inverse = rig.matrix_world.inverted(); o.matrix_world = mw
reparent(bpy.data.objects["T_carbody"], (X0, 0.2, 0.75))
reparent(bpy.data.objects["T_headlight"], (X0 + 0.46, 2.1, 0.7))
c = bpy.data.objects["Cam5_Inside"]
rot = (Vector((X0 - 0.05, 8, 0.95)) - Vector((X0 + 0.05, -0.9, 1.2))).to_track_quat("-Z", "Y").to_euler()
reparent(c, (X0 + 0.05, -0.9, 1.2), rot)
# headlight spots to true lamp position
for sx in (-0.58, 0.58):
    for pre, dy in (("HeadL", 2.2), ("HeadGlow", 2.3)):
        o = bpy.data.objects[f"{pre}{sx}"]
        r = o.matrix_world.to_euler(); reparent(o, (X0 + (0.46 if sx > 0 else -0.46), dy, 0.7), r)
# emissive lamp discs (4 round headlights), keyed with the lights
hm = bpy.data.materials.get("HeadLamp") or bpy.data.materials.new("HeadLamp"); hm.use_nodes = True
b = hm.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (1, 0.95, 0.85, 1)
b.inputs["Emission Color"].default_value = (1, 0.93, 0.78, 1)
es = b.inputs["Emission Strength"]
for f, v in [(1, 0), (82, 0), (84, 60), (391, 60), (393, 0)]: es.default_value = v; es.keyframe_insert("default_value", frame=f)
for o in [o for o in bpy.data.objects if o.name.startswith("LampDisc")]: bpy.data.objects.remove(o)
for x in (-0.56, -0.36, 0.36, 0.56):
    bpy.ops.mesh.primitive_circle_add(vertices=24, radius=0.07, fill_type="NGON", location=(X0 + x, 2.108, 0.70), rotation=(math.radians(-90), 0, 0))
    d = bpy.context.object; d.name = "LampDisc"; d.data.materials.append(hm)
    for u in list(d.users_collection): u.objects.unlink(d)
    bpy.data.collections["Car"].objects.link(d); bpy.context.view_layer.update()
    mw = d.matrix_world.copy(); d.parent = rig; d.matrix_parent_inverse = rig.matrix_world.inverted(); d.matrix_world = mw
bpy.context.view_layer.update()
print("cam5", [round(v, 2) for v in c.matrix_world.translation], "target", [round(v, 2) for v in bpy.data.objects["T_carbody"].matrix_world.translation])
