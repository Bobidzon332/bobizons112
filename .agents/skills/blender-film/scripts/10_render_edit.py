# Render the 10 s edit (only the good parts): shots = camera + frame range, numbered continuously.
# blender -b spidey.blend --python render_edit.py -- <outdir> <width> <spp> [blur 0/1]
import bpy, sys, os, time, json
a = sys.argv[sys.argv.index("--") + 1:]
out, wpx, spp = a[0], int(a[1]), int(a[2]); blur = (a[3] == "1") if len(a) > 3 else True
SHOTS = [("CAM_ROOF", 2, 22), ("Camera", 23, 62), ("Camera", 145, 180), ("Camera", 300, 372), ("CAM_LOW", 438, 462), ("CAM_HERO", 476, 525)]
ONLY = os.environ.get("ONLY_CAM")
if ONLY: SHOTS = [s for s in SHOTS if s[0] == ONLY]
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = wpx, int(wpx * 9 / 16), 100
cy = sc.cycles; cy.samples = spp; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05 if spp < 32 else 0.02
cy.use_denoising = True
sc.render.use_motion_blur = blur
sc.render.use_persistent_data = True
sc.render.image_settings.file_format = "JPEG" if wpx < 1500 else "PNG"; sc.render.image_settings.quality = 90
for n in ("Spider-Man Path", "Camera Path", "Spider-Man Empty", "Drone Path"):
    o = bpy.data.objects.get(n)
    if o: o.hide_render = True
k = 0
TOTAL = sum(f1 - f0 + 1 for _, f0, f1 in SHOTS)
STATUS = os.path.join(os.path.dirname(out.rstrip("/\\")), "status.json")
LABEL = {"CAM_ROOF": "rooftop take-off", "Camera": "chase", "CAM_LOW": "street-level dive", "CAM_HERO": "hover close-up"}
times = []; last = None
def status(done, cur):
    json.dump(dict(job=f"10 s video, {wpx}x{int(wpx * 9 / 16)}", total=TOTAL, done=done, current=cur, last=last,
                   avg=(sum(times[-12:]) / len(times[-12:])) if times else None, t=time.time()), open(STATUS, "w"))
for cam, f0, f1 in SHOTS:
    sc.camera = bpy.data.objects[cam]
    for f in range(f0, f1 + 1):
        k += 1
        path = os.path.join(out, f"e_{k:04d}" + (".jpg" if wpx < 1500 else ".png"))
        if os.path.exists(path):
            last = path; continue
        status(k - 1, f"frame {k}/{TOTAL}  {LABEL.get(cam, cam)}")
        sc.frame_set(f)
        sc.render.filepath = path
        t0 = time.time(); bpy.ops.render.render(write_still=True); times.append(time.time() - t0); last = path
        print("FRAME", k, cam, f, flush=True)
status(k, "finished")
print("EDIT DONE", k)
