"""Shared scene layout: where the cabins sit and where the gravel path runs.

Every stage (scatter masks, path boolean, cabins, cameras) reads these numbers,
so moving the cabin or bending the path is a one-place change.
Units: metres, terrain is a ~179 m disc centred on the origin.
"""
import numpy as np

# Cabin clearing (two A-frames + deck), rounded box.
CABIN_CENTER = (0.0, 6.0)
CABIN_HALF = (13.0, 9.0)      # half size x, y
CABIN_CORNER = 4.0            # corner rounding

# Gravel path: leaves the cabin deck southwards and winds to the terrain edge.
# No cabins any more: the road now runs right through the forest (north end extended).
PATH = [(6.0, 70.0), (2.0, 52.0), (-4.0, 36.0), (-6.0, 20.0), (-2.0, 8.0), (0.0, -3.0),
        (1.5, -14.0), (-2.5, -27.0), (-9.0, -39.0), (-8.0, -53.0), (-1.0, -66.0),
        (5.0, -80.0), (8.0, -90.0)]
PATH_HALF_WIDTH = 1.75         # 3.5 m gravel road (car is ~1.9 m wide)
USE_CABINS = False             # user dropped the cabins 2026-10-19

# Sun: his frames are backlit (sun behind trees/cabins). Azimuth from +X, degrees.
SUN_AZIMUTH = 110.0
SUN_ELEVATION = 40.0

# Path surface sits this far above the terrain (centre / edge) to avoid z-fighting.
LIFT_MID, LIFT_EDGE = 0.03, 0.005

# Cabins (from his frames). Local frame: gable/front faces -Y, floor top at z=0.
CABIN_A = dict(center=(-5.0, 7.2), rot=-15.0, W=6.6, D=10.0, eave=2.9, ridge=8.0)
CABIN_B = dict(center=(5.2, 8.0), rot=31.0, W=5.2, D=7.5, eave=2.6, ridge=6.6)
# Deck = union of rectangles (cx, cy, sx, sy, rot_deg), top a little above the highest ground.
DECK_RECTS = [(-5.1, 6.95, 8.4, 12.5, -15.0), (1.2, 4.0, 5.2, 4.8, 0.0), (5.2, 8.0, 6.8, 9.1, 31.0)]
DECK_THICK = 0.32

# Gravel pad between the path end and the cabin deck.
PAD_CENTER = (0.0, 0.5)
PAD_HALF = (7.0, 2.5)
PAD_CORNER = 2.0


def path_spline(step=0.1):
    """Catmull-Rom through PATH, resampled every `step` m. Returns (N,2)."""
    p = np.asarray(PATH, dtype=np.float64)
    p = np.vstack([2 * p[0] - p[1], p, 2 * p[-1] - p[-2]])
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        n = max(2, int(np.linalg.norm(p2 - p1) / step))
        for t in np.linspace(0.0, 1.0, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(p[-2])
    return np.asarray(out)


def dist_to_pad(xy):
    c = np.asarray(PAD_CENTER)
    h = np.asarray(PAD_HALF) - PAD_CORNER
    q = np.abs(xy - c) - h
    return (np.linalg.norm(np.maximum(q, 0.0), axis=1)
            + np.minimum(np.max(q, axis=1), 0.0) - PAD_CORNER)


def dist_to_deck(xy):
    """Signed distance to the union of deck rectangles (negative on the deck)."""
    best = np.full(len(xy), np.inf)
    for cx, cy, sx, sy, rot in DECK_RECTS:
        r = np.radians(rot)
        d = xy - np.array([cx, cy])
        lx = d[:, 0] * np.cos(r) + d[:, 1] * np.sin(r)
        ly = -d[:, 0] * np.sin(r) + d[:, 1] * np.cos(r)
        q = np.abs(np.stack([lx, ly], axis=1)) - np.array([sx / 2, sy / 2])
        sd = np.linalg.norm(np.maximum(q, 0.0), axis=1) + np.minimum(np.max(q, axis=1), 0.0)
        best = np.minimum(best, sd)
    return best


def dist_to_path(xy):
    """xy: (N,2) array -> distance to the smoothed path centre line."""
    p = path_spline(0.5)
    best = np.full(len(xy), np.inf)
    for a, b in zip(p[:-1], p[1:]):
        ab = b - a
        t = np.clip(((xy - a) @ ab) / (ab @ ab), 0.0, 1.0)
        proj = a + t[:, None] * ab
        best = np.minimum(best, np.linalg.norm(xy - proj, axis=1))
    return best


def dist_to_cabin(xy):
    """Signed distance to the rounded cabin clearing (negative inside)."""
    c = np.asarray(CABIN_CENTER)
    h = np.asarray(CABIN_HALF) - CABIN_CORNER
    q = np.abs(xy - c) - h
    outside = np.linalg.norm(np.maximum(q, 0.0), axis=1)
    inside = np.minimum(np.max(q, axis=1), 0.0)
    return outside + inside - CABIN_CORNER


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)
