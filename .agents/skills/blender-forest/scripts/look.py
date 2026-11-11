"""Stage G: realism / look pass, driven entirely by scripts/look_params.json.

Applies on top of the built scene (run AFTER camset.py when testing, so DOF can focus):
  sun (direction, strength, softness), world light/sky split, colour management,
  haze from the mist pass, glare, colour grade, vignette, slight lens dispersion, camera DOF.

  LOOK_SAVE=1 blender -b scene/forest.blend --python scripts/look.py     # bake into the .blend
  CAM=... blender -b scene/forest.blend --python scripts/camset.py --python scripts/look.py       --python scripts/test_still.py -- out.png 64 960                    # test still, no save
"""
import bpy, json, math, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "look_params.json"), encoding="utf-8"))
sc = bpy.context.scene


def sun():
    s = P["sun"]
    ob = bpy.data.objects.get("Sun")
    ob.data.angle = math.radians(s["angle_deg"])
    ob.data.color = s["color"]
    if ob.animation_data and ob.animation_data.action:
        return                                   # per-shot sun from build_shots.py wins
    az, el = math.radians(s["azimuth"]), math.radians(s["elevation"])
    to_sun = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    ob.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()
    ob.data.energy = s["energy"]
    ob.data.angle = math.radians(s["angle_deg"])     # smaller = crisper leaf dapples
    ob.data.color = s["color"]


def world():
    w = P["world"]
    for n in sc.world.node_tree.nodes:
        if n.type == "BACKGROUND":
            n.inputs["Strength"].default_value = w["light_strength"] if n.label == "Lighting" else w["sky_strength"]
        if n.type == "MAPPING":
            n.inputs["Rotation"].default_value[2] = math.radians(w["hdri_rot_z_deg"])
    m = sc.world.mist_settings
    m.start, m.depth, m.falloff = P["haze"]["start"], P["haze"]["depth"], "QUADRATIC"


def colour():
    c = P["colour"]
    vs = sc.view_settings
    vs.view_transform = "Filmic"
    vs.look = c["look"]
    vs.exposure, vs.gamma = c["exposure"], c["gamma"]
    sc.render.motion_blur_shutter = P.get("shutter", 0.5)     # his car shot is only lightly blurred


def pick(sockets, name, kind=None):
    return next(s for s in sockets if s.name == name and (kind is None or s.type == kind))


def set_menu(sock, *options):
    for o in options:
        try:
            sock.default_value = o
            return
        except Exception:
            pass


def compositor():
    bpy.context.view_layer.use_pass_mist = True
    ng = bpy.data.node_groups.get("LookComp") or bpy.data.node_groups.new("LookComp", "CompositorNodeTree")
    ng.nodes.clear()
    if not ng.interface.items_tree:
        ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    N, Lk = ng.nodes.new, ng.links.new
    rl = N("CompositorNodeRLayers")
    out = N("NodeGroupOutput")

    # Haze: mix toward haze colour by mist * strength.
    h = P["haze"]
    # Sky pixels have mist == 1: keep them out of the haze so the blue sky stays blue.
    notsky = N("ShaderNodeMath"); notsky.operation = "LESS_THAN"
    Lk(rl.outputs["Mist"], notsky.inputs[0]); notsky.inputs[1].default_value = 0.995
    m1 = N("ShaderNodeMath"); m1.operation = "MULTIPLY"
    Lk(rl.outputs["Mist"], m1.inputs[0]); Lk(notsky.outputs[0], m1.inputs[1])
    fac = N("ShaderNodeMath"); fac.operation = "MULTIPLY"
    Lk(m1.outputs[0], fac.inputs[0]); fac.inputs[1].default_value = h["strength"]
    haze = N("ShaderNodeMix"); haze.data_type = "RGBA"
    Lk(fac.outputs[0], pick(haze.inputs, "Factor", "VALUE"))
    Lk(rl.outputs["Image"], pick(haze.inputs, "A", "RGBA"))
    pick(haze.inputs, "B", "RGBA").default_value = (*h["color"], 1.0)
    img = pick(haze.outputs, "Result", "RGBA")

    # Glare (soft bloom on sun-lit leaves / windows).
    g = P["glare"]
    gl = N("CompositorNodeGlare")
    set_menu(gl.inputs["Type"], "Bloom", "BLOOM", "Fog Glow", "FOG_GLOW")
    gl.inputs["Threshold"].default_value = g["threshold"]
    gl.inputs["Strength"].default_value = g["strength"]
    if "Size" in gl.inputs:
        gl.inputs["Size"].default_value = g["size"]
    Lk(img, gl.inputs["Image"]); img = gl.outputs["Image"]

    # Grade: lift / gamma / gain, then saturation.
    gr = P["grade"]
    cb = N("CompositorNodeColorBalance")
    for nm in ("Lift", "Gamma", "Gain"):
        pick(cb.inputs, nm, "RGBA").default_value = (*gr[nm.lower()], 1.0)
    Lk(img, cb.inputs["Image"]); img = cb.outputs["Image"]
    hs = N("CompositorNodeHueSat")
    hs.inputs["Saturation"].default_value = gr["saturation"]
    Lk(img, hs.inputs["Image"]); img = hs.outputs["Image"]

    # Lens: tiny chromatic dispersion like a real lens.
    ld = N("CompositorNodeLensdist")
    ld.inputs["Dispersion"].default_value = P["lens"]["dispersion"]
    Lk(img, ld.inputs["Image"]); img = ld.outputs["Image"]

    # Vignette: soft ellipse mask darkening the corners.
    em = N("CompositorNodeEllipseMask")
    em.inputs["Size"].default_value = (0.95, 0.95)
    bl = N("CompositorNodeBlur")
    bl.inputs["Size"].default_value = (300, 300)
    Lk(em.outputs["Mask"], bl.inputs["Image"])
    vf = N("ShaderNodeMath"); vf.operation = "MULTIPLY_ADD"
    Lk(bl.outputs["Image"], vf.inputs[0])
    vf.inputs[1].default_value = P["vignette"]
    vf.inputs[2].default_value = 1.0 - P["vignette"]
    vg = N("ShaderNodeMix"); vg.data_type = "RGBA"; vg.blend_type = "MULTIPLY"
    pick(vg.inputs, "Factor", "VALUE").default_value = 1.0
    Lk(img, pick(vg.inputs, "A", "RGBA"))
    Lk(vf.outputs[0], pick(vg.inputs, "B", "RGBA"))
    Lk(pick(vg.outputs, "Result", "RGBA"), out.inputs[0])
    sc.compositing_node_group = ng
    sc.render.use_compositing = True


def dof():
    d = P["dof"]
    cam = sc.camera
    if not cam or "shot" in cam:
        return                                   # shot cameras carry their own DOF
    cam.data.dof.use_dof = d["enabled"]
    cam.data.dof.aperture_fstop = d["fstop"]
    # Focus on whatever is in the centre of frame.
    dg = bpy.context.evaluated_depsgraph_get()
    fwd = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
    hit, loc, *_ = sc.ray_cast(dg, cam.matrix_world.translation, fwd)
    cam.data.dof.focus_distance = (loc - cam.matrix_world.translation).length if hit else 10.0


def materials():
    """look_params "materials": {"<material name>": {"value": 0.9, "saturation": 1.0}} -> HSV before Base Color."""
    for name, o in P.get("materials", {}).items():
        m = bpy.data.materials.get(name)
        if not m or not m.node_tree:
            print("material not found:", name)
            continue
        nt = m.node_tree
        bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if not bsdf:
            continue
        hsv = nt.nodes.get("LookHSV")
        if not hsv:
            src = bsdf.inputs["Base Color"].links[0].from_socket if bsdf.inputs["Base Color"].links else None
            hsv = nt.nodes.new("ShaderNodeHueSaturation")
            hsv.name = "LookHSV"
            if src:
                nt.links.new(src, hsv.inputs["Color"])
            else:
                hsv.inputs["Color"].default_value = bsdf.inputs["Base Color"].default_value
            nt.links.new(hsv.outputs["Color"], bsdf.inputs["Base Color"])
        hsv.inputs["Value"].default_value = o.get("value", 1.0)
        hsv.inputs["Saturation"].default_value = o.get("saturation", 1.0)


sun(); world(); colour(); compositor(); dof(); materials()
print("LOOK applied")
if os.environ.get("LOOK_SAVE") == "1":
    bpy.ops.wm.save_mainfile(relative_remap=True)
    print("LOOK SAVED")
