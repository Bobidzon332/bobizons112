"""Stage C: our own scatter system (replaces his paid Geo-Scatter).

How it works:
  1. Link (not copy) his plant objects from the library .blend into hidden LIB_* collections.
  2. Compute one density-factor attribute per layer on the terrain vertices in Python
     (path/cabin clearings, focus area, Musgrave-like patterns, his "reduce density").
  3. Each layer = an empty mesh object with a Geometry Nodes modifier we build here:
     Object Info(Terrain) -> Distribute Points (density x attribute) -> Instance on Points
     with his rotation/scale rules. Everything stays instanced (12 GB VRAM friendly).

Run:  blender -b scene/forest.blend --python scripts/scatter.py
Re-runnable: removes the previous scatter first, then saves scene/forest.blend.
"""
import bpy, math, os, sys, ctypes
import numpy as np
from mathutils import noise, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

ROOT = os.path.join(os.path.expanduser("~"), "blender-forest")
LIB_BLEND = os.path.join(ROOT, "assets", "Plant models", "assets", "AE_15th Assets.blend")
P = "AE_15TH_"

try:
    k = ctypes.windll.kernel32
    k.SetPriorityClass(k.GetCurrentProcess(), 0x00004000)  # below normal
except Exception:
    pass


def names(prefix, nums):
    return [f"{P}{prefix}_{n:02d}" for n in nums]


# Layer table: his numbers from the tutorial where he gives them.
#  density   = instances per m2 before masks (Geo-Scatter "instances")
#  vi        = vertical influence (1 = straight up, 0 = follow ground normal)
#  scale     = (min, max) uniform scale; zmul squashes height
LAYERS = [
    dict(name="BirchTrees", objs=names("BIRCH", range(1, 12)), density=0.06, poisson=1.5,
         mask="trees", pattern=(1 / 25.0, 1.0, 1.0), pattern_infl=0.3, vi=0.85, tilt=5, scale=(1.6, 1.6), seed=11),
    dict(name="YoungTrees", objs=names("TREE_YOUNG", (1, 2)), density=0.05, poisson=1.5,
         mask="trees", vi=0.85, tilt=5, scale=(0.7, 1.3), seed=12),
    dict(name="BigTrees", objs=names("TREE", (1, 2, 3)), density=0.012, poisson=5.0,
         mask="trees", vi=0.9, tilt=3, scale=(0.9, 1.2), seed=13),
    dict(name="LargeShrubs", objs=names("FOREST_BUSH", range(1, 8)), density=0.5,
         mask="shrubs", pattern=(1 / 12.0, 0.7, 1.6), vi=0.4, tilt=8, scale=(1.07, 1.6), seed=14),
    dict(name="SmallShrubs", objs=names("FOREST_BUSH", range(3, 8)), density=0.4,
         mask="cabin_ring", vi=0.5, tilt=0, scale=(0.35, 0.7), seed=15),
    dict(name="Ferns", objs=names("FERN", range(1, 8)), density=5.0,
         mask="ground", pattern=(1 / 4.0, 1.23, 1.87), pattern_infl=0.6, vi=0.5, tilt=10, scale=(0.6, 1.5), seed=16),
    dict(name="Branches", objs=names("BRANCH", [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]),
         density=1.85, mask="ground", vi=0.0, tilt=0, scale=(0.5, 1.5), seed=17),
    dict(name="Debris", objs=names("DEBRIS", range(3, 16)), density=3.0,
         mask="ground", vi=0.0, tilt=0, scale=(0.34, 1.0), zoff=0.01, seed=18),
    dict(name="Leaves", objs=names("DRY_LEAVES", (1, 2, 3)), density=200.0 * 0.18,  # 70% reduce + thinned (litter read as tiles)
         mask="leaves", pattern=(1 / 10.0, 0.9, 1.0), pattern_infl=0.9,
         vi=0.0, tilt=0, scale=(0.4, 0.8), seed=19),
    dict(name="GroundPlants", objs=names("GROUND_PLANT", range(1, 7)), density=24.0 * 0.5,  # 50% reduce
         mask="ground", vi=0.5, tilt=0, scale=(0.6, 1.4), zmul=0.9, seed=20),
    # Seen in his frames (rocks, fallen logs, stumps) but placed by hand in the video.
    dict(name="Rocks", objs=names("ROCK", range(1, 9)), density=0.04,
         mask="ground", vi=0.3, tilt=20, scale=(0.6, 1.6), zoff=-0.05, seed=21),
    dict(name="FallenTrees", objs=names("FALLEN_TREE", range(1, 8)), density=0.008, poisson=4.0,
         mask="ground", vi=0.0, tilt=0, scale=(0.9, 1.4), zoff=-0.03, seed=22),
    dict(name="Stumps", objs=names("TREE_STUMP", (1, 2)), density=0.002,
         mask="trees", vi=0.6, tilt=0, scale=(0.8, 1.2), zoff=-0.03, seed=23),
]


# ---------------------------------------------------------------- cleanup
def remove_previous():
    for o in list(bpy.data.objects):
        if o.name.startswith("Scatter_"):
            me = o.data
            bpy.data.objects.remove(o, do_unlink=True)
            if me and me.users == 0:
                bpy.data.meshes.remove(me)
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith("ScatterGN_"):
            bpy.data.node_groups.remove(ng)
    for c in list(bpy.data.collections):
        if c.name.startswith("LIB_") or c.name in ("LIBRARY", "Scatter"):
            for o in list(c.objects):
                c.objects.unlink(o)
            bpy.data.collections.remove(c)


# ---------------------------------------------------------------- library
def link_library():
    wanted = sorted({n for layer in LAYERS for n in layer["objs"]})
    with bpy.data.libraries.load(LIB_BLEND, link=True) as (src, dst):
        missing = [n for n in wanted if n not in src.objects]
        if missing:
            raise RuntimeError(f"missing in library: {missing}")
        dst.objects = wanted
    linked = {o.name: o for o in dst.objects}
    lib_root = bpy.data.collections.new("LIBRARY")
    bpy.context.scene.collection.children.link(lib_root)
    for layer in LAYERS:
        col = bpy.data.collections.new("LIB_" + layer["name"])
        lib_root.children.link(col)
        for n in layer["objs"]:
            col.objects.link(linked[n])
        layer["collection"] = col
    # Excluded from the view layer: never rendered directly, only through instancing.
    bpy.context.view_layer.layer_collection.children["LIBRARY"].exclude = True


# ---------------------------------------------------------------- masks
def fbm(xy, freq, seed):
    off = Vector((seed * 31.7, seed * 17.3, seed * 5.1))
    return np.array([noise.fractal(Vector((x * freq, y * freq, 0.0)) + off, 1.0, 2.0, 4,
                                   noise_basis="PERLIN_ORIGINAL") for x, y in xy])


def pattern(xy, freq, bright, contrast, seed, infl=1.0):
    n = fbm(xy, freq, seed)
    v = np.clip(((0.5 + 0.5 * n) - 0.5) * contrast + 0.5, 0.0, 1.0) * bright
    v = np.clip(v, 0.0, 1.0)
    return 1.0 - infl + infl * v


def compute_masks(terrain):
    me = terrain.data
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    xy = co.reshape(-1, 3)[:, :2]
    d_path = L.dist_to_path(xy)
    d_cab = L.dist_to_cabin(xy)
    r = np.linalg.norm(xy, axis=1)
    hw = L.PATH_HALF_WIDTH
    edge_ok = 1.0 - L.smoothstep(84.0, 88.0, r)
    near = np.minimum(d_path, d_cab)
    focus = 1.0 - L.smoothstep(40.0, 55.0, near)
    if L.USE_CABINS:
        d_deck = L.dist_to_deck(xy)
        d_pad = L.dist_to_pad(xy)
    else:                                   # no cabins: nothing to clear there, forest fills in
        d_deck = d_pad = np.full(len(xy), 1e9)
        d_cab = np.full(len(xy), 1e9)
        near = d_path
    clear = np.maximum.reduce([1.0 - L.smoothstep(hw - 0.2, hw + 1.0, d_path),
                               1.0 - L.smoothstep(-0.2, 0.6, d_deck),
                               1.0 - L.smoothstep(-0.3, 0.8, d_pad)])
    focus = np.maximum(1.0 - L.smoothstep(40.0, 55.0, near), 1.0 - L.smoothstep(20.0, 30.0, d_cab))
    masks = {
        "trees": L.smoothstep(3.0, 5.0, d_path) * L.smoothstep(4.0, 7.0, d_cab) * edge_ok,
        "shrubs": L.smoothstep(2.0, 3.5, d_path) * L.smoothstep(2.0, 5.0, d_cab) * edge_ok,
        "ground": (1.0 - clear) * focus * edge_ok,
        "leaves": L.smoothstep(hw - 0.9, hw + 0.3, d_path) * (1.0 - clear * 0.85) * focus * edge_ok,
        "cabin_ring": L.smoothstep(-0.5, 0.5, d_cab) * (1.0 - L.smoothstep(4.0, 8.0, d_cab))
                      * L.smoothstep(2.0, 3.0, d_path),
    }
    # Path surface height above terrain, so litter at the gravel edges sits on top of it.
    t = np.clip(d_path / L.PATH_HALF_WIDTH, 0.0, 1.0)
    lift = np.where(d_path < L.PATH_HALF_WIDTH * 1.15,
                    L.LIFT_EDGE + (L.LIFT_MID - L.LIFT_EDGE) * (1.0 - t * t), 0.0)
    lift = np.maximum(lift, np.where(L.dist_to_pad(xy) < 0, L.LIFT_MID, 0.0))
    la = me.attributes.get("lift") or me.attributes.new("lift", "FLOAT", "POINT")
    la.data.foreach_set("value", lift.astype(np.float32))
    # Store a "center" weight like his vertex group (1 = cabin + path) for later stages.
    vg = terrain.vertex_groups.get("center") or terrain.vertex_groups.new(name="center")
    for i, w in enumerate(clear):
        if w > 0.001:
            vg.add([i], float(w), "REPLACE")
    for layer in LAYERS:
        f = masks[layer["mask"]].copy()
        if "pattern" in layer:
            freq, bright, contrast = layer["pattern"]
            f *= pattern(xy, freq, bright, contrast, layer["seed"], layer.get("pattern_infl", 1.0))
        attr_name = "d_" + layer["name"]
        a = me.attributes.get(attr_name) or me.attributes.new(attr_name, "FLOAT", "POINT")
        a.data.foreach_set("value", f.astype(np.float32))
        layer["attr"] = attr_name
        print(f"mask {layer['name']:13s} mean {f.mean():.3f}")


# ---------------------------------------------------------------- geometry nodes
def sock(sockets, name, kind=None):
    for s in sockets:
        if s.name == name and s.enabled and (kind is None or s.type == kind):
            return s
    raise KeyError(f"{name} ({kind})")


def build_group(layer, terrain):
    ng = bpy.data.node_groups.new("ScatterGN_" + layer["name"], "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, Ln = ng.nodes.new, ng.links.new
    gin = N("NodeGroupInput"); gout = N("NodeGroupOutput")

    info = N("GeometryNodeObjectInfo")
    info.transform_space = "RELATIVE"
    info.inputs["Object"].default_value = terrain

    attr = N("GeometryNodeInputNamedAttribute")
    attr.data_type = "FLOAT"
    attr.inputs["Name"].default_value = layer["attr"]

    dist = N("GeometryNodeDistributePointsOnFaces")
    if "poisson" in layer:
        dist.distribute_method = "POISSON"
        sock(dist.inputs, "Distance Min").default_value = layer["poisson"]
        sock(dist.inputs, "Density Max").default_value = layer["density"]
        Ln(sock(attr.outputs, "Attribute"), sock(dist.inputs, "Density Factor"))
    else:
        dist.distribute_method = "RANDOM"
        mul = N("ShaderNodeMath"); mul.operation = "MULTIPLY"
        mul.inputs[1].default_value = layer["density"]
        Ln(sock(attr.outputs, "Attribute"), mul.inputs[0])
        Ln(mul.outputs[0], sock(dist.inputs, "Density"))
    sock(dist.inputs, "Seed").default_value = layer["seed"]
    Ln(info.outputs["Geometry"], dist.inputs["Mesh"])

    # Rotation: lean between ground normal and world up, then random tilt + yaw.
    mix = N("ShaderNodeMix"); mix.data_type = "VECTOR"
    sock(mix.inputs, "Factor", "VALUE").default_value = layer["vi"]
    Ln(sock(dist.outputs, "Normal"), sock(mix.inputs, "A", "VECTOR"))
    sock(mix.inputs, "B", "VECTOR").default_value = (0, 0, 1)
    nrm = N("ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"
    Ln(sock(mix.outputs, "Result", "VECTOR"), nrm.inputs[0])
    align = N("FunctionNodeAlignRotationToVector"); align.axis = "Z"
    Ln(nrm.outputs["Vector"], sock(align.inputs, "Vector"))

    t = math.radians(layer["tilt"])
    rnd_rot = N("FunctionNodeRandomValue"); rnd_rot.data_type = "FLOAT_VECTOR"
    sock(rnd_rot.inputs, "Min", "VECTOR").default_value = (-t, -t, 0.0)
    sock(rnd_rot.inputs, "Max", "VECTOR").default_value = (t, t, 2 * math.pi)
    sock(rnd_rot.inputs, "Seed").default_value = layer["seed"] + 100
    e2r = N("FunctionNodeEulerToRotation")
    Ln(sock(rnd_rot.outputs, "Value", "VECTOR"), e2r.inputs[0])
    rot = N("FunctionNodeRotateRotation")
    try:
        rot.rotation_space = "LOCAL"
    except AttributeError:
        pass
    Ln(sock(align.outputs, "Rotation"), sock(rot.inputs, "Rotation"))
    Ln(e2r.outputs[0], sock(rot.inputs, "Rotate By"))

    # Scale: random uniform in (min, max), optional z squash.
    rnd_s = N("FunctionNodeRandomValue"); rnd_s.data_type = "FLOAT"
    sock(rnd_s.inputs, "Min", "VALUE").default_value = layer["scale"][0]
    sock(rnd_s.inputs, "Max", "VALUE").default_value = layer["scale"][1]
    sock(rnd_s.inputs, "Seed").default_value = layer["seed"] + 200
    zm = N("ShaderNodeMath"); zm.operation = "MULTIPLY"
    zm.inputs[1].default_value = layer.get("zmul", 1.0)
    s_out = sock(rnd_s.outputs, "Value", "VALUE")
    Ln(s_out, zm.inputs[0])
    cxyz = N("ShaderNodeCombineXYZ")
    Ln(s_out, cxyz.inputs[0]); Ln(s_out, cxyz.inputs[1]); Ln(zm.outputs[0], cxyz.inputs[2])

    # Random pick of which plant model.
    rnd_i = N("FunctionNodeRandomValue"); rnd_i.data_type = "INT"
    sock(rnd_i.inputs, "Min", "INT").default_value = 0
    sock(rnd_i.inputs, "Max", "INT").default_value = 9999
    sock(rnd_i.inputs, "Seed").default_value = layer["seed"] + 300

    col = N("GeometryNodeCollectionInfo")
    col.transform_space = "ORIGINAL"
    col.inputs["Collection"].default_value = layer["collection"]
    sock(col.inputs, "Separate Children").default_value = True
    sock(col.inputs, "Reset Children").default_value = True

    # Offset = (0, 0, lift + zoff): his z offset, plus riding on top of the gravel.
    lift = N("GeometryNodeInputNamedAttribute"); lift.data_type = "FLOAT"
    lift.inputs["Name"].default_value = "lift"
    add = N("ShaderNodeMath"); add.operation = "ADD"
    add.inputs[1].default_value = layer.get("zoff", 0.0)
    Ln(sock(lift.outputs, "Attribute"), add.inputs[0])
    off = N("ShaderNodeCombineXYZ")
    Ln(add.outputs[0], off.inputs[2])
    sp = N("GeometryNodeSetPosition")
    Ln(dist.outputs["Points"], sp.inputs["Geometry"])
    Ln(off.outputs[0], sp.inputs["Offset"])
    pts = sp.outputs["Geometry"]

    iop = N("GeometryNodeInstanceOnPoints")
    Ln(pts, iop.inputs["Points"])
    Ln(col.outputs[0], iop.inputs["Instance"])
    sock(iop.inputs, "Pick Instance").default_value = True
    Ln(sock(rnd_i.outputs, "Value", "INT"), sock(iop.inputs, "Instance Index"))
    Ln(rot.outputs[0], sock(iop.inputs, "Rotation"))
    Ln(cxyz.outputs[0], sock(iop.inputs, "Scale"))
    Ln(iop.outputs["Instances"], gout.inputs[0])
    return ng


def build_layers(terrain):
    scol = bpy.data.collections.new("Scatter")
    bpy.context.scene.collection.children.link(scol)
    for layer in LAYERS:
        me = bpy.data.meshes.new("Scatter_" + layer["name"])
        ob = bpy.data.objects.new("Scatter_" + layer["name"], me)
        scol.objects.link(ob)
        mod = ob.modifiers.new("Scatter", "NODES")
        mod.node_group = build_group(layer, terrain)
        mod.show_viewport = False   # keep the UI light when the file is opened by hand


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    counts = {}
    for inst in dg.object_instances:
        if inst.is_instance and inst.parent and inst.parent.name.startswith("Scatter_"):
            k = inst.parent.name[8:]
            counts[k] = counts.get(k, 0) + 1
    for k, v in counts.items():
        print(f"instances {k:13s} {v:8d}")
    print("instances total", sum(counts.values()))


def apply_overrides():
    """look_params.json -> "scatter": {"Ferns": {"density_mul": 1.5, "scale_mul": 1.1}, ...}"""
    import json
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "look_params.json")
    if not os.path.exists(p):
        return
    ov = json.load(open(p, encoding="utf-8")).get("scatter", {})
    for layer in LAYERS:
        o = ov.get(layer["name"])
        if o:
            layer["density"] *= o.get("density_mul", 1.0)
            sm = o.get("scale_mul", 1.0)
            layer["scale"] = (layer["scale"][0] * sm, layer["scale"][1] * sm)
            print("override", layer["name"], o)


def main():
    apply_overrides()
    remove_previous()
    terrain = bpy.data.objects["Terrain"]
    link_library()
    compute_masks(terrain)
    build_layers(terrain)
    if "--count" in sys.argv:
        for o in bpy.data.objects:
            if o.name.startswith("Scatter_"):
                o.modifiers["Scatter"].show_viewport = True
        report()
        for o in bpy.data.objects:
            if o.name.startswith("Scatter_"):
                o.modifiers["Scatter"].show_viewport = False
    bpy.ops.wm.save_mainfile(relative_remap=True)
    print("SAVED", bpy.data.filepath)


main()
