# CH_StarPlatinum: Roblox-ready Stand model

A rigged, textured 3D model of the Stand from `ref/stand_sheet_original.png`, built by a reproducible Blender
pipeline (`blender-image-to-3d` workflow) and delivered for Roblox Studio as an R15 skinned rig.

## Deliverables

| File | What it is |
| --- | --- |
| `exports/roblox/CH_StarPlatinum_R15.fbx` | **Use this in Roblox.** Skinned R15 rig: 15 meshes `<Part>_Geo` + armature `Root > HumanoidRootNode > LowerTorso > …`, 1 unit = 1 stud, 6.64 studs tall, Root/LowerTorso at the origin, textures embedded |
| `exports/roblox/T_StarPlatinum_{BC,N,R,M}.png` | 1024 px SurfaceAppearance maps: ColorMap (sRGB), NormalMap (OpenGL +Y), RoughnessMap, MetalnessMap |
| `exports/roblox/roblox-manifest.json` | Triangles per part, units, axes, import settings |
| `exports/glb/CH_StarPlatinum.glb` + `asset-manifest.json` | Single skinned mesh in metres (2.145 m) for Blender/other engines |
| `CH_StarPlatinum_master.blend` | Non-destructive master: `REF` (reference planes), `HIGH` (441k-tri sculpt source), `LOW` (authoring parts), `EXPORT` (delivery mesh), `RIG_DEF` (R15 armature, `AN_PoseTest` QA action) |
| `textures/T_StarPlatinum_*_2048.png` | 2048 px texture masters |

## Import into Roblox Studio

1. **Avatar tab → Import 3D** (3D Importer) → choose `CH_StarPlatinum_R15.fbx`.
2. Check **Rig Type = R15** (auto-detected from the part and bone names) and **Scale Unit = Studs**.
3. Import. If the importer does not apply the PBR maps, upload the four PNGs as **Images** (not Decals) and
   add a `SurfaceAppearance` to each MeshPart: ColorMap = BC, NormalMap = N, RoughnessMap = R, MetalnessMap = M.
4. Standard R15 animations target the same joint names. For a Stand, weld or `AlignPosition` it behind the
   player and play your barrage/idle animations on its `Humanoid.Animator`.

## Budgets and checks (all from the build logs)

| Check | Result |
| --- | --- |
| Triangles | 24,444 total (budget 30k); largest MeshPart Head 4,180 (Roblox cap 20k, target ≤ 10k) |
| Textures | one shared 1024 atlas set (Roblox cap 1024); UV coverage 55% |
| Skinning | ≤ 4 influences (max 2 used), 0 unweighted vertices, nothing on Root |
| `validate.py` (EXPORT, RIG_DEF) | 0 FAIL, 0 WARN |
| GLB round trip (`roundtrip.py`) | 24,444 tris, height 2.1449 m (expected 2.145), images resolve, 0 errors |
| FBX round trip (`tools/fbx_roundtrip.py`) | 15 `_Geo` parts, R15 hierarchy, no leaf bones, 6.639 studs, 0 errors |
| Colour gate (`tools/check_colours.py`) | ColorMap pixels match the palette hexes exactly (no sRGB/linear shift) |
| Silhouette gates (`world_gate.py`) | front IoU 0.863, side 0.833; band widths within 0.016 front, 0.042 side |

## Measured deviations and inferred parts

- Silhouette IoU stays below the skill's forms target of 0.90. Every front band width is within 0.016, but the
  remaining area difference comes from hand-drawn hair spikes, the side panel's arm overlapping the torso,
  and the loincloth's length, which the front and side panels draw differently (front ends at z 1.03 m,
  side at 0.92 m; built at 0.985 m).
- Inferred (not visible in the sheet): skull under the hair, ears, back of the hair mass, palms and fingers
  inside the fists, underside of the pads, the back of the knee straps, belt disc count, absolute height
  (no scale cue: 2.10 m chosen, delivered at 6.5 studs).
- The loincloth is rigid on LowerTorso, so it clips through the thighs in extreme leg raises
  (`review/06_rig/extreme_pose_sheet.png`).
- The body topology comes from an even voxel quad remesh, not hand-placed edge loops. Joints bend cleanly in
  the extreme-pose sheet, but there are no dedicated loops for facial animation.
- Roblox generates its own render LODs, so no custom LOD chain ships.

## Rebuild

```
python build/run_all.py --blender <path to blender 5.2> --from 01
```

The phases are `01_init` (calibrated master), `02_blockout`, `03_forms` (HIGH), `04_topology` (LOW + coverage
cuts + R15 part tags), `05a_uv`, `05b_bake` (skill `bake_maps.py`), `05c_paint` (texel-space painter),
`06_rig`, `07_export` (Roblox FBX), and `08_verify` (GLB export, round trips, validation, colour gate).
Shared code lives in `build/sp_lib.py` (anatomy), `build/sp_gear.py` (gear), `build/sp_r15.py` (skeleton and
part map), and `build/bt.py` (the skill's build template). Review renders and gate reports are in `review/`.

`tools/studio_preview.py` + `tools/studio_preview.lua` build a session-only preview in Studio without uploads
(EditableMesh/EditableImage). Serve the packed files on `127.0.0.1:48900` on the Studio machine first.
