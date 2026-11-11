"""Shared measurements and builders for CH_StarPlatinum phase scripts.

Units metres, Z up, subject faces -Y, origin at ground centre. The character's RIGHT side is -X.
Every constant is read from asset-brief.md (front panel 0.002665 m/px, side panel 0.002685 m/px,
side axis column 88) or marked '# inferred'. Entries are written for the right side and mirrored.
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix, Quaternion

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import bt  # vendored copy of blender-image-to-3d/assets/build_template.py

ASSET = "CH_StarPlatinum"
ROOT = os.path.dirname(HERE)
MASTER = os.path.join(ROOT, ASSET + "_master.blend")
META_K = 0.5714  # visible radius of a lone metaball element / its radius (stiffness 2, threshold 0.6), measured


def setup(phase):
    bt.PHASE = phase
    bt.OWNER_TAG = "phase:" + phase


def args():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--master", default=MASTER)
    return p.parse_args(bt.argv_after_dashes())


def mx(p):
    return (-p[0], p[1], p[2])


def V(*a):
    return Vector(a if len(a) == 3 else a[0])


def quat_x_to(d):
    return Vector((1, 0, 0)).rotation_difference(Vector(d).normalized())


def quat_z_to(d):
    return Vector((0, 0, 1)).rotation_difference(Vector(d).normalized())


def name(part, suffix):
    return f"{ASSET}_{part}_{suffix}"


# ---------------------------------------------------------------------------------------------
# METABALL ANATOMY (HIGH body). Each entry: visible half extents in metres.
# ---------------------------------------------------------------------------------------------

class Meta:
    def __init__(self, nm, res):
        self.mb = bpy.data.metaballs.new(nm)
        self.mb.resolution = res
        self.mb.render_resolution = res
        self.mb.threshold = 0.6
        self.ob = bpy.data.objects.new(nm, self.mb)
        bt.col("HIGH").objects.link(self.ob)
        bt.own(self.ob)

    def _el(self, typ, c, rad, sizes, rot, stiff, neg):
        e = self.mb.elements.new(type=typ)
        e.co = c
        e.radius = rad
        e.size_x, e.size_y, e.size_z = sizes
        e.rotation = rot
        e.stiffness = stiff
        e.use_negative = neg
        return e

    def ell(self, c, h, rot=None, stiff=2.0, neg=False, sym=True):
        """Ellipsoid with visible half extents h at centre c. rot: Quaternion."""
        hm = max(h)
        rad = hm / META_K
        sizes = tuple(x / hm for x in h)
        q = rot or Quaternion()
        self._el("ELLIPSOID", c, rad, sizes, q, stiff, neg)
        if sym and abs(c[0]) > 1e-6:
            qm = Quaternion((q.w, q.x, -q.y, -q.z))  # mirror across YZ plane
            self._el("ELLIPSOID", mx(c), rad, sizes, qm, stiff, neg)

    def cap(self, a, b, r, stiff=2.0, sym=True, neg=False):
        """Capsule from a to b with visible radius r."""
        a, b = Vector(a), Vector(b)
        c = (a + b) / 2
        half = (b - a).length / 2
        q = quat_x_to(b - a)
        self._el("CAPSULE", c, r / META_K, (half, 1, 1), q, stiff, neg)
        if sym and abs(c[0]) > 1e-6:
            qm = quat_x_to(Vector(mx(b)) - Vector(mx(a)))
            self._el("CAPSULE", Vector(mx(c)), r / META_K, (half, 1, 1), qm, stiff, neg)

    def to_mesh(self, nm, collection="HIGH"):
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        ev = self.ob.evaluated_get(dg)
        me = bpy.data.meshes.new_from_object(ev)
        me.name = nm
        ob = bpy.data.objects.new(nm, me)
        bt.col(collection).objects.link(ob)
        bt.own(ob)
        mb = self.ob.data
        bpy.data.objects.remove(self.ob, do_unlink=True)
        bpy.data.metaballs.remove(mb)
        return ob


def body_anatomy(m, detail, arms=None):
    """Fill a Meta with the body. detail=False -> silhouette masses only (blockout).
    Values corrected against review/02_blockout world_gate rows (front and side)."""
    # torso core: chest front -0.148 / back +0.11 (side 22%), half width 0.176 (front 22%),
    # 0.155 (26%), 0.116 (30%); belt front -0.113 (side 34%)
    m.ell((0, 0.008, 1.262), (0.112, 0.098, 0.085))          # pelvis, crotch ~1.19
    m.ell((0, -0.006, 1.415), (0.090, 0.092, 0.080))         # waist P6 (front 32%: +-0.10)
    m.ell((0, -0.018, 1.585), (0.135, 0.122, 0.128))         # rib cage
    m.ell((0, 0.018, 1.690), (0.140, 0.085, 0.052))          # shoulder girdle / upper back
    m.ell((-0.104, 0.030, 1.585), (0.045, 0.068, 0.085),
          rot=Quaternion((0, 1, 0), math.radians(10)))        # latissimus (front 22-26% width)
    m.ell((-0.074, -0.090, 1.630), (0.078, 0.048, 0.060),
          rot=Quaternion((0, 1, 0), math.radians(-12)))       # pectoralis (side 22% front)
    m.ell((-0.080, -0.050, 1.480), (0.032, 0.058, 0.065))    # obliques / serratus (front 30%)
    m.ell((-0.105, 0.000, 1.335), (0.050, 0.075, 0.050))     # iliac crest / hip (front 36%: +-0.15)
    m.ell((-0.068, 0.072, 1.215), (0.068, 0.058, 0.075))     # gluteus
    m.cap((0, 0.012, 1.71), (0, -0.002, 1.83), 0.050, sym=False)  # neck
    # head (P1 crown 1.96, P3 chin 1.80, P13 face width 0.12)
    m.ell((0, 0.004, 1.893), (0.064, 0.080, 0.072))          # cranium
    m.ell((0, -0.030, 1.842), (0.050, 0.050, 0.045))         # face / jaw mass
    A = arms or m   # separate metaball family keeps the arms from webbing into the lats
    # arms hang behind the torso line (side 22-46%): shoulder y +0.035, elbow +0.085, fist +0.045
    A.ell((-0.216, 0.045, 1.668), (0.062, 0.072, 0.068))     # deltoid (front 20-25%: armpit gap at x 0.18)
    A.cap((-0.228, 0.065, 1.650), (-0.262, 0.100, 1.468), 0.050)   # upper arm (side 24%: back +0.158)
    A.cap((-0.266, 0.098, 1.455), (-0.290, 0.072, 1.268), 0.042)   # forearm
    A.cap((-0.288, 0.072, 1.268), (-0.296, 0.062, 1.238), 0.034)   # wrist
    A.ell((-0.300, 0.045, 1.148), (0.046, 0.052, 0.072))     # fist core (front 42-48%: z 1.07-1.25)
    # legs: thigh centre -0.1375 @0.967, -0.144 @0.882 (front); thigh front -0.11 (side 58%)
    m.cap((-0.092, 0.006, 1.250), (-0.138, -0.030, 0.960), 0.080)  # upper thigh
    m.ell((-0.148, -0.066, 1.070), (0.060, 0.066, 0.125))    # quadriceps mass (front 54%, side 54%)
    m.cap((-0.138, -0.030, 0.960), (-0.160, -0.018, 0.840), 0.062)  # lower thigh
    m.cap((-0.162, -0.010, 0.830), (-0.262, 0.050, 0.140), 0.050)   # shin core (side 64%: depth 0.158)
    m.ell((-0.195, 0.060, 0.700), (0.050, 0.055, 0.110))     # calf
    m.ell((-0.128, 0.052, 1.090), (0.054, 0.052, 0.120))     # hamstrings (side 44-52%: back +0.107)
    m.ell((-0.170, -0.028, 0.765), (0.046, 0.052, 0.060))    # upper shin (side 64%: front -0.086)
    m.cap((-0.264, 0.048, 0.110), (-0.300, -0.120, 0.040), 0.038)   # foot (inside boot)
    if not detail:
        return
    for z in (1.535, 1.478, 1.421):                            # rectus abdominis rows (side 30% -0.126)
        m.ell((-0.031, -0.100, z), (0.029, 0.020, 0.025))
    m.ell((0, -0.105, 1.39), (0.040, 0.016, 0.03), sym=False)  # lower abdomen
    m.ell((-0.072, 0.034, 1.712), (0.070, 0.048, 0.036))     # trapezius
    m.ell((-0.040, 0.080, 1.43), (0.032, 0.028, 0.115))      # spinal erectors
    m.ell((0, 0.088, 1.50), (0.012, 0.03, 0.15), neg=True, stiff=1.0, sym=False)   # spine furrow
    m.ell((0, -0.122, 1.48), (0.008, 0.02, 0.10), neg=True, stiff=1.0, sym=False)  # linea alba
    # neck and face details
    m.cap((-0.030, -0.020, 1.80), (-0.012, -0.045, 1.74), 0.016)   # sternocleidomastoid
    m.ell((0, -0.060, 1.808), (0.022, 0.020, 0.018), sym=False)   # chin
    m.ell((0, -0.086, 1.857), (0.008, 0.012, 0.018), sym=False)   # nose
    m.ell((0, -0.068, 1.884), (0.050, 0.015, 0.012), sym=False)   # brow ridge
    m.ell((-0.040, -0.046, 1.860), (0.018, 0.020, 0.015))         # cheekbone
    m.ell((-0.064, 0.002, 1.864), (0.008, 0.016, 0.022))          # ear
    m.ell((-0.042, -0.040, 1.818), (0.020, 0.030, 0.020))         # jaw angle
    # arm musculature
    A.ell((-0.246, 0.022, 1.565), (0.040, 0.038, 0.062))     # biceps
    A.ell((-0.248, 0.118, 1.575), (0.040, 0.040, 0.075))     # triceps (side 22-24%: back +0.16)
    A.ell((-0.272, 0.074, 1.405), (0.044, 0.046, 0.058))     # forearm flexors (front 32%: elbow centre -0.277)
    # fist: curled fingers across the front, thumb over them (inferred inside glove)
    for i, z in enumerate((1.203, 1.168, 1.133, 1.098)):
        A.cap((-0.326, 0.000, z), (-0.280, 0.000, z), 0.0165 - 0.001 * i)
    A.cap((-0.268, -0.004, 1.193), (-0.300, -0.020, 1.158), 0.015)  # thumb
    # leg musculature
    m.ell((-0.175, -0.012, 1.075), (0.050, 0.058, 0.120))    # vastus lateralis
    m.ell((-0.120, -0.040, 0.925), (0.040, 0.040, 0.050))    # vastus medialis

    m.ell((-0.084, -0.004, 1.150), (0.042, 0.055, 0.075))    # adductors
    m.ell((-0.160, -0.030, 0.835), (0.048, 0.046, 0.044))    # knee



# ---------------------------------------------------------------------------------------------
# GENERIC GEOMETRY HELPERS
# ---------------------------------------------------------------------------------------------

def _frame(t, up=Vector((0, 0, 1))):
    t = t.normalized()
    ref = up if abs(t.dot(up)) < 0.95 else Vector((1, 0, 0))
    b = t.cross(ref).normalized()
    n = b.cross(t).normalized()
    return n, b


def sweep(nm, centers, profile, closed_path=True, collection="LOW", scales=None, cap=True, smooth=True):
    """Sweep a closed 2D profile [(u, v)] along a path of centres. u runs along the path normal
    (world-up for horizontal rings), v along the binormal (radial for rings).
    scales: per-centre (su, sv) multipliers."""
    bm = bmesh.new()
    rings = []
    n = len(centers)
    for i, c in enumerate(centers):
        c = Vector(c)
        if closed_path:
            t = Vector(centers[(i + 1) % n]) - Vector(centers[(i - 1) % n])
        else:
            t = Vector(centers[min(i + 1, n - 1)]) - Vector(centers[max(i - 1, 0)])
        nn, bb = _frame(t)
        su, sv = scales[i] if scales else (1, 1)
        rings.append([bm.verts.new(c + nn * (u * su) + bb * (v * sv)) for (u, v) in profile])
    m = len(profile)
    pairs = list(zip(rings, rings[1:])) + ([(rings[-1], rings[0])] if closed_path else [])
    for ra, rb in pairs:
        for j in range(m):
            bm.faces.new((ra[j], ra[(j + 1) % m], rb[(j + 1) % m], rb[j]))
    if cap and not closed_path:
        bm.faces.new(list(reversed(rings[0])))
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = bt.new_mesh_object(nm, bm, collection)
    if smooth:
        bt.shade_smooth(ob, math.radians(40))
    return ob


def ellipse_path(c, rx, ry, steps, z_fn=None, start=-math.pi / 2):
    pts = []
    for i in range(steps):
        a = start + 2 * math.pi * i / steps
        z = c[2] + (z_fn(a) if z_fn else 0)
        pts.append((c[0] + rx * math.cos(a), c[1] + ry * math.sin(a), z))
    return pts


def rect_profile(h, t, bevel=0.3):
    """Closed rounded-rectangle profile, h tall (u) and t thick (v), 8 points."""
    hu, hv, k = h / 2, t / 2, bevel
    return [(hu, hv * (1 - k)), (hu * (1 - k), hv), (-hu * (1 - k), hv), (-hu, hv * (1 - k)),
            (-hu, -hv * (1 - k)), (-hu * (1 - k), -hv), (hu * (1 - k), -hv), (hu, -hv * (1 - k))]


def circle_profile(r, n=8):
    return [(r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def lathe_along(nm, profile, a, b, segments=16, ellip=(1.0, 1.0), collection="LOW", cap=True, twist=0.0):
    """Revolve profile [(r, f)] or [(rx, ry, f)] (f = 0..1 from a to b) around the axis a->b; ellip
    scales the section on the local X (world-X-ish) and Y (world-Y-ish) axes."""
    a, b = Vector(a), Vector(b)
    L = (b - a).length
    bm = bmesh.new()
    rings = []
    for entry in profile:
        if len(entry) == 3:
            rx, ry, f = entry
        else:
            rx = ry = entry[0]
            f = entry[1]
        ring = []
        for s in range(segments):
            ang = 2 * math.pi * s / segments + twist
            ring.append(bm.verts.new((rx * ellip[0] * math.cos(ang), ry * ellip[1] * math.sin(ang), f * L)))
        rings.append(ring)
    for ra, rb in zip(rings, rings[1:]):
        for j in range(segments):
            bm.faces.new((ra[j], ra[(j + 1) % segments], rb[(j + 1) % segments], rb[j]))
    if cap:
        bm.faces.new(list(reversed(rings[0])))
        bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # orient: local Z -> a->b, keep local X roughly world X
    q = quat_z_to(b - a)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=q.to_matrix(), verts=bm.verts)
    bmesh.ops.translate(bm, vec=a, verts=bm.verts)
    ob = bt.new_mesh_object(nm, bm, collection)
    bt.shade_smooth(ob, math.radians(40))
    return ob


def dome(nm, c, normal, r, h, segments=16, rings=5, rim=0.0, collection="LOW"):
    """Shallow spherical cap of radius r and height h facing `normal`, with an optional flat rim width."""
    bm = bmesh.new()
    R = (r * r + h * h) / (2 * h)
    a0 = math.asin(min(1.0, r / R))
    top = bm.verts.new((0, 0, h))
    prev = None
    verts_rings = []
    for k in range(1, rings + 1):
        a = a0 * k / rings
        rr, zz = R * math.sin(a), h - R * (1 - math.cos(a))
        verts_rings.append([bm.verts.new((rr * math.cos(2 * math.pi * s / segments),
                                          rr * math.sin(2 * math.pi * s / segments), zz)) for s in range(segments)])
    if rim > 0:
        verts_rings.append([bm.verts.new(((r + rim) * math.cos(2 * math.pi * s / segments),
                                          (r + rim) * math.sin(2 * math.pi * s / segments), 0)) for s in range(segments)])
    base = [bm.verts.new((v.co.x, v.co.y, -h * 0.35)) for v in verts_rings[-1]]
    verts_rings.append(base)
    first = verts_rings[0]
    for s in range(segments):
        bm.faces.new((top, first[s], first[(s + 1) % segments]))
    for ra, rb in zip(verts_rings, verts_rings[1:]):
        for s in range(segments):
            bm.faces.new((ra[s], rb[s], rb[(s + 1) % segments], ra[(s + 1) % segments]))
    bm.faces.new(list(reversed(base)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    q = quat_z_to(normal)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=q.to_matrix(), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(c), verts=bm.verts)
    ob = bt.new_mesh_object(nm, bm, collection)
    bt.shade_smooth(ob, math.radians(50))
    return ob


def rounded_tray(nm, center, size, bevel_w, segs, thickness, collection="LOW", open_faces=("-Z",)):
    """Box with bevelled edges, the named faces removed, solidified inward (a shell)."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel_w, segments=segs, profile=0.5,
                    affect="EDGES", clamp_overlap=True)
    axes = {"-Z": Vector((0, 0, -1)), "+Z": Vector((0, 0, 1)), "-X": Vector((-1, 0, 0)),
            "+X": Vector((1, 0, 0)), "-Y": Vector((0, -1, 0)), "+Y": Vector((0, 1, 0))}
    bm.normal_update()
    dead = [f for f in bm.faces if any(f.normal.dot(axes[o]) > 0.999 for o in open_faces)]
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    ob = bt.new_mesh_object(nm, bm, collection, location=center)
    s = ob.modifiers.new("Solidify", "SOLIDIFY")
    s.thickness = thickness
    s.offset = -1.0
    s.use_rim = True
    s.use_even_offset = True
    bt.shade_smooth(ob, math.radians(35))
    return ob


def apply_mods(ob):
    bt.apply_all_modifiers(ob)
    return ob


def remove_object(ob):
    data = ob.data
    bpy.data.objects.remove(ob, do_unlink=True)
    if data is not None and getattr(data, "users", 1) == 0:
        if isinstance(data, bpy.types.Mesh):
            bpy.data.meshes.remove(data)
        elif isinstance(data, bpy.types.Curve):
            bpy.data.curves.remove(data)


def join_remove(nm, objects, collection="LOW"):
    """bt.join_meshes, then delete the sources so the scene holds only the merged object."""
    new = bt.join_meshes(nm, objects, collection)
    for o in objects:
        remove_object(o)
    new.name = nm
    new.data.name = nm
    return new


def fuse_meshes(nm, objects, voxel, band=0.012, iters=10, collection="HIGH"):
    """Union overlapping closed meshes with a voxel remesh, then smooth only the vertices within `band`
    of two different sources (the intersection crease)."""
    from mathutils.bvhtree import BVHTree
    dg = bpy.context.evaluated_depsgraph_get()
    trees = [BVHTree.FromObject(o, dg) for o in objects]
    ob = join_remove(nm, objects, collection)
    r = ob.modifiers.new("Remesh", "REMESH")
    r.mode = "VOXEL"
    r.voxel_size = voxel
    r.use_smooth_shade = True
    apply_mods(ob)
    vg = ob.vertex_groups.new(name="fuse_band")
    for v in ob.data.vertices:
        d = sorted((t.find_nearest(v.co)[3] or 1.0) for t in trees)
        if len(d) > 1 and d[1] < band:
            vg.add([v.index], 1.0 - d[1] / band, "REPLACE")
    s = ob.modifiers.new("Smooth", "SMOOTH")
    s.factor = 0.8
    s.iterations = iters
    s.vertex_group = "fuse_band"
    apply_mods(ob)
    g = ob.vertex_groups.get("fuse_band")
    if g is not None:
        ob.vertex_groups.remove(g)
    return ob


def mirror_copy(ob, nm):
    """Real mirrored duplicate across the YZ plane (geometry flipped, normals fixed)."""
    me = ob.data.copy()
    me.name = nm
    bm = bmesh.new()
    bm.from_mesh(me)
    for v in bm.verts:
        v.co = ob.matrix_world @ v.co
        v.co.x = -v.co.x
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    o2 = bpy.data.objects.new(nm, me)
    for c in ob.users_collection:
        c.objects.link(o2)
    bt.own(o2)
    return o2
