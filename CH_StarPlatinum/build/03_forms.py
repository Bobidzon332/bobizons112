"""Phase 03: forms. HIGH collection: full metaball anatomy (muscle groups, face planes, curled fingers)
and high-segment gear with the raised Greek-key inlay on the shoulder pads. HIGH is never exported;
it is the source for the normal/AO bake onto the LOW delivery meshes built in phase 04.

blender --background --python build/03_forms.py -- [--master CH_StarPlatinum_master.blend]
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt
import sp_lib as L
import sp_gear as G

L.setup("03_forms")
RES = 0.0045          # metaball polygonisation step (m): ~1/470 of the height


def main():
    a = L.args()
    bt.open_master(a.master)
    bt.clear_owned()
    m = L.Meta(L.name("BodyMeta", "tmp"), res=RES)
    arms = L.Meta(L.name("ArmMeta", "tmp"), res=RES)
    L.body_anatomy(m, detail=True, arms=arms)
    torso = m.to_mesh(L.name("Torso", "tmp"), collection="HIGH")
    limbs = arms.to_mesh(L.name("Arms", "tmp"), collection="HIGH")
    body = L.fuse_meshes(L.name("Body", "HIGH"), [torso, limbs], voxel=RES, collection="HIGH")
    bt.shade_smooth(body, 3.2)
    gear = G.build_all_gear(seg=2.0, collection="HIGH")
    for o in gear:
        boxy = any(k in o.name for k in ("ShoulderPad", "BeltBuckle", "BeltGem", "BootHeel"))
        if not boxy:
            s = o.modifiers.new("Subdivision", "SUBSURF")
            s.levels = 1
            L.apply_mods(o)
            bt.shade_smooth(o, math.radians(60))
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in bt.col("HIGH").objects if o.type == "MESH")
    bt.log("HIGH objects", len(bt.col("HIGH").objects), "tris", tris)
    bt.save_master(a.master)


main()
