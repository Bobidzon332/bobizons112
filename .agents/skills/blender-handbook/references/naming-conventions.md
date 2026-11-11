# Naming Conventions

## Canonical Blender scene names

Use these prefixes for anything created in the Blender scene:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `GEO-` | Geometry / mesh objects | `GEO-sword_blade` |
| `MAT-` | Materials | `MAT-steel_brushed` |
| `LGT-` | Lights | `LGT-key` |
| `CAM-` | Cameras | `CAM-hero` |
| `ARM-` | Armatures / rigs | `ARM-character` |
| `COL-` | Collections | `COL-SetDressing` |
| `WGT-` | Custom bone shapes / widgets | `WGT-hand_L` |

Use `.L` / `.R` suffixes for side symmetry. Never leave a `Cube.027` or `Material.003` in a delivered scene.

## Engine-specific naming

Delivery and collision manuals may use engine-native names. Treat them as an export-time mapping, not a replacement for the Blender-side convention:

| Context | Convention | Example |
|---------|------------|---------|
| Unreal static meshes | `SM_`, `SK_`, `UCX_` | `SM_Asset_LOD0`, `UCX_Asset_01` |
| Unity / Godot collision | `COL_` / `UCX_` | `COL_Collision_Asset` |
| Texture bake outputs | `T_[Asset]_[Map]` | `T_sword_Normal` |

When an engine convention and the canonical Blender convention both apply, name the Blender objects canonically and rename or map at export.

## Precedence

1. The entry `SKILL.md` naming rule is authoritative for Blender scene objects.
2. This document expands that rule and covers engine exceptions.
3. Manuals outside `07-delivery/` use the canonical hyphen prefixes throughout. The underscore forms exist only in two places: the engine-mapping table above, and the `07-delivery/` manuals that describe target-engine conventions.
