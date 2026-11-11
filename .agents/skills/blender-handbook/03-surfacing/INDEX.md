# 03 — Surfacing (Materials, UV, Texture, Hair)

**Open this when** the request is about how a model *looks* at the surface: PBR or stylized materials, look-dev iteration, UV unwrapping and packing, texture atlases and decals, baking maps, texture-driven reshaping, animated texture states, hair and fur.

Paths below are relative to this file's own directory.

## Materials and look-dev

| Manual | Use when | Path |
|--------|----------|------|
| `blender-materials` | **Canonical for material creation** — PBR via Principled BSDF, metals, glass, plastic, fabric, skin, organics; Coat/Sheen/Subsurface/Transmission recipes; procedural patterns (wood grain, marble, weave); the Blender 5.x `set_input` helper | `blender-materials/MANUAL.md` |
| `materials` | **Supplement** — only for material reuse, stylized libraries, or production shading recipes not covered in the canonical manual | `materials/MANUAL.md` |
| `lookdev` | You need to iterate materials + lighting + camera against screenshots until the shading reads correctly | `lookdev/MANUAL.md` |

## UV

| Manual | Use when | Path |
|--------|----------|------|
| `blender-uv-texturing` | Unwrap, atlas-map, project textures, alpha decals, bake maps/lightmaps, prepare a texture-driven asset for glTF/GLB export | `blender-uv-texturing/MANUAL.md` |
| `uv-workflow` | Production UV decisions — seam placement, packing, texel density, UDIM, lightmap UVs, modular layouts | `uv-workflow/MANUAL.md` |
| `atlas-uv-fitting` | A texture pack/atlas must fit a model 1:1 — map each source part to its own UV rectangle or projected surface. Also when textures look off/stretched, or alpha decals/lightmaps are supplied | `atlas-uv-fitting/MANUAL.md` |
| `closed-surface-uv-coverage` | Back caps or sidewalls render plain because the texture only arrived as a projected front plane. Ensures every visible surface of a closed/extruded asset is covered | `closed-surface-uv-coverage/MANUAL.md` |
| `texture-driven-mesh-fitting` | The **geometry** is wrong for the texture: reshape source-locked mesh boundaries so they fit atlas/decal contours before final UV work | `texture-driven-mesh-fitting/MANUAL.md` |

## Texture pipeline and texture states

| Manual | Use when | Path |
|--------|----------|------|
| `texture-workflow` | Production texture pipeline — atlases, baking AO/curvature/normal/roughness, decals, texture memory optimization | `texture-workflow/MANUAL.md` |
| `texture-state-animation` | Animating between multiple source textures (mascot/logo states, lightmaps, decals, UI skins) without whole-image crossfades, popping, or misregistration, and without target-engine-incompatible Python-only swaps | `texture-state-animation/MANUAL.md` |

## Hair

| Manual | Use when | Path |
|--------|----------|------|
| `hair-groom` | Hair and fur — curves, particle hair, geometry nodes, and real-time game hair cards | `hair-groom/MANUAL.md` |

## Next steps

- Lighting reveals materials → `../04-imaging/INDEX.md`
- Exact fidelity to a supplied texture/template → `../08-reference-locked/INDEX.md`
