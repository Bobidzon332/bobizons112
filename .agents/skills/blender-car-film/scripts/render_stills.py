import bpy, os, time
sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.render.use_overwrite = True
out = os.path.expanduser("~/blender-car-film/stills"); os.makedirs(out, exist_ok=True)
for f, name in [(36, "1_wide"), (100, "2_headlight"), (140, "3_wheel"), (230, "4_track"), (300, "5_inside"), (430, "6_house")]:
    sc.frame_set(f); t = time.time()
    sc.render.filepath = os.path.join(out, f"{name}_f{f}.png")
    bpy.ops.render.render(write_still=True)
    print(f"STILL {name} frame {f} {time.time() - t:.1f}s", flush=True)
