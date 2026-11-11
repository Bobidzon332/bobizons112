"""Phase 05c: paint the atlas. Every texel of the delivery mesh's UV layout is rasterised back to the
3D point it belongs to (no camera, no projection), then coloured by its region (skin, hair, gold, ...)
and by measured 3D features: face, gold piping traced from the front panel, boot ornaments, the pads'
Greek-key inlay (same pattern function as the raised HIGH strips), AO-driven ink lines. Writes
T_StarPlatinum_{BC,R,M}_2048.png (+ the baked normal) and rebuilds MAT_StarPlatinum on the delivery mesh.
Colours are pure albedo picked from the sheet's palette swatches; no light is baked in, the ink lines are
an art-direction choice (anime line work, asset-brief MATERIALS).

blender --background --python build/05c_paint.py -- [--master ...]
"""
import os, sys, math, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import numpy as np
from mathutils import Vector, Matrix
import bt
import sp_lib as L
import sp_gear as G
import sp_r15 as R

L.setup("05c_paint")
RES = 2048
TEX = os.path.join(L.ROOT, "textures")

HEX = lambda h: np.array([int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)], np.float32)
PAL = {  # sRGB albedo, from the sheet's palette swatches and panels
    "skin": HEX("#8C6CD4"), "skin_ink": HEX("#3E2A7E"), "hair": HEX("#1D1727"), "hair_tip": HEX("#4E3A82"),
    "gold": HEX("#C9A253"), "gold_dark": HEX("#7E6230"), "inlay": HEX("#E8E4F0"), "black": HEX("#1E1A24"),
    "black_hi": HEX("#2E2836"), "red": HEX("#A8352A"), "red_dark": HEX("#68201B"), "cloth": HEX("#DCD6F0"),
    "cloth_dark": HEX("#A49CC6"), "gem": HEX("#393246"), "eye": HEX("#EAE8F4"), "iris": HEX("#9C98B2"),
    "mask": HEX("#2A1F46"), "mouth": HEX("#3A2766"),
}
ROUGH = {"skin": 0.55, "hair": 0.6, "gold": 0.32, "black": 0.42, "red": 0.82, "cloth": 0.85, "gem": 0.12,
         "inlay": 0.35}
METAL = {"skin": 0.0, "hair": 0.0, "gold": 1.0, "black": 0.0, "red": 0.0, "cloth": 0.0, "gem": 0.0, "inlay": 0.25}


# ---------------------------------------------------------------- rasteriser

def rasterise(ob, res):
    me = ob.data
    me.calc_loop_triangles()
    nt = len(me.loop_triangles)
    loops = np.empty(nt * 3, np.int32)
    me.loop_triangles.foreach_get("loops", loops)
    loops = loops.reshape(nt, 3)
    tpoly = np.empty(nt, np.int32)
    me.loop_triangles.foreach_get("polygon_index", tpoly)
    nl = len(me.loops)
    uv = np.empty(nl * 2, np.float32)
    me.uv_layers["UVMap"].data.foreach_get("uv", uv)
    uv = uv.reshape(nl, 2)
    lv = np.empty(nl, np.int32)
    me.loops.foreach_get("vertex_index", lv)
    co = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    cn = np.empty(nl * 3, np.float32)
    me.corner_normals.foreach_get("vector", cn)
    cn = cn.reshape(nl, 3)
    reg_p = np.empty(len(me.polygons), np.int32)
    me.attributes["region"].data.foreach_get("value", reg_p)
    part_p = np.empty(len(me.polygons), np.int32)
    me.attributes["r15_part"].data.foreach_get("value", part_p)

    pos = np.zeros((res, res, 3), np.float32)
    nor = np.zeros((res, res, 3), np.float32)
    reg = np.full((res, res), -1, np.int8)
    part = np.full((res, res), -1, np.int8)
    P = uv[loops] * res - 0.5                        # (nt, 3, 2) pixel coords of corners
    X = co[lv[loops]]                                # (nt, 3, 3)
    Nn = cn[loops]
    for t in range(nt):
        a, b, c = P[t]
        x0, x1 = int(math.floor(min(a[0], b[0], c[0]))), int(math.ceil(max(a[0], b[0], c[0])))
        y0, y1 = int(math.floor(min(a[1], b[1], c[1]))), int(math.ceil(max(a[1], b[1], c[1])))
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, res - 1), min(y1, res - 1)
        if x1 < x0 or y1 < y0:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1, dtype=np.float32), np.arange(y0, y1 + 1, dtype=np.float32))
        den = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
        if abs(den) < 1e-12:
            continue
        w1 = ((xs - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (ys - a[1])) / den
        w2 = ((b[0] - a[0]) * (ys - a[1]) - (xs - a[0]) * (b[1] - a[1])) / den
        w0 = 1 - w1 - w2
        m = (w0 >= -0.02) & (w1 >= -0.02) & (w2 >= -0.02)
        if not m.any():
            continue
        yy, xx = ys[m].astype(np.int32), xs[m].astype(np.int32)
        W = np.stack([w0[m], w1[m], w2[m]], 1)
        pos[yy, xx] = W @ X[t]
        nor[yy, xx] = W @ Nn[t]
        reg[yy, xx] = reg_p[tpoly[t]]
        part[yy, xx] = part_p[tpoly[t]]
    n = np.linalg.norm(nor, axis=-1, keepdims=True)
    nor = nor / np.maximum(n, 1e-6)
    return pos, nor, reg, part


# ---------------------------------------------------------------- helpers

def seg_dist2d(px, py, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy + 1e-12
    t = np.clip(((px - ax) * dx + (py - ay) * dy) / L2, 0, 1)
    return np.hypot(px - (ax + t * dx), py - (ay + t * dy))


def poly_dist(px, py, pts):
    d = np.full(px.shape, 9.0, np.float32)
    for a, b in zip(pts, pts[1:]):
        d = np.minimum(d, seg_dist2d(px, py, a, b))
    return d


def smooth_step(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def mix(dst, mask, col, k=1.0):
    if np.isscalar(k):
        dst[mask] = dst[mask] * (1 - k) + col * k
    else:
        kk = k[mask][:, None]
        dst[mask] = dst[mask] * (1 - kk) + col * kk


# gold piping traced from the front panel (x, z in metres, character's right side; mirrored)
PIPING_TORSO = [(-0.140, 1.695), (-0.153, 1.628), (-0.140, 1.562), (-0.113, 1.495), (-0.100, 1.442), (-0.107, 1.39)]
PIPING_BACK = [(-0.150, 1.66), (-0.128, 1.60), (-0.112, 1.54), (-0.120, 1.48), (-0.105, 1.42)]
PIPING_THIGH = [(-0.153, 1.349), (-0.173, 1.269), (-0.193, 1.176), (-0.197, 1.096), (-0.187, 1.016),
                (-0.160, 0.936), (-0.140, 0.882)]
PIPING_KNEE_V = [[(-0.205, 0.800), (-0.178, 0.716)], [(-0.128, 0.800), (-0.178, 0.716)]]
LINE_W = 0.0032        # half width of the piping (m)


def boot_front_x(z):
    a, b = G.BOOT_TOP, G.BOOT_ANKLE
    f = (a.z - z) / (a.z - b.z)
    return a.x + (b.x - a.x) * f


# ---------------------------------------------------------------- painter

def paint(pos, nor, reg, part, ao):
    H, W = reg.shape
    col = np.zeros((H, W, 3), np.float32)
    rough = np.zeros((H, W), np.float32)
    metal = np.zeros((H, W), np.float32)
    names = R.REGIONS
    for i, r in enumerate(names):
        m = reg == i
        if r in PAL:
            col[m] = PAL[r]
        rough[m] = ROUGH.get(r, 0.5)
        metal[m] = METAL.get(r, 0.0)
    x, y, z = pos[..., 0], pos[..., 1], pos[..., 2]
    nx, ny, nz = nor[..., 0], nor[..., 1], nor[..., 2]
    ax = np.abs(x)
    sk = reg == R.REGION_INDEX["skin"]
    ink = smooth_step(0.64, 0.44, ao)                          # deep concave creases -> anime line work

    # skin: ink lines in creases
    mix(col, sk, PAL["skin_ink"], ink * 0.7)
    # face (Head part, front-facing): dark brow mask under the headband, eyes, nose bridge, mouth
    head = sk & (part == R.PART_INDEX["Head"]) & (ny < -0.15)
    mask = head & (z > 1.862) & (z < 1.886) & (ax < 0.052)
    bridge = head & (z > 1.836) & (z <= 1.862) & (ax < 0.004 + (z - 1.836) * 0.30)
    col[mask | bridge] = PAL["mask"]
    for sx in (-1, 1):
        ex, ez = 0.024 * sx, 1.872
        e = head & ((((x - ex) / 0.0135) ** 2 + ((z - ez) / 0.0055) ** 2) < 1) & (z < ez + 0.0055 - 0.004 * np.abs(x - ex) / 0.0135)
        col[e] = PAL["eye"]
        iris = head & (((x - ex) ** 2 + (z - ez + 0.0005) ** 2) < 0.0028 ** 2)
        col[iris] = PAL["iris"]
    mouth = head & (np.abs(z - 1.817) < 0.0011) & (ax < 0.012)
    col[mouth] = PAL["mouth"]
    # gold piping on the skin (front hemisphere: front panel trace; back hemisphere: back trace)
    front = ny < 0.05
    pip = np.zeros_like(sk)
    for pts in (PIPING_TORSO, PIPING_THIGH):
        pip |= front & (poly_dist(-ax, z, pts) < LINE_W)
    pip |= ~front & (poly_dist(-ax, z, PIPING_BACK) < LINE_W)
    for pts in PIPING_KNEE_V:
        pip |= (poly_dist(-ax, z, pts) < LINE_W) & front
    pip &= sk
    col[pip] = PAL["gold"]
    rough[pip] = ROUGH["gold"]
    metal[pip] = 0.85

    # hair: near-black with violet towards the lock tips, darker in the creases
    hr = reg == R.REGION_INDEX["hair"]
    d = np.sqrt(x ** 2 + ((y - G.SCALP_C.y) * 0.9) ** 2 + ((z - G.SCALP_C.z) * 1.1) ** 2)
    mix(col, hr, PAL["hair_tip"], smooth_step(0.10, 0.19, d) * 0.85)
    mix(col, hr, PAL["hair"], ink * 0.7)

    # gold: darker in creases, white Greek-key inlay on the pads
    gd = reg == R.REGION_INDEX["gold"]
    mix(col, gd, PAL["gold_dark"], ink * 0.6)
    pads = gd & (part >= 0) & (np.isin(part, [R.PART_INDEX["RightUpperArm"], R.PART_INDEX["LeftUpperArm"]]))
    if pads.any():
        Minv = np.array(G.pad_matrix().inverted(), np.float32)
        Rinv = Minv[:3, :3]
        p = pos[pads].copy()
        n = nor[pads].copy()
        p[:, 0] = -np.abs(p[:, 0])              # left pad mirrors the right one
        n[:, 0] = np.where(pos[pads][:, 0] > 0, -n[:, 0], n[:, 0])
        pl = p @ Rinv.T + Minv[:3, 3]
        nl = n @ Rinv.T
        inlay = np.zeros(len(p), bool)
        for key, (o, u, v, fn, Wf, Hf) in G.pad_faces().items():
            o, u, v, fn = (np.array(t, np.float32) for t in (o, u, v, fn))
            on = (nl @ fn) > 0.75
            if not on.any():
                continue
            rel = pl[on] - o
            pu, pv = rel @ u, rel @ v
            dmin = np.full(pu.shape, 9.0, np.float32)
            for a2, b2 in G.pad_pattern_segments(Wf, Hf):
                dmin = np.minimum(dmin, seg_dist2d(pu, pv, a2, b2))
            idx = np.nonzero(on)[0]
            inlay[idx[dmin < 0.0034]] = True
        sub = col[pads]
        sub[inlay] = PAL["inlay"]
        col[pads] = sub
        rs, ms = rough[pads], metal[pads]
        rs[inlay], ms[inlay] = ROUGH["inlay"], METAL["inlay"]
        rough[pads], metal[pads] = rs, ms

    # black leather: subtle lift on upward faces is lighting, so only a crease darkening here
    bk = reg == R.REGION_INDEX["black"]
    # boot ornaments: chevron line and three lozenges down the boot front (front panel 66-92%)
    lower = np.isin(part, [R.PART_INDEX["RightLowerLeg"], R.PART_INDEX["LeftLowerLeg"]])
    boot = bk & lower & (z < G.BOOT_TOP.z + 0.005) & (ny < -0.35)
    if boot.any():
        bx = boot_front_x(z)
        u = ax - (-bx)                           # signed offset from the boot's front centre line
        orn = boot & (np.abs(u) < 0.0035) & (z > 0.25) & (z < 0.70)
        for zc, hw, hh in ((0.600, 0.020, 0.032), (0.450, 0.017, 0.028), (0.310, 0.014, 0.024)):
            dd = np.abs(u) / hw + np.abs(z - zc) / hh
            orn |= boot & (dd < 1.0) & (dd > 0.55)
            orn |= boot & (dd < 0.30)
        col[orn] = PAL["gold"]
        rough[orn], metal[orn] = ROUGH["gold"], 0.9

    # red scarf and lavender cloth: fold shading from the AO creases
    rd = reg == R.REGION_INDEX["red"]
    mix(col, rd, PAL["red_dark"], ink * 0.45)
    cl = reg == R.REGION_INDEX["cloth"]
    mix(col, cl, PAL["cloth_dark"], ink * 0.6)
    return col, rough, metal


def dilate(img, valid, steps=24):
    img = img.copy()
    valid = valid.copy()
    for _ in range(steps):
        acc = np.zeros_like(img)
        cnt = np.zeros(valid.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = np.roll(valid, (dy, dx), (0, 1))
            acc += np.roll(img, (dy, dx), (0, 1)) * v[..., None] if img.ndim == 3 else np.roll(img, (dy, dx), (0, 1)) * v
            cnt += v
        new = (~valid) & (cnt > 0)
        if img.ndim == 3:
            img[new] = acc[new] / cnt[new][:, None]
        else:
            img[new] = acc[new] / cnt[new]
        valid |= new
    return img


def save_png(path, arr, colorspace):
    H, W = arr.shape[:2]
    rgba = np.ones((H, W, 4), np.float32)
    if arr.ndim == 2:
        rgba[..., 0] = rgba[..., 1] = rgba[..., 2] = arr
    else:
        rgba[..., :3] = arr
    img = bpy.data.images.new(os.path.basename(path).rsplit(".", 1)[0], W, H, alpha=False)
    img.colorspace_settings.name = colorspace
    img.pixels.foreach_set(np.clip(rgba, 0, 1).ravel())
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    return img


def box_blur(g, r, passes=2):
    k = 2 * r + 1
    for _ in range(passes):
        c = np.cumsum(np.pad(g, ((r + 1, r), (0, 0)), mode="edge"), 0)
        g = (c[k:] - c[:-k]) / k
        c = np.cumsum(np.pad(g, ((0, 0), (r + 1, r)), mode="edge"), 1)
        g = (c[:, k:] - c[:, :-k]) / k
    return g


def load_gray(path, res):
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    a = np.empty(w * h * 4, np.float32)
    img.pixels.foreach_get(a)
    g = a.reshape(h, w, 4)[..., 0]
    bpy.data.images.remove(img)
    if w != res:
        f = res // w
        g = np.kron(g, np.ones((f, f), np.float32))
    return box_blur(g, 2)      # AO sampling noise would otherwise turn into speckled ink


def build_material(me, maps):
    mat = bpy.data.materials.get("MAT_StarPlatinum") or bpy.data.materials.new("MAT_StarPlatinum")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    def tex(path, cs):
        n = nt.nodes.new("ShaderNodeTexImage")
        n.image = bpy.data.images.load(path, check_existing=True)
        n.image.colorspace_settings.name = cs
        return n
    nt.links.new(tex(maps["BC"], "sRGB").outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex(maps["R"], "Non-Color").outputs["Color"], bsdf.inputs["Roughness"])
    nt.links.new(tex(maps["M"], "Non-Color").outputs["Color"], bsdf.inputs["Metallic"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(tex(maps["N"], "Non-Color").outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    me.materials.clear()
    me.materials.append(mat)
    return mat


def main():
    a = L.args()
    bt.open_master(a.master)
    bt.clear_owned()
    ob = bpy.data.objects["CH_StarPlatinum_LOD0"]
    os.makedirs(TEX, exist_ok=True)
    pos, nor, reg, part = rasterise(ob, RES)
    valid = reg >= 0
    nrm_files = sorted(glob.glob(os.path.join(TEX, "bake", "*normal*.png")))
    ao_files = sorted(glob.glob(os.path.join(TEX, "bake", "*ao*.png")))
    ao = load_gray(ao_files[0], RES) if ao_files else np.ones(reg.shape, np.float32)
    col, rough, metal = paint(pos, nor, reg, part, ao)
    col = dilate(col, valid)
    rough = dilate(rough, valid)
    metal = dilate(metal, valid)
    maps = {
        "BC": os.path.join(TEX, "T_StarPlatinum_BC_2048.png"),
        "R": os.path.join(TEX, "T_StarPlatinum_R_2048.png"),
        "M": os.path.join(TEX, "T_StarPlatinum_M_2048.png"),
        "N": os.path.join(TEX, "T_StarPlatinum_N_2048.png"),
    }
    save_png(maps["BC"], col, "sRGB")
    save_png(maps["R"], rough, "Non-Color")
    save_png(maps["M"], metal, "Non-Color")
    if nrm_files:
        import shutil
        shutil.copyfile(nrm_files[0], maps["N"])
    build_material(ob.data, maps)
    cov = float(valid.mean())
    stats = {"uv_coverage": round(cov, 4), "res": RES, "normal_source": nrm_files[:1], "ao_source": ao_files[:1],
             "regions_px": {r: int((reg == i).sum()) for i, r in enumerate(R.REGIONS)}}
    json.dump(stats, open(os.path.join(TEX, "paint_report.json"), "w"), indent=1)
    bt.log("uv coverage", round(cov, 3), "normal", bool(nrm_files), "ao", bool(ao_files))
    bt.save_master(a.master)


main()
