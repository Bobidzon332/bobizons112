"""Gear builders for CH_StarPlatinum. Every builder makes the RIGHT (-X) piece; build_all_gear
mirrors them. seg scales segment counts (blockout 0.6, LOW 1.0, HIGH 2.0). Constants are from
asset-brief.md (PARTS, PROPORTIONS) or marked inferred."""
import bpy, bmesh, math
from mathutils import Vector, Matrix
import bt
from sp_lib import (name, sweep, ellipse_path, rect_profile, circle_profile, lathe_along, dome,
                    rounded_tray, apply_mods, mirror_copy, join_remove)


def _sfx(collection):
    return "LOD0" if collection == "LOW" else "HIGH"


def spike(nm, root, tip, r0, curl=(0, 0, 0), flat=0.65, seg=6, steps=5, collection="LOW"):
    """Tapered blade-like hair lock from root to tip, bent by `curl` (offset reached at the tip)."""
    root, tip, curl = Vector(root), Vector(tip), Vector(curl)
    pts, scl = [], []
    for i in range(steps + 1):
        f = i / steps
        pts.append(root.lerp(tip, f) + curl * (f * f))
        w = r0 * (1 - f) ** 0.85 + 0.0015
        scl.append((w, w * flat))
    return sweep(nm, pts, circle_profile(1.0, seg), closed_path=False, collection=collection,
                 scales=scl, cap=True, smooth=True)


# (azimuth deg from front toward +X, elevation deg, length m, root radius m, up bias, back bias, mirrored)
HAIR_LOCKS = [
    # crown, pointing up (front 2%: tips z 2.06 within x -0.064..+0.091)
    (0, 82, 0.150, 0.040, 1.6, 0.2, False), (30, 72, 0.130, 0.036, 1.6, 0.3, True),
    (100, 70, 0.120, 0.036, 1.4, 0.3, True), (170, 70, 0.125, 0.036, 1.0, 0.2, False),
    (140, 62, 0.120, 0.034, 0.9, 0.3, True),
    # upper ring (front 6%: width -0.117..+0.125 at z 1.97; side 6%: y -0.156..+0.126)
    (12, 42, 0.125, 0.034, 0.35, -0.55, True), (45, 45, 0.110, 0.034, 0.55, -0.1, True),
    (75, 40, 0.110, 0.034, 0.40, 0.1, True), (105, 38, 0.110, 0.034, 0.35, 0.3, True),
    (135, 38, 0.110, 0.034, 0.30, 0.5, True), (165, 36, 0.105, 0.034, 0.25, 0.6, True),
    # lower side and back ring (front 10%: sides reach +-0.095 at z 1.89)
    (60, 15, 0.105, 0.030, 0.10, 0.1, True), (90, 12, 0.110, 0.030, 0.05, 0.2, True),
    (120, 8, 0.105, 0.030, 0.05, 0.4, True), (150, 2, 0.100, 0.030, 0.05, 0.6, True),
    (180, 5, 0.095, 0.030, 0.10, 0.6, False), (165, -15, 0.085, 0.028, -0.1, 0.5, True),
    (130, -12, 0.080, 0.026, -0.05, 0.4, True),
    # fringe over the forehead, sweeping forward-up (side 6%: front at y -0.156)
    (8, 12, 0.125, 0.030, 0.05, -1.3, True), (25, 14, 0.115, 0.028, 0.05, -1.1, True),
]
SCALP_C = Vector((0.0, 0.012, 1.925))   # inferred: scalp ellipsoid hugging the cranium
SCALP_R = Vector((0.068, 0.084, 0.060))


def scalp_point(az, el):
    a, e = math.radians(az), math.radians(el)
    d = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    p = SCALP_C + Vector((d.x * SCALP_R.x, d.y * SCALP_R.y, d.z * SCALP_R.z))
    n = Vector((d.x / SCALP_R.x, d.y / SCALP_R.y, d.z / SCALP_R.z)).normalized()
    return p, n


def build_hair(seg=1.0, collection="LOW"):
    parts = []
    for (az, el, L, r0, up, back, sym) in HAIR_LOCKS:
        for sgn in ((1, -1) if sym else (1,)):
            p, n = scalp_point(az * sgn, el)
            d = (n + Vector((0, 0, 1)) * up + Vector((0, 1, 0)) * back).normalized()
            root = p - n * 0.012
            tip = root + d * L
            curl = Vector((0, 0.25 * L * max(0.0, back), 0.15 * L))
            parts.append(spike(name("HairLock", "tmp"), root, tip, r0 * 1.25, curl=curl,
                               seg=max(4, int(6 * seg)), steps=max(3, int(5 * seg)), collection=collection))
    cap = bt.sphere(name("HairCap", "tmp"), 1.0, collection=collection,
                    location=SCALP_C + Vector((0, 0.004, 0.004)),
                    u=max(12, int(20 * seg)), v=max(8, int(12 * seg)), scale=tuple(SCALP_R * 1.06))
    parts.append(cap)
    return join_remove(name("Hair", _sfx(collection)), parts, collection)


def build_headband(seg=1.0, collection="LOW"):
    sfx = _sfx(collection)
    steps = max(16, int(28 * seg))
    # P2 band at z 1.894 hugging the cranium; slightly lower at the back (inferred)
    path = ellipse_path((0, 0.004, 1.894), 0.070, 0.087, steps, z_fn=lambda a: -0.008 * max(0.0, math.sin(a)))
    band = sweep(name("Headband", sfx), path, rect_profile(0.024, 0.008, 0.35), collection=collection)
    bezel = dome(name("HeadGemBezel", sfx), (0, -0.090, 1.894), (0, -1, 0), 0.020, 0.007,
                 segments=max(10, int(16 * seg)), rings=3, collection=collection)
    gem = dome(name("HeadGem", sfx), (0, -0.0955, 1.894), (0, -1, 0), 0.014, 0.008,
               segments=max(10, int(16 * seg)), rings=3, collection=collection)
    for o in (bezel, gem):   # oval, taller than wide (head close-up)
        for v in o.data.vertices:
            v.co.z = 1.894 + (v.co.z - 1.894) * 1.3
    return [band, bezel, gem]


def build_scarf(seg=1.0, collection="LOW"):
    steps = max(20, int(36 * seg))
    cs, rad = [], []
    for i in range(steps):
        a = -math.pi / 2 + 2 * math.pi * i / steps
        front = max(0.0, -math.sin(a)) ** 1.5            # 1 at the front (-Y)
        r = 0.080 + 0.004 * front
        z = 1.772 - 0.030 * front + 0.004 * math.sin(5 * a)
        cs.append((r * math.cos(a), 0.012 + r * 1.02 * math.sin(a), z))
        tube = 0.036 + 0.006 * front + 0.004 * math.sin(7 * a + 1.0)
        rad.append((tube * 1.25, tube))
    return sweep(name("Scarf", _sfx(collection)), cs, circle_profile(1.0, max(8, int(10 * seg))),
                 collection=collection, scales=rad)


PAD_C = Vector((-0.214, 0.040, 1.706))     # top 1.79 (front 14%), y -0.085..+0.165 (side 18%)
PAD_SIZE = (0.192, 0.250, 0.128)
PAD_BEVEL = 0.022
PAD_ROT = (math.radians(-8), math.radians(-4), 0.0)  # outer edge lower (front), back lower (side 16-20%)


def pad_matrix():
    """Pad local frame (centre PAD_C, axes of the unrotated tray) -> world, right pad."""
    from mathutils import Euler
    return Matrix.Translation(PAD_C) @ Euler(PAD_ROT, "XYZ").to_matrix().to_4x4()


def pad_faces():
    """Flat faces of the right pad that carry the Greek-key inlay: (origin, u, v, normal, W, H) in pad-local
    coordinates; W, H are the flat area inside the bevel."""
    sx, sy, sz = PAD_SIZE
    b = PAD_BEVEL
    X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
    return {
        "front": (Vector((0, -sy / 2, 0)), X, Z, -Y, sx - 2 * b, sz - 2 * b),
        "back": (Vector((0, sy / 2, 0)), -X, Z, Y, sx - 2 * b, sz - 2 * b),
        "outer": (Vector((-sx / 2, 0, 0)), -Y, Z, -X, sy - 2 * b, sz - 2 * b),
        "top": (Vector((0, 0, sz / 2)), X, Y, Z, sx - 2 * b, sy - 2 * b),
    }


def pad_pattern_segments(W, H):
    """Greek-key inlay (shoulder detail callout): closed border, a ring open at the top, and an inner
    hook. Returns 2D segments in face coordinates centred on the face."""
    segs = []

    def rect(i, gap=0.0):
        x0, x1, y0, y1 = -W / 2 + i, W / 2 - i, -H / 2 + i, H / 2 - i
        pts = [(x0, y0), (x1, y0), (x1, y1)]
        if gap > 0:
            segs.append(((x1, y1), (gap / 2, y1)))
            segs.append(((-gap / 2, y1), (x0, y1)))
        else:
            segs.append(((x1, y1), (x0, y1)))
        segs.append(((x0, y1), (x0, y0)))
        segs.extend([(pts[k], pts[k + 1]) for k in range(len(pts) - 1)])
        return x0, x1, y0, y1

    s = min(W, H)
    rect(0.10 * s)
    x0, x1, y0, y1 = rect(0.24 * s, gap=0.30 * W)
    # inner hook: a U hanging from the gap, with a short return
    hx, hy0, hy1 = 0.15 * W, y0 + 0.16 * s, y1
    segs += [((-hx, hy1), (-hx, hy0)), ((-hx, hy0), (hx, hy0)), ((hx, hy0), (hx, hy1 - 0.12 * s)),
             ((hx, hy1 - 0.12 * s), (0.0, hy1 - 0.12 * s))]
    return segs


def build_pad_inlay(collection="HIGH", width=0.0055, height=0.0028):
    """Raised strips of the Greek-key inlay on the right pad (HIGH only, for the normal bake)."""
    M = pad_matrix()
    bm = bmesh.new()
    for (o, u, v, n, W, H) in pad_faces().values():
        for (a, b) in pad_pattern_segments(W, H):
            pa = o + u * a[0] + v * a[1]
            pb = o + u * b[0] + v * b[1]
            d = pb - pa
            L = d.length
            if L < 1e-5:
                continue
            side = n.cross(d.normalized())
            c = (pa + pb) / 2 + n * (height / 2)
            corners = []
            for sl in (-1, 1):
                for sw in (-1, 1):
                    for sh in (-1, 1):
                        corners.append(c + d.normalized() * (L / 2 + width / 2) * sl + side * (width / 2) * sw
                                       + n * (height / 2) * sh)
            vs = [bm.verts.new(M @ p) for p in corners]
            for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
                bm.faces.new([vs[i] for i in f])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bt.new_mesh_object(name("ShoulderPad_R", "HIGH_inlay"), bm, collection)


def build_shoulder_pads(seg=1.0, collection="LOW"):
    """Inverted rounded tray over the shoulder: front panel x -0.312..-0.12, z 1.68..1.81;
    side panel y -0.086..+0.18."""
    sfx = _sfx(collection)
    pad = rounded_tray(name("ShoulderPad_R", sfx), PAD_C, PAD_SIZE, PAD_BEVEL, max(2, int(3 * seg)), 0.016,
                       collection=collection, open_faces=("-Z",))
    pad.rotation_euler = PAD_ROT
    apply_mods(pad)
    bt.apply_transform(pad)
    out = [pad] + ([build_pad_inlay(collection)] if collection == "HIGH" else [])
    for y in (PAD_C.y - PAD_SIZE[1] / 2 - 0.001, PAD_C.y + PAD_SIZE[1] / 2 + 0.001):  # rivets front/back
        nrm = (0, -1 if y < PAD_C.y else 1, 0)
        out.append(dome(name("ShoulderPad_R", sfx + "_rivet"), (-0.160, y, 1.712), nrm, 0.011, 0.007,
                        segments=max(8, int(10 * seg)), rings=2, collection=collection))
    return out


def build_belt(seg=1.0, collection="LOW"):
    sfx = _sfx(collection)
    path = ellipse_path((0, 0.0, 1.378), 0.118, 0.100, max(20, int(32 * seg)))
    out = [sweep(name("Belt", sfx), path, rect_profile(0.044, 0.012, 0.3), collection=collection)]
    for sgn in (-1, 1):                  # hip discs ~75 deg from the front (P7)
        a = math.radians(-90 + sgn * 75)
        p = Vector((0.118 * math.cos(a), 0.100 * math.sin(a), 1.378))
        nrm = Vector((math.cos(a) / 0.118, math.sin(a) / 0.100, 0)).normalized()
        out.append(dome(name("BeltDisc" + ("R" if sgn < 0 else "L"), sfx), p + nrm * 0.006, nrm, 0.040, 0.016,
                        segments=max(12, int(20 * seg)), rings=3, rim=0.004, collection=collection))
    buckle = bt.box(name("BeltBuckle", sfx), (0.086, 0.012, 0.040), collection=collection, location=(0, -0.106, 1.378))
    gem = bt.box(name("BeltGem", sfx), (0.040, 0.008, 0.016), collection=collection, location=(0, -0.1135, 1.378))
    for o in (buckle, gem):
        bt.bevel(o, width=0.003, segments=1)
        apply_mods(o)
    return out + [buckle, gem]


def _flap(nm, top_y, bot_y, top_w, bot_w, z_top, z_bot, bulge, notch, cols, rows, collection):
    bm = bmesh.new()
    grid = []
    for j in range(rows + 1):
        f = j / rows
        z = z_top + (z_bot - z_top) * f
        w = top_w + (bot_w - top_w) * f
        row = []
        for i in range(cols + 1):
            u = -1 + 2 * i / cols
            y = top_y + (bot_y - top_y) * f ** 0.45 + (1 - u * u) * bulge   # eases out from the belt (side 34-42%)
            row.append(bm.verts.new((u * w, y, z + notch * (1 - abs(u)) * f * f)))
        grid.append(row)
    for j in range(rows):
        for i in range(cols):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = bt.new_mesh_object(nm, bm, collection)
    s = ob.modifiers.new("Solidify", "SOLIDIFY")
    s.thickness = 0.006
    s.offset = 0.0
    apply_mods(ob)
    bt.shade_smooth(ob, math.radians(60))
    return ob


def build_loincloth(seg=1.0, collection="LOW"):
    """Front flap from the belt (z 1.356) to P15 (z 1.022), 0.184 -> 0.124 wide; back flap to z 0.99."""
    sfx = _sfx(collection)
    cols, rows = max(4, int(6 * seg)), max(5, int(8 * seg))
    f = _flap(name("LoinclothFront", sfx), -0.115, -0.152, 0.092, 0.062, 1.356, 0.985, -0.010, 0.03,
              cols, rows, collection)
    b = _flap(name("LoinclothBack", sfx), 0.098, 0.118, 0.096, 0.072, 1.356, 0.970, 0.008, 0.0,
              cols, rows, collection)
    return [f, b]


BRACER_A = Vector((-0.258, 0.084, 1.405))   # front 34%: centre -0.267, 0.133 wide; side back edge +0.14
BRACER_B = Vector((-0.290, 0.068, 1.255))   # wrist ring (front 40%)


def build_bracers(seg=1.0, collection="LOW"):
    sfx = _sfx(collection)
    prof = [(0.050, -0.05), (0.064, 0.0), (0.067, 0.12), (0.062, 0.16), (0.066, 0.20), (0.065, 0.45),
            (0.060, 0.50), (0.063, 0.54), (0.060, 0.85), (0.058, 0.97), (0.048, 1.0)]
    out = [lathe_along(name("Bracer_R", sfx), prof, BRACER_A, BRACER_B, segments=max(12, int(18 * seg)),
                       ellip=(1.0, 1.08), collection=collection)]
    d = (BRACER_B - BRACER_A).normalized()
    out.append(lathe_along(name("WristRing_R", sfx), [(0.044, 0.0), (0.053, 0.15), (0.055, 0.5), (0.053, 0.85),
                                                      (0.044, 1.0)],
                           BRACER_B - d * 0.004, BRACER_B + d * 0.020, segments=max(12, int(18 * seg)),
                           collection=collection))
    return out


FIST_C = Vector((-0.300, 0.045, 1.150))     # front 42-48%: z 1.07-1.25, 0.12 wide


def build_gloves(seg=1.0, collection="LOW"):
    """Black glove shell over back of hand and palm; fingers stay exposed (hand detail callout)."""
    sfx = _sfx(collection)
    out = [bt.sphere(name("Glove_R", sfx), 1.0, collection=collection,
                     location=FIST_C + Vector((-0.004, 0.012, 0.010)),
                     u=max(12, int(16 * seg)), v=max(8, int(10 * seg)), scale=(0.054, 0.056, 0.082))]
    # six gold studs on the back of the hand (outer face, -X), staggered 3 + 3
    studs = [(-0.026, 1.195), (0.004, 1.204), (0.034, 1.190), (-0.016, 1.150), (0.014, 1.156), (0.040, 1.142)]
    for (dy, z) in studs:
        p = Vector((FIST_C.x - 0.052, FIST_C.y + dy, z))
        nrm = Vector((-1.0, -0.25, 0.1)).normalized()
        out.append(dome(name("GloveStud_R", sfx), p, nrm, 0.0125, 0.010,
                        segments=max(8, int(10 * seg)), rings=2, collection=collection))
    return out


KNEE_C = Vector((-0.160, -0.030, 0.835))   # P10; front 62%: pad centre -0.166, 0.141 wide


def build_knees(seg=1.0, collection="LOW"):
    sfx = _sfx(collection)
    nrm = Vector((-0.22, -1.0, 0.05)).normalized()
    out = [dome(name("KneePad_R", sfx), KNEE_C + nrm * 0.040, nrm, 0.068, 0.028,
                segments=max(14, int(22 * seg)), rings=max(3, int(4 * seg)), rim=0.006, collection=collection)]
    out.append(lathe_along(name("KneeStrap_R", sfx), [(0.060, 0.0), (0.066, 0.1), (0.066, 0.9), (0.060, 1.0)],
                           Vector((-0.157, -0.012, 0.860)), Vector((-0.166, -0.006, 0.815)),
                           segments=max(12, int(18 * seg)), ellip=(1.0, 1.05), collection=collection))
    return out


BOOT_TOP = Vector((-0.185, 0.025, 0.715))    # P11; boot centre per height from front/side rows
BOOT_ANKLE = Vector((-0.265, 0.048, 0.130))


def build_boots(seg=1.0, collection="LOW"):
    sfx = _sfx(collection)
    # (half width x, half depth y, f) measured at z 0.70, 0.63, 0.546, 0.51, 0.46, 0.38, 0.296, 0.21, 0.13
    prof = [(0.064, 0.074, -0.02), (0.072, 0.083, 0.0), (0.090, 0.090, 0.12), (0.087, 0.102, 0.27),
            (0.075, 0.092, 0.33), (0.060, 0.080, 0.42), (0.050, 0.070, 0.56), (0.056, 0.062, 0.71),
            (0.055, 0.068, 0.86), (0.060, 0.072, 1.0)]
    out = [lathe_along(name("BootShaft_R", sfx), prof, BOOT_TOP, BOOT_ANKLE, segments=max(12, int(20 * seg)),
                       collection=collection, cap=False)]
    # foot: loft from heel (+Y) to toe (-Y), splayed 8 deg outward (P12, P14 length 0.31)
    stations = [(0.125, 0.050, 0.070), (0.100, 0.060, 0.120), (0.050, 0.064, 0.150), (0.000, 0.064, 0.130),
                (-0.060, 0.060, 0.090), (-0.120, 0.058, 0.075), (-0.160, 0.050, 0.060), (-0.184, 0.030, 0.042)]
    n = max(8, int(12 * seg))
    secs = []
    for (y, hw, h) in stations:
        secs.append([(hw * math.cos(2 * math.pi * k / n), y, h / 2 + (h / 2) * math.sin(2 * math.pi * k / n))
                     for k in range(n)])
    foot = bt.loft(name("BootFoot_R", sfx), secs, collection=collection)
    rot = Matrix.Rotation(math.radians(-8), 4, "Z")
    for v in foot.data.vertices:
        v.co = rot @ Vector(v.co) + Vector((-0.290, 0.000, 0.008))  # front 98%: foot centre -0.296; side heel +0.132, toe -0.18
    out.append(foot)
    heel = bt.box(name("BootHeel_R", sfx), (0.070, 0.060, 0.034), collection=collection,
                  location=(-0.277, 0.095, 0.017))
    bt.bevel(heel, width=0.004, segments=1)
    apply_mods(heel)
    out.append(heel)
    d = (BOOT_ANKLE - BOOT_TOP).normalized()
    rc = BOOT_TOP + (BOOT_ANKLE - BOOT_TOP) * 0.86
    out.append(lathe_along(name("AnkleRing_R", sfx), [(0.064, 0.0), (0.072, 0.2), (0.072, 0.8), (0.064, 1.0)],
                           rc - d * 0.012, rc + d * 0.012, segments=max(14, int(20 * seg)), ellip=(1.0, 1.12),
                           collection=collection))
    out.append(dome(name("AnkleRing_R", sfx + "_disc"), rc + Vector((-0.074, 0.0, 0.0)), (-1, 0, 0), 0.028, 0.012,
                    segments=max(10, int(14 * seg)), rings=2, rim=0.003, collection=collection))
    return out


def build_all_gear(seg=1.0, collection="LOW"):
    """All gear objects, right side mirrored to the left. Pieces sharing a base name merge."""
    sfx = _sfx(collection)
    objs = [build_hair(seg, collection)]
    objs += build_headband(seg, collection)
    objs.append(build_scarf(seg, collection))
    objs += build_belt(seg, collection)
    objs += build_loincloth(seg, collection)
    right = (build_shoulder_pads(seg, collection) + build_bracers(seg, collection) + build_gloves(seg, collection)
             + build_knees(seg, collection) + build_boots(seg, collection))
    groups = {}
    for o in right:
        base = o.name.split(".")[0]
        base = base.split("_" + sfx)[0] + "_" + sfx      # PadRivet etc. fold into their part
        groups.setdefault(base, []).append(o)
    for base, obs in groups.items():
        o = join_remove(base, obs, collection) if len(obs) > 1 else obs[0]
        o.name = base
        objs.append(o)
        objs.append(mirror_copy(o, base.replace("_R_", "_L_")))
    return objs
