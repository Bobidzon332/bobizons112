---
name: blender-references
description: Shared Blender production reference sheets used by the blender-* skills - asset pipeline phases, naming conventions (SM_/MAT_/COL_ prefixes), polycount budgets, validation and visual-match checklists, reference-image matching, reference-analysis template, Blender MCP integration and tool catalog. Read when a blender-* skill links ../blender-references/<file>.md, or when you need these studio standards directly.
metadata:
  origin: arjun988/blender-skills .claude/skills/references (shared folder, not a skill upstream)
---

# Blender shared references

This folder holds the shared reference documents from [arjun988/blender-skills](https://github.com/arjun988/blender-skills)
(`.claude/skills/references/`). Upstream they were a plain folder next to the skills; it was given this SKILL.md during
import so every folder in `.agents/skills/` is a valid, discoverable skill.

| File | Use for |
|------|---------|
| [asset-pipeline.md](asset-pipeline.md) | Phase-by-phase production pipeline and hand-offs |
| [naming-conventions.md](naming-conventions.md) | Object, material, collection and texture prefixes |
| [polycount-budgets.md](polycount-budgets.md) | Triangle budgets per asset class and platform |
| [validation-checklist.md](validation-checklist.md) | Ship/no-ship asset checks |
| [visual-match-checklist.md](visual-match-checklist.md) | Comparing renders against references |
| [reference-image-match.md](reference-image-match.md) | Matching a reference photo or concept |
| [reference-analysis-template.md](reference-analysis-template.md) | Structured reference breakdown |
| [mcp-integration.md](mcp-integration.md) | Working through a Blender MCP server |
| [mcp-tools.md](mcp-tools.md) | MCP tool catalog and bpy fallbacks |

For Roblox targets, budgets and export settings in the `roblox-*` skills (e.g. `roblox-3d-model`) take precedence over the
generic engine budgets here.
