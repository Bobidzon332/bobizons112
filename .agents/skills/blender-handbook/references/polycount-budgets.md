# Polycount and Texture Budgets

Use these as starting ranges for a real-time target. The project's engine or art director overrides them.

| Asset class | LOD0 triangles | Texture budget (all maps) |
|-------------|----------------|---------------------------|
| Hero prop | 3k–12k | 2k–4k atlas |
| Character (real-time) | 20k–60k | 2k–4k atlas |
| Creature / organic hero | 25k–80k | 2k–4k atlas |
| Modular environment piece | 1k–5k | 1k–2k atlas |
| Vehicle hero | 30k–100k | 2k–4k atlas |
| Vegetation card / clump | 200–2k | 1k atlas |
| Background / dressing prop | 300–2k | 512–1k |

## Texture budgets

- Prefer one atlas per material family over many small maps.
- Bake AO, curvature, normal, and roughness once; reuse across LODs.
- Low-poly style can reduce triangle count by 50–90% while keeping silhouette readability.

## Enforcement points

- `../02-modeling/retopology/MANUAL.md` — enforce budget while building the low-poly mesh.
- `../07-delivery/asset-optimization/MANUAL.md` — audit before export.
- `../09-quality-gates/qa-review/MANUAL.md` — fail the gate when budget or naming is off.
