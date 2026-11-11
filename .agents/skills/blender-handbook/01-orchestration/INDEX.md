# 01 — Orchestration

**Open this when** the request spans multiple phases or skills, when two skills disagree about the same artifact, when the user has rejected a result and you need to diagnose *why* rather than retry blindly, or when you are driving the NIUA finisher MCP.

Paths below are relative to this file's own directory.

| Manual | Use when | Path |
|--------|----------|------|
| `blender-pro-workflow` | You need the end-to-end order for a complete scene/hero shot, critique protocols, time budgets, or a recovery pattern for a multi-phase job going wrong | `blender-pro-workflow/MANUAL.md` |
| `blender-skill-harmonizer` | Two or more skills want to act on the same artifact and you must decide precedence; or a task is reference-locked and needs handoff gates and a conflict policy | `blender-skill-harmonizer/MANUAL.md` |
| `quality-refinement-autoloop` | Output was rejected, the same issue keeps recurring, or the user asks to improve the skill stack before retrying. Diagnoses the gap and repairs the artifact; skill edits and publication require an explicit maintenance request | `quality-refinement-autoloop/MANUAL.md` |
| `niua-blender-finisher` | Driving the NIUA Blender Finisher MCP (`blender-finisher`, `feedback-critique`, `feedback-capture`, `system-execute_python`, mesh observation) without exploding the token window | `niua-blender-finisher/MANUAL.md` |

## Not here

- The MCP transport itself (install, client wiring, port 9876, safe mode, connection troubleshooting) → the separate **`blender-mcp`** skill.
- Choosing a *look* for the scene → `10-art-direction/`.
