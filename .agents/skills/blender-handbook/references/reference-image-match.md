# Reference Image Matching

Use this when a photo, concept art, or reference sheet is attached and the render must match it.

1. Record the source image as the target crop, lighting direction, palette, and subject scale.
2. Match camera first: focal length, framing, and subject placement.
3. Match value structure before colour: the darkest darks and brightest brights should land in the same places.
4. Match material read under that lighting: roughness variation, edge highlights, subsurface warmth.
5. Compare the render and source at thumbnail size and at 100% zoom.
6. If the mismatch is structural (wrong part count, wrong silhouette, wrong feature position), stop rendering and route to `08-reference-locked/` — this is a fit problem, not a lighting problem.

For calibrated adjustments use `reference-look-calibration`; for final gating use `${COMMANDCODE_SKILL_DIR}/references/visual-match-checklist.md`.
