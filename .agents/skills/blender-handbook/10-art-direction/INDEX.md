# 10 — Art Direction

**Open this when** the request is about choosing a *look* rather than a technique: a visual style, a horror register, a mood, a world setting, a game genre's presentational language, or a character archetype.

These manuals define the design language (palette, shape logic, materials, lighting attitude, framing). Pair the chosen one with the technical groups — art direction says what it should feel like; `02`–`07` say how to build it.

Choose art direction along orthogonal axes. Default selection is **one base style + at most one mood/era/world/genre manual**. Open more only when the request explicitly names them; otherwise the result becomes incoherent and wastes context.

These are appearance constraints, not workflow owners. Execution order and recovery follow `../references/intent-routing.md`; do not start a second production pipeline from a style choice.

Paths below are relative to this file's own directory.

## Styles

| Manual | Path |
|--------|------|
| `anime-style` — cel shading, hard colour breaks, anime proportion language | `anime-style/MANUAL.md` |
| `cartoon-style` — squash/stretch, readable shapes, bold colour, graphic silhouettes | `cartoon-style/MANUAL.md` |
| `chibi-style` — SD proportions, oversized heads, simplified anatomy | `chibi-style/MANUAL.md` |
| `comic-book-style` — ink-line emphasis, halftone cues, high-contrast framing | `comic-book-style/MANUAL.md` |
| `manga-style` — monochrome value design, speed lines, screentone, panel staging | `manga-style/MANUAL.md` |
| `pixel-art-style` — texel-constrained assets for pixel/low-res reads | `pixel-art-style/MANUAL.md` |
| `retro-8bit-style` — NES-era constraints and palettes | `retro-8bit-style/MANUAL.md` |
| `retro-16bit-style` — SNES/Genesis colour richness, dither cues, sprite clarity | `retro-16bit-style/MANUAL.md` |
| `hd-2d-style` — pixel characters in 3D environments, DoF, theatrical lighting | `hd-2d-style/MANUAL.md` |
| `voxel-style` — block-grid modeling, limited palettes, chunk-friendly assets | `voxel-style/MANUAL.md` |
| `lowpoly-style` — PS1/PS2-era minimal polygons, strong atmosphere | `lowpoly-style/MANUAL.md` |
| `isometric-style` — diorama framing, true-iso camera, tile asset rules | `isometric-style/MANUAL.md` |
| `visual-console-eras` — PS1→PS5 cues, arcade, DOS, CRT, VHS, film grain | `visual-console-eras/MANUAL.md` |
| `realistic-style` — photoreal AAA, photogrammetry cleanup, PBR accuracy | `realistic-style/MANUAL.md` |
| `stylized-style` — shape language, exaggeration, colour harmony, NPR | `stylized-style/MANUAL.md` |
| `hand-painted-style` — brushwork albedo, soft value transitions, restrained PBR | `hand-painted-style/MANUAL.md` |
| `painterly-style` — watercolour and oil looks, soft edges, pigment texture | `painterly-style/MANUAL.md` |
| `vector-style` — flat fills, sharp silhouettes, UI-like graphic clarity | `vector-style/MANUAL.md` |
| `minimalist-style` — reduced forms, limited palettes, negative space | `minimalist-style/MANUAL.md` |
| `noir-style` — high-contrast lighting, wet streets, limited-colour grading | `noir-style/MANUAL.md` |
| `neon-retrofuturism` — neon, vaporwave, synthwave, chrome, dusk palettes | `neon-retrofuturism/MANUAL.md` |
| `frutiger-aero-style` — glossy skeuomorphism, aqua UI, mid-2000s futurism | `frutiger-aero-style/MANUAL.md` |
| `dream-weirdcore-style` — dreamcore/weirdcore, liminal nostalgia, surreal childhood spaces | `dream-weirdcore-style/MANUAL.md` |
| `stop-motion-craft-style` — claymation, paper craft, handmade material cues | `stop-motion-craft-style/MANUAL.md` |

## Horror registers

| Manual | Path |
|--------|------|
| `horror-style` — psychological horror, sparse industrial spaces, analog aesthetics | `horror-style/MANUAL.md` |
| `psx-horror-style` — PS1-era low-poly, affine textures, limited colour depth, fog | `psx-horror-style/MANUAL.md` |
| `indie-horror-aesthetics` — the broader indie horror pack (Silent Hill, Puppet Combo, cabin/forest/hospital) | `indie-horror-aesthetics/MANUAL.md` |
| `analog-found-footage-horror` — VHS/CRT/found-footage, camera imperfections, documentary framing | `analog-found-footage-horror/MANUAL.md` |
| `body-horror-style` — flesh wrongness, mutation, fusion, visceral material storytelling | `body-horror-style/MANUAL.md` |
| `cosmic-eldritch-horror` — Lovecraftian, non-Euclidean cues, impossible scale | `cosmic-eldritch-horror/MANUAL.md` |
| `folk-horror-style` — rural ritual uncanny, pastoral daylight dread | `folk-horror-style/MANUAL.md` |
| `mascot-puppet-horror` — cheerful brand characters made wrong, felt/foam, uncanny performance | `mascot-puppet-horror/MANUAL.md` |

## Moods

| Manual | Path |
|--------|------|
| `brutalist-mood` — raw concrete, monumental scale, austere composition | `brutalist-mood/MANUAL.md` |
| `cozy-wholesome-mood` — cute, relaxing, peaceful | `cozy-wholesome-mood/MANUAL.md` |
| `dark-gritty-mood` — grim, rusty, abandoned, decayed, melancholic | `dark-gritty-mood/MANUAL.md` |
| `dream-surreal-mood` — dreamlike, mystical, hopeful, chaotic | `dream-surreal-mood/MANUAL.md` |
| `liminal-space-style` — empty transitional architecture, wrong familiarity, endless repetition | `liminal-space-style/MANUAL.md` |

## Worlds

| Manual | Path |
|--------|------|
| `fantasy-worlds` — medieval, high/dark/urban fantasy asset language | `fantasy-worlds/MANUAL.md` |
| `sci-fi-punk-worlds` — hard sci-fi, cyberpunk, steampunk, dieselpunk, atompunk, solarpunk, biopunk, clockpunk | `sci-fi-punk-worlds/MANUAL.md` |
| `biome-worlds` — underwater, desert, arctic, jungle, underground, floating islands | `biome-worlds/MANUAL.md` |
| `apocalypse-worlds` — post-apocalyptic, zombie, alien invasion, dystopian/utopian contrast | `apocalypse-worlds/MANUAL.md` |
| `historical-worlds` — Western, pirate, samurai, Viking, ancient Egypt/Greece/Rome, Victorian, modern, military | `historical-worlds/MANUAL.md` |
| `archviz` — architectural visualization, real-world scale, interiors/exteriors | `archviz/MANUAL.md` |

## Game genres

| Manual | Path |
|--------|------|
| `genre-action-combat` — hack-and-slash, beat 'em up, fighting-game readability | `genre-action-combat/MANUAL.md` |
| `genre-shooter` — FPS/TPS, battle royale, extraction; sightline and cover language | `genre-shooter/MANUAL.md` |
| `genre-soulslike` — monumental melancholy, fog gates, bonfire landmarks, lethal readability | `genre-soulslike/MANUAL.md` |
| `genre-stealth` — shadow volumes, patrol-friendly layouts, concealment materials | `genre-stealth/MANUAL.md` |
| `genre-survival` — resource props, crafting readability, tension routes | `genre-survival/MANUAL.md` |
| `genre-rpg` — JRPG/CRPG/ARPG/MMO worlds, loot rarity reads, region identity | `genre-rpg/MANUAL.md` |
| `genre-metroidvania-roguelike` — biome gates, room modules, run-readable props | `genre-metroidvania-roguelike/MANUAL.md` |
| `genre-puzzle-platformer` — readable interactables, jump volumes, hazard language | `genre-puzzle-platformer/MANUAL.md` |
| `genre-open-world-sandbox` — biome landmarks, traversable scale, discovery props | `genre-open-world-sandbox/MANUAL.md` |
| `genre-strategy-sim` — RTS, turn-based, tower defense, MOBA, city builder, colony sim | `genre-strategy-sim/MANUAL.md` |
| `genre-racing-sports` — track landmarks, stadium kits, high-speed readability | `genre-racing-sports/MANUAL.md` |
| `genre-narrative-vn` — visual novels, walking sims, story-driven presentation spaces | `genre-narrative-vn/MANUAL.md` |
| `genre-card-party-idle` — card, deck-builder, party, idle, educational, rhythm | `genre-card-party-idle/MANUAL.md` |

## Character archetypes

| Manual | Path |
|--------|------|
| `character-archetypes` — fantasy races, horror creatures, roles (knight, assassin, detective), body types (mecha, android, chibi) | `character-archetypes/MANUAL.md` |

## Related

- The technical side of making a character → `character-artist` / `creature-artist` in `../02-modeling/INDEX.md`
- Matching a *specific* supplied look 1:1 → `../08-reference-locked/INDEX.md`
