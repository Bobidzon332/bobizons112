"""Cross-platform runner for the CH_StarPlatinum pipeline (Linux, macOS, Windows).

    python build/run_all.py --blender <path to blender> [--from 02] [--device CPU|GPU]

Runs each phase headless (blender --background --factory-startup), then the verification step:
GLB export with manifest (skill export_delivery.py), GLB round trip (roundtrip.py), Roblox FBX round trip,
validate.py, and the colour gate when Pillow is available. Output is printed per phase.
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.dirname(HERE)
SKILL = os.path.normpath(os.path.join(ASSET, "..", ".agents", "skills", "blender-image-to-3d", "scripts"))
PHASES = ["01_init", "02_blockout", "03_forms", "04_topology", "05a_uv", "05b_bake", "05c_paint", "06_rig",
          "07_export", "08_verify"]
INFERRED = ("skull under hair,ears,back of head hair mass,palms and fingers inside fists,underside of shoulder "
            "pads,knee strap back,belt disc count,absolute height")
KEEP = ("[", "Error", "Traceback", "line ", "exported", "manifest", "MESHES", "ARMATURES", "HEIGHT", "ERRORS",
        "FBXCHECK", "FAIL", "WARN", "saved", "COLOURS")


def blender(bl, script, args=()):
    cmd = [bl, "--background", "--factory-startup", "--python", script, "--"] + list(args)
    p = subprocess.run(cmd, cwd=ASSET, capture_output=True, text=True, errors="replace")
    for line in (p.stdout + p.stderr).splitlines():
        if line.startswith(KEEP) or "Error" in line:
            print("   ", line, flush=True)
    return p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blender", required=True)
    ap.add_argument("--from", dest="first", default="02")
    ap.add_argument("--device", default="CPU", choices=["CPU", "GPU"])
    a = ap.parse_args()
    master = "CH_StarPlatinum_master.blend"
    for p in PHASES:
        if p[:2] < a.first or (p == "02_blockout" and a.first not in ("01", "02")):
            continue
        print("==", p, flush=True)
        if p == "01_init":
            # calibrated master: reference planes at real scale, collections, ruler, game camera (asset-brief)
            blender(a.blender, os.path.join(SKILL, "init_master.py"),
                    ["--out", master, "--name", "CH_StarPlatinum", "--height", "2.10", "--ref-front", "ref/front.png",
                     "--ref-right", "ref/side.png", "--ref-back", "ref/back.png", "--ref-extra",
                     "ref/stand_sheet_original.png", "--subject-frac", "0.9888", "--ground-frac", "0.0112",
                     "--cell", "2.0", "--capsule", "0.45", "2.1", "--cam-elev", "20", "--cam-az", "30",
                     "--cam-dist", "6", "--cam-lens", "35"])
        elif p == "05b_bake":
            bake = os.path.join(SKILL, "bake_maps.py")
            common = ["--blend", master, "--low", "EXPORT", "--high", "HIGH", "--out", "textures/bake",
                      "--extrusion", "0.015", "--ray-dist", "0.03", "--device", a.device]
            blender(a.blender, bake, common + ["--maps", "normal", "--res", "2048", "--margin", "16", "--samples", "4"])
            blender(a.blender, bake, common + ["--maps", "ao", "--res", "1024", "--margin", "8", "--samples", "128"])
        elif p == "08_verify":
            blender(a.blender, os.path.join(SKILL, "export_delivery.py"),
                    ["--blend", master, "--out", "exports/glb", "--name", "CH_StarPlatinum", "--format", "GLB",
                     "--collections", "EXPORT,RIG_DEF", "--no-animation", "--engine", "roblox", "--inferred", INFERRED])
            blender(a.blender, os.path.join(SKILL, "roundtrip.py"),
                    ["--file", "exports/glb/CH_StarPlatinum.glb", "--out", "review/09_roundtrip_glb",
                     "--expect-height", "2.145"])
            blender(a.blender, os.path.join(ASSET, "tools", "fbx_roundtrip.py"),
                    ["exports/roblox/CH_StarPlatinum_R15.fbx", "review/09_roundtrip_fbx"])
            blender(a.blender, os.path.join(SKILL, "validate.py"),
                    ["--blend", master, "--collections", "EXPORT,RIG_DEF", "--out", "review/09_validate.json",
                     "--budget-tris", "30000", "--require-uv"])
            try:
                import PIL  # noqa: F401
                subprocess.run([sys.executable, os.path.join(ASSET, "tools", "check_colours.py"),
                                os.path.join(ASSET, "exports", "roblox", "T_StarPlatinum_BC.png")], cwd=ASSET)
            except ImportError:
                print("    colour gate skipped (Pillow not installed)")
        else:
            blender(a.blender, os.path.join(HERE, p + ".py"))
    print("== done", flush=True)


if __name__ == "__main__":
    main()
