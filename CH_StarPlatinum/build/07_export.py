"""Phase 07: Roblox delivery.
  exports/roblox/CH_StarPlatinum_R15.fbx  skinned R15 rig: 15 meshes named <Part>_Geo + R15 armature
      * 1 file unit = 1 stud (scene unit scale 0.01, FBX Unit Scale), 6.5 studs tall (TARGET_STUDS)
      * Root and LowerTorso at the origin (Roblox body specification), Y up, -Z forward
      * Add Leaf Bones off, Path Mode Copy + embedded textures (Roblox export settings page)
      * custom split normals copied from the joined mesh so the R15 cuts do not show shading seams
  exports/roblox/T_StarPlatinum_{BC,N,R,M}.png  1024 px SurfaceAppearance maps (Roblox caps at 1024)
  exports/roblox/roblox-manifest.json           per-part triangle counts and import settings
The GLB (metres) is written by the skill's export_delivery.py (see build/run_all.sh).

blender --background --python build/07_export.py -- [--master ...]
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
import numpy as np
from mathutils import Matrix, Vector
import bt
import sp_lib as L
import sp_r15 as R

L.setup("07_export")
TARGET_STUDS = 6.5          # asset-brief TARGET: 2.10 m reference height -> 6.5 studs
REF_HEIGHT_M = 2.10
OUT = os.path.join(L.ROOT, "exports", "roblox")
TEX = os.path.join(L.ROOT, "textures")


def downsample(src, dst, res, colorspace):
    """2048 -> 1024 by a 2x2 box filter (pixel values copied as stored, no colour conversion)."""
    img = bpy.data.images.load(src, check_existing=False)
    img.colorspace_settings.name = colorspace
    w, h = img.size
    a = np.empty(w * h * 4, np.float32)
    img.pixels.foreach_get(a)
    f = w // res
    a = a.reshape(res, f, res, f, 4).mean(axis=(1, 3))
    bpy.data.images.remove(img)
    out = bpy.data.images.new(os.path.basename(dst).rsplit(".", 1)[0], res, res, alpha=False)
    out.colorspace_settings.name = colorspace
    out.pixels.foreach_set(a.ravel())
    out.filepath_raw = dst
    out.file_format = "PNG"
    out.save()
    return out


def roblox_material(maps):
    mat = bpy.data.materials.new("MAT_StarPlatinum")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")

    def tex(img):
        n = nt.nodes.new("ShaderNodeTexImage")
        n.image = img
        return n
    nt.links.new(tex(maps["BC"]).outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex(maps["R"]).outputs["Color"], bsdf.inputs["Roughness"])
    nt.links.new(tex(maps["M"]).outputs["Color"], bsdf.inputs["Metallic"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(tex(maps["N"]).outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def split_parts(src, arm, mat, M):
    """One object per R15 part, vertex groups kept, normals locked from the joined mesh."""
    me = src.data
    loop_normals = np.empty(len(me.loops) * 3, np.float32)
    me.corner_normals.foreach_get("vector", loop_normals)
    parts_attr = [0] * len(me.polygons)
    me.attributes["r15_part"].data.foreach_get("value", parts_attr)
    out = {}
    for pi, part in enumerate(R.R15_PARTS):
        nm = part + "_Geo"
        new_me = me.copy()
        new_me.name = nm
        new_me.normals_split_custom_set(loop_normals.reshape(-1, 3).tolist())
        ob = bpy.data.objects.new(nm, new_me)
        bpy.context.scene.collection.objects.link(ob)
        for vg in src.vertex_groups:
            ob.vertex_groups.new(name=vg.name)
        bm = bmesh.new()
        bm.from_mesh(new_me)
        layer = bm.faces.layers.int.get("r15_part")
        dead = [f for f in bm.faces if f[layer] != pi]
        bmesh.ops.delete(bm, geom=dead, context="FACES")
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
        bm.to_mesh(new_me)
        bm.free()
        new_me.transform(M)
        for attr in ("r15_part", "region"):
            if attr in new_me.attributes:
                new_me.attributes.remove(new_me.attributes[attr])
        new_me.materials.clear()
        new_me.materials.append(mat)
        ob.parent = arm
        mod = ob.modifiers.new("Armature", "ARMATURE")
        mod.object = arm
        # drop empty groups so each part lists only the bones that move it (by name: indices shift on removal)
        used = set()
        for v in new_me.vertices:
            for g in v.groups:
                if g.weight > 0:
                    used.add(ob.vertex_groups[g.group].name)
        for nm_g in [vg.name for vg in ob.vertex_groups if vg.name not in used]:
            ob.vertex_groups.remove(ob.vertex_groups[nm_g])
        out[part] = ob
    return out


def main():
    a = L.args()
    bt.open_master(a.master)
    os.makedirs(OUT, exist_ok=True)
    maps = {}
    for k, cs in (("BC", "sRGB"), ("N", "Non-Color"), ("R", "Non-Color"), ("M", "Non-Color")):
        maps[k] = downsample(os.path.join(TEX, f"T_StarPlatinum_{k}_2048.png"),
                             os.path.join(OUT, f"T_StarPlatinum_{k}.png"), 1024, cs)
    src = bpy.data.objects["CH_StarPlatinum_LOD0"]
    src_arm = bpy.data.objects["ARM_StarPlatinum"]
    # fresh scene holding only the delivery copy
    scn = bpy.data.scenes.new("ROBLOX_EXPORT")
    scn.unit_settings.system = "METRIC"
    scn.unit_settings.scale_length = 0.01
    scn.unit_settings.length_unit = "CENTIMETERS"
    s = TARGET_STUDS / REF_HEIGHT_M
    M = Matrix.Scale(s, 4) @ Matrix.Translation(-R.J["hip_centre"])
    arm_data = src_arm.data.copy()
    arm_data.name = "Armature"
    arm = bpy.data.objects.new("Armature", arm_data)
    scn.collection.objects.link(arm)
    arm_data.transform(M)
    mat = roblox_material(maps)
    with bpy.context.temp_override(scene=scn):
        parts = split_parts(src, arm, mat, M)
    for ob in list(scn.collection.objects):
        if ob.name not in [p.name for p in parts.values()] + [arm.name]:
            scn.collection.objects.unlink(ob)
    vl = scn.view_layers[0]
    fbx = os.path.join(OUT, "CH_StarPlatinum_R15.fbx")
    with bpy.context.temp_override(scene=scn, view_layer=vl, active_object=arm, selected_objects=list(scn.objects)):
        bpy.ops.export_scene.fbx(filepath=fbx, use_selection=False, object_types={"ARMATURE", "MESH"},
                                 apply_unit_scale=True, apply_scale_options="FBX_SCALE_UNITS", global_scale=1.0,
                                 axis_forward="-Z", axis_up="Y", bake_space_transform=False,
                                 use_mesh_modifiers=False, mesh_smooth_type="OFF", use_tspace=True,
                                 add_leaf_bones=False, use_armature_deform_only=False, primary_bone_axis="Y",
                                 secondary_bone_axis="X", bake_anim=False, path_mode="COPY", embed_textures=True)
    tri = {p: sum(len(f.vertices) - 2 for f in o.data.polygons) for p, o in parts.items()}
    zs = [(v.co.z) for o in parts.values() for v in o.data.vertices]
    manifest = {
        "asset": "CH_StarPlatinum", "file": os.path.basename(fbx), "format": "FBX 7.4 binary",
        "rig": "R15 skinned (Root > HumanoidRootNode > LowerTorso ...)", "units": "1 file unit = 1 stud",
        "height_studs": round(max(zs) - min(zs), 3), "scale_studs_per_metre": round(s, 4),
        "origin": "Root/LowerTorso joint at 0,0,0 (feet below origin)", "axes": "Y up, -Z forward",
        "max_influences": 4, "triangles_per_part": tri, "triangles_total": sum(tri.values()),
        "roblox_meshpart_cap": 20000, "budget_per_part": 10000,
        "textures": {k: f"T_StarPlatinum_{k}.png" for k in maps},
        "texture_colorspace": {"BC": "sRGB", "N": "Non-Color, tangent space OpenGL +Y", "R": "Non-Color",
                               "M": "Non-Color"},
        "studio_import": {"Rig Type": "R15 (auto-detected)", "Scale Unit": "Studs",
                          "SurfaceAppearance": "ColorMap=BC, NormalMap=N, RoughnessMap=R, MetalnessMap=M"},
    }
    json.dump(manifest, open(os.path.join(OUT, "roblox-manifest.json"), "w"), indent=1)
    bt.log("FBX", fbx, "parts", len(parts), "tris", sum(tri.values()), "max part", max(tri.items(), key=lambda kv: kv[1]),
           "height studs", manifest["height_studs"])


main()
