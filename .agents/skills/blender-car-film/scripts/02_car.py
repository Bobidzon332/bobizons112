import bpy, os
from mathutils import Vector
sc = bpy.context.scene
car = bpy.data.collections.new("Car"); sc.collection.children.link(car)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=os.path.expanduser("~/blender-car-film/assets/peugeot_504.glb"))
new = [o for o in bpy.data.objects if o not in before]
for o in new:
    for c in list(o.users_collection): c.objects.unlink(o)
    car.objects.link(o)
roots = [o for o in new if o.parent is None]
print("roots", [r.name for r in roots])
bpy.context.view_layer.update()
for o in new:
    if o.type == "MESH":
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        mn = [round(min(p[i] for p in bb), 3) for i in range(3)]; mx = [round(max(p[i] for p in bb), 3) for i in range(3)]
        print(o.name, "min", mn, "max", mx)
