import bpy, math, bmesh
setc = bpy.data.collections["Set"]
siding = pbr("Siding", "weathered_plank_siding", 0.5, tint=(0.75, 0.8, 0.85))
roofm = pbr("Roof", "grey_roof_tiles", 0.4)
def uvbox(name, size, loc, m):
    o = box(name, size, loc, m)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT"); bpy.ops.uv.cube_project(cube_size=1)
    bpy.ops.object.mode_set(mode="OBJECT"); o.select_set(False); return o
HX, HY = 13.0, 112.0  # house centre; front wall faces the road (-X)
uvbox("HouseBody", (8, 10, 3.4), (HX, HY, 1.7), siding)
# gable roof (prism along Y)
me = bpy.data.meshes.new("Roof"); bm = bmesh.new()
w, l, h, z0, ov = 4.6, 5.6, 2.4, 3.4, 0
vs = [bm.verts.new(v) for v in [(-w,-l,z0),(w,-l,z0),(0,-l,z0+h),(-w,l,z0),(w,l,z0),(0,l,z0+h)]]
for f in [(0,1,2),(3,5,4),(0,3,4,1),(0,2,5,3),(1,4,5,2)]: bm.faces.new([vs[i] for i in f])
bm.normal_update(); bm.to_mesh(me); bm.free()
ro = bpy.data.objects.new("HouseRoof", me); ro.location = (HX, HY, 0); setc.objects.link(ro); me.materials.append(roofm)
bpy.context.view_layer.objects.active = ro; ro.select_set(True)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT"); bpy.ops.uv.cube_project(cube_size=1); bpy.ops.object.mode_set(mode="OBJECT")
# snow on roof
sn = bpy.data.objects.new("RoofSnow", me.copy()); sn.location = (HX, HY, 0.06); sn.scale = (1.01, 1.0, 1.0); setc.objects.link(sn)
sn.data.materials.clear(); sn.data.materials.append(bpy.data.materials["Snow1"])
# front: door, windows, porch
fx = HX - 4.02
door = box("Door", (0.08, 1.0, 2.1), (fx, HY, 1.05), mat("DoorWood", (0.12, 0.05, 0.03), 0.6))
for dy in (-3, 3):
    box(f"Win{dy}", (0.06, 1.4, 1.2), (fx, HY + dy, 1.8), mat("WinHouse", (0.01, 0.012, 0.015), 0.05))
    box(f"WinFrame{dy}", (0.07, 1.55, 0.08), (fx - 0.01, HY + dy, 1.18), mat("Trim", (0.8, 0.8, 0.78), 0.5))
box("PorchFloor", (2.2, 3.4, 0.25), (fx - 1.1, HY, 0.12), bpy.data.materials["Snow1"])
box("PorchRoof", (2.4, 3.6, 0.12), (fx - 1.1, HY, 2.75), roofm)
for dy in (-1.6, 1.6): box("PorchPost", (0.12, 0.12, 2.6), (fx - 2.1, HY + dy, 1.35), bpy.data.materials["Trim"])
# porch lamp: bulb + light, both keyed off->on later
bulbm = mat("PorchBulb", (1, 0.8, 0.5), 0.3, emit=(1.0, 0.62, 0.28), strength=0)
box("PorchBulb", (0.18, 0.18, 0.25), (fx - 0.15, HY + 0.8, 2.35), bulbm)
pl = lamp_light("PorchLight", (fx - 0.5, HY + 0.8, 2.3), 0, (1.0, 0.62, 0.3), 0.1)
box("Path", (6.5, 1.4, 0.06), (fx - 4.2, HY, 0.05), bpy.data.materials["RoadSnow"])
# mailbox + fence near house
inst("modular_chainlink_fence", (6.5, 103, 0), rot=math.pi/2)
print("house ok")
