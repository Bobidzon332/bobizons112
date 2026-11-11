import bpy, math
from mathutils import Vector, Matrix
sc = bpy.context.scene
fx = bpy.data.collections.get("FX") or bpy.data.collections.new("FX")
if fx.name not in sc.collection.children: sc.collection.children.link(fx)
for o in list(fx.objects): bpy.data.objects.remove(o)
def link(o):
    for u in list(o.users_collection): u.objects.unlink(o)
    fx.objects.link(o); return o
def flake(name, r, m, subdiv=1):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=subdiv); o = link(bpy.context.object); o.name = name
    o.data.materials.append(m); o.hide_render = False; o.location = (0, -200, -50); return o
snowm = mat("Flake", (0.95, 0.97, 1.0), 0.4)
snowm.node_tree.nodes["Principled BSDF"].inputs["Subsurface Weight"].default_value = 0.3
def emitter(name, size, loc, count, life, start, end, vel=(0, 0, 0), normal=0.0, rand=0.0, grav=1.0, brown=0.0, inst=None, smin=1.0, srand=0.5, disp=10, parent=None):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc); o = link(bpy.context.object); o.name = name; o.scale = size
    o.hide_render = False; o.visible_camera = False; o.visible_shadow = False
    ps = o.modifiers.new(name, "PARTICLE_SYSTEM").particle_system.settings
    ps.count = count; ps.lifetime = life; ps.frame_start = start; ps.frame_end = end; ps.emit_from = "FACE"
    ps.normal_factor = normal; ps.object_align_factor = vel; ps.factor_random = rand
    ps.effector_weights.gravity = grav; ps.brownian_factor = brown; ps.use_rotations = True; ps.rotation_factor_random = 1
    ps.render_type = "OBJECT"; ps.instance_object = inst; ps.particle_size = smin; ps.size_random = srand
    ps.display_percentage = disp
    if parent:
        mw = o.matrix_world.copy(); o.parent = parent; o.matrix_world = mw
    return o, ps
# 1) falling snow over the whole route (pre-rolled so it is already falling at frame 1)
f1 = flake("SnowFlake", 0.02, snowm)
o, ps = emitter("SnowFall", (60, 170, 1), (0, 60, 16), 90000, 600, -400, 480, rand=0.3, grav=0.035, brown=0.6, inst=f1, smin=1.0, srand=0.7, disp=3)
o.visible_camera = False
# 2) volumetric fog box (gives light cones)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 60, 9)); fog = link(bpy.context.object); fog.name = "FogVolume"; fog.scale = (90, 220, 18)
fm = bpy.data.materials.new("Fog"); fm.use_nodes = True; nt = fm.node_tree; nt.nodes.remove(nt.nodes["Principled BSDF"])
pv = nt.nodes.new("ShaderNodeVolumePrincipled"); pv.inputs["Density"].default_value = 0.012; pv.inputs["Color"].default_value = (0.75, 0.82, 1.0, 1)
pv.inputs["Anisotropy"].default_value = 0.55
nt.links.new(pv.outputs[0], nt.nodes["Material Output"].inputs["Volume"]); fog.data.materials.append(fm); fog.display_type = "BOUNDS"
# 3) exhaust steam: small volumetric puffs from tail pipe (rear-right under bumper), on while engine runs
rig = bpy.data.objects["CarRig"]; sc.frame_set(1); bpy.context.view_layer.update()
sm = bpy.data.materials.new("Steam"); sm.use_nodes = True; nt = sm.node_tree; nt.nodes.remove(nt.nodes["Principled BSDF"])
pv = nt.nodes.new("ShaderNodeVolumePrincipled"); pv.inputs["Density"].default_value = 1.2; pv.inputs["Color"].default_value = (0.9, 0.92, 0.95, 1)
nt.links.new(pv.outputs[0], nt.nodes["Material Output"].inputs["Volume"])
puff = flake("SteamPuff", 0.12, sm, 2)
o, ps = emitter("Exhaust", (0.08, 0.08, 1), (1.9 + 0.45, -2.45, 0.28), 700, 45, 80, 396, vel=(0, -1.2, 0.25), rand=0.4, grav=-0.04, brown=0.8, inst=puff, smin=1.0, srand=0.8, disp=20, parent=rig)
o.rotation_euler = (math.radians(90), 0, 0); ps.use_size_deflect = False
# grow puffs over life via particle size curve is not exposed; use random size + brownian for spread
# 4) tyre snow spray: chunks + powder kicked back from each rear/front wheel while moving
chunk = flake("SnowChunk", 0.03, snowm)
for i, (wx, wy) in enumerate([(-0.72, -1.28), (0.72, -1.28), (-0.72, 1.5), (0.72, 1.5)]):
    o, ps = emitter(f"Spray{i}", (0.2, 0.15, 1), (1.9 + wx, wy - 0.3, 0.05), 1800 if wy < 0 else 700, 30, 128, 384,
                    vel=(0, -3.5, 1.6), rand=0.9, grav=1.0, inst=chunk, smin=0.8, srand=0.9, disp=20, parent=rig)
    o.rotation_euler = (math.radians(90), 0, 0)
print("fx ok")
