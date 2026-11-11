"""Create a neutral world only for a new scene or an in-scope repair.

Loading only defines reset_world(). Call reset_world(scene=target_scene)
explicitly after inspection. Existing worlds are retained as data blocks;
only the target scene receives the new world. Resolve the script's absolute
path before loading it through Blender MCP.
"""

import bpy

DEFAULT_COLOR = (0.04, 0.04, 0.05, 1.0)
DEFAULT_STRENGTH = 0.4


def reset_world(scene=None, color=DEFAULT_COLOR, strength=DEFAULT_STRENGTH):
    """Assign a fresh world without modifying a potentially shared node tree."""
    scene = scene or bpy.context.scene
    world = bpy.data.worlds.new("World-neutral")

    world.use_nodes = True
    nodes = world.node_tree.nodes
    for n in list(nodes):
        nodes.remove(n)

    output = nodes.new("ShaderNodeOutputWorld")
    bg = nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = color
    bg.inputs["Strength"].default_value = strength
    world.node_tree.links.new(bg.outputs["Background"], output.inputs["Surface"])

    scene.world = world
    return world

