# 07 — Delivery (Export, Engines, Optimization)

**Open this when** the asset has to leave Blender: choose an output format, meet a specific engine's expectations, hit a polycount/memory budget, or add collision and LODs.

Paths below are relative to this file's own directory.

## Export formats and pipelines

| Manual | Use when | Path |
|--------|----------|------|
| `blender-export` | **Canonical for export** — per-format export settings and validation: glTF/GLB (web, AR), FBX (engines), OBJ, USD, STL; texture embed/unpack, axis conversion, polygon optimization | `blender-export/MANUAL.md` |
| `export-pipeline` | **Supplement** — only for production export verification of scale, pivot, rotation, normals, materials, animation and collision | `export-pipeline/MANUAL.md` |

## Engine-specific

| Manual | Use when | Path |
|--------|----------|------|
| `unity-export` | Unity import expectations — scale, axis, materials, humanoid/generic rigs, LODs, collision | `unity-export/MANUAL.md` |
| `unreal-export` | Unreal — FBX scale, LODs, UCX collision, sockets, materials, skeletal mesh workflows | `unreal-export/MANUAL.md` |
| `godot-export` | Godot — GLTF/GLB with correct scale, materials, animation clips, collision shapes | `godot-export/MANUAL.md` |

## Optimization

| Manual | Use when | Path |
|--------|----------|------|
| `asset-optimization` | Pre-export audit: polycount, topology, UV efficiency, material count, naming, collections, game-ready performance | `asset-optimization/MANUAL.md` |
| `lod-pipeline` | Generating, naming, targeting and validating LOD levels for game meshes | `lod-pipeline/MANUAL.md` |
| `collision-proxy` | Authoring colliders — UCX/UHX naming, convex hulls, capsules, simple collider meshes | `collision-proxy/MANUAL.md` |

## Related

- Ship/no-ship review before delivery → `../09-quality-gates/INDEX.md`
- The connection itself failing (not the export) → the separate **`blender-mcp`** skill
