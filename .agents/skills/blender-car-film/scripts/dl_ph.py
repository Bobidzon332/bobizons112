import json, os, sys, urllib.request
o = urllib.request.build_opener(); o.addheaders = [("User-Agent", "blender-car-film/1.0")]; urllib.request.install_opener(o)
root = sys.argv[1]
def get(u, p):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p): return
    for i in range(4):
        try: urllib.request.urlretrieve(u, p + ".part"); os.replace(p + ".part", p); return
        except Exception as e: print("retry", os.path.basename(p), e)
    raise SystemExit("failed " + u)
def files(a): return json.load(urllib.request.urlopen(f"https://api.polyhaven.com/files/{a}"))
for m, res in [("street_lamp_01","2k"),("fire_hydrant","1k"),("modular_chainlink_fence","1k"),("utility_box_01","1k"),
               ("modular_electricity_poles","1k"),("pine_tree_01","1k"),("fir_tree_01","1k"),("pine_sapling_medium","1k")]:
    g = files(m)["gltf"][res]["gltf"]
    d = os.path.join(root, "models", m)
    get(g["url"], os.path.join(d, os.path.basename(g["url"])))
    for rel, f in g["include"].items(): get(f["url"], os.path.join(d, rel))
    print("model", m)
for t in ["asphalt_snow","snow_02","weathered_plank_siding","grey_roof_tiles","rough_plaster_brick"]:
    f = files(t)
    for k in ["Diffuse","nor_gl","Rough","Displacement"]:
        if k in f: u = f[k]["2k"]["jpg"]["url"]; get(u, os.path.join(root, "tex", t, os.path.basename(u)))
    print("tex", t)
u = files("narrow_moonlit_road")["hdri"]["2k"]["hdr"]["url"]; get(u, os.path.join(root, "hdri", os.path.basename(u))); print("hdri ok")
