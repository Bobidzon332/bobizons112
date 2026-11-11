"""IoU of the world_gate silhouette against the reference matte dilated by k px (ink outline test)."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image

view, sil = sys.argv[1], sys.argv[2]
ref = np.asarray(Image.open(os.path.join(ROOT, 'ref', f'matte_{view}.png')).convert('L')) > 127
m = Image.open(sil).convert('RGBA')
if m.size != (ref.shape[1], ref.shape[0]):
    m = m.resize((ref.shape[1], ref.shape[0]), Image.BOX)
m = np.asarray(m).astype(float)
mod = m[..., 3] > 127 if m[..., 3].min() < 250 else np.abs(m[..., :3].mean(-1) - m[0, 0, :3].mean()) > 60


def dil(x):
    y = x.copy()
    y[1:] |= x[:-1]; y[:-1] |= x[1:]; y[:, 1:] |= x[:, :-1]; y[:, :-1] |= x[:, 1:]
    return y


r = ref.copy()
for k in range(4):
    iou = (r & mod).sum() / (r | mod).sum()
    print(f'dilate {k}px: IoU {iou:.3f}  ref-only {(r & ~mod).sum() / r.sum():.3f}  model-only {(mod & ~r).sum() / r.sum():.3f}')
    r = dil(r)
