"""Detect Blender runtime version and API feature flags.

Run this at the start of a session or when encountering unexpected API behavior.
It probes current environment quirks and prints a structured JSON status.

Usage (via mcp__blender__execute_blender_code):

    exec(open(r"${COMMANDCODE_SKILL_DIR}/scripts/detect_blender_version.py").read())
"""

import json
import bpy


def detect_environment():
    version_tuple = bpy.app.version
    version_str = bpy.app.version_string

    # 1. EEVEE engine identifier
    engine_name = "BLENDER_EEVEE"
    scene = bpy.context.scene
    orig_engine = scene.render.engine
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
        engine_name = "BLENDER_EEVEE_NEXT"
    except (TypeError, ValueError):
        engine_name = "BLENDER_EEVEE"
    finally:
        scene.render.engine = orig_engine

    # 2. Action layered API
    has_layered_actions = hasattr(bpy.types.Action, "layers")

    # 3. Disabled / special BSDF inputs
    disabled_inputs = []
    temp_mat = bpy.data.materials.new("_temp_compat_probe")
    temp_mat.use_nodes = True
    bsdf = temp_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        disabled_inputs = [inp.name for inp in bsdf.inputs if not inp.enabled]
    bpy.data.materials.remove(temp_mat, do_unlink=True)

    # 4. Mesh auto-smooth
    has_mesh_auto_smooth = hasattr(bpy.types.Mesh, "use_auto_smooth")

    info = {
        "version": list(version_tuple),
        "version_string": version_str,
        "eevee_engine": engine_name,
        "layered_actions": has_layered_actions,
        "disabled_bsdf_inputs": disabled_inputs,
        "has_mesh_auto_smooth": has_mesh_auto_smooth,
    }
    return info


_info = detect_environment()
print(f"blender-env-detect: {json.dumps(_info)}")
