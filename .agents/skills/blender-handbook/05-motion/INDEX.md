# 05 — Motion (Animation, Rigging, Simulation, VFX)

**Open this when** something must move over time: keyframe animation, rigs that deform, physics/cloth simulation, or particle/VFX work.

Paths below are relative to this file's own directory.

## Animation

| Manual | Use when | Path |
|--------|----------|------|
| `blender-animation` | Keys, F-curves, easing curves (Bezier/Linear/Sine/Bounce/Elastic), shape keys / morph targets / blendshapes / visemes, Python-expression drivers, NLA actions for reuse and layering | `blender-animation/MANUAL.md` |
| `animation` | Game-ready cycles and mechanical motion — walk/run/idle, combat, mechanical animation, camera animation, constraints, Graph Editor, NLA workflows | `animation/MANUAL.md` |
| `orbital-hud-motion` | Tasteful circular/orbital HUD or aura animation around a subject, with arcs/dots/dashes derived from the source art rather than random oversized rings | `orbital-hud-motion/MANUAL.md` |

## Rigging

| Manual | Use when | Path |
|--------|----------|------|
| `rigging` | Armatures, IK/FK, constraints, weight painting, mechanical rigs, facial rigs, drivers. Do this before animating anything that deforms | `rigging/MANUAL.md` |

## Simulation and VFX

| Manual | Use when | Path |
|--------|----------|------|
| `physics-sim` | Rigid body, soft body, constraints, cell-fracture destruction, baked caches | `physics-sim/MANUAL.md` |
| `cloth-sim` | Garment blockout, cloth simulation, pin groups, baking to shape keys or caches | `cloth-sim/MANUAL.md` |
| `vfx-fx` | Cinematic and game VFX — smoke, fire, particles, trails, Geometry Nodes FX setups | `vfx-fx/MANUAL.md` |

## Next steps

- Deliver the animation to an engine → `../07-delivery/INDEX.md`
- Gate the animation before shipping → `animation-quality-gate` in `../09-quality-gates/INDEX.md`
- Animating between source textures rather than objects → `texture-state-animation` in `../03-surfacing/INDEX.md`
