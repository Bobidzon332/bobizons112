# Project Skills: Roblox + Blender

165 skill folders live here: **52 Roblox** (`roblox-*`) and **113 Blender** (`blender-*`). That is 164 imported
skills plus `blender-references`, a support skill created to host shared reference sheets. Each folder is one skill:
`<skill-name>/SKILL.md` plus its own `references/`, `scripts/`, `assets/` etc. Agent Skills clients that scan
`.agents/skills/` (e.g. Codex CLI `/skills`) discover them automatically. The project's Master Instructions in
[`/AGENTS.md`](../../AGENTS.md) take precedence over any skill.

**Start here:** Roblox: `roblox-architecture` (project structure), `roblox-create-game` (end-to-end pipeline).
Blender: `blender-director` (production planning), `blender-handbook` (router), `blender-image-to-3d`
(game-ready asset from references). Blender -> Roblox assets: `roblox-3d-model`, `roblox-animation`,
`blender-export-pipeline`.

## Import summary

Imported from 10 public GitHub repositories at the commits listed in [THIRD_PARTY_NOTICES](../THIRD_PARTY_NOTICES.md).
No ZIP uploads, no whole-repository copies, no large media.

| Repository | SKILL.md files found | Distinct skills | Installed | Deduplicated | Excluded |
|---|---:|---:|---:|---:|---:|
| EL4CTEO/roblox-skills | 23 | 23 | 23 | 0 | 0 |
| SyphoDev-yt/roblox-ai-skills | 11 | 11 | 11 | 0 | 0 |
| TabooHarmony/roblox-brain | 29 | 29 | 18 | 11 (absorbed as supplements) | 0 |
| JustineDevs/roblox-ai-os | 108 | 62 (46 were identical plugin copies) | 0 | 7 | 55 |
| izzyfrm/roblox-ai | 0 | 0 (media-only library, ~1 GB) | 0 | 0 | 0 |
| arjun988/blender-skills | 188 | 94 (`.cursor/` mirrors `.claude/`) | 94 | 0 | 0 |
| mromidev/claude-blender-skills | 3 | 3 | 3 | 0 | 0 |
| kevinbadi/blender-skills | 16 | 16 | 13 | 2 (merged) | 1 |
| linnnn89/blenderskill | 1 (router over 123 manuals) | 1 | 1 | 93 duplicate manuals -> redirect stubs | 0 |
| majidmanzarpour/blender-game-skills | 1 | 1 | 1 | 0 | 0 |
| **Total** | **380** | **240** | **164** | **20 skills** | **56** |

## Roblox skills (52)

### Production pipelines & Studio (5)

| Skill | Source | What it is for |
|---|---|---|
| [`roblox-create-game`](roblox-create-game/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Take a Roblox game from a genre to something built, assembled, playable and published, ONE SECTION PER SESSION - research and plan, code, art, anim... |
| [`roblox-build-orchestrator`](roblox-build-orchestrator/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Runs a Roblox game build pipeline as a timed, logged run (market research, design, code, 3D/materials/UI/animation/VFX/SFX, assembly, playtest, pub... |
| [`roblox-skills-setup`](roblox-skills-setup/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Set up the free Roblox game-creation skills on THIS machine - check which tools are installed (Python, Rojo, Wally, Lune, Selene, StyLua, Blender,... |
| [`roblox-collaboration-mode`](roblox-collaboration-mode/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Load FIRST for any Roblox task: build, change, fix, debug, review, audit, or plan. |
| [`roblox-studio-mcp`](roblox-studio-mcp/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Drive Roblox Studio from an AI agent via the built-in Studio MCP server - connecting Claude Code, Codex, Cursor, OpenCode, Gemini CLI; tools to exp... |

### Architecture, Luau & tooling (9)

| Skill | Source | What it is for |
|---|---|---|
| [`roblox-architecture`](roblox-architecture/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Roblox project structure and client/server model - replication, where code and assets belong (ServerScriptService, ReplicatedStorage, StarterPlayer... |
| [`roblox-luau`](roblox-luau/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Modern, type-safe Luau for Roblox, covering --!strict and the new type solver, generics, string interpolation, if-expressions, task library, requir... |
| [`roblox-luau-core`](roblox-luau-core/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when writing, editing, or debugging any Luau: tables, control flow, string patterns, scope, closures, and errors ported from JS/Python. |
| [`roblox-luau-patterns`](roblox-luau-patterns/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when writing or refactoring Roblox Luau modules, object lifecycles, signals, task scheduling, pcall, and cleanup. |
| [`roblox-luau-types`](roblox-luau-types/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when adding or fixing Luau type annotations: generics, unions, narrowing, strict mode, sealed tables, module type exports, typed metatables. |
| [`roblox-code`](roblox-code/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Write the Luau for a Roblox game the way it survives contact with a real playtest - server-authoritative, Knit services and controllers, plain Remo... |
| [`roblox-tooling`](roblox-tooling/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Professional Roblox toolchain - Studio Script Sync vs Rojo, Rokit, Wally/pesde packages, luau-lsp with sourcemaps, StyLua, selene, darklua, Lune, r... |
| [`roblox-testing`](roblox-testing/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Testing Roblox code - testable modules with dependency injection, Jest Lua (runCLI, .spec files), legacy TestEZ, running tests in Studio, via Studi... |
| [`roblox-code-review`](roblox-code-review/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Review Roblox/Luau code for exploits, data loss, memory leaks, performance problems, lifecycle bugs, policy issues, and deprecated or superseded AP... |

### Networking, data, security & cloud (8)

| Skill | Source | What it is for |
|---|---|---|
| [`roblox-networking`](roblox-networking/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Client-server communication - RemoteEvent, UnreliableRemoteEvent, RemoteFunction, what survives serialization, typed remote modules, server validat... |
| [`roblox-security`](roblox-security/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Anti-exploit design - never trust the client, validate every remote argument (NaN, spoofed instances, strings), rate limiting, ProximityPrompt/Clic... |
| [`roblox-data-stores`](roblox-data-stores/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Persistence and cross-server data - DataStoreService (UpdateAsync, retries, budgets, limits), session locking with ProfileStore, schema migrations,... |
| [`roblox-data`](roblox-data/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when writing, changing, debugging, or auditing Roblox player saves: DataStore, ProfileStore, session locks, schemas, migrations. |
| [`roblox-server-data`](roblox-server-data/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when building or fixing Roblox cross-server data: OrderedDataStore leaderboards, MessagingService, MemoryStore, world state, seasons. |
| [`roblox-teleport-matchmaking`](roblox-teleport-matchmaking/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Multi-place and multi-server games - universes and places, TeleportAsync with TeleportOptions (ReservedServerId, VipServerId, specific servers, tel... |
| [`roblox-open-cloud`](roblox-open-cloud/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Open Cloud REST APIs and HttpService - API keys/OAuth, v2 patterns, data/memory stores from outside, publishMessage, place publishing, server resta... |
| [`roblox-cloud`](roblox-cloud/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use for Roblox Open Cloud: API keys, OAuth 2.0, webhooks, scopes, token lifecycle, DataStore or messaging access from outside the game. |

### Gameplay systems (8)

| Skill | Source | What it is for |
|---|---|---|
| [`roblox-game-systems`](roblox-game-systems/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Recipes for common systems built on server authority - currency service and leaderstats, XP/levels, round loops with intermission and teams, valida... |
| [`roblox-characters-animation`](roblox-characters-animation/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Characters and animation - Humanoid properties/states, spawning (LoadCharacterAsync), health and damage, HumanoidDescription appearance, Animator/A... |
| [`roblox-npc-ai`](roblox-npc-ai/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | NPCs and enemy AI - PathfindingService (CreatePath, ComputeAsync, costs, modifiers, links, blocked paths), chase/follow loops, state machines, perc... |
| [`roblox-physics`](roblox-physics/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Physics and spatial queries - Raycast/Blockcast/Spherecast, overlap queries, collision groups, Touched pitfalls, collision summaries (impact point/... |
| [`roblox-input`](roblox-input/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Player input and cameras across keyboard/mouse, touch, gamepad, VR - Input Action System (InputContext, InputAction, InputBinding), UserInputServic... |
| [`roblox-camera`](roblox-camera/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when scripting or fixing Roblox camera behavior: CFrame placement, screen raycasts, first/third-person, shoulder views, cutscenes. |
| [`roblox-text-chat`](roblox-text-chat/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Chat and text safety - TextChatService (channels, SendAsync, ShouldDeliverCallback, OnIncomingMessage, commands, bubbles, custom UI, platform-integ... |
| [`roblox-localization`](roblox-localization/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when adding or fixing Roblox translation: localization tables, auto-translation, locale-specific content, or region detection. |

### World, art, animation, VFX & audio (11)

| Skill | Source | What it is for |
|---|---|---|
| [`roblox-world-building`](roblox-world-building/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Building worlds with code - parts, models and pivots, materials, Lighting (LightingStyle, Atmosphere, post-processing), day/night, Terrain API, in-... |
| [`roblox-building`](roblox-building/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when building or editing geometry, maps, props, or generated assets with MCP or standalone Luau. |
| [`roblox-map`](roblox-map/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Build and PROVE Roblox maps, levels and arenas headlessly from a JSON spec - greybox decks, cover, ledges, ramps, stairs, spawns, kill planes and s... |
| [`roblox-lighting`](roblox-lighting/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when setting up or changing Roblox lighting, atmosphere, day/night cycles, or post-processing effects. |
| [`roblox-3d-model`](roblox-3d-model/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Generate game-ready 3D models for Roblox from text prompts, headlessly and end to end, one asset or a whole batch - text to a VERIFIED 2D concept i... |
| [`roblox-texture-gen`](roblox-texture-gen/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Generate free AI textures/skins (camo, gold plated, carbon fiber, rust, etc.) for Roblox game assets like guns, weapons, tools, or any part/mesh, a... |
| [`roblox-animation`](roblox-animation/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Author Roblox character animations (R15 or R6) headlessly in Blender from a JSON pose spec, verify them by rendering contact sheets and GIFs and ma... |
| [`roblox-animation-vfx`](roblox-animation-vfx/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when adding, changing, or fixing Roblox animations, particles, beams, trails, tweens, camera shake, or other visual effects. |
| [`roblox-vfx`](roblox-vfx/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Build Roblox VFX to a pro standard headlessly - anime-style moves, slashes, beams, impacts, auras, ultimates, summons - authored as effect definiti... |
| [`roblox-audio`](roblox-audio/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Sound and music - the Audio API (AudioPlayer, AudioEmitter, AudioListener, AudioDeviceOutput, Wire, effects, faders), classic Sound/SoundGroup, 2D... |
| [`roblox-sfx`](roblox-sfx/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Source, verify and wire the sound for a Roblox game from the Creator Store by asset id - footsteps, gunshots, animal calls, UI clicks, ambience, mu... |

### UI (3)

| Skill | Source | What it is for |
|---|---|---|
| [`roblox-ui`](roblox-ui/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Responsive cross-platform UI - ScreenGui and safe areas (ScreenInsets), Scale vs Offset, UIListLayout flex/UIFlexItem, constraints, StyleSheets/tok... |
| [`roblox-gui`](roblox-gui/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when building or fixing Roblox menus, HUDs, shops, dialogs, or UI that must work on phones, tablets, desktop and console. |
| [`roblox-ui-builder`](roblox-ui-builder/SKILL.md) | [SyphoDev-yt/roblox-ai-skills](https://github.com/SyphoDev-yt/roblox-ai-skills) | Build Roblox game UI headlessly - HUD overlays, shops, inventories, quest lists, settings - from a JSON spec, and generate the icon set that goes i... |

### Design, monetization & live ops (6)

| Skill | Source | What it is for |
|---|---|---|
| [`roblox-game-design`](roblox-game-design/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when designing or reworking a Roblox game: core loop, tutorial/FTUE, levels, economy, retention phases, juice, grind, curation. |
| [`roblox-player-psychology`](roblox-player-psychology/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when designing or reviewing player-behavior mechanics: first minute, rewards, streaks, daily rewards, pricing, RNG/pity, community. |
| [`roblox-growth-design`](roblox-growth-design/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use for Roblox growth: diagnosing stats, discovery, retention, onboarding, experiments, LiveOps, thumbnails, and packaging. |
| [`roblox-monetization`](roblox-monetization/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Robux monetization - developer products with idempotent ProcessReceipt, passes, subscriptions, rewarded video ads, personalized shops, regional pri... |
| [`roblox-analytics`](roblox-analytics/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use when adding, changing, or auditing Roblox analytics: AnalyticsService events, economy, funnels, onboarding traces, rate limits. |
| [`roblox-analytics-liveops`](roblox-analytics-liveops/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Analytics and live ops - AnalyticsService economy/funnel/onboarding/progression/custom events, player segments, experience configs via ConfigServic... |

### Performance & release (2)

| Skill | Source | What it is for |
|---|---|---|
| [`roblox-performance`](roblox-performance/SKILL.md) | [EL4CTEO/roblox-skills](https://github.com/EL4CTEO/roblox-skills) | Performance diagnosis and optimization - MicroProfiler, Script Profiler, Developer Console, Scene Analysis, Luau heap and memory categories, memory... |
| [`roblox-publish-checklist`](roblox-publish-checklist/SKILL.md) | [TabooHarmony/roblox-brain](https://github.com/TabooHarmony/roblox-brain) | Use before publishing or updating a Roblox experience to run evidence-backed release gates and a pre-release audit. |

## Blender skills (113)

### Orchestration, shared references & QA (4)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-director`](blender-director/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Use when starting any Blender asset task, planning a production pipeline, coordinating multiple disciplines, or matching a reference photo/concept... |
| [`blender-handbook`](blender-handbook/SKILL.md) | [linnnn89/blenderskill](https://github.com/linnnn89/blenderskill) | Entry point and router for a 123-manual Blender 3D production handbook covering modeling, surfacing, lighting, animation, physics, scene assembly,... |
| [`blender-references`](blender-references/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Shared Blender production reference sheets used by the blender-* skills - asset pipeline phases, naming conventions (SM_/MAT_/COL_ prefixes), polyc... |
| [`blender-qa-review`](blender-qa-review/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Production QA gate for Blender assets using viewport screenshots, validation checklists, naming audits, and ship/no-ship verdicts via MCP. |

### Modeling (14)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-modeler`](blender-modeler/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Core Blender modeling specialist for Edit Mode, modifiers, collections, precision modeling, and scene organization. |
| [`blender-hard-surface`](blender-hard-surface/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | AAA hard surface modeling for sci-fi, industrial, military, vehicles, weapons, robotics, and mechanical props. |
| [`blender-character-artist`](blender-character-artist/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | AAA character modeling for human anatomy, stylization, facial topology, clothing, hair, and animation-ready meshes. |
| [`blender-creature-artist`](blender-creature-artist/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | AAA creature modeling for fantasy, aliens, monsters, and organic creature design with believable anatomy and movement. |
| [`blender-environment-artist`](blender-environment-artist/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | AAA environment art for modular kits, buildings, terrain, vegetation, architecture, and scene composition. |
| [`blender-prop-artist`](blender-prop-artist/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Everyday and hero prop modeling for furniture, tools, household objects, kitbash parts, and readable game props. |
| [`blender-vehicle-artist`](blender-vehicle-artist/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Dedicated vehicle modeling for cars, trucks, aircraft, ships, boats, mechs, and transit assets with proportion, panel flow, and game LOD awareness... |
| [`blender-vegetation-artist`](blender-vegetation-artist/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Vegetation and foliage authoring for Blender including trees, plants, grass cards, canopy LODs, and game-friendly leaf atlases via MCP. |
| [`blender-procedural-modeling`](blender-procedural-modeling/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Procedural asset creation for rocks, buildings, vegetation, roads, terrain, pipes, cables, and sci-fi panels using Geometry Nodes and modifier-base... |
| [`blender-geometry-nodes`](blender-geometry-nodes/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Blender Geometry Nodes for procedural modeling, scatter systems, vegetation, buildings, pipes, cables, and reusable node groups. |
| [`blender-sculpting`](blender-sculpting/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Blender sculpting for organic and hard surface detail using Dyntopo, multiresolution, brushes, alpha workflow, wrinkles, and damage. |
| [`blender-retopology`](blender-retopology/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Production retopology for animation-ready, low-poly, quad-dominant meshes with proper edge loops and efficient polygon flow. |
| [`blender-archviz`](blender-archviz/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Architectural visualization in Blender for interiors/exteriors with real-world scale, camera composition, PBR materials, and still/animation delive... |
| [`blender-hair-groom`](blender-hair-groom/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Hair and fur grooming in Blender using curves, particle hair, geometry nodes, and game hair-card workflows. |

### Scene assembly (2)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-scene-assembly`](blender-scene-assembly/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Large scene layout in Blender with collections, linking, overrides, streaming-friendly organization, and set assembly via MCP. |
| [`blender-set-dressing`](blender-set-dressing/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Set dressing and environmental storytelling placement for interiors and exteriors using prop density, narrative clusters, and readability rules via... |

### Surfacing (materials, textures, UVs) (4)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-materials`](blender-materials/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Blender PBR and stylized material creation for metal, wood, concrete, fabric, glass, dirt, rust, and procedural shaders. |
| [`blender-texture-workflow`](blender-texture-workflow/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Production texture workflow for atlases, baking AO/curvature/normal/roughness maps, decals, and texture memory optimization. |
| [`blender-uv-workflow`](blender-uv-workflow/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Production UV unwrapping for seam placement, UV packing, texel density, UDIM, lightmap UVs, and modular UV layouts. |
| [`blender-lookdev`](blender-lookdev/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Look development loop for Blender assets combining materials, lighting, camera, and screenshot comparison until shading reads correctly via MCP. |

### Rigging, animation & simulation (5)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-rigging`](blender-rigging/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Production rigging in Blender with armatures, IK/FK, constraints, weight painting, mechanical rigs, facial rigs, and drivers. |
| [`blender-animation`](blender-animation/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Game-ready animation in Blender including walk/run/idle cycles, combat, mechanical animation, camera animation, constraints, Graph Editor, and NLA... |
| [`blender-cloth-sim`](blender-cloth-sim/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Garment blockout, cloth simulation, pin groups, and bake to shape keys or caches for characters and props in Blender via MCP. |
| [`blender-physics-sim`](blender-physics-sim/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Rigid body, soft body, and destruction setups in Blender including constraints, cell fracture debris, and baked caches via MCP. |
| [`blender-vfx-fx`](blender-vfx-fx/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Cinematic and game VFX in Blender including smoke, fire, particles, trails, and Geometry Nodes FX setups via MCP. |

### Lighting, camera, rendering & compositing (4)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-lighting`](blender-lighting/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Cinematic and game lighting in Blender including three-point lighting, HDRI, horror lighting, volumetrics, rim lighting, and mood-driven illumination. |
| [`blender-camera-cinematography`](blender-camera-cinematography/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Cinematic camera work in Blender including framing, lenses, composition, camera animation, and shot language beyond basic rendering setup via MCP. |
| [`blender-rendering`](blender-rendering/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Blender rendering with Cycles and Eevee including sampling, denoising, camera setup, render passes, color management, and render optimization. |
| [`blender-compositing`](blender-compositing/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Blender compositor workflows for beauty stacks, render passes, color grade, glare, and delivery outputs via MCP. |

### Game-ready delivery & export (8)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-asset-optimization`](blender-asset-optimization/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Validates and optimizes Blender assets for polycount, topology, UV efficiency, material count, naming, collections, and game-ready performance. |
| [`blender-lod-pipeline`](blender-lod-pipeline/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Dedicated LOD generation, naming, screen-size targets, and validation for game meshes in Blender via MCP. |
| [`blender-collision-proxy`](blender-collision-proxy/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Collision proxy authoring for games including UCX/UHX naming, convex hulls, capsules, and simple collider meshes in Blender via MCP. |
| [`blender-export-pipeline`](blender-export-pipeline/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Production export from Blender to FBX, GLTF, OBJ, USD, and Alembic with scale, pivot, rotation, normals, materials, animation, and collision verifi... |
| [`blender-unity-export`](blender-unity-export/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Unity-specific Blender export for scale, axis, materials, humanoid/generic rigs, LODs, and collision import via MCP. |
| [`blender-unreal-export`](blender-unreal-export/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Unreal Engine-specific Blender export for FBX scale, LODs, UCX collision, sockets, materials, and skeletal mesh workflows via MCP. |
| [`blender-godot-export`](blender-godot-export/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Godot-specific Blender export favoring GLTF/GLB with correct scale, materials, animation clips, and collision shapes via MCP. |
| [`blender-threejs-export`](blender-threejs-export/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Export the current Blender scene as a GLB and generate a ready-to-use Three.js HTML viewer with orbit controls, lighting, and auto-rotation. |

### Image / reference to 3D (2)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-image-to-3d`](blender-image-to-3d/SKILL.md) | [majidmanzarpour/blender-game-skills](https://github.com/majidmanzarpour/blender-game-skills) | Build a game-ready 3D asset in Blender from reference images (concept art, photos, turnarounds, sketches, screenshots) for any category, including... |
| [`blender-meshy-image-to-3d`](blender-meshy-image-to-3d/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Convert 1-4 photos of the same object (single photo or multiple angles) into a textured 3D model with the paid Meshy API (MESHY_API_KEY) and import... |

### Product shots & camera moves (11)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-turntable`](blender-turntable/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | 360-degree turntable camera orbit around a 3D product. |
| [`blender-slow-zoom`](blender-slow-zoom/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Cinematic slow push-in zoom toward a hero detail on the product. |
| [`blender-crane-shot`](blender-crane-shot/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Camera starts low and rises up to reveal the full product. |
| [`blender-dolly-rotate`](blender-dolly-rotate/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Camera moves forward while rotating around the product. |
| [`blender-dynamic-full-loop`](blender-dynamic-full-loop/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Dynamic camera loop with speed ramping - slow reveals on each face, fast whips between. |
| [`blender-product-polish`](blender-product-polish/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Import a 3D model (GLB/GLTF) into Blender and apply a sleek, glossy product-shot finish with studio lighting. |
| [`blender-polyhaven-studio-setup`](blender-polyhaven-studio-setup/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Set up a professional product photography studio in Blender using PolyHaven HDRIs and PBR ground materials. |
| [`blender-polyhaven-scene-builder`](blender-polyhaven-scene-builder/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Build complete product scenes using PolyHaven assets — HDRI environment, textured ground/pedestal, and optional props from the 3D model library. |
| [`blender-polyhaven-texture-apply`](blender-polyhaven-texture-apply/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Apply realistic PBR textures from PolyHaven to any Blender object. |
| [`blender-polyhaven-material-swap`](blender-polyhaven-material-swap/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Cycle through multiple PolyHaven materials on a product and render each variant. |
| [`blender-polyhaven-hdri-showcase`](blender-polyhaven-hdri-showcase/SKILL.md) | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | Render the same product across multiple HDRI environments and output a comparison grid. |

### Cinematic film pipelines (3)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-film`](blender-film/SKILL.md) | [mromidev/claude-blender-skills](https://github.com/mromidev/claude-blender-skills) | Make a short, realistic cinematic shot in Blender with Claude, start to finish - storyboard, city layout, a physics-driven flight path, a chase cam... |
| [`blender-car-film`](blender-car-film/SKILL.md) | [mromidev/claude-blender-skills](https://github.com/mromidev/claude-blender-skills) | Make a short cinematic story film in Blender with Claude (about 20 seconds, several shots, a car, night, snow, sound and voice) - storyboard first,... |
| [`blender-forest`](blender-forest/SKILL.md) | [mromidev/claude-blender-skills](https://github.com/mromidev/claude-blender-skills) | Make an ultra-realistic 3D environment in Blender with Claude (a forest, a nature scene, a car driving through it) by following a long YouTube tuto... |

### Art direction: genres (13)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-genre-action-combat`](blender-genre-action-combat/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for action, hack-and-slash, beat 'em up, and fighting-game readable combat spaces and prop language in Blender. |
| [`blender-genre-card-party-idle`](blender-genre-card-party-idle/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for card games, deck builders, party games, idle/incremental, educational, and rhythm game presentational spaces in Blender. |
| [`blender-genre-metroidvania-roguelike`](blender-genre-metroidvania-roguelike/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for metroidvania, roguelike, and roguelite games in Blender with biome gates, room modules, and run-readable props. |
| [`blender-genre-narrative-vn`](blender-genre-narrative-vn/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for visual novel, interactive movie, walking simulator, and story-driven presentation spaces in Blender. |
| [`blender-genre-open-world-sandbox`](blender-genre-open-world-sandbox/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for open world and sandbox games in Blender with biome landmarks, traversable scale, and discovery props. |
| [`blender-genre-puzzle-platformer`](blender-genre-puzzle-platformer/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for puzzle and platformer games in Blender with readable interactables, jump volumes, and clear hazard language. |
| [`blender-genre-racing-sports`](blender-genre-racing-sports/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for racing and sports games in Blender with track landmarks, stadium kits, and high-speed readability. |
| [`blender-genre-rpg`](blender-genre-rpg/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for RPG, JRPG, CRPG, ARPG, and MMORPG worlds in Blender including loot rarity reads and region identity. |
| [`blender-genre-shooter`](blender-genre-shooter/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for FPS, TPS, shooter, battle royale, and extraction-shooter maps and props in Blender with sightline and cover language. |
| [`blender-genre-soulslike`](blender-genre-soulslike/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for soulslike games in Blender with monumental melancholy spaces, fog gates, bonfire landmarks, and lethal readability. |
| [`blender-genre-stealth`](blender-genre-stealth/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for stealth-game spaces in Blender with shadow volumes, patrol-friendly layouts, and concealment materials. |
| [`blender-genre-strategy-sim`](blender-genre-strategy-sim/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for strategy, RTS, turn-based strategy, tower defense, MOBA, city builder, colony sim, and simulation games in Blender. |
| [`blender-genre-survival`](blender-genre-survival/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Art direction for survival and survival-horror gameplay spaces in Blender emphasizing resource props, crafting readability, and tension routes. |

### Art direction: moods, worlds & archetypes (10)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-apocalypse-worlds`](blender-apocalypse-worlds/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Apocalyptic and dystopian world art direction for Blender including post-apocalyptic, zombie, alien invasion, post-human, dystopian, and utopian co... |
| [`blender-biome-worlds`](blender-biome-worlds/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Biome and setting art direction for Blender covering underwater, desert, arctic, jungle, underground, and floating-island environments. |
| [`blender-brutalist-mood`](blender-brutalist-mood/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Brutalist and concrete-monument mood direction for Blender architecture and scenes with raw concrete, monumental scale, and austere composition. |
| [`blender-character-archetypes`](blender-character-archetypes/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Character archetype art direction for Blender covering fantasy races, horror creatures, roles (knight, assassin, detective), and body types (mecha,... |
| [`blender-cozy-wholesome-mood`](blender-cozy-wholesome-mood/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Cozy, cute, wholesome, relaxing, and peaceful mood direction for Blender assets and scenes. |
| [`blender-dark-gritty-mood`](blender-dark-gritty-mood/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Dark, grim, gritty, rusty, abandoned, decayed, industrial, lonely, and melancholic mood direction for Blender. |
| [`blender-dream-surreal-mood`](blender-dream-surreal-mood/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Dreamlike, surreal, mysterious, mystical, hopeful, and chaotic mood direction for Blender scenes. |
| [`blender-fantasy-worlds`](blender-fantasy-worlds/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Fantasy world-building art direction for Blender covering medieval, high fantasy, dark fantasy, and urban fantasy asset language. |
| [`blender-historical-worlds`](blender-historical-worlds/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Historical and period world art direction for Blender including Western, pirate, samurai/ninja, Viking, ancient Egypt/Greece/Rome, Victorian, moder... |
| [`blender-sci-fi-punk-worlds`](blender-sci-fi-punk-worlds/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Sci-fi and punk world art direction for Blender including hard sci-fi, space, cyberpunk, steampunk, dieselpunk, atompunk, solarpunk, biopunk, and c... |

### Art direction: visual styles (33)

| Skill | Source | What it is for |
|---|---|---|
| [`blender-analog-found-footage-horror`](blender-analog-found-footage-horror/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Analog, VHS, CRT, and found-footage horror aesthetics for Blender shots including camera imperfections and documentary framing. |
| [`blender-anime-style`](blender-anime-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Anime and cel-shaded art direction for Blender with hard color breaks, toon shaders, clean silhouettes, and anime proportion language. |
| [`blender-body-horror-style`](blender-body-horror-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Body horror art direction for Blender focusing on flesh wrongness, mutation, fusion, and visceral material storytelling. |
| [`blender-cartoon-style`](blender-cartoon-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Cartoon art direction for Blender with squash-stretch readable shapes, bold colors, and graphic silhouettes for games and animation. |
| [`blender-chibi-style`](blender-chibi-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Chibi and SD proportion art direction for Blender characters with oversized heads, simplified anatomy, and cute silhouette rules. |
| [`blender-comic-book-style`](blender-comic-book-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Comic book and graphic-novel art direction for Blender with ink-line emphasis, halftone cues, and high-contrast framing. |
| [`blender-cosmic-eldritch-horror`](blender-cosmic-eldritch-horror/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Cosmic, eldritch, and Lovecraftian horror art direction for Blender with non-Euclidean cues, impossible scale, and incomprehensible forms. |
| [`blender-dream-weirdcore-style`](blender-dream-weirdcore-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Dreamcore, weirdcore, and traumacore-inspired art direction for Blender with nostalgic wrongness, liminal nostalgia, and surreal childhood spaces. |
| [`blender-folk-horror-style`](blender-folk-horror-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Folk horror art direction for Blender with rural ritual uncanny, pastoral daylight dread, and community-wrongness storytelling. |
| [`blender-frutiger-aero-style`](blender-frutiger-aero-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Frutiger Aero art direction for Blender with glossy skeuomorphism, aqua UI cues, nature-tech optimism, and mid-2000s futurism. |
| [`blender-hand-painted-style`](blender-hand-painted-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Hand-painted texture art direction for Blender with brushwork albedo, soft value transitions, and stylized PBR restraint. |
| [`blender-hd-2d-style`](blender-hd-2d-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | HD-2D art direction combining pixel characters/sprites with 3D environments, depth of field, and theatrical lighting. |
| [`blender-horror-style`](blender-horror-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Psychological horror art direction for Blender assets inspired by Silent Hill, Resident Evil, Chilla's Art, Fear to Fathom, and Iron Lung. |
| [`blender-indie-horror-aesthetics`](blender-indie-horror-aesthetics/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Indie horror aesthetic pack for Blender covering Silent Hill, Fear to Fathom, Puppet Combo, corporate horror, cabin/forest/hospital horror, and rel... |
| [`blender-isometric-style`](blender-isometric-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Isometric and strategy-game art direction for Blender including diorama framing, true-iso camera setup, readable silhouettes, and tile asset rules. |
| [`blender-liminal-space-style`](blender-liminal-space-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Liminal space and Backrooms art direction for Blender with empty transitional architecture, wrong familiarity, and endless repetition. |
| [`blender-lowpoly-style`](blender-lowpoly-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Low-poly art direction for Blender inspired by PS1/PS2, Lethal Company, Mouthwashing, and Fear to Fathom. |
| [`blender-manga-style`](blender-manga-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Manga-inspired art direction for Blender emphasizing monochrome value design, speed lines, screentone feel, and manga panel staging. |
| [`blender-mascot-puppet-horror`](blender-mascot-puppet-horror/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Mascot and puppet horror art direction for Blender with cheerful brand characters made wrong, felt/foam materials, and uncanny performance. |
| [`blender-minimalist-style`](blender-minimalist-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Minimalist and abstract-leaning art direction for Blender with reduced forms, limited palettes, and negative space. |
| [`blender-neon-retrofuturism`](blender-neon-retrofuturism/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Neon, vaporwave, synthwave, and retrofuturistic mood/art direction for Blender with grid horizons, chrome, and dusk palettes. |
| [`blender-noir-style`](blender-noir-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Noir art direction for Blender with high-contrast lighting, wet streets, silhouettes, and monochrome or limited-color grading. |
| [`blender-painterly-style`](blender-painterly-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Painterly art direction spanning watercolor and oil-painting looks for Blender using soft edges, pigment texture, and illustrative lighting. |
| [`blender-pixel-art-style`](blender-pixel-art-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Pixel-art and texel-constrained art direction for Blender assets destined for pixel rendering, low-res textures, or HD-2D-adjacent pixel reads. |
| [`blender-psx-horror-style`](blender-psx-horror-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | PS1/PSX-era horror art direction combining low-poly affine textures, limited color depth, fog, and psychological horror staging for Blender assets. |
| [`blender-realistic-style`](blender-realistic-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Photorealistic AAA art direction for Blender including photogrammetry cleanup, real-world scale, high-poly workflows, PBR accuracy, and scan optimi... |
| [`blender-retro-16bit-style`](blender-retro-16bit-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Retro 16-bit art direction for Blender-assisted SNES/Genesis-era color richness, dither cues, and sprite-like clarity. |
| [`blender-retro-8bit-style`](blender-retro-8bit-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Retro 8-bit art direction for Blender-assisted pixel/low-res aesthetics inspired by NES-era constraints. |
| [`blender-stop-motion-craft-style`](blender-stop-motion-craft-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Stop-motion and craft aesthetics for Blender including claymation, paper craft, and handmade physical-material cues. |
| [`blender-stylized-style`](blender-stylized-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Stylized art direction for Blender with shape language, exaggeration, color harmony, NPR rendering, and hand-painted asset workflows. |
| [`blender-vector-style`](blender-vector-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Vector-clean art direction for Blender with flat fills, sharp silhouettes, and UI-like graphic clarity. |
| [`blender-visual-console-eras`](blender-visual-console-eras/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Visual era art direction for Blender covering PS1–PS5 stylistic cues, retro arcade, DOS, CRT, VHS, and film-grain presentation. |
| [`blender-voxel-style`](blender-voxel-style/SKILL.md) | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Voxel and Minecraft-adjacent art direction for Blender with block grid modeling, limited palettes, and chunk-friendly assets. |

## Overlap decisions

- **EL4CTEO vs roblox-brain (same names):** `architecture`, `audio`, `input`, `networking`, `npc-ai`, `performance`, `physics`,
  `security`, `studio-mcp`, `tooling`, `monetization`. EL4CTEO wins: its SKILL.md files carry current, runnable Luau and verified
  APIs, while roblox-brain's are short stubs over one large `references/full.md`. Nothing unique was dropped: each roblox-brain
  stub and its full reference were preserved as `references/roblox-brain-supplement.md` inside the winning skill.
- **Kept both (different scope):** `roblox-ui` (EL4CTEO, API reference), `roblox-gui` (roblox-brain, mobile-first QA) and
  `roblox-ui-builder` (SyphoDev headless UI pipeline, renamed from `roblox-ui` to avoid the collision). Likewise
  `data-stores`/`data`/`server-data`, `analytics-liveops`/`analytics`, `open-cloud`/`cloud`, `luau`/`luau-core|patterns|types`,
  `characters-animation`/`animation-vfx`/`animation`, `world-building`/`building`/`lighting`/`map`.
- **roblox-ai-os `.agents/skills` (7):** `roblox-animations`, `roblox-datastores`, `roblox-gui`, `roblox-monetization`,
  `roblox-performance`, `roblox-remote-events`, `roblox-security`. All are dominated by the versions above, and reviewers found
  concrete errors: wrong animation-priority order, no session locking, wrong `RequestStreamAroundAsync` target, stale DevEx rate,
  and a kick-on-speed heuristic.
- **arjun988 vs linnnn89:** 93 of linnnn89's 123 manuals are copies of arjun988 skills. 65 are byte-identical; the other 28 differ
  only in object-name prefixes (`GEO-` vs `SM_`) and path placeholders. The arjun988 originals are installed as standalone skills;
  inside `blender-handbook` those 93 manuals are short redirect stubs. Its 30 unique manuals (reference-locked reconstruction,
  quality gates, orchestration, general lighting/materials/cameras/export manuals), references and scripts are kept whole.
  The handbook's own `skill_graph_audit.py` passes on the installed tree.
- **kevinbadi:** `perfect-loop` duplicated `turntable` (its seamless-loop checklist was appended to `blender-turntable`).
  `image-to-3d` duplicated `multi-image-to-3d` for one photo (its single-image endpoint and options were appended to
  `blender-meshy-image-to-3d`). Meshy (cloud AI) and `blender-image-to-3d` (offline, measured, scripted) are different jobs,
  so both are kept.

## Not installed

- **roblox-ai-os, 55 more skills:** these are commands for that project's own `rcs` CLI runtime (tmux crews, `.rcs/` state,
  hooks, HUD, notifications, `$autopilot`-style modes) or generic engineering helpers outside Roblox/Blender scope. The
  Roblox-flavoured ones are 15-30-line aliases into that runtime, and their content is covered in more depth by
  `roblox-game-design`, `roblox-player-psychology`, `roblox-growth-design`, `roblox-security` and `roblox-code-review`. Several
  also act outside the project: `doctor` deletes `~/.agents/skills`, `configure-notifications` posts to Discord/Telegram/Slack,
  and `team` launches workers with `--dangerously-skip-permissions`. The repository's exploit-script corpus was never downloaded.
- **kevinbadi `blender-toolkit`:** a non-functional stub. Its CLI, add-on and all four referenced docs are absent from the repo,
  and it depends on another plugin marketplace.
- **izzyfrm/roblox-ai:** contains no skills. It is ~1 GB of reference images, MP3s and MP4s, so it was not downloaded
  (requirement: no large media). Browse it on GitHub when you need visual references.
- **Omitted files:** SyphoDev's 4 disabled Kaggle scripts; linnnn89's dev-only `tests/`, `evals/`, README and 24 unreferenced
  screenshots; repo-level READMEs, installers, site/docs and `docs/img` photos.

## Changes made during import

Skill bodies are otherwise unchanged from upstream. Every folder got a `roblox-`/`blender-` prefix where it lacked one, and
cross-references were rewritten to the new names. Frontmatter was normalized to the Agent Skills spec: extra keys moved under
`metadata`, roblox-brain's `when_to_use` merged into `description`, over-long or invalid descriptions fixed. Per-skill changes:

- `blender-crane-shot`: renamed from crane-shot; script paths point at .agents/skills/blender-crane-shot/
- `blender-director`: removed duplicate `role:` metadata key (invalid YAML)
- `blender-dolly-rotate`: renamed from dolly-rotate; script paths point at .agents/skills/blender-dolly-rotate/
- `blender-dynamic-full-loop`: renamed from dynamic-full-loop; script paths point at .agents/skills/blender-dynamic-full-loop/
- `blender-handbook`: renamed from blender-skill; kept 30 unique manuals; 93 manuals duplicating arjun988 skills replaced by redirect stubs; omitted dev-only tests/, evals/, README.md and 24 unreferenced .webp screenshots (kept the 4 referenced ones)
- `blender-meshy-image-to-3d`: renamed from multi-image-to-3d; script paths point at .agents/skills/blender-meshy-image-to-3d/; merged duplicate kevinbadi image-to-3d (single-image endpoint + options); API key now read from MESHY_API_KEY
- `blender-polyhaven-hdri-showcase`: renamed from polyhaven-hdri-showcase; script paths point at .agents/skills/blender-polyhaven-hdri-showcase/
- `blender-polyhaven-material-swap`: renamed from polyhaven-material-swap; script paths point at .agents/skills/blender-polyhaven-material-swap/
- `blender-polyhaven-scene-builder`: renamed from polyhaven-scene-builder; script paths point at .agents/skills/blender-polyhaven-scene-builder/
- `blender-polyhaven-studio-setup`: renamed from polyhaven-studio-setup; script paths point at .agents/skills/blender-polyhaven-studio-setup/
- `blender-polyhaven-texture-apply`: renamed from polyhaven-texture-apply; script paths point at .agents/skills/blender-polyhaven-texture-apply/
- `blender-product-polish`: renamed from product-polish; script paths point at .agents/skills/blender-product-polish/
- `blender-references`: import-support skill: SKILL.md written during import to host shared references
- `blender-slow-zoom`: renamed from slow-zoom; script paths point at .agents/skills/blender-slow-zoom/
- `blender-threejs-export`: renamed from threejs-export; script paths point at .agents/skills/blender-threejs-export/
- `blender-turntable`: renamed from turntable; script paths point at .agents/skills/blender-turntable/; merged duplicate kevinbadi perfect-loop (seamless-loop checklist)
- `roblox-3d-model`: omitted disabled Kaggle scripts: scripts/kaggle_run.py, scripts/kaggle_hi3dgen.py, scripts/kaggle_flux.py; ~/.claude/skills/ paths rewritten to .agents/skills/; description condensed to the 1024-character spec limit
- `roblox-analytics`: frontmatter normalized to the Agent Skills spec
- `roblox-animation`: ~/.claude/skills/ paths rewritten to .agents/skills/
- `roblox-animation-vfx`: frontmatter normalized to the Agent Skills spec
- `roblox-architecture`: absorbed duplicate roblox-brain core/roblox-architecture as references/roblox-brain-supplement.md
- `roblox-audio`: fixed non-existent SoundService.ListenerLocation -> DefaultListenerLocation (verified against Roblox/creator-docs SoundService.yaml); absorbed duplicate roblox-brain gameplay/roblox-audio as references/roblox-brain-supplement.md
- `roblox-build-orchestrator`: added repo-level agents/roblox-asset-map.md so the subagent roster is complete; ~/.claude/skills/ paths rewritten to .agents/skills/
- `roblox-building`: frontmatter normalized to the Agent Skills spec
- `roblox-camera`: frontmatter normalized to the Agent Skills spec
- `roblox-cloud`: frontmatter normalized to the Agent Skills spec
- `roblox-code`: ~/.claude/skills/ paths rewritten to .agents/skills/
- `roblox-collaboration-mode`: frontmatter normalized to the Agent Skills spec
- `roblox-create-game`: renamed from create-roblox-game; ~/.claude/skills/ paths rewritten to .agents/skills/; frontmatter normalized to the Agent Skills spec
- `roblox-data`: frontmatter normalized to the Agent Skills spec
- `roblox-game-design`: frontmatter normalized to the Agent Skills spec
- `roblox-growth-design`: frontmatter normalized to the Agent Skills spec
- `roblox-gui`: frontmatter normalized to the Agent Skills spec
- `roblox-input`: absorbed duplicate roblox-brain gameplay/roblox-input as references/roblox-brain-supplement.md
- `roblox-lighting`: frontmatter normalized to the Agent Skills spec
- `roblox-localization`: frontmatter normalized to the Agent Skills spec
- `roblox-luau-core`: frontmatter normalized to the Agent Skills spec
- `roblox-luau-patterns`: frontmatter normalized to the Agent Skills spec
- `roblox-luau-types`: frontmatter normalized to the Agent Skills spec
- `roblox-map`: ~/.claude/skills/ paths rewritten to .agents/skills/; description condensed to the 1024-character spec limit
- `roblox-monetization`: absorbed duplicate roblox-brain design/roblox-monetization as references/roblox-brain-supplement.md
- `roblox-networking`: absorbed duplicate roblox-brain core/roblox-networking as references/roblox-brain-supplement.md
- `roblox-npc-ai`: absorbed duplicate roblox-brain gameplay/roblox-npc-ai as references/roblox-brain-supplement.md
- `roblox-performance`: absorbed duplicate roblox-brain core/roblox-performance as references/roblox-brain-supplement.md
- `roblox-physics`: absorbed duplicate roblox-brain gameplay/roblox-physics as references/roblox-brain-supplement.md
- `roblox-player-psychology`: frontmatter normalized to the Agent Skills spec
- `roblox-publish-checklist`: frontmatter normalized to the Agent Skills spec
- `roblox-security`: absorbed duplicate roblox-brain core/roblox-security as references/roblox-brain-supplement.md
- `roblox-server-data`: frontmatter normalized to the Agent Skills spec
- `roblox-sfx`: ~/.claude/skills/ paths rewritten to .agents/skills/
- `roblox-skills-setup`: check_setup.py now looks for sibling skills in .agents/skills instead of ~/.claude/skills; ~/.claude/skills/ paths rewritten to .agents/skills/
- `roblox-studio-mcp`: absorbed duplicate roblox-brain tools/roblox-studio-mcp as references/roblox-brain-supplement.md
- `roblox-texture-gen`: ~/.claude/skills/ paths rewritten to .agents/skills/
- `roblox-tooling`: absorbed duplicate roblox-brain tools/roblox-tooling as references/roblox-brain-supplement.md
- `roblox-ui-builder`: omitted disabled Kaggle scripts: scripts/kaggle_icon_ab.py; renamed from roblox-ui; added SIL OFL 1.1 text for the bundled Fredoka fonts (from google/fonts); ~/.claude/skills/ paths rewritten to .agents/skills/
- `roblox-vfx`: ~/.claude/skills/ paths rewritten to .agents/skills/; description condensed to the 1024-character spec limit

## Known caveats (upstream content, not verified here)

- Nothing was executed in Blender or Roblox Studio here (neither is available in this Linux environment). The scripts' "works /
  proven" claims are the upstream authors'.
- **Blender versions:** SyphoDev scripts hard-code `BLENDER_EEVEE_NEXT` (Blender 4.2-4.x). arjun988 content assumes 4.x and
  mentions Auto Smooth (removed in 4.1). linnnn89 and majidmanzarpour target Blender 5.x.
- **Naming conventions differ:** arjun988 uses `SM_`/`MAT_`/`COL_`, linnnn89 `GEO-`/`MAT-`/`COL-`, majidmanzarpour `CH_`/`PR_`/`COL_`.
  Pick one per project.
- **Port clash:** mromidev's film skills run their own bridge on `127.0.0.1:9876`, the same port as the blender-mcp add-on. Run
  one at a time. `blender-film` scripts load `$FILM_ROOT/tools/lib.py`, so copy `tools/` into your film work dir.
- **Some kevinbadi Poly Haven example IDs no longer exist** (`brushed_metal`, `painted_metal_02`, `burlap_01`, `carbon_fiber`,
  HDRI `sunset`). Query the Poly Haven API for current IDs.
- **SyphoDev autonomy rules:** `roblox-create-game` says "never ask / never offer options". Asset uploads via `ROBLOX_API_KEY` run
  without a confirmation flag. Under AGENTS.md, ask before uploading with real credentials or publishing.
- **External services:** some skills call paid or free external services: Meshy, HuggingFace Spaces, Cloudflare Workers AI,
  Pollinations, ElevenLabs, Open Cloud. Keys are read from environment variables only, and none are stored here.

## Licensing

See [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md). kevinbadi/blender-skills and linnnn89/blenderskill ship **no license
file**. SyphoDev's custom license allows free use and sharing with a link back, but forbids selling or bundling the skills.
