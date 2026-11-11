import bpy
sc = bpy.context.scene
if sc.render.fps != 30:
    sc.render.fps = 30; sc.render.fps_base = 1.0
    sc.render.frame_map_old = 24; sc.render.frame_map_new = 30   # stretch timing so 20 s stays 20 s
    sc.frame_end = 600
    pass  # markers stay in 24 fps frame space (frame_map remaps them)
sc.cycles.samples = 30; sc.cycles.adaptive_min_samples = 12
print("fps", sc.render.fps, "frames", sc.frame_end, "markers", [(m.name, m.frame) for m in sc.timeline_markers], "samples", sc.cycles.samples)
