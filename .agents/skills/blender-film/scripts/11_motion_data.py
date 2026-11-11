# Per edit frame: active camera, drone distance / radial speed / bearing, throttle, drone + camera speed,
# nearest moving cars (distance, radial speed), street lamps nearby. -> audio/motion.json
import os
exec(open(os.path.join(os.environ.get("FILM_ROOT", os.path.expanduser("~/blender-film")), "tools", "lib.py")).read())
import json
from mathutils import Vector
SHOTS = [("CAM_ROOF", 2, 22), ("Camera", 23, 62), ("Camera", 145, 180), ("Camera", 300, 372), ("CAM_LOW", 438, 462), ("CAM_HERO", 476, 525)]
sc = bpy.context.scene
dp = json.load(open(os.path.join(ROOT, "research", "drone_path.json")))
emp = bpy.data.objects["Drone Empty"]
cars = [o for o in bpy.data.collections["STREET"].objects if o.name.startswith(("moving", "stopped", "cross"))]
out = []
k = 0
for si, (cn, f0, f1) in enumerate(SHOTS):
    cam = bpy.data.objects[cn]
    prev = None
    for f in range(f0 - 1, f1 + 1):
        sc.frame_set(f)
        c = cam.matrix_world.translation.copy()
        fwd = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
        right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
        d = emp.matrix_world.translation.copy()
        carp = [(o.name, o.matrix_world.translation.copy()) for o in cars]
        cur = dict(c=c, d=d, cars=carp)
        if f >= f0 and prev is not None:
            k += 1
            rel = d - c; dist = rel.length
            prel = prev["d"] - prev["c"]
            radial = (dist - prel.length) * 24.0                     # + = moving away
            pan = max(-1.0, min(1.0, rel.normalized().dot(right)))
            front = rel.normalized().dot(fwd)
            camspd = (c - prev["c"]).length * 24.0
            dspd = (d - prev["d"]).length * 24.0
            thr = dp["frames"][min(len(dp["frames"]) - 1, f - 1)]["thrust"] / 9.81
            near = []
            for (nm, p), (_, pp) in zip(carp, prev["cars"]):
                r = (p - c); dd = r.length
                if dd < 60:
                    near.append(dict(name=nm, dist=round(dd, 2), radial=round((dd - (pp - prev["c"]).length) * 24.0, 2),
                                     speed=round((p - pp).length * 24.0, 2), pan=round(max(-1, min(1, r.normalized().dot(right))), 2)))
            near.sort(key=lambda x: x["dist"])
            out.append(dict(k=k, shot=si, cam=cn, frame=f, t=(k - 1) / 24.0, dist=round(dist, 3), radial=round(radial, 3), pan=round(pan, 3),
                            front=round(front, 3), cam_speed=round(camspd, 2), drone_speed=round(dspd, 2), throttle=round(thr, 3),
                            cam_z=round(c.z, 2), drone_z=round(d.z, 2), cars=near[:6]))
        prev = cur
json.dump(dict(fps=24, frames=out, shots=SHOTS, take_off=dp["take_off"], hover=dp["hover"]), open(os.path.join(ROOT, "audio", "motion.json"), "w"), indent=0)
print("frames", k, "shot starts", [next(x["k"] for x in out if x["shot"] == s) for s in range(len(SHOTS))])
