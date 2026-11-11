# MCP Integration

The Blender MCP transport, install, client wiring, safe mode, telemetry, and connection troubleshooting live in the separate **`blender-mcp`** skill. Use that skill when the problem is the connection or the MCP surface.

The PyPI package was renamed from `blender-mcp` to **`mcp-for-blender`** (existing configs still work). Repo: `ahujasid/mcp-for-blender`.

---

## Capability discovery

Inspect the live tool inventory and schemas before executing. Tool namespaces, argument names, optional asset services, limits and protocol versions vary by server build. Query the running Blender version with the available execution tool (for example `bpy.app.version_string`). Missing optional asset tools do not block manual modeling; do not install services, upload references or download assets beyond the user-authorized scope.

The tables below are integration examples from a particular server implementation, not a live compatibility contract. Verify version-specific details against the connected server or its matching documentation. Root-path substitution is defined in the entry `SKILL.md`.

## Core tool examples

| Tool | Purpose | Key parameters |
|------|---------|----------------|
| `mcp__blender__execute_blender_code` | Run Python code inside Blender | `code` (string) |
| `mcp__blender__get_scene_info` | Scene overview: objects, materials, lights, cameras | — |
| `mcp__blender__get_object_info` | Detailed info for one object | `object_name` (string) |
| `mcp__blender__get_viewport_screenshot` | Capture the current 3D viewport | — |

Execution rules for generated Python: `${COMMANDCODE_SKILL_DIR}/references/code-execution-rules.md`.

---

## Asset download tools

### Poly Haven — HDRIs, textures, and models

Free CC0 library. Preferred source for production-quality environments, PBR textures, and pre-built models.

| Tool | Purpose |
|------|---------|
| `mcp__blender__search_polyhaven_assets` | Search the Poly Haven catalog |
| `mcp__blender__download_polyhaven_asset` | Download and import an asset by slug |

**Key behaviours** (from addon source):
- **Models import from `.blend`** (lossless); glTF/FBX are lossy fallbacks used only when the `.blend` was authored in a newer Blender than the running version.
- **Textures** download only the maps that wire to Principled BSDF: Diffuse, Rough, Metal, Displacement, nor_gl. AO, spec, anisotropy maps are skipped to keep downloads small.
- **HDRIs** default to `.hdr` format; `.exr` also available.
- Timeouts: API 10s connect / 30s read; file downloads 10s / 60s.
- Search results capped at 20 (max 50).

**Typical usage:**
```python
# Search for a forest HDRI
mcp__blender__search_polyhaven_assets(query="forest", type="hdris")

# Download and apply
mcp__blender__download_polyhaven_asset(slug="forest_slope", type="hdris", resolution="2k")
```

### Sketchfab — Community 3D models

Large catalog of user-uploaded models. Requires API key for downloads.

| Tool | Purpose |
|------|---------|
| `mcp__blender__search_sketchfab_models` | Search the Sketchfab catalog |
| `mcp__blender__download_sketchfab_model` | Download and import a model by UID |

**Notes:**
- API credentials can be set persistently in the addon preferences.
- Downloaded models may use non-Principled materials; rebuild if export is needed.

### Poly Pizza — Low-poly models

Curated low-poly / stylized models. Good for game assets and quick prototyping.

| Tool | Purpose |
|------|---------|
| `mcp__blender__search_polypizza_models` | Search with optional category and licence filters |
| `mcp__blender__download_polypizza_model` | Download and import a model by ID |

**Known issue — Cloudflare CDN blocking:**
Poly Pizza's CDN (`static.poly.pizza`) uses Cloudflare bot protection. Downloads from datacenter/VPN/cloud IPs get a 403 HTML challenge instead of the GLB file. This is **not** an API key problem. Workarounds:
1. Retry from a residential IP connection.
2. Download the `.glb` manually from `https://poly.pizza` and import via File → Import → glTF 2.0.

**Category IDs** (0–11): passed as integers. Licence IDs: 0 = CC-BY, 1 = CC0.

---

## AI 3D generation tools

### Hyper3D Rodin — Text/image to 3D

Generate 3D models from text descriptions or reference images using the Rodin API.

| Tool | Purpose |
|------|---------|
| `mcp__blender__generate_hyper3d_model_via_text` | Generate a 3D model from a text prompt |
| `mcp__blender__generate_hyper3d_model_via_image` | Generate a 3D model from a reference image |

**Notes:**
- Free trial available with key `vibecoding`.
- Results are stylized meshes, not production topology. Use as a starting point, then retopologize.
- API credentials can be stored persistently in addon preferences.

### Hunyuan3D — Tencent's 3D generation

Another AI model generation option.

| Tool | Purpose |
|------|---------|
| `mcp__blender__generate_hunyuan3d_model` | Generate a 3D model via Hunyuan3D |

---

## When to use asset tools vs. manual modeling

| Situation | Approach |
|-----------|----------|
| User asks for a "human" / "character" / "face" | Use asset tools for a base mesh, then chain materials + lighting |
| Need realistic environment backdrop | Poly Haven HDRIs or models |
| Quick prototype / game jam style | Poly Pizza low-poly models |
| Specific branded/custom object | Manual modeling via `02-modeling/` manuals |
| "Make a 3D model from this description" | Try Hyper3D Rodin text-to-3D, then refine |

---

## Recorded connection limits (verify against the running server)

| Parameter | Value | Source |
|-----------|-------|--------|
| Max snapshot objects | 4000 | `MAX_SNAPSHOT_OBJECTS` in addon.py |
| Max snapshot selected | 1000 | `MAX_SNAPSHOT_SELECTED` in addon.py |
| Default port | 9876 | Configurable via `BLENDER_PORT` env var |
| Code execution timeout | 180 s | Per-call limit |
| Protocol version | 9 | `ADDON_PROTOCOL_VERSION` in addon.py |
