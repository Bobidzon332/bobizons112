# Output Validation and Reporting

The user only sees the picture and the numbers you give them. Both must be honest.

---

## Visual validation checkpoint (always between render and reporting)

A render passing every numerical check (object count, vertex count, file size, no error messages) can still look completely wrong. After rendering, **always**:

1. Call `mcp__blender__get_viewport_screenshot` (or read the rendered file with `Read`).
2. Visually verify against the user's request. Specifically:
   - **Subject is visible and recognisable** — not a thin streak, not magenta-flooded, not entirely in shadow.
   - **Proportions match** the real-world reference dimensions for that subject (`${COMMANDCODE_SKILL_DIR}/references/common-object-dimensions.md`).
   - **Composition is reasonable** — subject in frame, not clipped at edges, not microscopic in one corner.
   - **Materials have visible variation** — not perfectly flat plastic-looking surfaces. For production-quality scenes, add procedural texture nodes.
3. **If the render is obviously wrong, do NOT report success.** Iterate: identify the specific problem, fix it, re-render, re-check.

Magenta is a diagnostic signal, not permission to reset the world. Inspect world and material image nodes and their file paths, then repair the missing resource in scope. Only use `reset_world(scene=target_scene)` from `${COMMANDCODE_SKILL_DIR}/scripts/reset_world.py` when replacing that scene's world is the chosen repair; loading the helper alone does nothing.

---

## Reporting back to the user

When work is done, report concretely:

- ✅ **Created**: list objects + polycounts.
- ✅ **Lit**: list lights + their roles.
- ✅ **Rendered**: file path + size + dimensions + render time.
- ⚠️ **Warnings**: any auto-decimation, naming conflicts, fallback materials.

### Template

> Created `GEO-sword_blade` (1 240 verts), `GEO-sword_grip` (320 verts).  
> Materials: `MAT-steel_brushed`, `MAT-leather_dark`.  
> Lit with `LGT-key` (warm 3200K), `LGT-fill` (cool 5500K), `LGT-rim` (cool blue).  
> Rendered to `/tmp/sword_hero.png` (1920×1080, 2.3 MB, 38 s with 256 samples + OptiX denoise).

Always give the user an inspectable path to the proof render, not just a description of it.

---

## Delivering the viewport result

The user is often looking at Blender's viewport, not the rendered file. Blender defaults the viewport to **Solid** shading, which ignores all materials and shows everything as flat grey — the render is correct, but the viewport looks broken.

Switch the viewport to Material Preview after scene assembly: `${COMMANDCODE_SKILL_DIR}/scripts/set_viewport_material_preview.py`. Skip this only when the user has explicitly asked you to leave the viewport alone.

---

## Honesty rules

- Never report success on the basis of numerical checks alone.
- Never describe a result you have not visually inspected.
- If you fell back to a substitute (auto-decimation, fallback material, placeholder instead of a real asset), say so in the Warnings line.
