"""Round-trip check of the Roblox R15 FBX in a clean Blender: names, hierarchy, influences, tris, scale."""
import bpy, sys, json, os
path, out = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.unit_settings.scale_length = 0.01      # read back in the authoring units (1 unit = 1 stud)
bpy.ops.import_scene.fbx(filepath=path, use_custom_normals=True)
EXPECT = ["Head", "UpperTorso", "LowerTorso", "LeftUpperArm", "LeftLowerArm", "LeftHand", "RightUpperArm",
          "RightLowerArm", "RightHand", "LeftUpperLeg", "LeftLowerLeg", "LeftFoot", "RightUpperLeg", "RightLowerLeg",
          "RightFoot"]
rep = {"file": os.path.basename(path), "errors": []}
meshes = {o.name: o for o in bpy.data.objects if o.type == "MESH"}
arms = [o for o in bpy.data.objects if o.type == "ARMATURE"]
rep["meshes"] = sorted(meshes)
missing = [p + "_Geo" for p in EXPECT if p + "_Geo" not in meshes]
if missing:
    rep["errors"].append(f"missing meshes {missing}")
if len(arms) != 1:
    rep["errors"].append(f"armatures {len(arms)}")
arm = arms[0]
bones = {b.name: (b.parent.name if b.parent else None) for b in arm.data.bones}
rep["bones"] = bones
for need, parent in (("Root", None), ("HumanoidRootNode", "Root"), ("LowerTorso", "HumanoidRootNode"),
                     ("UpperTorso", "LowerTorso"), ("Head", "UpperTorso"), ("RightUpperArm", "UpperTorso"),
                     ("LeftUpperLeg", "LowerTorso"), ("RightFoot", "RightLowerLeg")):
    if bones.get(need, "missing") != parent:
        rep["errors"].append(f"bone {need} parent {bones.get(need, 'missing')} != {parent}")
leaf = [b for b in bones if b.endswith("_end")]
if leaf:
    rep["errors"].append(f"leaf bones present {leaf}")
tris, maxinf, unweighted, root_w = {}, 0, 0, 0
zmin, zmax = 1e9, -1e9
for n, o in meshes.items():
    me = o.data
    tris[n] = sum(len(p.vertices) - 2 for p in me.polygons)
    names = {g.index: g.name for g in o.vertex_groups}
    for v in me.vertices:
        ws = [g for g in v.groups if g.weight > 1e-4]
        maxinf = max(maxinf, len(ws))
        unweighted += not ws
        root_w += any(names.get(g.group) == "Root" for g in ws)
        z = (o.matrix_world @ v.co).z
        zmin, zmax = min(zmin, z), max(zmax, z)
    if tris[n] > 10000:
        rep["errors"].append(f"{n} {tris[n]} tris > 10k budget")
rep.update(tris=tris, tris_total=sum(tris.values()), max_influences=maxinf, unweighted_verts=unweighted,
           verts_on_root=root_w, height_units=round(zmax - zmin, 3), z_min=round(zmin, 3), z_max=round(zmax, 3),
           lowertorso_head=[round(c, 4) for c in (arm.matrix_world @ arm.data.bones["LowerTorso"].head_local)],
           images=sorted(i.name for i in bpy.data.images if i.has_data or i.packed_file))
if maxinf > 4:
    rep["errors"].append(f"max influences {maxinf} > 4")
if unweighted:
    rep["errors"].append(f"{unweighted} unweighted vertices")
if root_w:
    rep["errors"].append("vertices weighted to Root")
os.makedirs(out, exist_ok=True)
json.dump(rep, open(os.path.join(out, "fbx_roundtrip.json"), "w"), indent=1)
print("FBXCHECK", json.dumps({k: rep[k] for k in ("errors", "tris_total", "max_influences", "unweighted_verts",
                                                  "height_units", "z_min", "lowertorso_head", "images")}))
