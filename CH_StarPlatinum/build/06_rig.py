"""Phase 06: R15 skeleton and skinning for the delivery mesh.
  * ARM_StarPlatinum in RIG_DEF: Root > HumanoidRootNode > LowerTorso > UpperTorso > Head, arm and leg
    chains (Roblox body specification names). Bones run joint to joint: limbs point down, torso/head up.
  * Weights: each vertex belongs to its face's r15_part; body vertices near a joint blend up to 50% into
    the neighbouring part with a smooth falloff; gear stays rigid on its part (asset-brief ARTICULATION).
    Normalised, max 4 influences, nothing on Root.
  * AN_PoseTest action (frames 1-5) for the extreme-pose gate.

blender --background --python build/06_rig.py -- [--master ...]
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Vector, Quaternion, Matrix
import bt
import sp_lib as L
import sp_r15 as R

L.setup("06_rig")
ARM = "ARM_StarPlatinum"
GEAR_REGIONS_RIGID = True

# joint between a part and its parent part: (child part, parent part, joint position key, blend radius m)
JOINTS = [("UpperTorso", "LowerTorso", "waist", 0.09), ("Head", "UpperTorso", "neck", 0.05)]
for _S, _f in (("Right", lambda v: v), ("Left", R.mx)):
    JOINTS += [(f"{_S}UpperArm", "UpperTorso", ("shoulder", _f), 0.075), (f"{_S}LowerArm", f"{_S}UpperArm", ("elbow", _f), 0.055),
               (f"{_S}Hand", f"{_S}LowerArm", ("wrist", _f), 0.035), (f"{_S}UpperLeg", "LowerTorso", ("hip", _f), 0.085),
               (f"{_S}LowerLeg", f"{_S}UpperLeg", ("knee", _f), 0.06), (f"{_S}Foot", f"{_S}LowerLeg", ("ankle", _f), 0.05)]


def jpos(key):
    if isinstance(key, tuple):
        return key[1](R.J[key[0]])
    return R.J[key]


def bone_table():
    """name -> (head, tail, parent)"""
    J = R.J
    hc = J["hip_centre"]
    t = {
        "Root": (hc.copy(), hc + Vector((0, 0, 0.08)), None),
        "HumanoidRootNode": (hc.copy(), hc + Vector((0, 0, 0.08)), "Root"),
        "LowerTorso": (hc.copy(), J["waist"].copy(), "HumanoidRootNode"),
        "UpperTorso": (J["waist"].copy(), J["neck"].copy(), "LowerTorso"),
        "Head": (J["neck"].copy(), J["head_top"].copy(), "UpperTorso"),
    }
    for S, f in (("Right", lambda v: v.copy()), ("Left", R.mx)):
        t[S + "UpperArm"] = (f(J["shoulder"]), f(J["elbow"]), "UpperTorso")
        t[S + "LowerArm"] = (f(J["elbow"]), f(J["wrist"]), S + "UpperArm")
        t[S + "Hand"] = (f(J["wrist"]), f(J["hand_end"]), S + "LowerArm")
        t[S + "UpperLeg"] = (f(J["hip"]), f(J["knee"]), "LowerTorso")
        t[S + "LowerLeg"] = (f(J["knee"]), f(J["ankle"]), S + "UpperLeg")
        t[S + "Foot"] = (f(J["ankle"]), f(J["toe"]), S + "LowerLeg")
    return t


def build_armature():
    data = bpy.data.armatures.new(ARM)
    ob = bpy.data.objects.new(ARM, data)
    bt.col("RIG_DEF").objects.link(ob)
    bt.own(ob)
    vl = bpy.context.view_layer
    vl.objects.active = ob
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]):
        bpy.ops.object.mode_set(mode="EDIT")
        eb = data.edit_bones
        for nm, (h, tl, parent) in bone_table().items():
            b = eb.new(nm)
            b.head, b.tail = h, tl
            b.roll = 0.0
            b.use_deform = nm != "Root"
        for nm, (h, tl, parent) in bone_table().items():
            if parent:
                eb[nm].parent = eb[parent]
                eb[nm].use_connect = False
        bpy.ops.object.mode_set(mode="OBJECT")
    data.display_type = "STICK"
    return ob


def skin(mesh_ob, arm_ob):
    me = mesh_ob.data
    parts = [0] * len(me.polygons)
    me.attributes["r15_part"].data.foreach_get("value", parts)
    regs = [0] * len(me.polygons)
    me.attributes["region"].data.foreach_get("value", regs)
    skin_id = R.REGION_INDEX["skin"]
    vpart, vskin = {}, {}
    for p in me.polygons:
        for v in p.vertices:
            vpart.setdefault(v, {}).setdefault(parts[p.index], 0)
            vpart[v][parts[p.index]] += 1
            vskin[v] = vskin.get(v, False) or regs[p.index] == skin_id
    groups = {n: mesh_ob.vertex_groups.new(name=n) for n in R.R15_PARTS}
    joints_by_part = {}
    for child, parent, key, rad in JOINTS:
        joints_by_part.setdefault(child, []).append((parent, jpos(key), rad))
        joints_by_part.setdefault(parent, []).append((child, jpos(key), rad))
    max_inf = 0
    for v in me.vertices:
        counts = vpart.get(v.index)
        if not counts:
            continue
        P = R.R15_PARTS[max(counts, key=counts.get)]
        w = {P: 1.0}
        if vskin.get(v.index):
            co = mesh_ob.matrix_world @ v.co
            blend = {}
            for Q, jp, rad in joints_by_part.get(P, []):
                d = (co - jp).length
                if d < rad:
                    s = 1 - d / rad
                    blend[Q] = blend.get(Q, 0) + 0.5 * s * s * (3 - 2 * s)
            tot = sum(blend.values())
            if tot > 0.5:
                blend = {k: x * 0.5 / tot for k, x in blend.items()}
            for Q, x in sorted(blend.items(), key=lambda kv: -kv[1])[:3]:
                if x >= 0.01:          # no sub-1% influences (validate.py WARN)
                    w[Q] = x
            w[P] = 1.0 - sum(x for k, x in w.items() if k != P)
        max_inf = max(max_inf, len(w))
        for nm, x in w.items():
            if x > 1e-4:
                groups[nm].add([v.index], x, "REPLACE")
    mesh_ob.parent = arm_ob
    m = mesh_ob.modifiers.new("Armature", "ARMATURE")
    m.object = arm_ob
    m.use_deform_preserve_volume = False
    return max_inf


def world_rot(arm_ob, pb, axis, deg):
    """Rotate a pose bone about a world axis through its head (rest frame)."""
    ml = pb.bone.matrix_local.to_quaternion()
    qw = Quaternion(Vector(axis).normalized(), math.radians(deg))
    pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = ml.inverted() @ qw @ ml


POSES = {  # frame -> list of (bone, world axis, degrees); +X = character's left, -Y = forward
    1: [],
    2: [("RightUpperArm", (0, 1, 0), 150), ("LeftUpperArm", (0, 1, 0), -150)],                     # arms overhead
    3: [("RightUpperArm", (1, 0, 0), 85), ("RightLowerArm", (1, 0, 0), 10), ("UpperTorso", (0, 0, 1), -25),
        ("LeftUpperArm", (1, 0, 0), -40), ("LeftLowerArm", (1, 0, 0), 100)],                          # punch
    4: [("RightUpperLeg", (1, 0, 0), 75), ("LeftUpperLeg", (1, 0, 0), 75), ("RightLowerLeg", (1, 0, 0), -100),
        ("LeftLowerLeg", (1, 0, 0), -100), ("UpperTorso", (1, 0, 0), 20)],                             # crouch
    5: [("Head", (0, 0, 1), 50), ("UpperTorso", (0, 0, 1), 30), ("RightLowerArm", (1, 0, 0), 120),
        ("LeftUpperLeg", (1, 0, 0), -35)],                                                          # twist
}


def pose_action(arm_ob):
    act = bpy.data.actions.new("AN_PoseTest")
    arm_ob.animation_data_create()
    arm_ob.animation_data.action = act
    for frame, rots in POSES.items():
        for pb in arm_ob.pose.bones:
            pb.rotation_mode = "QUATERNION"
            pb.rotation_quaternion = Quaternion()
        for nm, axis, deg in rots:
            world_rot(arm_ob, arm_ob.pose.bones[nm], axis, deg)
        for pb in arm_ob.pose.bones:
            pb.keyframe_insert("rotation_quaternion", frame=frame)
    act.use_fake_user = True
    arm_ob.animation_data.action = None      # rest pose stays the default state of the file
    return act


def main():
    a = L.args()
    bt.open_master(a.master)
    for o in [o for o in bpy.data.objects if o.get("owner") == bt.OWNER_TAG]:
        L.remove_object(o)
    for act in [x for x in bpy.data.actions if x.name.startswith("AN_PoseTest")]:
        bpy.data.actions.remove(act)
    ob = bpy.data.objects["CH_StarPlatinum_LOD0"]
    ob.parent = None
    ob.modifiers.clear()
    ob.vertex_groups.clear()
    arm = build_armature()
    max_inf = skin(ob, arm)
    pose_action(arm)
    bt.log("bones", len(arm.data.bones), "max influences", max_inf)
    bt.save_master(a.master)


main()
