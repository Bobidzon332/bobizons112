"""Switch every 3D viewport to Material Preview shading.

Why: Blender defaults the viewport to **Solid** shading, which ignores all
materials and renders everything as flat grey. The user is usually looking at
the viewport, not the rendered file, so they will report "the scene is grey"
even though the render is correct. Run this after scene assembly, as the last
step before reporting.

Usage (via mcp__blender__execute_blender_code):

    exec(open(r"${COMMANDCODE_SKILL_DIR}/scripts/set_viewport_material_preview.py").read())

Loading the file switches the viewport and prints how many areas were changed.
For full quality instead of preview, pass the shading type explicitly:

    set_viewport_material_preview(shading_type="RENDERED")

Skip this entirely only when the user has explicitly asked you to leave the
viewport alone.
"""

import bpy

DEFAULT_SHADING_TYPE = "MATERIAL"


def set_viewport_material_preview(shading_type=DEFAULT_SHADING_TYPE):
    """Set shading for every VIEW_3D space. Returns the number of spaces changed."""
    changed = 0
    screen = bpy.context.screen
    if screen is None:
        print("viewport-shading: no screen in context (headless run) -- skipped")
        return 0

    for area in screen.areas:
        if area.type != "VIEW_3D":
            continue
        for space in area.spaces:
            if space.type == "VIEW_3D":
                space.shading.type = shading_type
                space.shading.use_scene_lights = True
                space.shading.use_scene_world = True
                changed += 1

    return changed


_changed = set_viewport_material_preview()
print(f"viewport-shading: set to {DEFAULT_SHADING_TYPE} on {_changed} space(s)")
