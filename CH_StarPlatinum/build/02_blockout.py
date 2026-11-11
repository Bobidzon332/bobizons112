"""Phase 02: blockout. Primary body masses (metaball, coarse) and gear volumes, all in LOW.
Rerunnable: deletes what this phase owns, rebuilds, saves the master.

blender --background --python build/02_blockout.py -- [--master CH_StarPlatinum_master.blend]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt
import sp_lib as L
import sp_gear as G

L.setup("02_blockout")


def main():
    a = L.args()
    bt.open_master(a.master)
    bt.clear_owned()
    m = L.Meta(L.name("BodyMeta", "tmp"), res=0.012)
    L.body_anatomy(m, detail=False)
    body = m.to_mesh(L.name("Body", "LOD0"), collection="LOW")
    bt.shade_smooth(body, 3.2)
    G.build_all_gear(seg=0.6, collection="LOW")
    n = sum(len(o.data.polygons) for o in bt.col("LOW").objects if o.type == "MESH")
    bt.log("LOW objects", len(bt.col("LOW").objects), "faces", n)
    bt.save_master(a.master)


main()
