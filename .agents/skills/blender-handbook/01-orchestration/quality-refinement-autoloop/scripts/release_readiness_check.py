#!/usr/bin/env python3
"""Upstream plugin repository release checks, not an installed-handbook gate.

For this standalone handbook use skill_graph_audit.py instead.
"""
import argparse, json, re
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root', required=True)
    ap.add_argument('--expected-version', required=True)
    ap.add_argument('--out')
    args=ap.parse_args()
    root=Path(args.repo_root)
    required = ['plugin/manifest.json', 'README.md', 'plugin/README.md', 'CHANGELOG.md']
    missing_layout = [name for name in required if not (root/name).is_file()]
    if missing_layout:
        report = {'schema': 'cc_blender_release_readiness.v1', 'passed': False,
                  'error': 'This checker requires the upstream plugin repository. Use skill_graph_audit.py for the installed handbook.',
                  'missing': missing_layout}
        txt = json.dumps(report, indent=2)
        if args.out:
            Path(args.out).write_text(txt, encoding='utf-8')
        print(txt)
        raise SystemExit(2)
    manifest=json.loads((root/'plugin/manifest.json').read_text(encoding='utf-8'))
    checks=[]
    def check(name, ok, detail=''):
        checks.append({'name':name,'ok':bool(ok),'detail':detail})
    check('manifest_version', manifest.get('version')==args.expected_version, manifest.get('version'))
    missing=[]
    for s in manifest.get('skills',[]):
        if not (root/'plugin'/s['path']).exists(): missing.append(s['path'])
    check('manifest_paths_exist', not missing, ', '.join(missing[:10]))
    for doc in ['README.md','plugin/README.md','CHANGELOG.md']:
        p=root/doc
        check(f'{doc}_mentions_version', args.expected_version in p.read_text(errors='ignore'), doc)
    report={'schema':'cc_blender_release_readiness.v1','expected_version':args.expected_version,'checks':checks,'passed':all(c['ok'] for c in checks)}
    txt=json.dumps(report,indent=2)
    if args.out: open(args.out,'w').write(txt)
    print(txt)
    raise SystemExit(0 if report['passed'] else 2)
if __name__=='__main__': main()
