"""Row-by-row silhouette comparison in world units: reference matte vs world_gate model silhouette.
usage: compare_rows.py <front|side> <sil.png> [pct,pct,...]"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image

CAL = {'front': dict(mpp=0.002665, axis=140, ground=796), 'side': dict(mpp=0.002685, axis=88, ground=790)}
view, sil = sys.argv[1], sys.argv[2]
pcts = [int(p) for p in sys.argv[3].split(',')] if len(sys.argv) > 3 else list(range(2, 100, 4))
c = CAL[view]
ref = np.asarray(Image.open(os.path.join(ROOT, 'ref', f'matte_{view}.png')).convert('L')) > 127
mod_img = Image.open(sil).convert('RGBA')
if mod_img.size != (ref.shape[1], ref.shape[0]):
    mod_img = mod_img.resize((ref.shape[1], ref.shape[0]), Image.BOX)
mod_img = np.asarray(mod_img).astype(float)
if mod_img[..., 3].min() < 250:
    mod = mod_img[..., 3] > 127
else:
    g = mod_img[..., :3].mean(-1)
    mod = np.abs(g - g[0, 0]) > 60
rows = np.where(ref.any(1))[0]
top = rows.min()


def runs(m, y):
    xs = np.where(m[y])[0]
    out = []
    if len(xs):
        s = p = xs[0]
        for x in xs[1:]:
            if x != p + 1:
                out.append((s, p)); s = x
            p = x
        out.append((s, p))
    return [(round(float((a - c['axis']) * c['mpp']), 3), round(float((b - c['axis']) * c['mpp']), 3))
            for a, b in out if b - a >= 2]


print(view, 'model', mod.shape, 'ref', ref.shape)
for pct in pcts:
    y = int(top + pct / 100 * (c['ground'] - top))
    z = round((c['ground'] - y) * c['mpp'], 3)
    print(f"{pct:3d}% z{z:.3f} R {runs(ref, y)}  M {runs(mod, y)}")
