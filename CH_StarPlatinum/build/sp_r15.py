"""R15 skeleton layout and part assignment shared by phases 04-06 and the exporter.
Joint positions are read from the anatomy in sp_lib (asset-brief.md proportions)."""
from mathutils import Vector

R15_PARTS = ["Head", "UpperTorso", "LowerTorso",
             "LeftUpperArm", "LeftLowerArm", "LeftHand", "RightUpperArm", "RightLowerArm", "RightHand",
             "LeftUpperLeg", "LeftLowerLeg", "LeftFoot", "RightUpperLeg", "RightLowerLeg", "RightFoot"]
PART_INDEX = {p: i for i, p in enumerate(R15_PARTS)}

# right side (-X) joints; left side mirrors x
J = {
    "root": Vector((0.0, 0.0, 0.0)),
    "hip_centre": Vector((0.0, 0.004, 1.300)),     # HumanoidRootNode / LowerTorso head (RootJoint)
    "waist": Vector((0.0, -0.004, 1.430)),         # Waist joint (LowerTorso -> UpperTorso)
    "neck": Vector((0.0, 0.010, 1.765)),           # Neck joint (UpperTorso -> Head)
    "head_top": Vector((0.0, 0.004, 1.965)),
    "shoulder": Vector((-0.212, 0.050, 1.660)),
    "elbow": Vector((-0.264, 0.098, 1.455)),
    "wrist": Vector((-0.292, 0.068, 1.250)),
    "hand_end": Vector((-0.300, 0.040, 1.075)),
    "hip": Vector((-0.095, 0.006, 1.250)),
    "knee": Vector((-0.160, -0.020, 0.835)),
    "ankle": Vector((-0.265, 0.048, 0.130)),
    "toe": Vector((-0.300, -0.150, 0.030)),
}


def mx(v):
    return Vector((-v.x, v.y, v.z))


def segments():
    """part -> (head, tail, radius) used for nearest-part assignment and weights."""
    s = {
        "LowerTorso": (J["hip_centre"] + Vector((0, 0, -0.10)), J["waist"], 0.115),
        "UpperTorso": (J["waist"], J["neck"], 0.135),
        "Head": (J["neck"], J["head_top"], 0.070),
    }
    for side, f in (("Right", lambda v: v), ("Left", mx)):
        s[side + "UpperArm"] = (f(J["shoulder"]), f(J["elbow"]), 0.055)
        s[side + "LowerArm"] = (f(J["elbow"]), f(J["wrist"]), 0.045)
        s[side + "Hand"] = (f(J["wrist"]), f(J["hand_end"]), 0.050)
        s[side + "UpperLeg"] = (f(J["hip"]), f(J["knee"]), 0.080)
        s[side + "LowerLeg"] = (f(J["knee"]), f(J["ankle"]), 0.050)
        s[side + "Foot"] = (f(J["ankle"]), f(J["toe"]), 0.045)
    return s


def seg_dist(p, a, b):
    ab = b - a
    t = max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared))
    return (p - (a + ab * t)).length, t


def nearest_part(p, segs=None):
    """Closest bone by (distance - radius). Past a bone's end only a third of the radius is credited, so a
    fat segment (UpperTorso) cannot claim points that lie beyond its end (the face above the neck)."""
    segs = segs or segments()
    best, bp = 1e9, None
    for part, (a, b, r) in segs.items():
        d, t = seg_dist(p, a, b)
        d -= r if 0.0 < t < 1.0 else r * 0.35
        if d < best:
            best, bp = d, part
    return bp


# gear object base name -> owning R15 part (rigid attachment, asset-brief PARTS)
GEAR_PART = {
    "Hair": "Head", "Headband": "Head", "HeadGemBezel": "Head", "HeadGem": "Head",
    "Scarf": "UpperTorso", "Belt": "LowerTorso", "BeltDiscR": "LowerTorso", "BeltDiscL": "LowerTorso",
    "BeltBuckle": "LowerTorso", "BeltGem": "LowerTorso",
    "LoinclothFront": "LowerTorso", "LoinclothBack": "LowerTorso",
}
for _s, _S in (("R", "Right"), ("L", "Left")):
    GEAR_PART.update({
        f"ShoulderPad_{_s}": f"{_S}UpperArm", f"Bracer_{_s}": f"{_S}LowerArm", f"WristRing_{_s}": f"{_S}LowerArm",
        f"Glove_{_s}": f"{_S}Hand", f"GloveStud_{_s}": f"{_S}Hand", f"KneePad_{_s}": f"{_S}LowerLeg", f"KneeStrap_{_s}": f"{_S}LowerLeg",
        f"BootShaft_{_s}": f"{_S}LowerLeg", f"AnkleRing_{_s}": f"{_S}LowerLeg",
        f"BootFoot_{_s}": f"{_S}Foot", f"BootHeel_{_s}": f"{_S}Foot",
    })

# colour/material regions for the painter
REGIONS = ["skin", "hair", "gold", "black", "red", "cloth", "gem", "inlay"]
REGION_INDEX = {r: i for i, r in enumerate(REGIONS)}
GEAR_REGION = {
    "Hair": "hair", "Headband": "gold", "HeadGemBezel": "gold", "HeadGem": "gem", "Scarf": "red",
    "Belt": "gold", "BeltDiscR": "gold", "BeltDiscL": "gold", "BeltBuckle": "gold", "BeltGem": "gem",
    "LoinclothFront": "cloth", "LoinclothBack": "cloth",
}
for _s in ("R", "L"):
    GEAR_REGION.update({
        f"ShoulderPad_{_s}": "gold", f"Bracer_{_s}": "black", f"WristRing_{_s}": "gold", f"Glove_{_s}": "black",
        f"GloveStud_{_s}": "gold",
        f"KneePad_{_s}": "gold", f"KneeStrap_{_s}": "black", f"BootShaft_{_s}": "black",
        f"AnkleRing_{_s}": "gold", f"BootFoot_{_s}": "black", f"BootHeel_{_s}": "black",
    })


def base_of(obname, asset="CH_StarPlatinum"):
    """CH_StarPlatinum_Glove_R_LOD0 -> Glove_R"""
    n = obname.split(".")[0]
    if n.startswith(asset + "_"):
        n = n[len(asset) + 1:]
    for suf in ("_LOD0", "_HIGH"):
        if n.endswith(suf):
            n = n[: -len(suf)]
    return n
