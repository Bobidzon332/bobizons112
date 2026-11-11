"""Cheap look-dev still from scene/forest.blend (does not modify the .blend).

  blender -b scene/forest.blend --python scripts/test_still.py -- <out.png> [samples] [width]
"""
import bpy, sys, os, math, ctypes
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[0] if argv else os.path.join(os.path.expanduser("~"), "blender-forest", "scene", "tests", "still.png")
samples = int(argv[1]) if len(argv) > 1 else 32
width = int(argv[2]) if len(argv) > 2 else 960

try:
    k = ctypes.windll.kernel32
    k.SetPriorityClass(k.GetCurrentProcess(), 0x00004000)  # below normal
except Exception:
    pass

sc = bpy.context.scene
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "OPTIX"
sc.cycles.device = "GPU"

cam = sc.camera
if cam is None:
    # Default look-dev camera: eye level (~0.6 m) like shot 2, looking across the ground.
    data = bpy.data.cameras.new("LookDev")
    data.lens = 28
    cam = bpy.data.objects.new("LookDev", data)
    sc.collection.objects.link(cam)
    terrain = bpy.data.objects["Terrain"]
    dg = bpy.context.evaluated_depsgraph_get()
    x, y = 6.0, -4.0
    hit, loc, *_ = sc.ray_cast(dg, Vector((x, y, 50)), Vector((0, 0, -1)))
    z = loc.z if hit else 0.0
    cam.location = (x, y, z + 0.6)
    cam.rotation_euler = (math.radians(86), 0, math.radians(20))
    sc.camera = cam

sc.render.resolution_x = width
sc.render.resolution_y = round(width * 9 / 16)
sc.render.resolution_percentage = 100
sc.cycles.samples = samples
sc.render.use_simplify = True
sc.cycles.texture_limit_render = "2048"
sc.render.use_motion_blur = False
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = out
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.render.render(write_still=True)
print("STILL", out)
