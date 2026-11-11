# His Part 2 method, driven by the physics sim:
#  - "Spider-Man Path" curve through the swing (ANIMATION collection, In Front)
#  - "Spider-Man Empty" with Follow Path; offset keyed per frame from the sim (physical speed, not linear)
#  - rig parented to the empty at the centre-of-gravity bone (torso), Keep Transform
#  - empty ROTATION = whole-body momentum: hangs along the web while swinging, keeps turning in free flight,
#    front flip after web A, tucked back flip at the top of the slingshot, dive, flip feet-down for the landing
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
import json
from mathutils import Vector, Matrix, Quaternion
sim = json.load(open(os.path.join(ROOT, "research", "sim_shift.json")))
HOLD = sim.get("hold", 0)
F = sim["frames"]
A = {k: Vector(v["pos"]) for k, v in sim["anchors"].items()}
WEBS = {w["id"]: w for w in sim["webs"]}
sc = bpy.context.scene
anim = coll("ANIMATION")
for n in ("Spider-Man Path", "Spider-Man Empty"):
    o = bpy.data.objects.get(n)
    if o: bpy.data.objects.remove(o)

# ---------- path ----------
pts = [Vector(f["p"]) for f in F]
cu = bpy.data.curves.new("Spider-Man Path", "CURVE")
cu.dimensions = "3D"
sp = cu.splines.new("POLY")
sp.points.add(len(pts) - 1)
for p_, q in zip(sp.points, pts):
    p_.co = (q.x, q.y, q.z, 1)
cu.path_duration = sc.frame_end
path = bpy.data.objects.new("Spider-Man Path", cu)
path.show_in_front = True
anim.objects.link(path)
seg = [0.0]
for a, b in zip(pts, pts[1:]):
    seg.append(seg[-1] + (b - a).length)
total = seg[-1]

# ---------- empty + follow path ----------
emp = bpy.data.objects.new("Spider-Man Empty", None)
emp.empty_display_type = "PLAIN_AXES"
emp.empty_display_size = 0.8
anim.objects.link(emp)
c = emp.constraints.new("FOLLOW_PATH")
c.target = path
c.use_fixed_location = True
c.use_curve_follow = False
for i in range(len(F)):
    fr = i + 1
    c.offset_factor = seg[i] / total
    c.keyframe_insert("offset_factor", frame=fr)

# ---------- momentum rotation ----------
def basis(up, fwd):
    """rig rest: faces -Y, head +Z.  Returns quaternion that maps rig axes onto (fwd, up)."""
    up = up.normalized()
    fwd = (fwd - up * fwd.dot(up))
    if fwd.length < 1e-4:
        fwd = Vector((1, 0, 0)) - up * up.x
    fwd.normalize()
    y = -fwd
    x = y.cross(up).normalized()
    m = Matrix((x, y, up)).transposed()
    return m.to_quaternion()

def on_web(t):
    return [w for w in WEBS.values() if w["t0"] <= t < w["t1"]]

def web_q(i):
    t = F[i]["t"]; p = Vector(F[i]["p"]); v = Vector(F[i]["v"])
    ws = on_web(t)
    anc = sum((A[w["id"]] for w in ws), Vector()) / len(ws)
    up = anc - p
    return basis(up, v)

def smooth(x):
    x = min(1, max(0, x)); return x * x * (3 - 2 * x)

def rot_local_x(q, ang):
    return q @ Quaternion((1, 0, 0), ang)

n = len(F)
Q = [None] * n
fps = sim["fps"]
for i in range(n):
    if on_web(F[i]["t"]):
        Q[i] = web_q(i)
# free-flight gaps: blend from the last web pose to the next one (or to the landing pose), plus flips
landed = sim["landed"]
i = 0
segments = []
while i < n:
    if Q[i] is None:
        j = i
        while j < n and Q[j] is None:
            j += 1
        segments.append((i, j))
        i = j
    else:
        i += 1
land_i = int(round(landed * fps))
for (i0, i1) in segments:
    t0 = F[i0]["t"]
    if i0 == 0:                      # opening jump: crouched-on-ledge pose (upright, leaning forward) -> first web pose
        qa = basis(Vector((0.0, 0.3, 1.0)), Vector((1, 0.15, 0)))
        qb = Q[i1]
        for k in range(i0, i1):
            Q[k] = qa.slerp(qb, smooth(max(0, k - i0 - HOLD - 4) / max(1, i1 - i0 - HOLD - 4)))
        continue
    qa = Q[i0 - 1]
    if i1 < n:                        # between two webs
        qb = Q[i1]
        for k in range(i0, i1):
            s = (k - i0) / max(1, i1 - i0)
            Q[k] = qa.slerp(qb, smooth(s))
        if abs(t0 - WEBS["A"]["t1"]) < 0.05:          # front flip after web A (head goes forward and down)
            fa, fb = i0 + 3, i1 - 4
            for k in range(fa, fb):
                Q[k] = rot_local_x(Q[k], -2 * math.pi * smooth((k - fa) / (fb - fa)))
    else:                             # last flight: slingshot release -> back flip -> dive -> feet down -> landing
        v_land = Vector(F[min(n - 1, land_i - 1)]["v"])
        q_dive = basis(Vector(F[land_i - 20]["v"]).normalized(), Vector((0, 0, -1)))   # head first, chest to the street
        q_land = basis(Vector((0, 0, 1)), Vector((v_land.x, v_land.y, 0)))
        keys = [(t0, qa), (t0 + 0.35, qa), (landed - 2.66, q_dive), (landed - 1.01, q_dive), (landed - 0.12, q_land)]
        for k in range(i0, n):
            t = F[k]["t"]
            if t >= keys[-1][0]:
                Q[k] = q_land; continue
            for (ta, qa_), (tb, qb_) in zip(keys, keys[1:]):
                if ta <= t < tb:
                    Q[k] = qa_.slerp(qb_, smooth((t - ta) / (tb - ta))); break
        bf0, bf1 = int((t0 + 0.45) * fps), int((t0 + 1.75) * fps)            # tucked back flip at the top
        for k in range(bf0, bf1):
            Q[k] = rot_local_x(Q[k], 2 * math.pi * smooth((k - bf0) / (bf1 - bf0)))
        break

emp.rotation_mode = "XYZ"
prev = None
for i in range(n):
    e = Q[i].to_euler("XYZ", prev) if prev else Q[i].to_euler("XYZ")
    prev = e
    emp.rotation_euler = e
    emp.keyframe_insert("rotation_euler", frame=i + 1)
set_interp(emp, "LINEAR")

# ---------- parent the rig at the centre of gravity (his Shift+S cursor-to-selected, Keep Transform) ----------
rig = bpy.data.objects["SPIDER-MAN"]
RIG_SCALE = 0.2653                                  # the rig's own object scale in his file
rig.parent = None
rig.matrix_world = Matrix.Diagonal((RIG_SCALE, RIG_SCALE, RIG_SCALE, 1.0))
bpy.context.view_layer.update()
torso_head = rig.matrix_world @ rig.pose.bones["torso"].head      # (0, 0.035, 1.036) m
rig.parent = emp
rig.matrix_parent_inverse = Matrix.Translation(-torso_head)
rig.location = (0, 0, 0)
rig.rotation_euler = (0, 0, 0)
rig.scale = (RIG_SCALE,) * 3
sc.frame_set(1)
save()
print("path length %.1f m, frames %d, torso head %s" % (total, n, tuple(round(v, 2) for v in torso_head)))
