# Asset brief: CH_StarPlatinum

Phase 0 output of the `blender-image-to-3d` workflow. Every number below is measured from
`ref/stand_sheet_original.png` (1536 x 1024 model sheet) unless marked *inferred*.

```text
ASSET      CH_StarPlatinum (prefix CH_)

CATEGORY   character, humanoid biped (hyper-heroic anime proportions), deforming skin + rigid gear

VIEWS      sheet panel "Front View"  px box (20,95)-(302,900): orthographic, az 0, el 0, lens 0.
                                     Subject 788 px tall (hair tip y=104 to sole y=891), ground row 891.
           sheet panel "Back View"   px box (312,95)-(598,900): orthographic, az 180, el 0. 773 px tall,
                                     ground row 887 (drawn ~2% smaller than front; used for detail only).
           sheet panel "Side View"   px box (602,95)-(762,900): orthographic, az 90 (camera on +X, subject
                                     faces image-left = -Y), el 0. 782 px tall, ground row 885.
           "Head Close-up", "Head Back", "Hand Detail", "Shoulder Detail": perspective callouts,
                                     surface detail only (never proportions).
           "Dynamic Pose", manga panel: perspective concepts, silhouette/likeness only.
           Cropped panels: ref/front.png, ref/back.png, ref/side.png; mattes ref/matte_*.png
           (tools/extract_mattes.py + tools/profiles.py).

SCALE      No absolute scale cue in the sheet. Height chosen: 2.10 m sole-to-hair-tip
           (crown of skull ~1.96 m), a tall heroic figure. Front panel scale 0.002665 m/px,
           side 0.002685 m/px. Roblox delivery height: 6.5 studs total (see TARGET).

PROPORTIONS (fraction of total height from hair tip; front panel unless noted)
           P1  crown of skull (under hair)        6.5%   -> z 1.96 m   (inferred from eye line)
           P2  headband centre                    9.8%   -> z 1.894 m
           P3  chin                               14.3%  -> z 1.80 m
           P4  shoulder-pad span (widest, 18%)    232 px -> 0.618 m (0.294 of height)
           P5  chest width under pads (26%)       116 px -> 0.309 m
           P6  waist width (32%)                  79 px  -> 0.211 m
           P7  belt line                          34.4%  -> z 1.378 m, belt+discs width 113 px -> 0.301 m
           P8  fist centre                        45%    -> z 1.155 m, fist x offset 114 px -> 0.304 m
           P9  crotch                             54.5%  -> z 0.955 m (leg = 45.5% of height)
           P10 knee-pad centre                    60%    -> z 0.84 m, knee x offset 64 px -> 0.171 m
           P11 boot top                           67%    -> z 0.693 m
           P12 foot centres apart                 210 px -> 0.56 m (wide A-stance)
           P13 head width (face, cheek to cheek)  ~45 px -> 0.12 m; head height crown-chin ~0.16 m
           P14 foot length (side, 98%)            116 px -> 0.31 m
           P15 loincloth bottom                   ~51%   -> z 1.03 m

PARTS      (construction / overlap order; all gear is a separate object in the master)
           Body (skin, deforming): head+neck+torso+arms+fingers+legs, one fused organic mesh
           Hair (rigid to head): ~40 spiky locks, wild crown sweeping up and back
           Headband (rigid to head): gold band, oval dark gem with gold bezel at centre
           Scarf (rigid to upper torso, deforming at neck): red wrapped cowl, bunched on clavicles,
               shallow drape at the back
           Shoulder pads L/R (rigid to upper arm): curved gold plates, raised white Greek-key
               (nested square spiral) inlay, gold rivet on outer face
           Belt (rigid to lower torso): gold band, buckle plate with dark gem, 2 large gold hip discs
           Loincloth front/back (deforming, LowerTorso + thighs): lavender-white cloth flaps
           Bracers L/R (rigid to lower arm): black, wrist to below elbow, ribbed bands, gold wrist ring
           Gloves L/R (rigid to hand): black, fingers exposed (purple), 6 gold knuckle studs
           Knee pads L/R (rigid to lower leg): gold domes + black strap round the knee
           Boots L/R (rigid to lower leg / foot): black knee-high, gold chevron piping and lozenges
               down the shin, gold ankle ring with outer disc, low block heel
           Gold body piping: painted (texture), runs shoulders -> chest -> obliques, spine sides,
               outer thighs -> knees -> boots

SILHOUETTE 1 wild spiked hair crown; 2 wide flat-topped gold shoulder pads; 3 V-taper torso into
           narrow belted waist with white loincloth; 4 heavy black bracers + studded fists;
           5 wide stance with round gold knee pads and tall black boots

MATERIALS  skin: violet #8F6FD6 lit / #5B3FA6 shade, roughness 0.55, cel-style ink lines in albedo
           hair: near-black violet #1E1828 with violet rim strands, roughness 0.6
           gold (pads, belt, headband, studs, knee pads, piping): #C9A253, metallic 1, roughness 0.35
           white inlay on pads: #E6E2EE, metallic 0.2, roughness 0.4
           scarf: red #A8352A, woven cloth roughness 0.8
           black leather (boots, bracers, gloves): #1C1820, roughness 0.45
           loincloth: lavender-white #D8D2EE, cloth roughness 0.85
           eyes: white #E8E6F2 with pale iris, gem: dark violet-grey #3A3346 glossy

ARTICULATION Roblox R15 skeleton (Root > HumanoidRootNode > LowerTorso > UpperTorso > Head, arm and
           leg chains), skinned, max 4 influences, rigid gear weighted to one bone each.
           Rest pose = the sheet's pose (relaxed A-stance, fists, elbows soft).
           Animation: none requested (R15 rig plays standard R15 animations).

INFERRED   - skull shape under the hair, ears (hidden), back of the head hair mass (Head Back callout
             used for direction, not dimensions)
           - inner faces of thighs/arms, sole and palm geometry, fingers inside the fists
           - belt disc count (2 hip discs visible in all three panels; buckle detail from front)
           - underside of shoulder pads and inner straps; knee-strap buckle at the back
           - exact depth of torso and limbs where the side view overlaps arm over torso
           - absolute height (no scale cue)

TARGET     Engine Roblox Studio. Deliverables:
             * FBX, R15 skinned rig: 15 meshes `<Part>_Geo` + armature, 1 file unit = 1 stud,
               Add Leaf Bones off, embedded textures (Roblox export settings page)
             * GLB, single skinned mesh (metres) for interchange / Blender round trip
             * textures 1024 px (SurfaceAppearance cap): ColorMap, NormalMap (OpenGL +Y),
               RoughnessMap, MetalnessMap; 2048 masters kept in textures/
           Budget: Roblox in-experience hero (not a Marketplace avatar body): total LOW <= 30k
             triangles, every MeshPart <= 10k (Roblox hard cap 20k per MeshPart). Roblox builds its
             own render LODs; no custom LOD chain is imported.
           Game camera: third-person 70 deg FOV-equivalent, el 20 deg, ~12 studs; subject ~160 px
             tall at 1080p (gameplay-px 160 for gates).
```
