# 08 — Reference-Locked Reconstruction

**Open this when** the user needs a **1:1 match to supplied source material** — branding templates, mascot/logo art, orthographic front/side/back/top views, texture atlases, character sheets — rather than a plausible interpretation. "Does not look like the reference", "exact number of parts", and "fit this texture 1:1" all belong here.

**This group outranks generic production workflow.** Fidelity gates are not optional extras: establish the source of truth first, then model.

Paths below are relative to this file's own directory.

## Start here

| Manual | Use when | Path |
|--------|----------|------|
| `reference-to-3d` | The main entry for source-locked reconstruction — reference sheets, branding templates, atlases, orthographic views. Chains the rest of this group | `reference-to-3d/MANUAL.md` |
| `mascot-logo-reconstruction` | Fail-gated, source-locked reconstruction of mascots, logos, brand avatars and stylized flat characters from wireframes + texture packs + orthographic views | `mascot-logo-reconstruction/MANUAL.md` |

## Establish and measure the source contract

| Manual | Use when | Path |
|--------|----------|------|
| `orthographic-registration` | Register front/side/back/top views into one shared coordinate contract before adding depth | `orthographic-registration/MANUAL.md` |
| `multiview-constraint-solver` | The views contradict each other (bboxes, silhouettes, part counts, depth ratios). Decide whether one rigid model can satisfy them and choose a canonical source — **before** rebuilding | `multiview-constraint-solver/MANUAL.md` |
| `source-part-segmentation` | Touching or overlapping parts must be separated from the source images before contour-to-mesh, UV fitting or landmark repair | `source-part-segmentation/MANUAL.md` |
| `reference-analysis-validator` | Measure supplied references/renders before claiming 1:1 — exact part counts, masks, wireframe and atlas validation | `reference-analysis-validator/MANUAL.md` |

## Fit and repair

| Manual | Use when | Path |
|--------|----------|------|
| `multiview-fit-loop` | Compare → adjust → repeat until the model passes measurable bbox/centroid/silhouette/edge validation across all views | `multiview-fit-loop/MANUAL.md` |
| `fit-repair-optimizer` | Turn a fit report into a sequential/parallel repair queue; trigger self-refinement when the real gap is a missing skill | `fit-repair-optimizer/MANUAL.md` |
| `landmark-fit-repair` | bbox/IoU is insufficient and the model must align at designed feature points — leaf tips, shell corners, eyes, smile, rim thickness, aura centre/radius | `landmark-fit-repair/MANUAL.md` |
| `reference-look-calibration` | Materials, lighting, crop, emission/glow, colour management or aura styling must match a source image — calibrated against measured colour/brightness/saturation/bbox/mask statistics | `reference-look-calibration/MANUAL.md` |

## Related

- Mesh-from-contour and DXF-style surface construction → `contour-to-mesh`, `wireframe-to-3d` in `../02-modeling/INDEX.md`
- Making a texture pack fit 1:1 → `atlas-uv-fitting`, `closed-surface-uv-coverage` in `../03-surfacing/INDEX.md`
- Conflicting skills on the same artifact → `blender-skill-harmonizer` in `../01-orchestration/INDEX.md`
