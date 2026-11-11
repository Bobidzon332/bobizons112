--!strict
-- In-Studio preview of CH_StarPlatinum without uploads (roblox-3d-model no-upload route, extended to 15 R15
-- parts with normals and SurfaceAppearance maps). Run through the Studio MCP execute_luau in EDIT mode while
-- tools/studio_preview.py output is served on http://127.0.0.1:48900/ from the same machine.
-- Builds workspace.StarPlatinum_Preview (anchored MeshParts). The meshes and images are session-local
-- (EditableMesh/EditableImage): they do not survive saving or publishing; the permanent path is the FBX
-- through the 3D Importer.
local HttpService = game:GetService("HttpService")
local AssetService = game:GetService("AssetService")
local ChangeHistoryService = game:GetService("ChangeHistoryService")
local BASE = "http://127.0.0.1:48900/"

local function u32(b: buffer, o: number): number
	return buffer.readu32(b, o)
end

local function buildMesh(name: string): (MeshPart, number)
	local b = buffer.fromstring(HttpService:GetAsync(BASE .. name .. ".mesh.bin"))
	assert(buffer.readstring(b, 0, 4) == "RMSH" and u32(b, 4) == 2, "bad mesh header " .. name)
	local nv, nuv, nn, nt = u32(b, 8), u32(b, 12), u32(b, 16), u32(b, 20)
	local pOff = 24
	local uOff = pOff + nv * 12
	local nOff = uOff + nuv * 8
	local tOff = nOff + nn * 12
	local qOff = tOff + nt * 12
	local rOff = qOff + nt * 12
	local em = AssetService:CreateEditableMesh()
	local vid, uid, nid = table.create(nv), table.create(nuv), table.create(nn)
	for i = 0, nv - 1 do
		local o = pOff + i * 12
		vid[i + 1] = em:AddVertex(Vector3.new(buffer.readf32(b, o), buffer.readf32(b, o + 4), buffer.readf32(b, o + 8)))
	end
	for i = 0, nuv - 1 do
		local o = uOff + i * 8
		uid[i + 1] = em:AddUV(Vector2.new(buffer.readf32(b, o), buffer.readf32(b, o + 4)))
	end
	for i = 0, nn - 1 do
		local o = nOff + i * 12
		nid[i + 1] = em:AddNormal(Vector3.new(buffer.readf32(b, o), buffer.readf32(b, o + 4), buffer.readf32(b, o + 8)))
	end
	for i = 0, nt - 1 do
		local o, q, r = tOff + i * 12, qOff + i * 12, rOff + i * 12
		local f = em:AddTriangle(vid[u32(b, o) + 1], vid[u32(b, o + 4) + 1], vid[u32(b, o + 8) + 1])
		em:SetFaceUVs(f, { uid[u32(b, q) + 1], uid[u32(b, q + 4) + 1], uid[u32(b, q + 8) + 1] })
		em:SetFaceNormals(f, { nid[u32(b, r) + 1], nid[u32(b, r + 4) + 1], nid[u32(b, r + 8) + 1] })
	end
	local part = AssetService:CreateMeshPartAsync(Content.fromObject(em), { CollisionFidelity = Enum.CollisionFidelity.Box })
	return part, nt
end

local function image(key: string): EditableImage
	local raw = buffer.fromstring(HttpService:GetAsync(BASE .. key .. ".tex.bin"))
	assert(buffer.readstring(raw, 0, 4) == "RTEX", "bad texture header " .. key)
	local n = u32(raw, 4)
	local px = buffer.create(n * n * 4)
	buffer.copy(px, 0, raw, 8, n * n * 4)
	local ei = AssetService:CreateEditableImage({ Size = Vector2.new(n, n) })
	ei:WritePixelsBuffer(Vector2.zero, Vector2.new(n, n), px)
	return ei
end

local manifest = HttpService:JSONDecode(HttpService:GetAsync(BASE .. "parts.json"))
local recording = ChangeHistoryService:TryBeginRecording("StarPlatinum preview import")
local old = workspace:FindFirstChild("StarPlatinum_Preview")
if old then
	old:Destroy()
end
local model = Instance.new("Model")
model.Name = "StarPlatinum_Preview"
local maps = { BC = image("BC"), N = image("N"), R = image("R"), M = image("M") }
local bp = workspace:FindFirstChild("Baseplate")
local groundY = if bp and bp:IsA("BasePart") then bp.Position.Y + bp.Size.Y / 2 else 0
local minY = math.huge
for _, info in manifest.parts do
	minY = math.min(minY, info.centre[2] - info.size[2] / 2)
end
local origin = Vector3.new(0, groundY - minY, -12)
local report, total, surface = {}, 0, "SurfaceAppearance"
for name, info in manifest.parts do
	local part, tris = buildMesh(name)
	part.Name = name
	part.Anchored = true
	part.CFrame = CFrame.new(origin + Vector3.new(info.centre[1], info.centre[2], info.centre[3]))
	local ok = pcall(function()
		local sa = Instance.new("SurfaceAppearance")
		sa.ColorMapContent = Content.fromObject(maps.BC)
		sa.NormalMapContent = Content.fromObject(maps.N)
		sa.RoughnessMapContent = Content.fromObject(maps.R)
		sa.MetalnessMapContent = Content.fromObject(maps.M)
		sa.Parent = part
	end)
	if not ok then
		surface = "TextureContent (SurfaceAppearance content rejected)"
		part.TextureContent = Content.fromObject(maps.BC)
	end
	part.Parent = model
	total += tris
	table.insert(report, string.format("%s %d", name, tris))
end
model.Parent = workspace
if recording then
	ChangeHistoryService:FinishRecording(recording, Enum.FinishRecordingOperation.Commit)
end
local cf, size = model:GetBoundingBox()
return string.format("parts=%d tris=%d size=%s at=%s maps=%s | %s", #report, total, tostring(size),
	tostring(cf.Position), surface, table.concat(report, ", "))
