"""check_colours-style gate: do the delivered ColorMap pixels carry the palette hexes (no linear/sRGB shift)?"""
import sys
import numpy as np
from PIL import Image
img = np.asarray(Image.open(sys.argv[1]).convert('RGB')).reshape(-1, 3)
cols, counts = np.unique(img, axis=0, return_counts=True)
top = cols[np.argsort(-counts)[:80]]
spec = {'skin #8C6CD4': (0x8C, 0x6C, 0xD4), 'gold #C9A253': (0xC9, 0xA2, 0x53), 'black #1E1A24': (0x1E, 0x1A, 0x24),
        'cloth #DCD6F0': (0xDC, 0xD6, 0xF0), 'red #A8352A': (0xA8, 0x35, 0x2A), 'hair #1D1727': (0x1D, 0x17, 0x27)}
ok = True
for name, c in spec.items():
    d = np.abs(top.astype(int) - np.array(c)).sum(1).min()
    print(f'{name}: nearest frequent colour off by {d} (sum of RGB steps)')
    ok &= d <= 6
print('COLOURS', 'PASS' if ok else 'FAIL')
