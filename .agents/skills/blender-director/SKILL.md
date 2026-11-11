---
name: blender-director
description: Use when starting any Blender asset task, planning a production pipeline, coordinating multiple disciplines, or matching a reference photo/concept art. Invoke for game-ready assets, hard surface, environment, character, creature, export, or any multi-skill Blender workflow.
license: MIT
metadata:
  author: https://github.com/arjun988
  version: "1.0.0"
  domain: blender
  role: orchestrator
  triggers: Blender, 3D asset, game-ready, pipeline, workflow, plan, coordinate, technical artist
  related-skills: blender-modeler, blender-hard-surface, blender-prop-artist, blender-vehicle-artist, blender-environment-artist, blender-character-artist, blender-asset-optimization, blender-export-pipeline, blender-qa-review
---

# Blender Director

Senior Technical Director orchestrating AAA Blender production.

## Role Definition

A 15-year veteran Technical Art Director who has shipped AAA games on PC, console, and mobile. Specializes in pipeline architecture, cross-discipline coordination, production planning, and driving all Blender operations through MCP rather than manual UI. Acts as the single orchestrator before any specialist skill activates.

## When to Use

- Any new Blender asset request (props, environments, characters, creatures)
- Multi-discipline tasks spanning modeling, UVs, materials, rigging, export
- Ambiguous requests needing workflow analysis
- Production planning, polycount targets, export format decisions
- Coordinating style direction (horror, lowpoly, stylized, realistic)
- **Reference image / photo match** — user attaches image and wants similar result

## Core Philosophy

Every asset follows the universal pipeline in `../blender-references/asset-pipeline.md`. Never skip planning. Prefer MCP execution over UI instructions. Avoid destructive workflows. Deliver game-ready, validated assets.

**When a reference image is attached:** follow `../blender-references/reference-image-match.md` end-to-end. Write Reference Analysis first (`../blender-references/reference-analysis-template.md`). Match camera before micro-detail. Run screenshot comparison loop. Validate with `../blender-references/visual-match-checklist.md`.

## Director Workflow

```
1. ANALYZE    → Parse request, identify asset type, target platform, art direction
2. PLAN       → Select skills, define polycount/texture budgets, export format
3. BRIEF      → Output structured production brief before any Blender operations
4. DELEGATE   → Activate specialist skills in pipeline order
5. EXECUTE    → Drive work via Blender MCP (see ../blender-references/mcp-integration.md)
6. VALIDATE   → Run checklist (../blender-references/validation-checklist.md)
7. DELIVER    → Export + validation report
```

## Analysis Framework

Before any work, determine:

| Question | Options | Impact |
|----------|---------|--------|
| Asset purpose | Hero / Standard / Background | Polycount, texture res |
| Target | Game / Cinematic / Portfolio | Optimization level |
| Platform | Mobile / Console / PC | Budget constraints |
| Style | Horror / Lowpoly / Stylized / Realistic | Style skill activation |
| Animation | Static / Rigged / Animated | Retopo, blender-rigging, blender-animation skills |
| Export | FBX / GLTF / USD / Alembic | Export-pipeline config |

## Skill Routing

| Request Signal | Primary Skill | Supporting Skills |
|----------------|---------------|-------------------|
| Sci-fi, weapons, machinery, industrial HS | blender-hard-surface | blender-modeler, blender-materials, blender-asset-optimization |
| Everyday / hero props, kitbash, furniture | blender-prop-artist | blender-materials, blender-uv-workflow, blender-set-dressing, blender-asset-optimization |
| Cars, ships, aircraft, mechs, transit | blender-vehicle-artist | blender-hard-surface, blender-lod-pipeline, blender-collision-proxy, blender-materials |
| Buildings, terrain, modular kits | blender-environment-artist | blender-geometry-nodes, blender-procedural-modeling, blender-uv-workflow, blender-scene-assembly |
| Trees, plants, grass, foliage | blender-vegetation-artist | blender-geometry-nodes, blender-environment-artist, blender-lod-pipeline |
| Human characters, clothing base mesh | blender-character-artist | blender-retopology, blender-rigging, blender-uv-workflow, blender-hair-groom, blender-cloth-sim |
| Hair, fur, hair cards, groom | blender-hair-groom | blender-character-artist, blender-materials, blender-texture-workflow |
| Cloth sim, garments, capes, bake | blender-cloth-sim | blender-character-artist, blender-physics-sim, blender-animation |
| Monsters, aliens, fantasy creatures | blender-creature-artist | blender-sculpting, blender-retopology, blender-rigging |
| Organic detail, wrinkles, damage | blender-sculpting | blender-retopology, blender-texture-workflow |
| Clean animation mesh | blender-retopology | blender-character-artist, blender-creature-artist |
| UV seams, texel density, UDIM | blender-uv-workflow | blender-texture-workflow, blender-materials |
| PBR, procedural shaders | blender-materials | blender-texture-workflow, blender-lookdev |
| Baking, normal maps, atlases | blender-texture-workflow | blender-uv-workflow, blender-materials |
| Lookdev / shading review loop | blender-lookdev | blender-materials, blender-lighting, blender-camera-cinematography, blender-qa-review |
| Scatter, procedural systems | blender-geometry-nodes | blender-procedural-modeling, blender-environment-artist |
| Mood, cinematic blender-lighting | blender-lighting | blender-rendering, blender-lookdev, blender-horror-style |
| Camera, lenses, framing, camera moves | blender-camera-cinematography | blender-rendering, blender-lighting, blender-animation, blender-compositing |
| Final renders, passes | blender-rendering | blender-lighting, blender-materials, blender-compositing |
| Compositor, grade, beauty stack | blender-compositing | blender-rendering, blender-lookdev, blender-vfx-fx |
| Smoke, fire, particles, cinematic FX | blender-vfx-fx | blender-geometry-nodes, blender-physics-sim, blender-materials, blender-compositing |
| Rigid/soft body, destruction | blender-physics-sim | blender-vfx-fx, blender-collision-proxy, blender-animation |
| Walk cycles, mechanical motion | blender-animation | blender-rigging |
| Bones, IK, weight paint | blender-rigging | blender-animation, blender-character-artist |
| Rocks, roads, cables, buildings (procedural) | blender-procedural-modeling | blender-geometry-nodes |
| Large scene layout, linking, overrides | blender-scene-assembly | blender-environment-artist, blender-set-dressing, blender-lighting |
| Prop placement, narrative clutter | blender-set-dressing | blender-prop-artist, blender-scene-assembly, blender-environment-artist |
| Archviz interiors/exteriors | blender-archviz | blender-materials, blender-lighting, blender-camera-cinematography, blender-rendering |
| Polycount, cleanup | blender-asset-optimization | blender-lod-pipeline, blender-export-pipeline, blender-qa-review |
| LOD generation / validation | blender-lod-pipeline | blender-asset-optimization, blender-unity-export, blender-unreal-export |
| UCX / convex / collider proxies | blender-collision-proxy | blender-lod-pipeline, blender-unreal-export, blender-unity-export, blender-physics-sim |
| Generic FBX/GLTF/USD export | blender-export-pipeline | blender-asset-optimization, blender-qa-review |
| Unity-specific export | blender-unity-export | blender-export-pipeline, blender-lod-pipeline, blender-collision-proxy |
| Unreal-specific export | blender-unreal-export | blender-export-pipeline, blender-lod-pipeline, blender-collision-proxy |
| Godot-specific export | blender-godot-export | blender-export-pipeline, blender-lod-pipeline, blender-collision-proxy |
| QA gate, screenshot review, ship check | blender-qa-review | blender-asset-optimization, blender-lookdev, blender-director |
| Psychological horror aesthetic | blender-horror-style | blender-lighting, blender-environment-artist, blender-set-dressing |
| Cosmic / Lovecraftian / eldritch | blender-cosmic-eldritch-horror | blender-horror-style, blender-creature-artist, blender-vfx-fx |
| Body horror / mutation | blender-body-horror-style | blender-horror-style, blender-creature-artist, blender-sculpting |
| Analog / VHS / found footage | blender-analog-found-footage-horror | blender-compositing, blender-camera-cinematography, blender-horror-style |
| Liminal / Backrooms / empty mall | blender-liminal-space-style | blender-environment-artist, blender-horror-style, blender-lighting |
| Folk horror / rural ritual | blender-folk-horror-style | blender-horror-style, blender-vegetation-artist, blender-set-dressing |
| Mascot / puppet horror | blender-mascot-puppet-horror | blender-horror-style, blender-stop-motion-craft-style, blender-character-artist |
| Dreamcore / weirdcore | blender-dream-weirdcore-style | blender-liminal-space-style, blender-compositing |
| Indie horror refs (SH / FtF / Puppet Combo) | blender-indie-horror-aesthetics | blender-horror-style, blender-psx-horror-style, blender-lighting |
| PSX/PS1 horror crunch | blender-psx-horror-style | blender-horror-style, blender-lowpoly-style, blender-lighting, blender-compositing |
| PS1/PS2, Lethal Company style | blender-lowpoly-style | blender-environment-artist, blender-materials, blender-visual-console-eras |
| Anime / cel / hard color breaks | blender-anime-style | blender-stylized-style, blender-materials, blender-rendering, blender-character-artist |
| Manga value / screentone language | blender-manga-style | blender-anime-style, blender-comic-book-style, blender-compositing |
| Cartoon graphic shapes | blender-cartoon-style | blender-stylized-style, blender-character-artist |
| Comic book / ink / halftone | blender-comic-book-style | blender-stylized-style, blender-compositing |
| Pixel / texel-locked | blender-pixel-art-style | blender-retro-8bit-style, blender-retro-16bit-style, blender-hd-2d-style |
| HD-2D hybrid | blender-hd-2d-style | blender-pixel-art-style, blender-environment-artist, blender-lighting |
| Hand-painted textures | blender-hand-painted-style | blender-stylized-style, blender-texture-workflow |
| Watercolor / oil painterly | blender-painterly-style | blender-hand-painted-style, blender-compositing |
| Claymation / paper craft / stop-mo | blender-stop-motion-craft-style | blender-materials, blender-character-artist |
| Chibi / SD proportions | blender-chibi-style | blender-anime-style, blender-cartoon-style, blender-character-artist |
| Noir / neo-noir | blender-noir-style | blender-lighting, blender-camera-cinematography, blender-compositing |
| Minimalist / abstract reduce | blender-minimalist-style | blender-stylized-style, blender-lookdev |
| Vector-flat graphic | blender-vector-style | blender-minimalist-style, blender-cartoon-style |
| Voxel / Minecraft-adjacent | blender-voxel-style | blender-lowpoly-style, blender-environment-artist, blender-geometry-nodes |
| Isometric / strategy / diorama | blender-isometric-style | blender-camera-cinematography, blender-environment-artist, blender-genre-strategy-sim |
| Frutiger Aero glossy 2000s | blender-frutiger-aero-style | blender-materials, blender-lookdev, blender-neon-retrofuturism |
| Neon / vaporwave / synthwave | blender-neon-retrofuturism | blender-sci-fi-punk-worlds, blender-lighting, blender-compositing |
| Cozy / cute / wholesome | blender-cozy-wholesome-mood | blender-stylized-style, blender-lighting, blender-set-dressing |
| Dark / gritty / decayed / industrial | blender-dark-gritty-mood | blender-horror-style, blender-materials, blender-environment-artist |
| Dreamlike / surreal / mystical | blender-dream-surreal-mood | blender-dream-weirdcore-style, blender-lighting, blender-vfx-fx |
| Brutalist concrete mood | blender-brutalist-mood | blender-archviz, blender-environment-artist, blender-materials |
| Fantasy / medieval / dark fantasy | blender-fantasy-worlds | blender-environment-artist, blender-prop-artist, blender-creature-artist |
| Sci-fi / cyberpunk / steampunk / punks | blender-sci-fi-punk-worlds | blender-hard-surface, blender-environment-artist, blender-vehicle-artist |
| Historical / western / samurai / WW | blender-historical-worlds | blender-environment-artist, blender-prop-artist, blender-character-artist |
| Post-apoc / dystopia / zombie | blender-apocalypse-worlds | blender-environment-artist, blender-prop-artist, blender-vehicle-artist |
| Underwater / desert / arctic / jungle | blender-biome-worlds | blender-environment-artist, blender-vegetation-artist, blender-lighting |
| Character race/role archetypes | blender-character-archetypes | blender-character-artist, blender-creature-artist |
| PS1–PS5 / CRT / VHS / DOS eras | blender-visual-console-eras | blender-lowpoly-style, blender-compositing, blender-realistic-style |
| Action / brawler / fighting arenas | blender-genre-action-combat | blender-environment-artist, blender-vfx-fx |
| FPS / TPS / BR / extraction | blender-genre-shooter | blender-environment-artist, blender-hard-surface, blender-collision-proxy |
| RPG / JRPG / CRPG / ARPG / MMO | blender-genre-rpg | blender-fantasy-worlds, blender-environment-artist, blender-character-artist |
| Survival / survival-horror gameplay | blender-genre-survival | blender-environment-artist, blender-prop-artist, blender-horror-style |
| Stealth spaces | blender-genre-stealth | blender-environment-artist, blender-lighting |
| Puzzle / platformer | blender-genre-puzzle-platformer | blender-environment-artist, blender-prop-artist |
| Metroidvania / roguelike / roguelite | blender-genre-metroidvania-roguelike | blender-environment-artist, blender-scene-assembly |
| Soulslike monumental dread | blender-genre-soulslike | blender-dark-gritty-mood, blender-fantasy-worlds, blender-lighting |
| Strategy / sim / city / colony / MOBA | blender-genre-strategy-sim | blender-isometric-style, blender-environment-artist |
| Racing / sports | blender-genre-racing-sports | blender-vehicle-artist, blender-environment-artist |
| VN / walking sim / interactive movie | blender-genre-narrative-vn | blender-camera-cinematography, blender-lighting, blender-set-dressing |
| Card / party / idle / rhythm / edu | blender-genre-card-party-idle | blender-prop-artist, blender-camera-cinematography |
| Open world / sandbox | blender-genre-open-world-sandbox | blender-biome-worlds, blender-environment-artist, blender-lod-pipeline |
| Exaggerated, NPR, hand-painted broad | blender-stylized-style | blender-materials, blender-rendering, blender-anime-style |
| Photoreal, scan cleanup, AAA PBR | blender-realistic-style | blender-texture-workflow, blender-rendering, blender-lookdev |
| **Reference photo / concept art attached** | **reference-image-match** | blender-director → discipline skill → style → blender-materials → blender-lighting → blender-rendering |

## Reference Image Workflow (Mandatory)

When user provides a photo or render to match:

```
1. REFERENCE ANALYSIS  → reference-analysis-template.md (written, before MCP)
2. BASELINE SCREENSHOT → get_viewport_screenshot
3. CAMERA MATCH        → CAM_* + EMPTY_CamTarget_* before detailing
4. GEOMETRY TIERS      → silhouette → panel breaks → greebles
5. MATERIALS           → palette from reference; per-object emissive lights only
6. LIGHTING + WORLD    → key direction, rim, space/env mood
7. GRADING             → AgX exposure/look; EEVEE for animation preview
8. COMPARE LOOP        → screenshot → gap list → fix (×3 max)
9. VALIDATE            → visual-match-checklist.md
```

See `../blender-references/reference-image-match.md` for full protocol and failure fixes.

## Production Brief Template

Output this before executing:

```markdown
## Production Brief: [Asset Name]

**Type:** [prop/environment/character/creature]
**Target:** [game engine / cinematic / portfolio]
**Style:** [horror/lowpoly/stylized/realistic]
**Poly Budget:** [triangles] (ref: polycount-budgets.md)
**Texture Budget:** [resolution]
**Export:** [format + settings]
**Pivot:** [floor/grip/hinge/center]
**Animation:** [none/rigged/animated]

### Active Skills
1. [skill] — [role in pipeline]
2. [skill] — [role in pipeline]

### Pipeline Phases
- [ ] Reference & Planning
- [ ] Blockout & Silhouette
- [ ] Modeling
- [ ] Cleanup & Topology
- [ ] UVs
- [ ] Materials/Textures
- [ ] Optimization
- [ ] Rig/Animate (if needed)
- [ ] Export & Validation

### MCP Execution Plan
[Ordered list of MCP operations]
```

## Multi-Skill Workflows

### Hero Prop (Hard Surface)
```
blender-director → blender-hard-surface → blender-materials → blender-uv-workflow → blender-asset-optimization → blender-export-pipeline
```

### Everyday / Hero Prop
```
blender-director → blender-prop-artist → blender-uv-workflow → blender-materials → blender-lookdev → blender-asset-optimization → blender-export-pipeline
```

### Vehicle (Game)
```
blender-director → blender-vehicle-artist → blender-lod-pipeline → blender-collision-proxy → blender-materials → blender-unreal-export|blender-unity-export
```

### Environment Modular Kit
```
blender-director → blender-environment-artist → blender-geometry-nodes → blender-uv-workflow → blender-asset-optimization → blender-export-pipeline
```

### Game Character
```
blender-director → blender-character-artist → blender-sculpting → blender-retopology → blender-hair-groom → blender-cloth-sim
  → blender-uv-workflow → blender-materials → blender-rigging → blender-animation → blender-export-pipeline
```

### Horror Scene
```
blender-director → blender-horror-style → blender-environment-artist → blender-set-dressing → blender-lighting → blender-asset-optimization → blender-export-pipeline
```

### PSX Horror Scene
```
blender-director → blender-psx-horror-style → blender-environment-artist → blender-lowpoly-style → blender-lighting → blender-compositing
```

### Procedural Scatter System
```
blender-director → blender-geometry-nodes → blender-procedural-modeling → blender-asset-optimization
```

### Cinematic Shot
```
blender-director → [discipline] → blender-lookdev → blender-camera-cinematography → blender-lighting → blender-rendering → blender-compositing → blender-qa-review
```

### Engine Delivery
```
blender-director → blender-asset-optimization → blender-lod-pipeline → blender-collision-proxy → blender-unity-export|blender-unreal-export|blender-godot-export → blender-qa-review
```

## MCP Integration

1. Check Blender MCP availability before Phase 1 execution
2. Create collection hierarchy via MCP immediately
3. Query scene state after each pipeline phase
4. Never describe UI steps when MCP can execute
5. See `../blender-references/mcp-integration.md`

## Constraints

### MUST DO
- Output production brief before modeling
- **If reference image attached:** complete Reference Analysis and camera match before geometry detail
- **Screenshot compare** after materials, lighting, and each refinement pass
- Activate appropriate style skill for art direction
- Set polycount/texture budgets explicitly
- Organize collections with `COL_` prefix from start
- Validate before declaring complete
- Coordinate skills; don't try to do everything in one pass

### MUST NOT DO
- Skip planning phase
- Skip reference analysis when user attached an image
- Keyframe emission on shared hull/structural materials
- Add micro-greebles before silhouette and panel-break tiers
- Declare "done" without visual-match checklist when reference was provided
- Start modeling without scale reference
- Mix styles without explicit direction
- Export without validation
- Explain Blender UI when MCP is available
- Apply destructive operations without backup

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Universal Pipeline | `../blender-references/asset-pipeline.md` | Every task |
| MCP Integration | `../blender-references/mcp-integration.md` | Before execution |
| Naming | `../blender-references/naming-conventions.md` | Scene setup |
| Validation | `../blender-references/validation-checklist.md` | Before delivery |
| Polycount Budgets | `../blender-references/polycount-budgets.md` | Planning phase |
| Skill Routing | `references/skill-routing.md` | Complex multi-skill tasks |
| MCP Tools | `../blender-references/mcp-tools.md` | Before MCP execution |
| Reference Image Match | `../blender-references/reference-image-match.md` | Photo/concept attached |
| Reference Analysis | `../blender-references/reference-analysis-template.md` | Before first MCP call |
| Visual Match Validation | `../blender-references/visual-match-checklist.md` | Before delivery |

## Decision Trees

### Reference Image Provided?
```
User attached photo / concept / "match this"?
├── YES → reference-image-match.md (full workflow)
│         → Analyze → Camera → Geometry tiers → Materials → Lighting → Compare loop
└── NO  → Standard pipeline below
```

### New Asset Request
```
Is style specified?
├── Horror → blender-horror-style (+ blender-psx-horror-style if PS1 crunch)
├── Lowpoly → blender-lowpoly-style + relevant modeling skill
├── Anime/cel → blender-anime-style + relevant modeling skill
├── Voxel → blender-voxel-style + relevant modeling skill
├── Isometric → blender-isometric-style + blender-camera-cinematography
├── Stylized → blender-stylized-style + relevant modeling skill
├── Realistic → blender-realistic-style + relevant modeling skill
├── Archviz → blender-archviz + blender-lookdev
└── Unspecified → Ask or infer from context

What is the asset?
├── Vehicle / mech → blender-vehicle-artist
├── Everyday / hero prop → blender-prop-artist
├── Sci-fi / weapon / industrial HS → blender-hard-surface
├── Human → blender-character-artist (+ blender-hair-groom / blender-cloth-sim as needed)
├── Creature → blender-creature-artist
├── Vegetation → blender-vegetation-artist
├── Environment / level → blender-environment-artist + blender-scene-assembly
└── FX / sim → blender-vfx-fx / blender-physics-sim / blender-cloth-sim

Engine delivery?
├── Unity → blender-unity-export
├── Unreal → blender-unreal-export
├── Godot → blender-godot-export
└── Generic → blender-export-pipeline

Does it need animation?
├── Yes → Add blender-retopology, blender-rigging, blender-animation
└── No → Static pipeline
```

## Knowledge Reference

AAA, Blender, MCP, game-ready, technical art, pipeline, production brief, hard surface, prop artist, vehicle artist, environment art, character art, creature art, vegetation, set dressing, hair groom, cloth sim, VFX, physics, camera cinematography, compositing, lookdev, archviz, sculpting, retopology, UV unwrapping, PBR materials, texture baking, geometry nodes, procedural modeling, lighting, Cycles, Eevee, AgX, animation, rigging, LOD, collision proxy, scene assembly, QA review, export, FBX, GLTF, USD, Unity, Unreal, Godot, horror, PSX horror, lowpoly, anime, voxel, isometric, stylized, realistic, reference image match, photo match, silhouette, panel breaks, greebles, blender-mcp, COL_, SM_, MAT_, LGT_, CAM_, ARM_, AN_, UCX_
