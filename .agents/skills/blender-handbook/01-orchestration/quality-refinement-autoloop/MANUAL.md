---
name: quality-refinement-autoloop
description: Diagnose recurring or unexplained Blender quality failures, preserve the baseline, repair the artifact and verify the failed workflow. Skill maintenance and publication are separate modes used only when explicitly requested.
when_to_use: Recurring visual mismatch, failed validation, rejected animation or export, unclear failure causes; explicit requests to improve the handbook or prepare an upstream release.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info
---

# Quality Recovery and Optional Skill Maintenance

Follow `../../references/intent-routing.md` for activation and ownership. The default goal is to repair the user's artifact within the existing scope.

## Artifact recovery (default)

1. Preserve the last accepted baseline and collect the smallest evidence set: feedback, source, output and a relevant render, contact sheet or validation report.
2. Identify the failed dimension: geometry, multi-view depth, UV/coverage, look, animation, export compatibility or conflicting instructions.
3. Select the existing domain repair method. Consult the harmonizer only for an actual ownership/order conflict. A missing recipe is not permission to edit the installed skill; inspect current APIs or matching documentation when needed.
4. Make a bounded repair, then rerun the failed workflow and its visual/format gate. Do not mask geometry errors with lighting or claim runtime support from a Blender-only effect.
5. After 3 unsuccessful change/verify cycles for the same issue, stop modifications and re-check requirements, evidence and the hypothesis. Resume only with a materially better hypothesis or a user-approved route. Do not restart the counter by entering another manual. Respect earlier domain stops.

Use existing project artifacts and concise response updates. Do not require separate plan, lesson, sanitization or release reports for an ordinary repair. If a capability or source is missing, state the concrete limitation rather than looping indefinitely.

## Skill maintenance (explicit request only)

When the user asks to improve the skill itself:

1. Demonstrate the reusable gap from evidence; make the smallest change to the relevant rule or helper.
2. Remove private paths, project-specific data, credentials and copyrighted source content from reusable guidance. Sanitization does not authorize persistent memory writes.
3. Run `../blender-skill-harmonizer/scripts/skill_graph_audit.py --skill-root <absolute-handbook-root>` and focused behavior checks for changed helpers. Script syntax and link checks are not runtime proof.
4. Resume artifact work only if it remains in the authorized task. Do not add version/manifest files to this standalone handbook just to satisfy an upstream plugin layout.

## Publication (explicit request only)

For a requested commit/push, inspect the actual repository, branch, status, remote and diff; include only authorized changes. Use upstream versioning/release checks only in their corresponding repository layout. Do not publish during artifact recovery.

## Helpers

- `scripts/ralph_autoloop_plan.py`: optional feedback classification; defaults to artifact recovery, with `--skill-maintenance` only for an explicitly requested maintenance task. Its keyword hints are not a diagnosis.
- `scripts/sanitize_skill_contributions.py`: optional scan when preparing reusable skill changes.
- `scripts/release_readiness_check.py`: upstream plugin repository release checks only. It reports an incompatible layout for an installed handbook; use the graph audit above here.
