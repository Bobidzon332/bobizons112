"""Print width profiles of the cleaned mattes (largest component, holes filled) and save cleaned mattes."""
import json
import numpy as np
from PIL import Image
from collections import deque

import os
REF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ref')
info = json.load(open(f'{REF}/mattes.json'))


def components(m):
    h, w = m.shape
    lab = np.zeros((h, w), np.int32)
    n = 0; sizes = {}
    for y in range(h):
        for x in range(w):
            if m[y, x] and not lab[y, x]:
                n += 1; q = deque([(y, x)]); lab[y, x] = n; c = 0
                while q:
                    cy, cx = q.popleft(); c += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n; q.append((ny, nx))
                sizes[n] = c
    return lab, sizes


def fill_holes(m):
    h, w = m.shape
    outside = np.zeros_like(m)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not m[y, x]:
                outside[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if not m[y, x] and not outside[y, x]:
                outside[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not m[ny, nx] and not outside[ny, nx]:
                outside[ny, nx] = True; q.append((ny, nx))
    return ~outside


out = {}
for name in ('front', 'back', 'side'):
    m = np.asarray(Image.open(f'{REF}/matte_{name}.png')) > 127
    lab, sizes = components(m)
    big = max(sizes, key=sizes.get)
    m = lab == big
    # holes between arm and torso are open to the border at the bottom, so only enclosed specks fill
    filled = fill_holes(m)
    small_holes = filled & ~m
    hl, hs = components(small_holes)
    for k, s in hs.items():
        if s < 60:
            m[hl == k] = True
    Image.fromarray((m * 255).astype(np.uint8)).save(f'{REF}/matte_{name}.png')
    rows = np.where(m.any(axis=1))[0]
    top, bot = rows.min(), rows.max()
    H = bot - top + 1
    x0 = info[name]['panel'][0]
    prof = []
    print(f'== {name}: top {top + info[name]["panel"][1]} ground {bot + info[name]["panel"][1]} H {H}px')
    for pct in range(0, 101, 2):
        y = min(bot, top + int(round(pct / 100 * (H - 1))))
        xs = np.where(m[y])[0]
        # runs
        runs = []
        if len(xs):
            start = xs[0]; prev = xs[0]
            for x in xs[1:]:
                if x != prev + 1:
                    runs.append((int(start), int(prev))); start = x
                prev = x
            runs.append((int(start), int(prev)))
        prof.append(dict(pct=pct, y=int(y), span=[int(xs.min()), int(xs.max())] if len(xs) else None, runs=runs))
        print(f'{pct:3d}% y{y:4d} ' + ' '.join(f'[{a}-{b}]' for a, b in runs))
    out[name] = dict(top=int(top), bottom=int(bot), H=int(H), profile=prof)
json.dump(out, open(f'{REF}/profiles.json', 'w'))
