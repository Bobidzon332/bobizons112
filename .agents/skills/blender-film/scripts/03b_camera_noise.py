# His randomized noise: camera = slow sway + micro shake (two Noise modifiers per rotation channel); Spidey empty = subtle wobble.
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
cam = bpy.data.objects["Camera"]
for fc in fcurves(cam):
    if fc.data_path == "rotation_euler":
        for m in list(fc.modifiers): fc.modifiers.remove(m)
        a = fc.modifiers.new("NOISE"); a.scale = 26; a.strength = math.radians(1.2); a.phase = fc.array_index * 7.3; a.offset = fc.array_index * 41
        b = fc.modifiers.new("NOISE"); b.scale = 2.2; b.strength = math.radians(0.22); b.phase = fc.array_index * 3.1 + 11; b.offset = fc.array_index * 13
emp = bpy.data.objects["Spider-Man Empty"]
for fc in fcurves(emp):
    if fc.data_path == "rotation_euler":
        for m in list(fc.modifiers): fc.modifiers.remove(m)
        a = fc.modifiers.new("NOISE"); a.scale = 14; a.strength = math.radians(4.0); a.phase = fc.array_index * 5.7 + 2; a.offset = fc.array_index * 29
        a.use_restricted_range = True; a.frame_start = 12; a.frame_end = 444; a.blend_in = 8; a.blend_out = 10
cam.data.dof.use_dof = True; cam.data.dof.focus_object = emp; cam.data.dof.aperture_fstop = 2.8
save()
