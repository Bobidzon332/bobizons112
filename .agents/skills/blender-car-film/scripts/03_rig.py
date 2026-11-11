import bpy
from mathutils import Vector, Matrix
sc = bpy.context.scene; car = bpy.data.collections["Car"]
root = bpy.data.objects["Sketchfab_model"]
rig = bpy.data.objects.new("CarRig", None); car.objects.link(rig); rig.empty_display_size = 1
S = 2.52
c = Vector((-3.956, 7.33, -0.003))
root.parent = rig
root.matrix_parent_inverse = Matrix.Translation(-c)  # car centre at rig origin
rig.scale = (S, S, S)
# wheel origins at their geometry centre so they spin in place
bpy.context.view_layer.update()
for n in ("wheel_003_tire_DefaultMaterial_0", "wheel_004_tire_DefaultMaterial_0"):
    o = bpy.data.objects[n]
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
bpy.context.view_layer.update()
for n in ("wheel_003_tire_DefaultMaterial_0", "wheel_004_tire_DefaultMaterial_0", "body_66_body_0"):
    o = bpy.data.objects[n]; bb = [o.matrix_world @ Vector(v) for v in o.bound_box]
    print(n, "origin", [round(x,3) for x in o.matrix_world.translation], "zmin", round(min(p.z for p in bb),3), "zmax", round(max(p.z for p in bb),3), "rot", [round(x,3) for x in o.rotation_euler], o.rotation_mode, "parent", o.parent.name if o.parent else None)
