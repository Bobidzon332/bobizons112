import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = json.load(open(os.path.join(ROOT, 'ref', 'profiles.json')))
name = sys.argv[1]; lo = int(sys.argv[2]); hi = int(sys.argv[3])
d = p[name]
print(name, 'H', d['H'])
for r in d['profile']:
    if lo <= r['pct'] <= hi:
        print(r['pct'], ' '.join(f"{a}-{b}" for a, b in r['runs']))
