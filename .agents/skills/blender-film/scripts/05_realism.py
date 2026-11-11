# Realism pass (from the research notes):
#  1 exposure for the shaded street like a real camera would, AgX kept close to neutral (no grade)
#  2 atmospheric perspective: one low-density scatter volume over the city -> depth haze + sun shafts in the canyons
#  3 asphalt: break the texture repeat, dark polished wheel paths, oil drip line, repair patches, worn and less saturated paint
#  4 dirt deposition: darker splash zone at the foot of every facade + faint vertical run-off streaks
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
sc = bpy.context.scene
PH = os.path.join(ROOT, "downloads", "polyhaven")

# ---------- 1 exposure ----------
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Base Contrast"
sc.view_settings.exposure = 0.55

# ---------- 2 haze volume ----------
hz = bpy.data.objects.get("Atmosphere")
if hz is None:
    me = bpy.data.meshes.new("Atmosphere")
    x0, x1, y0, y1, z0, z1 = -150, 950, -280, 280, -1, 160
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f); me.update()
    hz = bpy.data.objects.new("Atmosphere", me)
    coll("ENVIRONMENT").objects.link(hz)
hz.display_type = "BOUNDS"
m = bpy.data.materials.get("Atmosphere Haze") or bpy.data.materials.new("Atmosphere Haze")
m.use_nodes = True; n = m.node_tree.nodes; l = m.node_tree.links; n.clear()
out = n.new("ShaderNodeOutputMaterial")
vol = n.new("ShaderNodeVolumePrincipled")
vol.inputs["Color"].default_value = (0.80, 0.86, 0.95, 1)
vol.inputs["Density"].default_value = 0.0012
vol.inputs["Anisotropy"].default_value = 0.35
l.new(vol.outputs[0], out.inputs["Volume"])
hz.data.materials.clear(); hz.data.materials.append(m)
cy = sc.cycles
cy.volume_bounces = 1
cy.volume_step_rate = 4.0
cy.volume_max_steps = 256

# ---------- 3 asphalt ----------
road = bpy.data.materials["Street Asphalt"]
n = road.node_tree.nodes; l = road.node_tree.links
bsdf = next(x for x in n if x.type == "BSDF_PRINCIPLED")
if "RealismAsphalt" not in n:
    marker = n.new("NodeFrame"); marker.name = "RealismAsphalt"; marker.label = "realism layer"
    geo = n.new("ShaderNodeNewGeometry"); geo.location = (-1500, -1900)
    sep = n.new("ShaderNodeSeparateXYZ"); sep.location = (-1300, -1900); l.new(geo.outputs["Position"], sep.inputs[0])
    X, Y = sep.outputs["X"], sep.outputs["Y"]
    def m_(op, a=None, b=None, loc=(0, 0)):
        k = n.new("ShaderNodeMath"); k.operation = op; k.location = loc
        if isinstance(a, (int, float)): k.inputs[0].default_value = a
        elif a is not None: l.new(a, k.inputs[0])
        if isinstance(b, (int, float)): k.inputs[1].default_value = b
        elif b is not None: l.new(b, k.inputs[1])
        return k.outputs[0]
    # wheel paths: |y| = 1.1 and 2.7 (two per lane), soft bands broken by noise
    ay = m_("ABSOLUTE", Y, None, (-1100, -2000))
    def band(c, w, loc):
        d = m_("ABSOLUTE", m_("SUBTRACT", ay, c, loc), None, (loc[0] + 120, loc[1]))
        return m_("SUBTRACT", 1.0, m_("MINIMUM", m_("DIVIDE", d, w, (loc[0] + 240, loc[1])), 1.0, (loc[0] + 360, loc[1])), (loc[0] + 480, loc[1]))
    w1 = band(1.1, 0.55, (-1000, -2100)); w2 = band(2.7, 0.55, (-1000, -2250))
    wheels = m_("MAXIMUM", w1, w2, (-450, -2150))
    # oil drip line in the middle of each lane (|y| = 1.9), blotchy
    oil_n = n.new("ShaderNodeTexNoise"); oil_n.location = (-1000, -2450); oil_n.inputs["Scale"].default_value = 0.9; oil_n.inputs["Detail"].default_value = 6
    l.new(geo.outputs["Position"], oil_n.inputs["Vector"])
    oil_b = band(1.9, 0.35, (-1000, -2600))
    oil_m = m_("MULTIPLY", oil_b, m_("POWER", oil_n.outputs["Fac"], 3.0, (-800, -2450)), (-450, -2500))
    # repair patches: sparse large voronoi cells
    vor = n.new("ShaderNodeTexVoronoi"); vor.location = (-1000, -2800); vor.inputs["Scale"].default_value = 0.09
    l.new(geo.outputs["Position"], vor.inputs["Vector"])
    sepc = n.new("ShaderNodeSeparateColor"); sepc.location = (-800, -2800); l.new(vor.outputs["Color"], sepc.inputs[0])
    patch = m_("GREATER_THAN", sepc.outputs[0], 0.82, (-600, -2800))
    # large-scale variation to kill the repeat
    big = n.new("ShaderNodeTexNoise"); big.location = (-1000, -3000); big.inputs["Scale"].default_value = 0.05; big.inputs["Detail"].default_value = 4
    l.new(geo.outputs["Position"], big.inputs["Vector"])
    bigv = m_("MULTIPLY_ADD", big.outputs["Fac"], 0.35, (-800, -3000)); n_last = bigv.node; n_last.inputs[2].default_value = 0.82
    # darken factor = (1 - 0.18 wheels) * (1 - 0.35 oil) * (patch ? 0.8 : 1) * big
    dk = m_("MULTIPLY", m_("SUBTRACT", 1.0, m_("MULTIPLY", wheels, 0.18, (-300, -2150)), (-150, -2150)),
            m_("SUBTRACT", 1.0, m_("MULTIPLY", oil_m, 0.45, (-300, -2500)), (-150, -2500)), (0, -2300))
    dk = m_("MULTIPLY", dk, m_("SUBTRACT", 1.0, m_("MULTIPLY", patch, 0.22, (-300, -2800)), (-150, -2800)), (150, -2400))
    dk = m_("MULTIPLY", dk, bigv, (300, -2500))
    # apply to base colour (before paint) and roughness (polished wheel paths are smoother)
    base_link = bsdf.inputs["Base Color"].links[0]
    src = base_link.from_socket
    mulc = n.new("ShaderNodeMix"); mulc.data_type = "RGBA"; mulc.blend_type = "MULTIPLY"; mulc.location = (450, -300)
    mulc.inputs["Factor"].default_value = 1.0
    l.new(src, mulc.inputs["A"])
    cmb = n.new("ShaderNodeCombineColor"); cmb.location = (300, -650)
    for i in range(3): l.new(dk, cmb.inputs[i])
    l.new(cmb.outputs[0], mulc.inputs["B"])
    l.new(mulc.outputs[2], bsdf.inputs["Base Color"])
    rl = bsdf.inputs["Roughness"].links[0].from_socket
    rmix = m_("SUBTRACT", None, m_("MULTIPLY", wheels, 0.12, (300, -900)), (450, -800))
    l.new(rl, rmix.node.inputs[0]); l.new(rmix, bsdf.inputs["Roughness"])
# worn, less saturated paint
for x in n:
    if x.bl_idname == "ShaderNodeMix" and x.data_type == "RGBA" and tuple(round(c, 2) for c in x.inputs["B"].default_value[:3]) == (0.85, 0.62, 0.12):
        x.inputs["B"].default_value = (0.66, 0.50, 0.17, 1)
    if x.bl_idname == "ShaderNodeMix" and x.data_type == "RGBA" and tuple(round(c, 2) for c in x.inputs["B"].default_value[:3]) == (0.82, 0.82, 0.8):
        x.inputs["B"].default_value = (0.70, 0.70, 0.68, 1)
for x in n:
    if x.type == "MAP_RANGE" and abs(x.inputs["From Min"].default_value - 0.35) < 1e-3:
        x.inputs["From Min"].default_value = 0.42; x.inputs["From Max"].default_value = 0.62

# ---------- 4 facade dirt deposition ----------
for mname in ("Building_1", "Building_2", "Building_3", "Building_3_Store", "Building_4", "Building__5"):
    mm = bpy.data.materials.get(mname)
    if not mm or "Grime" in mm.node_tree.nodes: continue
    n = mm.node_tree.nodes; l = mm.node_tree.links
    bsdf = next(x for x in n if x.type == "BSDF_PRINCIPLED")
    src = bsdf.inputs["Base Color"].links[0].from_socket
    tc = n.new("ShaderNodeTexCoord"); tc.location = (bsdf.location.x - 1100, bsdf.location.y - 600)
    sep = n.new("ShaderNodeSeparateXYZ"); sep.location = (tc.location.x + 180, tc.location.y); l.new(tc.outputs["Object"], sep.inputs[0])
    foot = n.new("ShaderNodeMapRange"); foot.location = (sep.location.x + 180, sep.location.y)
    foot.inputs["From Min"].default_value = 0.0; foot.inputs["From Max"].default_value = 3.2
    foot.inputs["To Min"].default_value = 0.72; foot.inputs["To Max"].default_value = 1.0
    l.new(sep.outputs["Z"], foot.inputs["Value"])
    mp = n.new("ShaderNodeMapping"); mp.location = (tc.location.x + 180, tc.location.y - 250)
    mp.inputs["Scale"].default_value = (1.6, 1.6, 0.06)            # long vertical streaks
    l.new(tc.outputs["Object"], mp.inputs["Vector"])
    st = n.new("ShaderNodeTexNoise"); st.location = (mp.location.x + 180, mp.location.y); st.inputs["Detail"].default_value = 3
    l.new(mp.outputs[0], st.inputs["Vector"])
    stm = n.new("ShaderNodeMapRange"); stm.location = (st.location.x + 180, st.location.y)
    stm.inputs["From Min"].default_value = 0.45; stm.inputs["From Max"].default_value = 0.75
    stm.inputs["To Min"].default_value = 1.0; stm.inputs["To Max"].default_value = 0.86
    l.new(st.outputs["Fac"], stm.inputs["Value"])
    mul = n.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.location = (stm.location.x + 180, stm.location.y + 100)
    l.new(foot.outputs[0], mul.inputs[0]); l.new(stm.outputs[0], mul.inputs[1])
    g = n.new("ShaderNodeMix"); g.name = "Grime"; g.data_type = "RGBA"; g.blend_type = "MULTIPLY"; g.location = (bsdf.location.x - 200, bsdf.location.y - 150)
    g.inputs["Factor"].default_value = 1.0
    cmb = n.new("ShaderNodeCombineColor"); cmb.location = (mul.node.location.x + 160 if hasattr(mul, "node") else mul.location.x + 160, mul.location.y)
    for i in range(3): l.new(mul.outputs[0], cmb.inputs[i])
    l.new(src, g.inputs["A"]); l.new(cmb.outputs[0], g.inputs["B"]); l.new(g.outputs[2], bsdf.inputs["Base Color"])
save()
print("realism pass applied")
