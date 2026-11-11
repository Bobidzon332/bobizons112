"""Ensure the scene has a camera before rendering.

Multiple manuals reference an ensure_camera() guard but no shared script
existed. Run this before any render call.

Usage (via mcp__blender__execute_blender_code):

    exec(open(r"${COMMANDCODE_SKILL_DIR}/scripts/ensure_camera.py").read())

Behaviour:
- If scene.camera already exists → do nothing.
- If no camera exists → create CAM-hero at (7, -6, 5) aimed at the origin,
  50 mm focal length, and set it as scene.camera.

Override defaults by calling the function directly:

    ensure_camera(name="CAM-closeup", location=(3, -2, 2), focal_length=85)
"""

import bpy
import math

DEFAULT_NAME = "CAM-hero"
DEFAULT_LOCATION = (7.0, -6.0, 5.0)
DEFAULT_FOCAL_LENGTH = 50.0


def ensure_camera(
    scene=None,
    name=DEFAULT_NAME,
    location=DEFAULT_LOCATION,
    focal_length=DEFAULT_FOCAL_LENGTH,
    look_at=(0.0, 0.0, 0.0),
):
    """Return the scene camera, creating one if none exists."""
    scene = scene or bpy.context.scene

    if scene.camera is not None:
        print(f"ensure-camera: already set to '{scene.camera.name}' — no change")
        return scene.camera

    # Create camera data and object
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = focal_length
    cam_obj = bpy.data.objects.new(name, cam_data)

    # Link to scene's active collection
    collection = scene.collection
    collection.objects.link(cam_obj)

    # Position
    cam_obj.location = location

    # Aim at look_at point using a Track To constraint
    constraint = cam_obj.constraints.new(type="TRACK_TO")
    # Create an empty target at the look_at point
    target = bpy.data.objects.new(f"{name}_target", None)
    target.location = look_at
    target.empty_display_size = 0.1
    collection.objects.link(target)

    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"

    # Set as active camera
    scene.camera = cam_obj

    print(
        f"ensure-camera: created '{name}' at {location}, "
        f"focal={focal_length}mm, looking at {look_at}"
    )
    return cam_obj


_cam = ensure_camera()
