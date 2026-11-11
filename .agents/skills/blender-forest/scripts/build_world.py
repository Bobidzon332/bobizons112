"""Stage B: terrain + ground material + HDRI world (light-path split) + sun + colour management.

Run (headless, low priority set inside):
  blender -b --factory-startup --python scripts/build_world.py
Writes scene/forest.blend. Re-runnable: always rebuilds from scratch.
"""
import bpy, bmesh, math, os, sys, ctypes
from mathutils import Vector

ROOT = os.path.join(os.path.expanduser("~"), "blender-forest")
ASSETS = os.path.join(ROOT, "assets")
TERRAIN_BLEND = os.path.join(ASSETS, "Remeshed Terrain", "Remeshed Terrain.blend")
LIB_BLEND = os.path.join(ASSETS, "Plant models", "assets", "AE_15th Assets.blend")
HDRI = os.path.join(ASSETS, "Ever_cabins_cloud_layers_8k", "Ever_cabins_cloud_layers_8k.hdr")
OUT = os.path.join(ROOT, "scene", "forest.blend")


def low_priority():
    # Keep the PC responsive: BELOW_NORMAL_PRIORITY_CLASS for this Blender process.
    try:
        k = ctypes.windll.kernel32
        k.SetPriorityClass(k.GetCurrentProcess(), 0x00004000)
    except Exception as e:
        print("priority not set:", e)


def clear_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)


def get_collection(name):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    return col


def append(blend, kind, name):
    with bpy.data.libraries.load(blend, link=False) as (src, dst):
        if name not in getattr(src, kind):
            raise RuntimeError(f"{name} not in {blend}")
        setattr(dst, kind, [name])
    return getattr(dst, kind)[0]


def build_terrain():
    obj = append(TERRAIN_BLEND, "objects", "Terrain")
    get_collection("Terrain").objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    # Apply the 90x scale (his file keeps it unapplied).
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    # More geometry for masks/displacement (he subdivides before painting).
    sub = obj.modifiers.new("Subdiv", "SUBSURF")
    sub.subdivision_type = "SIMPLE"
    sub.levels = sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier=sub.name)

    # Gentle clouds displacement: size 6, depth 5, almost flat (his settings).
    tex = bpy.data.textures.new("TerrainClouds", "CLOUDS")
    tex.noise_scale = 6.0
    tex.noise_depth = 5
    disp = obj.modifiers.new("Displace", "DISPLACE")
    disp.texture = tex
    disp.texture_coords = "GLOBAL"
    disp.strength = 1.6
    disp.mid_level = 0.5
    bpy.ops.object.modifier_apply(modifier=disp.name)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    obj.location = (0, 0, 0)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

    # Level the cabin site (his cabins sit on flat ground), blending out over 6 m.
    import numpy as np
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import layout as L
    me = obj.data
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    d = L.dist_to_cabin(co[:, :2])
    site_z = float(np.median(co[d < 0, 2]))
    w = (1.0 - L.smoothstep(0.0, 6.0, d)) * (1.0 if L.USE_CABINS else 0.0)
    co[:, 2] = co[:, 2] * (1.0 - w) + site_z * w
    me.vertices.foreach_set("co", co.ravel())
    me.update()
    print(f"cabin site levelled at z={site_z:.2f}")

    # Planar top-down UVs, 0..1 across the terrain (mapping scale 50 tiles it).
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    uv = bm.loops.layers.uv.new("UVMap")
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    minx, miny = min(xs), min(ys)
    size = max(max(xs) - minx, max(ys) - miny)
    for f in bm.faces:
        for l in f.loops:
            l[uv].uv = ((l.vert.co.x - minx) / size, (l.vert.co.y - miny) / size)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    print(f"terrain: {len(me.vertices)} verts, size {size:.1f} m")
    return obj


def ground_material(obj):
    mat = append(LIB_BLEND, "materials", "AE_15th_Leafs_Soil_Ground")
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    nt = mat.node_tree
    for n in nt.nodes:
        if n.type == "HUE_SAT":
            n.inputs["Saturation"].default_value = 1.2
            n.inputs["Value"].default_value = 1.2
        if n.type == "DISPLACEMENT":
            n.inputs["Scale"].default_value = 0.2
    # Library material has no mapping: add UV -> Mapping (scale 50) into every image,
    # so the 4k soil texture tiles every ~3.6 m instead of stretching over 179 m.
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-1300, 0)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-1100, 0)
    mp.inputs["Scale"].default_value = (50, 50, 50)
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
    for n in nt.nodes:
        if n.type == "TEX_IMAGE":
            nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
    mat.displacement_method = "BOTH"
    print("ground material nodes:", sorted({n.type for n in nt.nodes}))


def build_world():
    world = bpy.data.worlds.new("ForestWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    N = nt.nodes.new
    L = nt.links.new
    img = bpy.data.images.load(HDRI, check_existing=True)

    def chain(y, strength, label):
        tc = N("ShaderNodeTexCoord"); tc.location = (-1400, y)
        mp = N("ShaderNodeMapping"); mp.location = (-1200, y)
        mp.inputs["Location"].default_value = (0, 0, 0.25)  # pushes the HDRI ground below the horizon
        mp.inputs["Rotation"].default_value = (0, 0, math.radians(0))
        env = N("ShaderNodeTexEnvironment"); env.location = (-1000, y); env.image = img
        gm = N("ShaderNodeGamma"); gm.location = (-700, y); gm.inputs["Gamma"].default_value = 1.0
        hs = N("ShaderNodeHueSaturation"); hs.location = (-500, y)
        bg = N("ShaderNodeBackground"); bg.location = (-250, y); bg.label = label
        bg.inputs["Strength"].default_value = strength
        L(tc.outputs["Generated"], mp.inputs["Vector"])
        L(mp.outputs["Vector"], env.inputs["Vector"])
        L(env.outputs["Color"], gm.inputs["Color"])
        L(gm.outputs["Color"], hs.inputs["Color"])
        L(hs.outputs["Color"], bg.inputs["Color"])
        return bg

    light = chain(300, 2.25, "Lighting")   # what objects see
    sky = chain(-300, 1.0, "Sky")          # what the camera sees directly
    lp = N("ShaderNodeLightPath"); lp.location = (-250, 650)
    mix = N("ShaderNodeMixShader"); mix.location = (0, 0)
    out = N("ShaderNodeOutputWorld"); out.location = (200, 0)
    L(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
    L(light.outputs["Background"], mix.inputs[1])
    L(sky.outputs["Background"], mix.inputs[2])
    L(mix.outputs["Shader"], out.inputs["Surface"])


def build_sun():
    data = bpy.data.lights.new("Sun", "SUN")
    data.energy = 10.0
    data.color = (1.0, 0.95, 0.88)  # slightly warm
    data.angle = math.radians(1.5)
    sun = bpy.data.objects.new("Sun", data)
    get_collection("Lighting").objects.link(sun)
    sun.location = (0, 0, 30)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import layout as L
    az, el = math.radians(L.SUN_AZIMUTH), math.radians(L.SUN_ELEVATION)
    to_sun = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    sun.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()


def colour_management():
    sc = bpy.context.scene
    sc.display_settings.display_device = "sRGB"
    vs = sc.view_settings
    vs.view_transform = "Filmic"
    # Look enum is dynamic (enum_items only shows NONE), so set by name.
    vs.look = "High Contrast"
    vs.exposure = 1.5
    vs.gamma = 0.9
    print("colour:", vs.view_transform, "/", vs.look)


def render_settings():
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = d.type == "OPTIX"
    sc.cycles.device = "GPU"
    sc.render.fps = 30
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.cycles.samples = 256
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.01
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPTIX"
    sc.render.use_motion_blur = True
    # Keep the CPU free for your other apps.
    sc.render.threads_mode = "FIXED"
    sc.render.threads = 8
    sc.render.use_persistent_data = False


def main():
    low_priority()
    clear_scene()
    terrain = build_terrain()
    ground_material(terrain)
    build_world()
    build_sun()
    colour_management()
    render_settings()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT, relative_remap=True)
    print("SAVED", OUT)


main()
