# Skill Routing Reference

Extended routing tables for the Blender Director.

## By Engine Target

| Engine | Export Skill | Notes |
|--------|--------------|-------|
| Unity | blender-unity-export | GLB/GLTF modern; FBX for humanoid/legacy |
| Unreal | blender-unreal-export | FBX; UCX collision; verify cm scale |
| Godot | blender-godot-export | GLTF/GLB preferred |
| Generic / multi | blender-export-pipeline | Confirm axis and scale; then engine skill if known |

## By Production Phase

| Phase | Lead Skill | Validators |
|-------|------------|------------|
| Reference analysis | blender-director + reference-image-match | reference-analysis-template |
| Genre / style / world lock | matching genre/style/world/mood skill | production brief |
| Blockout | blender-modeler / discipline skill | blender-director |
| Detail pass | discipline skill | blender-asset-optimization |
| UV pass | blender-uv-workflow | blender-texture-workflow |
| Look dev | blender-lookdev + blender-materials | style skill, blender-qa-review |
| Camera / shot | blender-camera-cinematography | blender-rendering |
| FX / sim | blender-vfx-fx / blender-physics-sim / blender-cloth-sim | blender-compositing |
| Reference compare | blender-rendering + blender-lighting | visual-match-checklist |
| Scene layout | blender-scene-assembly + blender-set-dressing | blender-qa-review |
| Performance | blender-asset-optimization + blender-lod-pipeline | blender-collision-proxy |
| Delivery | blender-unity-export / blender-unreal-export / blender-godot-export / blender-export-pipeline | blender-qa-review + validation-checklist |

## Style + Discipline Matrix (core)

|  | Hard Surface | Prop | Vehicle | Environment | Character | Creature |
|--|-------------|------|---------|-------------|-----------|----------|
| Horror | + blender-horror-style | + blender-horror-style | + blender-horror-style | + blender-horror-style | + blender-horror-style | + blender-horror-style |
| PSX Horror | + blender-psx-horror-style | + blender-psx-horror-style | + blender-psx-horror-style | + blender-psx-horror-style | + blender-psx-horror-style | + blender-psx-horror-style |
| Lowpoly | + blender-lowpoly-style | + blender-lowpoly-style | + blender-lowpoly-style | + blender-lowpoly-style | + blender-lowpoly-style | + blender-lowpoly-style |
| Anime | + blender-anime-style | + blender-anime-style | + blender-anime-style | + blender-anime-style | + blender-anime-style | + blender-anime-style |
| Voxel | + blender-voxel-style | + blender-voxel-style | + blender-voxel-style | + blender-voxel-style | + blender-voxel-style | + blender-voxel-style |
| Isometric | + blender-isometric-style | + blender-isometric-style | + blender-isometric-style | + blender-isometric-style | + blender-isometric-style | + blender-isometric-style |
| Stylized | + blender-stylized-style | + blender-stylized-style | + blender-stylized-style | + blender-stylized-style | + blender-stylized-style | + blender-stylized-style |
| Realistic | + blender-realistic-style | + blender-realistic-style | + blender-realistic-style | + blender-realistic-style | + blender-realistic-style | + blender-realistic-style |

Add world/mood/genre packs on top (e.g. `blender-sci-fi-punk-worlds` + `blender-neon-retrofuturism` + `blender-genre-shooter`).

## Pack Routers (load references inside)

| Pack | Examples covered in refs |
|------|--------------------------|
| blender-sci-fi-punk-worlds | hard sci-fi, space, cyber/steam/diesel/atom/solar/bio/clockpunk |
| blender-fantasy-worlds | medieval, high/dark/urban fantasy |
| blender-historical-worlds | western, pirate, samurai, viking, ancients, victorian, military |
| blender-apocalypse-worlds | wasteland, zombie, dystopia/utopia, alien invasion |
| blender-biome-worlds | underwater, desert, arctic, jungle, underground, floating islands |
| blender-indie-horror-aesthetics | Silent Hill, Fear to Fathom, Puppet Combo, corporate, cabin/hospital/forest |
| blender-character-archetypes | fantasy races, horror bodies, sci-fi bodies, role kits |
| blender-visual-console-eras | PS1–PS5, CRT, VHS, DOS, arcade, film grain |
| blender-painterly-style | watercolor, oil |
| blender-stop-motion-craft-style | claymation, paper craft |
| blender-genre-rpg | JRPG, CRPG, ARPG, MMORPG |
| blender-genre-shooter | FPS, TPS, BR, extraction |
| blender-genre-strategy-sim | RTS, TBS, TD, MOBA, city/colony/life/farming sim |

## Parallel vs Sequential

**Sequential (default):** Genre/style lock → Modeling → UV → Materials → Lookdev → Export

**Parallel allowed:**
- Material prototyping while UVs in progress (separate collections)
- Lighting setup while optimization runs on duplicate collection
- Collision proxies while LOD1+ generates
- Mood/world reference gathering during blockout

**Never parallel:**
- Retopology before sculpt complete
- Export before validation / blender-qa-review
- Rigging before final topology locked
- Engine export before LOD/collision plan when required
