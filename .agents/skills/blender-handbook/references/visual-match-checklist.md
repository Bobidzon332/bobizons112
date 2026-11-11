# Visual Match Checklist

Use when the result must look like a supplied photo, concept, template, or reference sheet.

Compare at the same crop and scale, then check:

- [ ] Silhouette matches the reference; no extra or missing major parts.
- [ ] Part count and part placement match.
- [ ] Proportions match real-world dimensions in `${COMMANDCODE_SKILL_DIR}/references/common-object-dimensions.md`.
- [ ] Camera crop and focal length match the reference framing.
- [ ] Colour, brightness, and saturation are within the tolerance of the source image.
- [ ] Emission / glow strength and halo extent match the source.
- [ ] Materials read the same way at thumbnail size and at 100% zoom.
- [ ] No clipping, magenta world, or subject-in-shadow artifacts.

For measurable colour, bbox, mask, and silhouette checks use `reference-look-calibration` and `reference-analysis-validator`.
