"""Extract subject mattes from the orthographic panels of the Star Platinum model sheet.

Background: dark violet gradient (B notably above R and G, low luminance). Flood-fill from the
panel border over background-like pixels, then the complement is the subject. Ground shadow and
labels are cut at the measured ground row.
"""
import os, sys, json
import numpy as np
from PIL import Image
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'ref', 'stand_sheet_original.png')
OUT = os.path.join(ROOT, 'ref')
PANELS = {  # x0, y0, x1, y1 in sheet pixels (exclusive end)
    'front': (20, 95, 302, 900),
    'back': (312, 95, 598, 900),
    'side': (602, 95, 762, 900),
}

im = np.asarray(Image.open(SRC).convert('RGB')).astype(np.int32)


def bg_like(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r + g + b) / 3.0
    return (lum < 64) & (lum > 12) & ((b - r) >= 9) & ((b - g) >= 14)


def flood(mask_ok):
    h, w = mask_ok.shape
    seen = np.zeros_like(mask_ok, dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if mask_ok[y, x] and not seen[y, x]:
                seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if mask_ok[y, x] and not seen[y, x]:
                seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and mask_ok[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    return seen


def close_open(m, it=1):
    # tiny binary morphology without scipy
    def dil(x):
        y = x.copy()
        y[1:] |= x[:-1]; y[:-1] |= x[1:]; y[:, 1:] |= x[:, :-1]; y[:, :-1] |= x[:, 1:]
        return y
    def ero(x):
        return ~dil(~x)
    for _ in range(it):
        m = ero(dil(m))
    for _ in range(it):
        m = dil(ero(m))
    return m


report = {}
for name, (x0, y0, x1, y1) in PANELS.items():
    a = im[y0:y1, x0:x1]
    bg = flood(bg_like(a))
    subj = close_open(~bg, 1)
    # ground: the lowest row where subject spans a boot-sole sized width; drop the cast shadow below
    rows = np.where(subj.any(axis=1))[0]
    top = int(rows.min())
    # shadow is brownish-dark (R >= B); sole rows are near-black or have outline. find lowest row whose
    # subject pixels are mostly not shadow-coloured
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    shadow = (r >= b - 2) & ((r + g + b) / 3 < 70)
    ground = int(rows.max())
    for y in range(int(rows.max()), top, -1):
        s = subj[y]
        if s.sum() == 0:
            continue
        frac_shadow = (shadow[y] & s).sum() / s.sum()
        if frac_shadow < 0.6:
            ground = y
            break
    subj[ground + 1:] = False
    cols = np.where(subj.any(axis=0))[0]
    report[name] = dict(panel=[x0, y0, x1, y1], top_row=top + y0, ground_row=ground + y0,
                        height_px=ground - top + 1, left=int(cols.min()) + x0, right=int(cols.max()) + x0)
    Image.fromarray((subj * 255).astype(np.uint8)).save(f'{OUT}/matte_{name}.png')
    # visual check: subject over magenta
    vis = a.copy().astype(np.uint8)
    vis[~subj] = (255, 0, 255)
    Image.fromarray(vis).save(os.path.join(ROOT, 'review', f'00_matte_check_{name}.png'))
    # cropped colour reference panel with the same window, for init_master / compose_review
    Image.fromarray(a.astype(np.uint8)).save(f'{OUT}/{name}.png')
print(json.dumps(report, indent=1))
json.dump(report, open(f'{OUT}/mattes.json', 'w'), indent=1)
