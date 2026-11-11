# NIGHT conversion (refs: Extra 3D "Realistic Night Time Lighting" + "Photorealistic Renders", Enhanced Sight urban breakdown):
#  night is lit by PRACTICAL sources, not the sky -> dark gradient sky with city glow, faint blue moon,
#  LED street lamps (3200 K, real lamp head glows), lit windows (warm/cool, random), car head/tail lights on moving cars,
#  red traffic signals, blue-tinted fog with a little emission, wet asphalt (puddles + damp) for reflections.
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
from mathutils import Vector, Matrix, Euler
sc = bpy.context.scene
NIGHT = coll("NIGHT LIGHTS", coll("ENVIRONMENT"))
for o in list(NIGHT.objects): bpy.data.objects.remove(o)

def bb(k):
    """blackbody approx (Kelvin -> linear RGB), good enough for lamp colours"""
    t = k / 100.0
    r = 255 if t <= 66 else 329.7 * ((t - 60) ** -0.1332)
    g = 99.47 * math.log(t) - 161.12 if t <= 66 else 288.12 * ((t - 60) ** -0.0755)
    b = 255 if t >= 66 else (0 if t <= 19 else 138.52 * math.log(t - 10) - 305.04)
    c = [max(0, min(255, x)) / 255 for x in (r, g, b)]
    return tuple((x / 1.0) ** 2.2 for x in c)

# ---------- sky: dark, warm city glow at the horizon, deep blue overhead ----------
day = bpy.data.worlds.get("City Sky")
wd = bpy.data.worlds.get("City Night") or bpy.data.worlds.new("City Night")
sc.world = wd; wd.use_nodes = True
nt = wd.node_tree; n = nt.nodes; l = nt.links; n.clear()
tc = n.new("ShaderNodeTexCoord"); sep = n.new("ShaderNodeSeparateXYZ"); l.new(tc.outputs["Generated"], sep.inputs[0])
mr = n.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -0.02; mr.inputs["From Max"].default_value = 0.55
l.new(sep.outputs["Z"], mr.inputs["Value"])
ramp = n.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.030, 0.022, 0.020, 1)      # sodium/LED light pollution at the horizon
ramp.color_ramp.elements[1].color = (0.0025, 0.0040, 0.0095, 1)   # night blue overhead
ramp.color_ramp.interpolation = "EASE"
l.new(mr.outputs[0], ramp.inputs["Fac"])
cn = n.new("ShaderNodeTexNoise"); cn.inputs["Scale"].default_value = 3.0; cn.inputs["Detail"].default_value = 6
l.new(tc.outputs["Generated"], cn.inputs["Vector"])
cmix = n.new("ShaderNodeMix"); cmix.data_type = "RGBA"; cmix.blend_type = "MULTIPLY"; cmix.inputs["Factor"].default_value = 0.35
l.new(ramp.outputs["Color"], cmix.inputs["A"]); l.new(cn.outputs["Color"], cmix.inputs["B"])
bg = n.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = 1.0
out = n.new("ShaderNodeOutputWorld")
l.new(cmix.outputs[2], bg.inputs["Color"]); l.new(bg.outputs[0], out.inputs[0])

# ---------- moon ----------
moon = bpy.data.objects.new("Moon", bpy.data.lights.new("Moon", "SUN")); NIGHT.objects.link(moon)
moon.data.energy = 0.035; moon.data.color = (0.62, 0.72, 1.0); moon.data.angle = math.radians(0.6)
moon.rotation_euler = Euler((math.radians(38), 0, math.radians(150 + 90)), "XYZ")

# ---------- street lamps ----------
lc_mat = bpy.data.materials["light_cold"]
for nd in lc_mat.node_tree.nodes:
    if nd.type == "EMISSION":
        nd.inputs["Strength"].default_value = 60.0
        nd.inputs["Color"].default_value = (*bb(3300), 1)
    if nd.type == "BLACKBODY":
        nd.inputs["Temperature"].default_value = 3300
LAMP_HEAD = Vector((0.0, -0.80, 5.50))
lamp_col = bb(3300)
for o in bpy.data.collections["STREET"].objects:
    if not o.name.startswith("lamp_"): continue
    m = o.matrix_world
    p = m @ LAMP_HEAD
    ld = bpy.data.lights.new("L_" + o.name, "AREA"); ld.shape = "DISK"; ld.size = 2.4
    ld.energy = 800; ld.color = lamp_col; ld.spread = math.radians(130)
    lo = bpy.data.objects.new("L_" + o.name, ld); NIGHT.objects.link(lo)
    lo.location = p; lo.rotation_euler = (0, 0, 0)          # area light points down (-Z)
    lo.visible_camera = False; lo.visible_glossy = True

# ---------- traffic signals: red facing the avenue ----------
for cname, on in (("Red Light", True), ("Orange Light", False), ("Green Light", False)):
    m = bpy.data.materials[cname]; nn = m.node_tree.nodes
    b = next(x for x in nn if x.type == "BSDF_PRINCIPLED")
    col = {"Red Light": (1.0, 0.04, 0.02), "Orange Light": (1.0, 0.35, 0.02), "Green Light": (0.05, 1.0, 0.45)}[cname]
    b.inputs["Emission Color"].default_value = (*col, 1)
    b.inputs["Emission Strength"].default_value = 25.0 if on else 0.4
for o in bpy.data.collections["STREET"].objects:
    if o.name.startswith("signal_"):
        p = o.matrix_world @ Vector((0, -0.42, 1.96))
        ld = bpy.data.lights.new("S_" + o.name, "POINT"); ld.energy = 6; ld.color = (1.0, 0.05, 0.02); ld.shadow_soft_size = 0.1
        so = bpy.data.objects.new("S_" + o.name, ld); NIGHT.objects.link(so); so.location = p; so.visible_camera = False

# ---------- lit windows on every building (glass = low saturation in the facade photo) ----------
for mname in ("Building_1", "Building_2", "Building_3", "Building_3_Store", "Building_4", "Building__5"):
    mm = bpy.data.materials.get(mname)
    if not mm: continue
    nn = mm.node_tree.nodes; ll = mm.node_tree.links
    for x in [x for x in nn if x.name.startswith("NightWin")]: nn.remove(x)
    bsdf = next(x for x in nn if x.type == "BSDF_PRINCIPLED")
    diff = next(x for x in nn if x.type == "TEX_IMAGE" and x.image and ("NRM" not in x.image.name and "ROUGH" not in x.image.name))
    def N(t, nm, loc):
        k = nn.new(t); k.name = "NightWin_" + nm; k.location = (bsdf.location.x - 1600 + loc[0], bsdf.location.y - 1200 + loc[1]); return k
    rough = next((x for x in nn if x.type == "TEX_IMAGE" and x.image and "ROUGH" in x.image.name), None)
    if rough is not None:      # his hand-painted roughness map: 0 = glass, 0.88 = wall -> exact window mask
        glass = N("ShaderNodeMath", "glass", (400, -100)); glass.operation = "LESS_THAN"; glass.inputs[1].default_value = 0.3
        ll.new(rough.outputs["Color"], glass.inputs[0])
    else:                      # shop front (no roughness map): dark, grey parts of the photo
        hsv = N("ShaderNodeSeparateColor", "hsv", (0, 0)); hsv.mode = "HSV"; ll.new(diff.outputs["Color"], hsv.inputs[0])
        glass = N("ShaderNodeMath", "glass", (400, -100)); glass.operation = "LESS_THAN"; glass.inputs[1].default_value = 0.16
        ll.new(hsv.outputs[2], glass.inputs[0])
    tc = N("ShaderNodeTexCoord", "tc", (0, -500))
    oi = N("ShaderNodeObjectInfo", "oi", (0, -700))
    vadd = N("ShaderNodeVectorMath", "vadd", (200, -550)); vadd.operation = "ADD"
    ll.new(tc.outputs["Object"], vadd.inputs[0]); ll.new(oi.outputs["Location"], vadd.inputs[1])
    vs = N("ShaderNodeVectorMath", "vscale", (380, -550)); vs.operation = "MULTIPLY"; vs.inputs[1].default_value = (0.55, 0.55, 0.32)
    ll.new(vadd.outputs[0], vs.inputs[0])
    cell = N("ShaderNodeVectorMath", "cell", (560, -550)); cell.operation = "FLOOR"; ll.new(vs.outputs[0], cell.inputs[0])
    wn = N("ShaderNodeTexWhiteNoise", "rand", (740, -550)); wn.noise_dimensions = "3D"; ll.new(cell.outputs[0], wn.inputs["Vector"])
    on = N("ShaderNodeMath", "on", (920, -500)); on.operation = "GREATER_THAN"; on.inputs[1].default_value = 0.72
    ll.new(wn.outputs["Value"], on.inputs[0])
    lit = N("ShaderNodeMath", "lit", (1100, -300)); lit.operation = "MULTIPLY"; ll.new(glass.outputs[0], lit.inputs[0]); ll.new(on.outputs[0], lit.inputs[1])
    sepc = N("ShaderNodeSeparateColor", "rgb", (920, -700)); ll.new(wn.outputs["Color"], sepc.inputs[0])
    tint = N("ShaderNodeMix", "tint", (1100, -700)); tint.data_type = "RGBA"
    tint.inputs["A"].default_value = (*bb(2700), 1); tint.inputs["B"].default_value = (*bb(5200), 1)
    tm = N("ShaderNodeMath", "tintfac", (1000, -850)); tm.operation = "GREATER_THAN"; tm.inputs[1].default_value = 0.78
    ll.new(sepc.outputs[1], tm.inputs[0]); ll.new(tm.outputs[0], tint.inputs["Factor"])
    br = N("ShaderNodeMapRange", "bright", (1100, -950)); br.inputs["To Min"].default_value = 0.25; br.inputs["To Max"].default_value = 2.6
    ll.new(sepc.outputs[2], br.inputs["Value"])
    st = N("ShaderNodeMath", "strength", (1300, -500)); st.operation = "MULTIPLY"; ll.new(lit.outputs[0], st.inputs[0]); ll.new(br.outputs[0], st.inputs[1])
    ll.new(tint.outputs[2], bsdf.inputs["Emission Color"]); ll.new(st.outputs[0], bsdf.inputs["Emission Strength"])

# ---------- cars: head + tail lights on the moving / stopped / waiting cars ----------
def coll_bounds(c):
    pts = [o.matrix_world @ Vector(b) for o in c.all_objects if o.type == "MESH" for b in o.bound_box]
    return [min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)]
lib = bpy.data.collections["CAR LIBRARY"]
for o in bpy.data.collections["STREET"].objects:          # re-run safe: point lit cars back at the plain bodies first
    if o.instance_collection and o.instance_collection.name.startswith("CARON_"):
        o.instance_collection = bpy.data.collections["CAR_" + o.instance_collection.name[6:]]
for c in list(lib.children):
    if c.name.startswith("CARON_"):
        for o in list(c.objects): bpy.data.objects.remove(o)
        bpy.data.collections.remove(c)
head_col = bb(5600)
for src in [c for c in lib.children if c.name.startswith("CAR_")]:
    on = bpy.data.collections.new("CARON_" + src.name[4:]); lib.children.link(on)
    e = bpy.data.objects.new("body_" + src.name, None); e.instance_type = "COLLECTION"; e.instance_collection = src; on.objects.link(e)
    mn, mx = coll_bounds(src)
    w = mx[0] - mn[0]
    for sx in (-1, 1):
        hd = bpy.data.lights.new(f"head_{src.name}_{sx}", "SPOT"); hd.energy = 45; hd.color = head_col
        hd.spot_size = math.radians(70); hd.spot_blend = 0.45; hd.shadow_soft_size = 0.05
        ho = bpy.data.objects.new(hd.name, hd); on.objects.link(ho)
        ho.location = (sx * w * 0.34, mn[1] + 0.06, 0.68); ho.rotation_euler = (math.radians(-86), 0, 0)
        tl = bpy.data.lights.new(f"tail_{src.name}_{sx}", "POINT"); tl.energy = 1.6; tl.color = (1.0, 0.02, 0.01); tl.shadow_soft_size = 0.05
        to = bpy.data.objects.new(tl.name, tl); on.objects.link(to)
        to.location = (sx * w * 0.38, mx[1] - 0.02, 0.86)
n_on = 0
for o in bpy.data.collections["STREET"].objects:
    if o.name.startswith(("moving", "stopped", "cross")) and o.instance_collection and o.instance_collection.name.startswith("CAR_"):
        o.instance_collection = bpy.data.collections["CARON_" + o.instance_collection.name[4:]]; n_on += 1

# ---------- fog: blue-tinted scatter + a touch of emission (Extra 3D trick) ----------
hz = bpy.data.materials["Atmosphere Haze"]; v = hz.node_tree.nodes["Principled Volume"]
v.inputs["Color"].default_value = (0.82, 0.86, 0.95, 1)
v.inputs["Density"].default_value = 0.0035
v.inputs["Anisotropy"].default_value = 0.6
v.inputs["Emission Color"].default_value = (0.12, 0.22, 0.62, 1)
v.inputs["Emission Strength"].default_value = 0.00007
sc.cycles.volume_bounces = 1

# ---------- wet asphalt: damp everywhere, puddles in the dips ----------
def wet(mat, damp_mul, puddles):
    nn = mat.node_tree.nodes; ll = mat.node_tree.links
    b = next(x for x in nn if x.type == "BSDF_PRINCIPLED")
    def orig(sock, wet_node, wet_input):
        """source feeding the BSDF before any previous wet pass"""
        if not sock.links: return None
        fs = sock.links[0].from_socket
        if fs.node.name == wet_node:
            ip = fs.node.inputs[wet_input]
            return ip.links[0].from_socket if ip.links else None
        return fs
    r_src = orig(b.inputs["Roughness"], "Wet_rough", "A")
    if r_src is not None and r_src.node.name == "Wet_damp":
        r_src = r_src.node.inputs[0].links[0].from_socket
    c_src = orig(b.inputs["Base Color"], "Wet_col", "A")
    n_src = orig(b.inputs["Normal"], "Wet_nrm", 4)
    for x in [x for x in nn if x.name.startswith("Wet_")]: nn.remove(x)
    def N(t, nm, loc):
        k = nn.new(t); k.name = "Wet_" + nm; k.location = (b.location.x - 700 + loc[0], b.location.y - 1500 + loc[1]); return k
    geo = N("ShaderNodeNewGeometry", "geo", (-400, 0))
    nz = N("ShaderNodeTexNoise", "noise", (-200, 0)); nz.inputs["Scale"].default_value = 0.35; nz.inputs["Detail"].default_value = 8; nz.inputs["Roughness"].default_value = 0.6
    ll.new(geo.outputs["Position"], nz.inputs["Vector"])
    pd = N("ShaderNodeMapRange", "puddle", (0, 0)); pd.inputs["From Min"].default_value = 0.56; pd.inputs["From Max"].default_value = 0.6
    pd.inputs["To Max"].default_value = 1.0 if puddles else 0.0
    ll.new(nz.outputs["Fac"], pd.inputs["Value"])
    rd = N("ShaderNodeMath", "damp", (0, -200)); rd.operation = "MULTIPLY"; rd.inputs[1].default_value = damp_mul; ll.new(r_src, rd.inputs[0])
    rm = N("ShaderNodeMix", "rough", (200, -100)); rm.data_type = "FLOAT"; rm.inputs["B"].default_value = 0.02
    ll.new(pd.outputs[0], rm.inputs["Factor"]); ll.new(rd.outputs[0], rm.inputs["A"]); ll.new(rm.outputs[0], b.inputs["Roughness"])
    dk = N("ShaderNodeMapRange", "dark", (200, -300)); dk.inputs["To Min"].default_value = 0.72; dk.inputs["To Max"].default_value = 0.55
    ll.new(pd.outputs[0], dk.inputs["Value"])
    cm = N("ShaderNodeMix", "col", (400, -200)); cm.data_type = "RGBA"; cm.blend_type = "MULTIPLY"; cm.inputs["Factor"].default_value = 1.0
    cc = N("ShaderNodeCombineColor", "dk3", (300, -400))
    for i in range(3): ll.new(dk.outputs[0], cc.inputs[i])
    ll.new(c_src, cm.inputs["A"]); ll.new(cc.outputs[0], cm.inputs["B"]); ll.new(cm.outputs[2], b.inputs["Base Color"])
    if n_src is not None and puddles:
        nm = N("ShaderNodeMix", "nrm", (400, -500)); nm.data_type = "VECTOR"
        ll.new(pd.outputs[0], nm.inputs["Factor"]); ll.new(n_src, nm.inputs[4]); ll.new(geo.outputs["Normal"], nm.inputs[5])
        ll.new(nm.outputs[1], b.inputs["Normal"])
wet(bpy.data.materials["Street Asphalt"], 0.45, True)
wet(bpy.data.materials["Sidewalk Concrete"], 0.7, False)

# ---------- exposure / render ----------
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Base Contrast"
sc.view_settings.exposure = 0.2
sc.cycles.use_light_tree = True
save()
print("night: lamps", len([o for o in NIGHT.objects if o.name.startswith("L_")]), "cars lit", n_on)
