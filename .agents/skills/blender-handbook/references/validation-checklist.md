# Validation Checklist

Run this before export or before reporting an asset complete.

- [ ] Object names follow `${COMMANDCODE_SKILL_DIR}/references/naming-conventions.md`.
- [ ] Collections are named and organized; no stray `Cube.027`-style names.
- [ ] Triangle count is within `${COMMANDCODE_SKILL_DIR}/references/polycount-budgets.md` or an explicit project budget.
- [ ] Topology is quad-dominant where deformation or subdivision matters.
- [ ] UVs have no obvious stretch; texel density is consistent within the asset.
- [ ] Materials use supported nodes (Principled BSDF for exported assets).
- [ ] Collision meshes use the engine's expected naming and convex shapes.
- [ ] LODs exist where the target platform requires them.
- [ ] Output file exists at the reported absolute path and opens.
- [ ] Visual checkpoint passed: `${COMMANDCODE_SKILL_DIR}/references/output-and-reporting.md`.
- [ ] Reference-matched work also passes `${COMMANDCODE_SKILL_DIR}/references/visual-match-checklist.md`.
