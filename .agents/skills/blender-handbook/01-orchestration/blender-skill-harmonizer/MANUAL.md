---
name: blender-skill-harmonizer
description: Resolve actual conflicts between active Blender manuals about source policy, object ownership or execution order, then return control to one workflow owner. Also provides a standalone handbook structure audit.
when_to_use: Conflicting instructions or handoff policies, or an explicitly requested handbook structure audit; not every multi-phase Blender task.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info
---

# Blender Skill Harmonizer

This is the meta-layer for the Blender skill stack. It prevents independently useful skills from producing incoherent work when combined.

Use a **Merge → Consistency → Optimize → Store** cycle:

1. **Merge:** list all triggered skills and their intended outputs.
2. **Consistency:** detect conflicts in assumptions, coordinate systems, source hierarchy, object naming, or validation gates.
3. **Optimize:** choose one orchestrator, one source-of-truth policy, and a staged/parallel execution plan.
4. **Return:** hand the resolved policy back to the selected workflow owner. Keep decisions in the response or required validation artifact; persist lessons only when explicitly requested.

## Skill category map

- **Top-level orchestrators:** `blender-skill`, `quality-refinement-autoloop`, `mascot-logo-reconstruction`.
- **General production:** `blender-pro-workflow`, `blender-modeling`, `blender-materials`, `blender-lighting`, `blender-cameras`, `blender-rendering`, `blender-animation`, `blender-export`.
- **Reference reconstruction:** `reference-to-3d`, `wireframe-to-3d`, `reference-analysis-validator`, `source-part-segmentation`, `orthographic-registration`, `multiview-constraint-solver`, `contour-to-mesh`, `texture-driven-mesh-fitting`, `landmark-fit-repair`, `multiview-fit-loop`, `fit-repair-optimizer`.
- **Texture/UV:** `blender-uv-texturing`, `atlas-uv-fitting`, `closed-surface-uv-coverage`.
- **Look calibration:** `reference-look-calibration`.
- **Animation/motion design:** `texture-state-animation`, `orbital-hud-motion`, `animation-quality-gate`, coordinated by `blender-animation`.
- **Task-specific/full workflow:** `mascot-logo-reconstruction`.

## Activation and ownership

Follow `../../references/intent-routing.md`, the authority for workflow selection. Enter this manual only for an actual conflict between active manuals; a multi-phase request alone does not require harmonization. Select one owner and return to it once the conflict is resolved.

For reference-locked work, resolve source disagreement before geometry, geometry before final UV fitting, and visual/target-format validation before final export. Only include stages required by the source and requested deliverable. Animation follows accepted static geometry and needs animation QA before animated export.

## Conditional artifact contracts

Produce the artifacts required by the active stages, not a fixed bundle for every task:

- source reconstruction: `reference_manifest.json`;
- multi-view registration: `registration_report.json`;
- atlas fitting: `atlas_regions.json`;
- multi-view validation: fit report and relevant overlays;
- failed dependency gates: a repair queue if needed to coordinate repairs.

Ordinary material edits, lighting adjustments and exports do not need unrelated source reports. Do not create build notes or planning documents unless requested or required by the project. See `references/handoff-contracts.md` for reference-workflow handoffs.

## Conflict rules

- **Source conflict beats implementation.** If templates disagree, stop claiming final fit and write a conflict report.
- **Front-view brand read beats side/back/top unless canonical policy says otherwise.**
- **Reference-locked geometry beats generic modeling.** Do not primitive-first rebuild after a contour/source mask exists.
- **UV/texture fit waits for geometry lock.** Texture audit may run in parallel, but final UV assignment waits.
- **Lighting/look waits for material and camera lock.** Do not tune lights to compensate for wrong geometry.
- **Export waits for validation.** No final GLB without pass/fail reports.

## Sequential vs parallel orchestration

Sequential gates:

1. source conflict / multiview rigidity
2. structural part count
3. front geometry
4. multiview geometry
5. UV/material texture fit
6. lighting/look
7. export/animation

Parallel lanes allowed after their blockers clear:

- atlas region classification can run while geometry is being repaired;
- lighting reference statistics can run while UVs are being prepared;
- export target checks can run while visual validation is pending;
- validation tooling improvements can run anytime, but must not mutate product geometry.

## Read when needed

- `references/handoff-contracts.md` for exact input/output contracts between skills.

## Script

- `scripts/skill_graph_audit.py --skill-root <absolute-handbook-root>` checks index coverage, manual names, explicit resource paths, Python syntax and eval JSON. It writes JSON to stdout (optional `--out`) and exits nonzero on errors; it does not prove live Blender behavior. No manifest is required.


## Animation handoff rule

For reference-locked mascots/logos, animation is not a generic spin/pulse task. Use `texture-state-animation` for material/texture state changes, `orbital-hud-motion` for circles/HUD/aura, and `animation-quality-gate` before accepting or exporting. If animation fails, diagnose the failed dimension and follow artifact recovery; skill edits require a separate explicit request.

## Closed-surface coverage handoff rule

For closed or extruded reference-locked assets, front texture fit is not enough. Before look-dev or animation acceptance, run `closed-surface-uv-coverage` to verify that front cap, back cap, and sidewall surfaces each have explicit UV/generated/procedural coverage. Curves, planes, HUD, and aura elements are accents only and do not count as surface texture fill.

## Quality-refinement autoloop handoff rule

When a user rejects output quality, or repeated failures show missing skill depth, do not continue blind retries. Invoke `quality-refinement-autoloop`: preserve the baseline, capture evidence, classify failure dimension, decide whether existing skills are sufficient, repair the artifact with the existing methods, then revalidate. Skill maintenance and publication prep occur only when explicitly requested.
