"""Point-mass web-swing simulation for the 20 s shot.
Street runs along +X, centre line y = 0, building faces at y = +-FACE (north = +y = Spidey's left).
Each web = rope with max length (inextensible), reeled in at a rate (Spidey pulls).
Outputs per-frame COM positions/velocities (24 fps) -> sim_out.json, plus a top/side plot PNG.
"""
import json, math, sys, os
import numpy as np

FPS = 24
DT = 1.0 / 480
G = np.array([0, 0, -9.81])
DRAG = 0.0025          # quadratic air drag per metre (terminal ~60 m/s)
FACE = 10.0            # building faces at y = +-10
GROUND_COM = 0.95      # COM height when crouched on the street
T_END = 20.0 + 1.0     # a little tail for motion blur / handles

# ---- the plan (tuned by hand, see notes in PLAN) ----
START = dict(p=(0.0, -10.12, 24.42), v=(7.5, 1.9, 3.8))   # crouched at the roof edge of the start building (south side)
CORRIDOR_K, CORRIDOR_C = 1.6, 0.9      # soft sideways "flight line" back to the middle of the street (|y|>2.5)
WEBS = [
    # id, side(+1 north/-1 south), hand, attach t, release t, anchor dx ahead, anchor height, reel m/s
    dict(id="A", side=-1, hand="R", t0=1.25, t1=4.05, lead=None, h=33.0, z_low=3.4, reel=1.2),
    dict(id="B", side=+1, hand="L", t0=5.35, t1=7.95, lead=None, h=32.0, z_low=3.8, reel=1.4),
    dict(id="C", side=-1, hand="R", t0=8.55, t1=10.85, lead=None, h=33.0, z_low=3.2, reel=1.6),
    # slingshot: two webs at once, both sides, ahead and high, hard reel
    dict(id="D", side=+1, hand="L", t0=11.25, t1=12.75, lead=26.0, h=35.0, z_low=None, reel=9.0),
    dict(id="E", side=-1, hand="R", t0=11.25, t1=12.75, lead=26.0, h=35.0, z_low=None, reel=9.0),
]
LAND_SLIDE = 0.40      # seconds to stop after touching down
ROPE_SOFT = 0.35       # fraction of the overstretch removed per pass (1 = rigid rope)


def anchor_for(w, p):
    """Place the anchor on the facade so the bottom of the swing lands near z_low."""
    ay = w["side"] * FACE
    az = w["h"]
    if w["lead"] is not None:
        return np.array([p[0] + w["lead"], ay, az])
    L = az - w["z_low"]                      # rope length that gives that low point
    dy, dz = ay - p[1], az - p[2]
    dx2 = L * L - dy * dy - dz * dz
    dx = math.sqrt(dx2) if dx2 > 4 else 2.0
    return np.array([p[0] + dx, ay, az])


def run(start=START, webs=WEBS):
    p = np.array(start["p"], float)
    v = np.array(start["v"], float)
    t = 0.0
    active = {}            # id -> [anchor, length, reel]
    anchors = {}
    landed_t = None
    out = []
    next_sample = 0.0
    while t <= T_END + 1e-9:
        # events
        for w in webs:
            if w["id"] not in anchors and t >= w["t0"]:
                a = anchor_for(w, p)
                anchors[w["id"]] = dict(pos=a.tolist(), hand=w["hand"], t0=w["t0"], t1=w["t1"])
                active[w["id"]] = [a, float(np.linalg.norm(p - a)), w["reel"]]
            if w["id"] in active and t >= w["t1"]:
                del active[w["id"]]
        if t >= next_sample - 1e-9:
            out.append(dict(t=round(t, 5), p=p.tolist(), v=v.tolist(), webs=sorted(active.keys())))
            next_sample += 1.0 / FPS
        # integrate
        if landed_t is None:
            acc = G - DRAG * np.linalg.norm(v) * v
            if t > 0.5:
                off = p[1] - math.copysign(min(abs(p[1]), 2.5), p[1])
                acc = acc + np.array([0.0, -CORRIDOR_K * off - CORRIDOR_C * v[1], 0.0])
            v = v + acc * DT
            pn = p + v * DT
            for _ in range(4):                       # rope constraints (max length), slightly elastic catch
                for k, (a, L, reel) in active.items():
                    d = pn - a
                    n = np.linalg.norm(d)
                    if n > L:
                        pn = a + d / n * (n - (n - L) * ROPE_SOFT)
            for k in active:
                active[k][1] = max(2.0, active[k][1] - active[k][2] * DT)
            v = (pn - p) / DT
            p = pn
            if p[2] <= GROUND_COM and t > 13:
                p[2] = GROUND_COM
                landed_t = t
                v_land = v.copy()
                v_land[2] = 0
        else:
            k = min(1.0, (t - landed_t) / LAND_SLIDE)
            v = v_land * (1 - k) ** 2
            p = p + v * DT
            p[2] = GROUND_COM
        t += DT
    return out, anchors, landed_t


def report(out, anchors, landed_t):
    P = np.array([o["p"] for o in out])
    V = np.array([o["v"] for o in out])
    sp = np.linalg.norm(V, axis=1)
    print(f"frames {len(out)}  landed at t={landed_t and round(landed_t,2)}")
    print(f"x range {P[:,0].min():.1f}..{P[:,0].max():.1f}  y range {P[:,1].min():.1f}..{P[:,1].max():.1f}  z range {P[:,2].min():.1f}..{P[:,2].max():.1f}")
    for k, a in anchors.items():
        print(" web", k, a["hand"], [round(x, 1) for x in a["pos"]], "t", a["t0"], "-", a["t1"])
    for s in range(0, 21):
        i = min(len(out) - 1, s * FPS)
        o = out[i]
        print(f"  t={s:4.1f}s  p=({o['p'][0]:6.1f},{o['p'][1]:5.1f},{o['p'][2]:5.1f})  speed {sp[i]:5.1f} m/s  webs {o['webs']}")
    # clearance checks
    bad = [(o["t"], o["p"]) for o in out if abs(o["p"][1]) > FACE - 1.2 and o["p"][2] < 30 and o["t"] > 0.6]
    if bad:
        print("!! too close to a facade at", [(round(b[0], 2), [round(x, 1) for x in b[1]]) for b in bad[:6]], "...", len(bad))
    low = [(o["t"], round(o["p"][2], 2)) for o in out if 1.2 < o["p"][2] < 2.6 and o["t"] < 17]
    if low:
        print("!! low over cars at", low[:5])


def plot(out, anchors, path):
    from PIL import Image, ImageDraw
    W, H = 1800, 900
    img = Image.new("RGB", (W, H), (245, 245, 240))
    d = ImageDraw.Draw(img)
    P = np.array([o["p"] for o in out])
    x0, x1 = P[:, 0].min() - 20, P[:, 0].max() + 30
    sx = (W - 80) / (x1 - x0)
    # top view (upper half): y in [-25, 25]
    def tv(x, y):
        return 40 + (x - x0) * sx, 220 - y * 6
    def sv(x, z):
        return 40 + (x - x0) * sx, 860 - z * 9
    for yy in (FACE, -FACE):
        d.line([tv(x0, yy), tv(x1, yy)], fill=(120, 120, 120), width=2)
    d.line([tv(x0, 0), tv(x1, 0)], fill=(200, 200, 200), width=1)
    d.line([sv(x0, 0), sv(x1, 0)], fill=(120, 120, 120), width=2)
    for zz in (10, 20, 30, 40):
        d.line([sv(x0, zz), sv(x1, zz)], fill=(225, 225, 225), width=1)
        d.text(sv(x0, zz), f"{zz} m", fill=(150, 150, 150))
    for i in range(1, len(P)):
        col = (30, 80, 220) if out[i]["webs"] else (220, 60, 60)
        d.line([tv(*P[i - 1, :2]), tv(*P[i, :2])], fill=col, width=3)
        d.line([sv(P[i - 1, 0], P[i - 1, 2]), sv(P[i, 0], P[i, 2])], fill=col, width=3)
    for i in range(0, len(P), FPS):
        d.ellipse([tv(*P[i, :2])[0] - 3, tv(*P[i, :2])[1] - 3, tv(*P[i, :2])[0] + 3, tv(*P[i, :2])[1] + 3], fill=(0, 0, 0))
        d.text((tv(*P[i, :2])[0] - 6, tv(*P[i, :2])[1] + 6), f"{i // FPS}", fill=(0, 0, 0))
        d.text((sv(P[i, 0], P[i, 2])[0] - 6, sv(P[i, 0], P[i, 2])[1] - 16), f"{i // FPS}", fill=(0, 0, 0))
    for k, a in anchors.items():
        x, y, z = a["pos"]
        d.ellipse([tv(x, y)[0] - 6, tv(x, y)[1] - 6, tv(x, y)[0] + 6, tv(x, y)[1] + 6], fill=(240, 120, 0))
        d.text((tv(x, y)[0] + 8, tv(x, y)[1] - 6), k, fill=(240, 120, 0))
        d.ellipse([sv(x, z)[0] - 6, sv(x, z)[1] - 6, sv(x, z)[0] + 6, sv(x, z)[1] + 6], fill=(240, 120, 0))
        d.text((sv(x, z)[0] + 8, sv(x, z)[1] - 6), k, fill=(240, 120, 0))
    d.text((40, 20), "TOP VIEW (y = across street, faces at +-10 m)   blue = on a web, red = free flight, numbers = seconds", fill=(0, 0, 0))
    d.text((40, 420), "SIDE VIEW (height)", fill=(0, 0, 0))
    img.save(path)


if __name__ == "__main__":
    out, anchors, landed = run()
    report(out, anchors, landed)
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(dict(fps=FPS, frames=out, anchors=anchors, landed=landed, face=FACE),
              open(os.path.join(here, "..", "research", "sim_out.json"), "w"))
    plot(out, anchors, os.path.join(here, "..", "shots", "sim_plot.png"))
