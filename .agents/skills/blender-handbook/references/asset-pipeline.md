# Asset Pipeline

Shared phase context for modeling, UV, surfacing, delivery, and QA manuals.

| Phase | Exit condition | Typical manuals |
|-------|----------------|-----------------|
| Reference / plan | Goal, target platform, and source-of-truth are explicit | `blender-pro-workflow`, `reference-to-3d` |
| Block-out | Silhouette and scale read from the hero camera | `blender-modeler`, `blender-cameras` |
| Camera lock | Framing and focal length are fixed | `blender-cameras`, `camera-cinematography` |
| Light v1 | Subject separates from background | `blender-lighting`, `lighting` |
| Geometry refinement | Final topology and part count | `blender-modeling`, specialist manuals |
| Materials v1 | Values read in grayscale | `blender-materials`, `materials` |
| Light v2 | Colour and ratio support the material read | `blender-lighting`, `lighting` |
| Detail pass | Surface detail and story props | `sculpting`, `set-dressing` |
| QA / optimization | Budget, naming, topology and visual checks pass | `qa-review`, `asset-optimization` |
| Delivery | Engine import verified | `blender-export`, `export-pipeline`, engine manuals |

For the full sequence and recovery patterns see `${COMMANDCODE_SKILL_DIR}/references/assembly-order.md`.
