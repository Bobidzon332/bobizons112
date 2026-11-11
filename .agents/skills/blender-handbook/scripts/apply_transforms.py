"""Apply explicitly chosen transforms to explicitly named static objects.

Loading only defines the helper. Example after resolving its absolute path:
    apply_transforms(names=["GEO-sword"], scale=True)

Use an export copy for rigs, animation, parents, constraints or shared data.
Transform baking is target-dependent, not a mandatory export operation.
"""

import bpy


def apply_transforms(names, *, location=False, rotation=False, scale=False):
    """Validate the entire scope first, then bake and restore selection state."""
    if isinstance(names, str) or not names:
        raise ValueError("Provide an explicit non-empty list of object names")
    if not any((location, rotation, scale)):
        raise ValueError("Choose location, rotation and/or scale explicitly")
    if bpy.context.mode != "OBJECT":
        raise ValueError("Transform baking requires Object mode")

    targets = []
    for name in dict.fromkeys(names):
        obj = bpy.context.view_layer.objects.get(name)
        if obj is None:
            raise ValueError(f"Object is absent from the active view layer: {name}")
        if obj.type not in {"MESH", "CURVE", "SURFACE", "META", "FONT"}:
            raise ValueError(f"Unsupported transform target: {name}")
        if (obj.library or obj.data.library or obj.data.users > 1
                or obj.animation_data or obj.data.animation_data
                or obj.parent or obj.children or obj.constraints
                or any(mod.type == "ARMATURE" for mod in obj.modifiers)
                or getattr(obj.data, "shape_keys", None)):
            raise ValueError(f"Use an independently verified export copy for: {name}")
        if obj.hide_select or not obj.visible_get():
            raise ValueError(f"Target must be visible and selectable: {name}")
        targets.append(obj)

    selected = list(bpy.context.selected_objects)
    active = bpy.context.view_layer.objects.active
    processed = []
    try:
        bpy.ops.object.select_all(action="DESELECT")
        for obj in targets:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            result = bpy.ops.object.transform_apply(
                location=location, rotation=rotation, scale=scale)
            if "FINISHED" not in result:
                raise RuntimeError(f"Transform apply failed: {obj.name}; processed={processed}")
            obj.select_set(False)
            processed.append(obj.name)
    finally:
        bpy.ops.object.select_all(action="DESELECT")
        for obj in selected:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = active
    return processed
