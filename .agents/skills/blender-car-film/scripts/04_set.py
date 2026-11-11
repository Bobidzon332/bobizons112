import bpy, os, math, random
from mathutils import Vector
A = os.path.expanduser("~/blender-car-film/assets/ph")
sc = bpy.context.scene; random.seed(7)
for n in ("_tmpsun",):
    if n in bpy.data.objects: bpy.data.objects.remove(bpy.data.objects[n])
rig = bpy.data.objects["CarRig"]; rig.rotation_euler = (0, 0, 0)  # model front already faces +Y
def col(name, parent=None):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    p = parent or sc.collection
    if c.name not in p.children: p.children.link(c)
    return c
lib = col("Lib"); setc = col("Set")
sc.view_layers[0].layer_collection.children["Lib"].exclude = True
def load(m):
    if m in bpy.data.collections: return bpy.data.collections[m]
    d = os.path.join(A, "models", m); f = next(x for x in os.listdir(d) if x.endswith(".gltf"))
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(d, f))
    c = col(m, lib)
    for o in set(bpy.data.objects) - before:
        for u in list(o.users_collection): u.objects.unlink(o)
        c.objects.link(o)
    return c
def inst(m, loc, rot=0, s=1.0, name=None):
    o = bpy.data.objects.new(name or m, None); o.instance_type = "COLLECTION"; o.instance_collection = load(m)
    o.location = loc; o.rotation_euler = (0, 0, rot); o.scale = (s, s, s); setc.objects.link(o); return o
def mat(name, color, rough=0.6, emit=None, strength=0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    return m
def box(name, size, loc, m, rot=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name
    o.scale = size; o.rotation_euler = (0, 0, rot); bpy.ops.object.transform_apply(scale=True)
    bpy.ops.uv.cube_project(cube_size=1) if False else None
    o.data.materials.append(m)
    for u in list(o.users_collection): u.objects.unlink(o)
    setc.objects.link(o); return o
def text(name, body, loc, size, m, rot=(math.pi/2, 0, 0)):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.extrude = 0.02
    o = bpy.data.objects.new(name, cu); o.location = loc; o.rotation_euler = rot; o.data.materials.append(m); setc.objects.link(o); return o
def lamp_light(name, loc, power, color, radius=0.15, spot=None):
    L = bpy.data.lights.new(name, "SPOT" if spot else "POINT"); L.energy = power; L.color = color; L.shadow_soft_size = radius
    if spot: L.spot_size = spot; L.spot_blend = 0.6
    o = bpy.data.objects.new(name, L); o.location = loc; setc.objects.link(o); return o

SODIUM = (1.0, 0.55, 0.22)
# streetlights: hero lamp over the parked car + every ~32 m alternating sides
for i, y in enumerate([1.5, 30, 62, 94, 118]):
    side = 1 if i % 2 == 0 else -1
    inst("street_lamp_01", (side * 4.6, y, 0), rot=(math.pi/2 if side > 0 else -math.pi/2))
    l = lamp_light(f"StreetLight{i}", (side * 3.0, y, 6.2), 2500 if i == 0 else 1600, SODIUM, 0.2, spot=math.radians(120))
# power poles on left side
for y in range(-20, 190, 34): inst("modular_electricity_poles", (-6.5, y, 0), rot=math.pi/2)
inst("fire_hydrant", (4.3, 6, 0), rot=0.3)
inst("utility_box_01", (-4.8, 12, 0), rot=math.pi/2)
# pine forest both sides
for y in range(-40, 200, 5):
    for side in (-1, 1):
        for k in range(2):
            x = side * random.uniform(9 + k * 10, 18 + k * 14)
            if 100 < y < 125 and side > 0: continue  # clearing for house
            if 20 < y < 34 and side > 0 and x < 20: continue  # school yard
            inst(random.choice(["pine_tree_01", "fir_tree_01", "pine_tree_01"]), (x, y + random.uniform(-2, 2), 0), random.uniform(0, 6.28), random.uniform(0.8, 1.3))

# SCHOOL gate (right side, y 22..32)
brick = bpy.data.materials.get("Brick") or bpy.data.materials.new("Brick")
stone = mat("Pillar", (0.35, 0.3, 0.27), 0.85); iron = mat("Iron", (0.03, 0.03, 0.03), 0.4)
signm = mat("SchoolSign", (0.08, 0.2, 0.12), 0.5); letter = mat("Letters", (0.9, 0.88, 0.8), 0.4)
for y in (23.5, 30.5): box("GatePillar", (0.6, 0.6, 2.6), (5.0, y, 1.3), stone)
for k in range(24): box("GateBar", (0.04, 0.04, 2.1), (5.0, 23.9 + k * 0.27, 1.05), iron)
box("GateRail", (0.06, 6.6, 0.08), (5.0, 27, 2.0), iron); box("GateRail2", (0.06, 6.6, 0.08), (5.0, 27, 0.2), iron)
box("SchoolBoard", (0.08, 4.2, 0.8), (5.0, 27, 3.0), signm)
text("SchoolText", "SCHOOL", (4.94, 27, 2.86), 0.45, letter, rot=(math.pi/2, 0, -math.pi/2))
box("SchoolBuilding", (12, 18, 7), (19, 27, 3.5), mat("SchoolWall", (0.25, 0.2, 0.17), 0.9))
for k in range(5): box("SchoolWin", (0.05, 1.6, 1.4), (12.97, 20 + k * 3.5, 4.2), mat("WinDark", (0.02, 0.025, 0.03), 0.1))
# HOSPITAL sign (left side, y ~44)
box("HospPole", (0.15, 0.15, 3.2), (-4.8, 44, 1.6), iron)
box("HospBox", (0.25, 1.4, 1.4), (-4.8, 44, 3.6), mat("HospBlue", (0.02, 0.15, 0.6), 0.3, emit=(0.1, 0.4, 1.0), strength=6))
text("HospH", "H", (-4.65, 44, 3.25), 1.0, mat("HospWhite", (1, 1, 1), 0.3, emit=(1, 1, 1), strength=12), rot=(math.pi/2, 0, math.pi/2))
lamp_light("HospGlow", (-4.2, 44, 3.6), 120, (0.3, 0.55, 1.0), 0.6)
hb = box("HospBuilding", (16, 30, 12), (-24, 52, 6), mat("HospWall", (0.55, 0.57, 0.6), 0.8))
winlit = mat("WinLit", (0.6, 0.6, 0.5), 0.2, emit=(1.0, 0.9, 0.7), strength=3)
for r in range(3):
    for k in range(7): box("HospWin", (0.05, 2.2, 1.4), (-15.97, 40 + k * 4, 2.5 + r * 3.5), winlit if random.random() < 0.45 else bpy.data.materials["WinDark"])
print("set ok", len(setc.objects))
