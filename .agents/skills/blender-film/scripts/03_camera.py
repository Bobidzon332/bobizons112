# His Part 3 camera, built from the storyboard panels: a "Camera Path" that trails Spidey's path, camera on Follow
# Path (offset keyed per frame), rotation keys aiming at Spidey, lens per panel. Noise layers come later.
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
import json
from mathutils import Vector, Matrix, Quaternion
sim = json.load(open(os.path.join(ROOT, "research", "sim_shift.json")))
F = sim["frames"]; fps = sim["fps"]; n = len(F)
P = [Vector(f["p"]) for f in F]
V = [Vector(f["v"]) for f in F]
sc = bpy.context.scene
anim = coll("ANIMATION")
for nm in ("Camera Path", "Camera"):
    o = bpy.data.objects.get(nm)
    if o: bpy.data.objects.remove(o)

# storyboard panels -> chase offsets: back (m behind), side (+ = Spidey's left/north), up (m), lens (mm)
KEYS = [  # scene time, back, side, up, lens   (storyboard panel in the comment)
    (0.0, 3.6, -0.8, 1.3, 24),    # 1 behind, slightly above, on the roof
    (0.6, 3.6, -0.8, 1.3, 24),
    (1.9, 4.5, -1.0, 0.4, 24),
    (3.0, 5.0, -1.2, -1.0, 26),   # 2 behind, slightly below, tracking forward
    (5.4, 5.0, -1.6, -1.4, 28),   # 3 behind, slight up tilt (front flip)
    (7.9, 4.6, 3.0, 0.2, 26),     # 4 other side, tracking
    (10.4, 5.2, 1.0, 1.4, 28),    # 5 behind, slightly above, following the arc
    (12.4, 4.2, 0.0, -2.0, 24),   # 6 low behind, tilt up (slingshot)
    (14.0, 5.0, -0.5, 0.8, 24),
    (15.0, 4.6, -1.0, 3.2, 26),   # 7 above and behind, looking down (back flip at the top)
    (16.4, 4.4, 0.0, 2.2, 26),    # 8 behind, fast follow (dive)
    (17.6, 4.0, -0.6, 1.0, 26),
    (18.3, 3.5, -1.6, 0.2, 24),   # 9 low, close (landing)
    (19.3, 3.2, -1.5, 0.15, 24),
    (20.5, 2.6, -1.3, 0.25, 26),  # 10 slight push-in
]

def interp_keys(t):
    if t <= KEYS[0][0]: return KEYS[0][1:]
    for a, b in zip(KEYS, KEYS[1:]):
        if a[0] <= t <= b[0]:
            s = (t - a[0]) / (b[0] - a[0]); s = s * s * (3 - 2 * s)
            return tuple(x + (y - x) * s for x, y in zip(a[1:], b[1:]))
    return KEYS[-1][1:]

# heading = smoothed horizontal velocity (so the camera does not whip on every wobble)
head = []
hprev = Vector((1, 0, 0))
for i in range(n):
    h = Vector((V[i].x, V[i].y, 0))
    if h.length < 0.5: h = hprev
    h.normalize()
    hprev = (hprev * 0.92 + h * 0.08).normalized() if i else h
    head.append(hprev.copy())

# offset in the chase frame, smoothed on its own (no speed lag), added to Spidey's position 2 frames ago
offs = []
for i in range(n):
    b, s_, u, _ = interp_keys(F[i]["t"])
    fwd = head[i]; left = Vector((0, 0, 1)).cross(fwd).normalized()
    offs.append(-fwd * b + left * s_ + Vector((0, 0, u)))

# critically damped spring follow -> natural lag
def spring(seq, omega, dt=1 / fps):
    x = seq[0].copy(); v = Vector((0, 0, 0)); out = []
    for tgt in seq:
        a = omega * omega * (tgt - x) - 2 * omega * v
        v = v + a * dt; x = x + v * dt
        out.append(x.copy())
    return out

offs_s = spring(offs, 3.5)
cam_pos = [P[max(0, i - 1)] + offs_s[i] for i in range(n)]
# keep the lens away from the web lines (a 3.6 cm web 30 cm from the lens fills half the frame)
from mathutils.geometry import intersect_point_line
WEB_T = {k: (a["t0"], a["t1"]) for k, a in sim["anchors"].items()}
ANC = {k: Vector(a["pos"]) for k, a in sim["anchors"].items()}
for _ in range(2):
    push = [Vector((0, 0, 0)) for _ in range(n)]
    for i in range(n):
        t = F[i]["t"]
        for k, (t0, t1) in WEB_T.items():
            if t0 - 0.15 <= t <= t1 + 0.3:
                hand = P[i] + (ANC[k] - P[i]).normalized() * 0.9
                pt, fac = intersect_point_line(cam_pos[i], hand, ANC[k])
                fac = max(0.0, min(1.0, fac)); pt = hand.lerp(ANC[k], fac)
                d = cam_pos[i] - pt
                if d.length < 1.8:
                    push[i] += d.normalized() * (1.8 - d.length) if d.length > 1e-3 else Vector((0, 0, 1.8))
    push = spring(push, 6.0)
    cam_pos = [c + q for c, q in zip(cam_pos, push)]
for i, c in enumerate(cam_pos):         # keep it in the street and above the ground
    c.y = max(-8.4, min(8.4, c.y))
    c.z = max(0.45, c.z)
_raw = [P[i] + V[i] * (0.10 if F[i]['t'] < 17.6 else 0.02) for i in range(n)]
aim = [sum((_raw[max(0, min(n - 1, i + k))] for k in range(-3, 4)), Vector()) / 7 for i in range(n)]   # centred average: smooth, no lag

# camera path curve (his duplicate-the-path idea, here traced from the chase positions)
cu = bpy.data.curves.new("Camera Path", "CURVE"); cu.dimensions = "3D"
spl = cu.splines.new("POLY"); spl.points.add(n - 1)
for pt, q in zip(spl.points, cam_pos): pt.co = (q.x, q.y, q.z, 1)
path = bpy.data.objects.new("Camera Path", cu); path.show_in_front = True; anim.objects.link(path)
seg = [0.0]
for a, b in zip(cam_pos, cam_pos[1:]): seg.append(seg[-1] + (b - a).length)

camd = bpy.data.cameras.new("Camera")
camd.sensor_width = 36
camd.clip_start, camd.clip_end = 0.05, 3000
cam = bpy.data.objects.new("Camera", camd); anim.objects.link(cam)
sc.camera = cam
c = cam.constraints.new("FOLLOW_PATH"); c.target = path; c.use_fixed_location = True
cam.rotation_mode = "XYZ"
prev = None
for i in range(n):
    fr = i + 1
    c.offset_factor = seg[i] / seg[-1]; c.keyframe_insert("offset_factor", frame=fr)
    d = (aim[i] - cam_pos[i]).normalized()
    q = d.to_track_quat("-Z", "Y")
    e = q.to_euler("XYZ", prev) if prev else q.to_euler("XYZ"); prev = e
    cam.rotation_euler = e; cam.keyframe_insert("rotation_euler", frame=fr)
    camd.lens = interp_keys(F[i]["t"])[3]; camd.keyframe_insert("lens", frame=fr)
set_interp(cam, "LINEAR"); set_interp(camd, "LINEAR")
sc.frame_set(1)
save()
dmin = min((cam_pos[i] - P[i]).length for i in range(n))
print("camera path %.0f m, closest to Spidey %.1f m" % (seg[-1], dmin))
