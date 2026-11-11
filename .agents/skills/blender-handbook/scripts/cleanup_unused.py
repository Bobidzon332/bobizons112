"""Preview or remove explicitly named, unused task-owned data blocks.

Loading has no scene side effects. Inspect ownership before passing candidates:
    cleanup_unused({"materials": ["MAT-temporary"]})  # preview only
    cleanup_unused({"materials": ["MAT-temporary"]}, dry_run=False)

This is a single scoped pass, not a recursive or whole-file orphan purge.
"""

import bpy

CATEGORIES = (
    "materials", "meshes", "images", "node_groups", "textures", "curves",
    "armatures", "cameras", "lights", "worlds", "actions",
)


def cleanup_unused(candidates, dry_run=True):
    """Return eligible counts; preserve used, linked and fake-user data."""
    unknown = set(candidates) - set(CATEGORIES)
    if unknown:
        raise ValueError(f"Unsupported data categories: {sorted(unknown)}")
    plan = {}
    for category, names in candidates.items():
        if isinstance(names, str):
            raise ValueError("Each category requires a list of explicit data-block names")
        collection = getattr(bpy.data, category)
        blocks = []
        for name in dict.fromkeys(names):
            item = collection.get(name)
            if item is None:
                raise ValueError(f"Unknown data block: {category}/{name}")
            if item.users == 0 and not item.use_fake_user and item.library is None:
                blocks.append(item)
        plan[category] = blocks
    if not dry_run:
        for category, blocks in plan.items():
            for item in blocks:
                getattr(bpy.data, category).remove(item)
    return {category: len(blocks) for category, blocks in plan.items()}
