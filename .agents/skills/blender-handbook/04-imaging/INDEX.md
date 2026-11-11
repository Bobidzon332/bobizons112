# 04 — Imaging (Lighting, Camera, Render, Composite)

**Open this when** the request is about turning an assembled scene into a picture: lighting, framing and camera, engine/sample settings, or post-processing.

Paths below are relative to this file's own directory.

## Lighting

| Manual | Use when | Path |
|--------|----------|------|
| `blender-lighting` | **Canonical for lighting** — three-point setups, HDRI environments, studio/cinematic/dramatic configurations, light groups, colour temperature, soft vs hard shadows | `blender-lighting/MANUAL.md` |
| `lighting` | **Supplement** — only for horror/volumetric/game lighting recipes and mood-specific rigs not covered in the canonical manual | `lighting/MANUAL.md` |

## Camera and shot language

| Manual | Use when | Path |
|--------|----------|------|
| `blender-cameras` | Focal length, depth of field (f-stop/focus object), composition (rule of thirds, leading lines), animated cameras (orbit, dolly, push-in), tracking constraints | `blender-cameras/MANUAL.md` |
| `camera-cinematography` | Shot language beyond basic setup — framing, lens choice, composition and camera animation as a storytelling decision | `camera-cinematography/MANUAL.md` |

## Render and composite

| Manual | Use when | Path |
|--------|----------|------|
| `blender-rendering` | **Canonical for rendering** — engine choice (Cycles vs EEVEE), sample counts, denoising, light-path tuning, colour management (AgX/Filmic), output files, animation rendering | `blender-rendering/MANUAL.md` |
| `rendering` | **Supplement** — only for render passes, render optimization, or look-validation recipes not covered in the canonical manual | `rendering/MANUAL.md` |
| `compositing` | Compositor node work — beauty stacks, render passes, colour grade, glare, vignette, delivery outputs | `compositing/MANUAL.md` |

## Related

- A render that looks wrong but passes every numeric check → `${COMMANDCODE_SKILL_DIR}/references/failure-modes.md`
- Grinding materials/lighting together until it reads right → `lookdev` in `../03-surfacing/INDEX.md`
