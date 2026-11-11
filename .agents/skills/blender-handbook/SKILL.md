---
name: blender-handbook
description: Entry point and router for a 123-manual Blender 3D production handbook covering modeling, surfacing, lighting, animation, physics, scene assembly, export, and art direction.
---

# Blender Handbook — Router

Entry router for the 3D production handbook (**123 manuals across 10 groups**). Load only what is needed.

## Navigation: 3 Levels

```text
${COMMANDCODE_SKILL_DIR}/SKILL.md                     ← Level 0: Global entry router (this file)
${COMMANDCODE_SKILL_DIR}/<group>/INDEX.md             ← Level 1: Domain member index and trigger rules
${COMMANDCODE_SKILL_DIR}/<group>/<skill>/MANUAL.md    ← Level 2: Task-specific production manual
```

1. **Route**: Start with the 1–2 domain groups needed for the current phase; load additional groups only as their work becomes relevant. Choose one workflow owner using `references/intent-routing.md`, the authority for activation and recovery precedence.
2. **Index**: Read that group's `<group>/INDEX.md` to pick the concrete manual.
3. **Execute**: Read and strictly follow only the relevant `MANUAL.md` files in production order.

## Paths and runtime capabilities

In this project `${COMMANDCODE_SKILL_DIR}` = `.agents/skills/blender-handbook`. 93 manuals that duplicated arjun988 skills are short redirect stubs here; the full content lives in the sibling standalone `blender-*` skills they point to.

`${COMMANDCODE_SKILL_DIR}` is a documentation placeholder for the absolute directory containing this `SKILL.md`, not an automatically defined environment variable. Resolve it before executing any example; quote paths containing spaces. Paths inside a manual are relative to that manual unless the root placeholder is used. If Blender runs on another host, do not assume it can read local files: send the required script text through the available execution tool instead.

Discover the connected MCP tool names and schemas before using them. Query the live Blender version before version-sensitive operations. The names and limits in `references/mcp-integration.md` are examples, not capability guarantees. Load the separate `blender-mcp` skill only for transport/setup problems.

## Level-1 Routing Table

| Group | Open when the request is about… |
|-------|--------------------------------|
| `01-orchestration/` | Multi-step/multi-skill planning, precedence rules, user recovery, finisher MCP |
| `02-modeling/` | Mesh creation, hard-surface/mechanical, character, creature, environment, procedural, sculpting |
| `03-surfacing/` | Materials, look-dev, UV unwrapping, texture atlases, decals, hair and fur |
| `04-imaging/` | Lighting schemes, camera composition, Cycles/EEVEE render engines, compositing |
| `05-motion/` | Keyframe animation, rigging/armatures, physics & cloth simulation, VFX particles |
| `06-scene/` | Large scene assembly, collection hierarchies, set dressing and prop placement |
| `07-delivery/` | Multi-engine export (glTF/FBX/USD/OBJ/STL), LODs, polycount optimization, collision meshes |
| `08-reference-locked/` | 1:1 Reference/blueprint/wireframe matching, dimension verification, misalignment repair |
| `09-quality-gates/` | Final ship/no-ship validation checklists for assets and animations |
| `10-art-direction/` | Visual styles (anime, stylized, voxel, retro, sci-fi, horror, pixel) |

*For MCP connection troubleshooting (port 9876, safe mode), refer to the separate `blender-mcp` skill.*

## Always-On Rules (Critical Baseline)

1. **Scope preflight**: Inspect the current scene through the available scene-info tool. Identify target objects/collections before mutation; preserve other objects, worlds, cameras and user data. A default-named cube is not proof that it is disposable. Knowledge-only requests do not require a Blender connection.
2. **World inspection**: Keep existing lighting by default. Investigate missing image nodes if a render is magenta. For a new scene or a diagnosed, in-scope world repair, load `scripts/reset_world.py` and explicitly call `reset_world(scene=target_scene)`. It assigns a new world without altering the old world data block; do not run it for every build.
3. **Execution**: Re-import required modules per call and use stable object names. Size calls to the live timeout and meaningful checkpoints, not a fixed line count. Naming prefixes are conventions, not permission to modify every matching object (`references/code-execution-rules.md`).
4. **Visual validation**: Preserve an existing active camera. When rendering requires a missing camera, `scripts/ensure_camera.py` can create one. Inspect the actual render or viewport for visibility, framing and proportions (`references/output-and-reporting.md`).
5. **Dimensions**: User measurements and source contracts take priority. Use `references/common-object-dimensions.md` as a plausibility baseline, not a substitute for unknown exact dimensions.
6. **Export scope**: Export only the agreed objects. Apply transforms only when the target requires them; `scripts/apply_transforms.py` requires explicit names and flags, e.g. `apply_transforms(names=["GEO-prop"], scale=True)`. Rigs, animation and shared data need a separately verified export-copy workflow. Cleanup is optional: load `scripts/cleanup_unused.py`, preview explicit task-owned candidates with `cleanup_unused({"materials": ["MAT-temporary"]})`, and set `dry_run=False` only for the inspected list. These three helpers only define functions when loaded; they never mutate the scene automatically.
7. **Sequence and recovery**: Follow the selected workflow in `references/intent-routing.md`. Art-direction manuals constrain appearance; they do not own execution order. Repairing an artifact does not authorize modifying the installed handbook or persistent memory.

## Core Orchestrator References

- **Intent & Recovery**: `references/intent-routing.md`, `references/failure-modes.md`
- **Execution & Tools**: `references/code-execution-rules.md`, `references/mcp-integration.md`
- **Quality & Checklist**: `references/output-and-reporting.md`, `references/validation-checklist.md`
- **Workflow & Scales**: `references/assembly-order.md`, `references/common-object-dimensions.md`
- **Automation Scripts**: `scripts/reset_world.py`, `scripts/ensure_camera.py`, `scripts/apply_transforms.py`, `scripts/cleanup_unused.py`, `scripts/detect_blender_version.py`

## Scope Boundary (What This Is NOT For)

- Custom GPU render engine development (use Cycles / EEVEE).
- Real-time gameplay logic (use Unity / Unreal / Godot directly).
- Manual brush sculpting strokes from natural language (interactive sculpting requires manual input).
- CAD precision engineering CFD (Mantaflow is visual VFX only).
