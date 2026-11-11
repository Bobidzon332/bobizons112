# Helpers loaded into the live bridge namespace: exec(open(LIB).read())
import bpy, os, math, mathutils
ROOT = os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film"))   # your project folder
SHOTS = os.path.join(ROOT, "shots")
ASSETS = os.path.join(ROOT, "assets_zip", "Assets")
SCENE_FILE = os.path.join(ROOT, "scene", "film.blend")


def win_area(kind="VIEW_3D"):
    w = bpy.context.window_manager.windows[0]
    for a in w.screen.areas:
        if a.type == kind:
            return w, a
    return w, None


def snap(name):
    """Screenshot of the whole Blender window -> shots/<name>.png"""
    w, a = win_area()
    path = os.path.join(SHOTS, name + ".png")
    with bpy.context.temp_override(window=w, area=a, screen=w.screen):
        bpy.ops.screen.screenshot(filepath=path)
    print("snap", path)
    return path


def save(path=SCENE_FILE):
    bpy.ops.wm.save_as_mainfile(filepath=path)
    print("saved", path)


def redraw():
    for w in bpy.context.window_manager.windows:
        for a in w.screen.areas:
            a.tag_redraw()


def view3d():
    w, a = win_area()
    return a.spaces.active if a else None


def look(loc, rot_euler_deg, dist, persp="PERSP"):
    """Point the main 3D viewport: pivot loc, view rotation (x,y,z deg), distance."""
    sp = view3d()
    r = sp.region_3d
    r.view_location = mathutils.Vector(loc)
    r.view_rotation = mathutils.Euler([math.radians(v) for v in rot_euler_deg]).to_quaternion()
    r.view_distance = dist
    r.view_perspective = persp
    redraw()


def top_view(center, dist):
    look(center, (0, 0, 0), dist, "ORTHO")


def shade(kind="SOLID"):
    view3d().shading.type = kind
    redraw()


def coll(name, parent=None):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


def fcurves(idblock):
    """F-curves of an ID's action (Blender 5 layered actions)."""
    ad = idblock.animation_data
    if not ad or not ad.action:
        return []
    from bpy_extras import anim_utils
    cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
    return list(cb.fcurves) if cb else []


def set_interp(idblock, kind="LINEAR", data_path_prefix=""):
    for fc in fcurves(idblock):
        if fc.data_path.startswith(data_path_prefix):
            for kp in fc.keyframe_points:
                kp.interpolation = kind


def follow_view(obj_name="Spider-Man Empty", frame=None, dist=9.0, rot=(70, 0, 30), persp="PERSP"):
    sc = bpy.context.scene
    if frame is not None:
        sc.frame_set(frame)
    o = bpy.data.objects[obj_name]
    look(o.matrix_world.translation, rot, dist, persp)
