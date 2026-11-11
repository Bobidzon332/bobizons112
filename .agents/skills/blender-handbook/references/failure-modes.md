# Failure Modes — Symptom → Action

The orchestrator's job when something goes wrong is to classify the symptom fast and route to the right fix. Most entries end with a pointer into the sub-skill that owns the real recipe — load that sub-skill before improvising.

---

## 1. Execution and MCP mechanics

| Problem | Action |
|---------|--------|
| MCP timeout | Break the failing chunk into smaller pieces |
| `Code execution error: <line>` | Read the error; fix that one line; retry |
| Object not found in next call | You used a Python variable instead of `bpy.data.objects['name']` |
| Render took too long | Reduce samples, enable adaptive sampling, lower resolution |
| File not at expected path | Use absolute paths; verify with Bash `ls` |
| `ConnectionRefusedError` / "Could not connect to Blender" | Blender is not running or BlenderMCP addon is not started. Tell user: **Edit → Preferences → Add-ons → enable 'Interface: MCP for Blender'**, press **N** in 3D Viewport → **MCP for Blender** tab → click **Start MCP Server** (port 9876 default). |
| Poly Pizza 403 / Cloudflare HTML challenge | Cloudflare blocks datacenter/VPN IPs. Retry on residential network or download `.glb` manually from `https://poly.pizza` and import via `File > Import > glTF 2.0`. |
| Poly Haven `.blend` open error | Asset was created in a newer Blender version. Switch download format parameter or fallback to glTF. |
| Large scene snapshot truncated / JSON error | Exceeded `MAX_SNAPSHOT_OBJECTS` (4000) or `MAX_SNAPSHOT_SELECTED` (1000). Inspect scene per collection instead of selecting all. |

---

## 2. Blender 5.x version compatibility

Full matrix and smoke test: `${COMMANDCODE_SKILL_DIR}/references/blender-version-compat.md`.

| Problem | Action |
|---------|--------|
| `'Action' object has no attribute 'fcurves'` | Blender 5.x layered Actions; walk `action.layers[].strips[].channelbags[].fcurves` instead. See `blender-animation` Recipe 3 for the compat helper. |
| `BLENDER_EEVEE_NEXT` rejected | Blender 5.x renamed it back to `BLENDER_EEVEE`. See `blender-rendering` Recipe 3 for the try/except fallback. |
| `KeyError: 'Subsurface IOR'` (or other input names) | Blender 5.x marks some BSDF inputs `enabled=False` (currently `Weight`, `Subsurface IOR`); they're reachable by iteration but not string-key lookup. See `blender-materials` Recipe 9 for the `set_input` helper. |
| `Error: Cannot render, no camera` | `scene.camera is None`. Always run the `ensure_camera()` guard before any render — see `blender-rendering` Recipes 5 / 6. The orchestrator must check this before chaining to render even if the user's prompt didn't ask for a camera explicitly. |

---

## 3. The user says it looks wrong

| Problem | Action |
|---------|--------|
| "Scene is grey / no materials visible" while looking at Blender's viewport | Blender's viewport defaults to **Solid** shading mode, which ignores materials. The render is correct; only the viewport looks grey. After every scene assembly, set the viewport to Material Preview — see `${COMMANDCODE_SKILL_DIR}/scripts/set_viewport_material_preview.py`. |
| "Materials look flat / no texture" | Flat PBR colors lack surface variation. Add procedural textures (Noise/Voronoi → ColorRamp → Roughness or Bump) for steel scratches, hammered metal, leather grain, etc. See `blender-materials` Recipe 12 (procedural wood) for the pattern. |
| Coloured glass renders flat/metallic instead of "glass-like" | Tint was set on `Base Color` of the Principled BSDF only. Real coloured glass needs **Volume Absorption** for depth-based tint. See `blender-materials` Recipe 6b. Also: `Roughness=0.0` produces mirror-flat highlights that look metallic — use 0.02–0.05 instead. |
| Glass renders black on the inside | `transmission_bounces` too low. Default 12 is insufficient for thick or layered glass. Set `scene.cycles.transmission_bounces = 24`. |
| Elongated subject renders as a thin pole instead of a recognisable shape | Camera is viewing the **thin axis** of an elongated object. Rotate the object so its broad axis faces the camera. See `blender-modeling` "Critical: axis orientation for elongated objects". |
| Blade/spike has a "chiselled flat" tip instead of a point | Top vertices were scaled toward zero but not merged. Use the proper tapering recipe in `blender-modeling` ("Critical: tapering to a point") — collapse top verts to the centreline AND `remove_doubles`. |

---

## 4. Subject fidelity and scope

| Problem | Action |
|---------|--------|
| Subject looks wrongly proportioned (e.g. blade too short, chair too narrow) | The orchestrator skipped the dimension lookup. Always read `${COMMANDCODE_SKILL_DIR}/references/common-object-dimensions.md` BEFORE generating modelling code. Don't guess. |
| User asks for a "human" / "character" / "face" / "person" | Pure-recipe primitives produce a recognisable silhouette only, NOT a human face. Suggest one of: (a) `mcp__blender__download_polyhaven_asset` / `download_sketchfab_model` / `generate_hyper3d_model_via_text` for an actual human base mesh, then chain materials + lighting + render; (b) load `blender-mcp` for the asset-source workflow and `character-artist` for proportions. Do NOT pretend a sphere-with-features looks human — it doesn't. See `${COMMANDCODE_SKILL_DIR}/references/common-object-dimensions.md` "Characters / avatars" section. |
| Material looks wrong after export | You used non-Principled-BSDF nodes; rebuild the material with Principled only. |

---

## Escalation rule

If the same failure class repeats after a fix attempt, stop patching and load `quality-refinement-autoloop` — collect evidence and distinguish an artifact defect from an instruction conflict. Ordinary recovery does not authorize skill edits. When two skills disagree about the artifact, `blender-skill-harmonizer` owns the resolution.
