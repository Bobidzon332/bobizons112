# 02 — Modeling & Geometry

**Open this when** the request is about creating or shaping geometry: a mesh from nothing, a specific asset class (character, creature, environment, vehicle, prop, vegetation), surface detail, retopology, procedural generation, or building geometry from a 2D drawing.

If the model must match a supplied template/wireframe/texture **exactly**, start in `08-reference-locked/` instead — fidelity work has its own gated pipeline.

Paths below are relative to this file's own directory.

## Core modeling

| Manual | Use when | Path |
|--------|----------|------|
| `blender-modeling` | **Canonical for general mesh work** — primitives, mesh operators, modifier stacks (Bevel/Subdivision/Boolean/Mirror/Array/Solidify), bmesh edits, tapering and axis-orientation recipes | `blender-modeling/MANUAL.md` |
| `blender-modeler` | **Supplement** — only for blockouts, Edit Mode workflow, precision modeling, collection/scene organization, non-destructive workflows. Do not load alongside `blender-modeling` unless the request needs both | `blender-modeler/MANUAL.md` |
| `hard-surface` | Sci-fi, industrial, military, vehicles, weapons, robotics — boolean/bevel workflows, panel lines, greebles, chamfers | `hard-surface/MANUAL.md` |

## Asset-class specialists

| Manual | Use when | Path |
|--------|----------|------|
| `prop-artist` | Grounded everyday/hero props — furniture, tools, household objects, kitbash parts. Use when `hard-surface` is too sci-fi/mechanical | `prop-artist/MANUAL.md` |
| `character-artist` | Human characters — anatomy, facial topology, clothing, hair, animation-ready meshes | `character-artist/MANUAL.md` |
| `creature-artist` | Fantasy/alien/monster creatures — believable anatomy, muscle flow, bone structure | `creature-artist/MANUAL.md` |
| `environment-artist` | Modular kits, buildings, terrain, architecture, game-optimized environments | `environment-artist/MANUAL.md` |
| `vehicle-artist` | Cars, trucks, aircraft, ships, boats, mechs, transit — proportion, panel flow, LOD awareness | `vehicle-artist/MANUAL.md` |
| `vegetation-artist` | Trees, plants, grass cards, canopy LODs, game-friendly leaf atlases | `vegetation-artist/MANUAL.md` |

## Detail, retopology, procedural

| Manual | Use when | Path |
|--------|----------|------|
| `sculpting` | High-frequency surface detail is needed: Dyntopo, multiresolution, brushes, alpha workflow, wrinkles, damage | `sculpting/MANUAL.md` |
| `retopology` | After sculpting / high-poly, before rigging or UV: quad-dominant low-poly meshes, proper edge loops | `retopology/MANUAL.md` |
| `geometry-nodes` | Procedural scatter systems, vegetation, buildings, pipes, cables, reusable node groups | `geometry-nodes/MANUAL.md` |
| `procedural-modeling` | Procedural rocks, buildings, roads, terrain, cables, sci-fi panels via Geometry Nodes + modifiers | `procedural-modeling/MANUAL.md` |

## From 2D source art to mesh

| Manual | Use when | Path |
|--------|----------|------|
| `wireframe-to-3d` | The user supplies 2D orthographic wireframe/technical/line drawings and wants a 3D model or `.glb` | `wireframe-to-3d/MANUAL.md` |
| `contour-to-mesh` | The mesh surface must be built directly from an extracted 2D contour/mask rather than approximated with primitives | `contour-to-mesh/MANUAL.md` |

## Next steps after modeling

- Give it surfaces → `../03-surfacing/INDEX.md`
- Light and render it → `../04-imaging/INDEX.md`
- Get it into an engine → `../07-delivery/INDEX.md`
