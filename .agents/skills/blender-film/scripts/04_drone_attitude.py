# FPV drone flight, built from the same physics path (his path + empty method, new hero):
#  * position = swing sim (it is already smooth, physical and threads the street), start smoothed from rest,
#    ending replaced by a hard braking flare into a hover above the double yellow line
#  * attitude = how a real quad flies: thrust axis points along (acceleration + gravity), nose along the velocity
#  * where the path is ballistic (thrust ~ 0) the pilot "cuts throttle": nose follows the velocity, and we add the
#    freestyle tricks: power flip after the first dive, barrel roll on the slingshot climb, back flip at the top
#  * ending: hover, slow yaw round to stare at the camera
# Writes research/drone_path.json (per frame position/quaternion/thrust) and keys the "Drone Empty".
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
import json
from mathutils import Vector, Quaternion, Matrix
sc = bpy.context.scene
sim = json.load(open(os.path.join(ROOT, "research", "sim_shift.json")))
F = sim["frames"]; fps = sim["fps"]; HOLD = sim["hold"]
N = 545                       # sim has 492 frames; the hover is extended for the close-up
P = [Vector(F[min(i, 491)]["p"]) for i in range(N)]
T = [i / 24.0 for i in range(N)]
G = Vector((0, 0, 9.81))

def smooth(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def hermite(p0, v0, p1, v1, dur, s):
    s2, s3 = s * s, s * s * s
    return (2 * s3 - 3 * s2 + 1) * p0 + (s3 - 2 * s2 + s) * dur * v0 + (-2 * s3 + 3 * s2) * p1 + (s3 - s2) * dur * v1

# ---- start: sits on the parapet, props spin up, lifts and falls away (no instant jump) ----
SIT = Vector(F[0]["p"]) + Vector((0.0, 0.25, -0.30))         # on the stone coping, 0.12 m above it
i_go, i_join = HOLD + 1, HOLD + 9                             # take-off frame, frame it joins the sim path
p_join = P[i_join]; v_join = (P[i_join + 1] - P[i_join - 1]) * (fps / 2)
for i in range(0, i_go):
    P[i] = SIT.copy()
dur = (i_join - i_go) / fps
for i in range(i_go, i_join):
    s = (i - i_go) / (i_join - i_go)
    P[i] = hermite(SIT, Vector((2.0, 0.6, 1.2)), p_join, v_join, dur, s)

# ---- ending: braking flare into a hover ----
land_t = sim["landed"]
i_b = int(round((land_t - 0.62) * fps))                       # brake from here (late and hard)
v_b = (P[i_b + 1] - P[i_b - 1]) * (fps / 2)
i_h = int(round((land_t + 0.55) * fps))                       # settled in the hover
H = Vector((P[i_b].x + v_b.x * 0.45, -0.8, 1.35))
dur = (i_h - i_b) / fps
for i in range(i_b, i_h):
    P[i] = hermite(P[i_b], v_b, H, Vector((0, 0, 0)), dur, (i - i_b) / (i_h - i_b))
for i in range(i_h, N):
    tt = (i - i_h) / fps
    P[i] = H + Vector((0.05 * tt, 0.04 * math.sin(tt * 2.1), 0.05 * math.sin(tt * 3.3)))

# ---- kinematics ----
def deriv(seq):
    out = []
    for i in range(len(seq)):
        a, b = seq[max(0, i - 1)], seq[min(len(seq) - 1, i + 1)]
        out.append((b - a) * (fps / max(1, (min(len(seq) - 1, i + 1) - max(0, i - 1)))))
    return out
def blur(seq, r):
    out = []
    for i in range(len(seq)):
        acc = Vector((0, 0, 0)); wsum = 0
        for k in range(-r, r + 1):
            j = max(0, min(len(seq) - 1, i + k)); w = math.exp(-(k * k) / (2 * (r / 2 + 0.5) ** 2))
            acc += seq[j] * w; wsum += w
        out.append(acc / wsum)
    return out
V = blur(deriv(P), 2)
A = blur(deriv(V), 3)

def frame_q(up, fwd):
    """drone model: nose = +Y? decided by NOSE_AXIS below; build rotation with body up = up, body nose = fwd"""
    up = up.normalized()
    f = fwd - up * fwd.dot(up)
    if f.length < 1e-4: f = Vector((1, 0, 0)) - up * up.x
    f.normalize()
    side = f.cross(up)
    # columns: body X = side(right), body Y = nose, body Z = up
    return Matrix((side, f, up)).transposed().to_quaternion()

Q = []; THR = []
head_prev = Vector((1, 0, 0))
for i in range(N):
    thrust = A[i] + G
    hv = Vector((V[i].x, V[i].y, 0))
    head = hv.normalized() if hv.length > 0.6 else head_prev
    head_prev = head
    THR.append(thrust.length)
    q_thr = frame_q(thrust if thrust.length > 1e-3 else Vector((0, 0, 1)), head)
    # ballistic: nose follows the velocity (camera looks where it flies, classic dive)
    vel = V[i] if V[i].length > 1 else head
    vn = vel.normalized(); upf = Vector((0, 0, 1)) - vn * vn.z
    if upf.length < 1e-3: upf = -head
    q_free = frame_q(upf, vn)
    k = smooth((7.0 - thrust.length) / 4.0)                    # thrust < 3 m/s^2 -> fully "throttle cut"
    Q.append(q_thr.slerp(q_free, k))
for i in range(0, i_go):                                       # sitting flat on the parapet, nose down the avenue
    Q[i] = frame_q(Vector((0, 0, 1)), Vector((1, 0.12, 0)))

# smooth the attitude (pilots are smooth, sensors are not)
Qs = [Q[0]]
for i in range(1, N):
    q = Q[i]
    if q.dot(Qs[-1]) < 0: q = -q
    Qs.append(Qs[-1].slerp(q, 0.45))
Q = Qs

# ---- tricks (body-axis rotations layered on top) ----
def trick(t0, t1, axis, turns):
    i0, i1 = int(t0 * fps), int(t1 * fps)
    for i in range(i0, min(N, i1 + 1)):
        ang = 2 * math.pi * turns * smooth((i - i0) / max(1, i1 - i0))
        Q[i] = Q[i] @ Quaternion(axis, ang)
aw = sim["anchors"]
tA1 = aw["A"]["t1"]; tB0 = aw["B"]["t0"]; tD1 = aw["D"]["t1"]
trick(tA1 + 0.15, tB0 - 0.25, (1, 0, 0), -1)                    # power flip forward (nose over) between web A and B
trick(aw["D"]["t0"] + 0.35, tD1 - 0.05, (0, 1, 0), 1)           # barrel roll during the slingshot climb
trick(tD1 + 0.45, tD1 + 1.35, (1, 0, 0), 1)                     # back flip at the top
# ending: yaw round to look back at the camera
i_y0 = i_h + 18; i_y1 = min(N - 1, i_h + 52)      # slow turn to the lens during the close-up, then a held stare
for i in range(i_y0, N):
    s = smooth((i - i_y0) / max(1, i_y1 - i_y0))
    Q[i] = Quaternion((0, 0, 1), math.radians(165) * s) @ Q[i]

# ---- write + key the empty (his structure: path curve + empty on Follow Path) ----
anim = coll("ANIMATION")
for nm in ("Drone Path", "Drone Empty"):
    o = bpy.data.objects.get(nm)
    if o: bpy.data.objects.remove(o)
cu = bpy.data.curves.new("Drone Path", "CURVE"); cu.dimensions = "3D"
sp = cu.splines.new("POLY"); sp.points.add(N - 1)
for pt, q in zip(sp.points, P): pt.co = (q.x, q.y, q.z, 1)
path = bpy.data.objects.new("Drone Path", cu); path.show_in_front = True; anim.objects.link(path)
seg = [0.0]
for a_, b_ in zip(P, P[1:]): seg.append(seg[-1] + (b_ - a_).length)
emp = bpy.data.objects.new("Drone Empty", None); emp.empty_display_type = "ARROWS"; emp.empty_display_size = 0.3
anim.objects.link(emp)
c = emp.constraints.new("FOLLOW_PATH"); c.target = path; c.use_fixed_location = True
emp.rotation_mode = "QUATERNION"
for i in range(N):
    fr = i + 1
    # identical consecutive points (hover/sit) still need unique offsets: nudge by frame
    c.offset_factor = seg[i] / seg[-1]; c.keyframe_insert("offset_factor", frame=fr)
    emp.rotation_quaternion = Q[i]; emp.keyframe_insert("rotation_quaternion", frame=fr)
set_interp(emp, "LINEAR")
json.dump(dict(fps=fps, take_off=i_go + 1, hover=i_h + 1,
               frames=[dict(t=T[i], p=list(P[i]), v=list(V[i]), q=list(Q[i]), thrust=THR[i]) for i in range(N)]),
          open(os.path.join(ROOT, "research", "drone_path.json"), "w"))
sc.frame_set(1)
save()
print("drone path %.0f m, take-off f%d, hover f%d, max thrust %.1f g" % (seg[-1], i_go + 1, i_h + 1, max(THR) / 9.81))
