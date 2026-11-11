#!/usr/bin/env python3
"""Read-only checks for the installed handbook; no plugin manifest required."""
import argparse
import ast
import json
import re
from pathlib import Path


def audit(root):
    root = Path(root).resolve()
    errors, warnings = [], []
    manuals = sorted(root.glob("[0-9][0-9]-*/*/MANUAL.md"))
    groups = sorted(p for p in root.glob("[0-9][0-9]-*") if p.is_dir())
    indexed = set()
    if not (root / "SKILL.md").is_file():
        errors.append("Missing SKILL.md")
    if not manuals or not groups:
        errors.append("No domain groups/manuals found")
    for group in groups:
        index = group / "INDEX.md"
        if not index.is_file():
            errors.append(f"Missing index: {group.name}/INDEX.md")
            continue
        for ref in re.findall(r"`([^`]+/MANUAL\.md)`", index.read_text(encoding="utf-8")):
            target = (group / ref).resolve()
            if target in indexed:
                errors.append(f"Duplicate index target: {ref}")
            indexed.add(target)
            if not target.is_file():
                errors.append(f"Missing index target: {group.name}/{ref}")
    for manual in manuals:
        if manual.resolve() not in indexed:
            errors.append(f"Unindexed manual: {manual.relative_to(root)}")

    # Check explicit resource paths, not output artifact names or prose mentions.
    docs = [root / "SKILL.md", *root.glob("references/*.md")]
    docs += [p for group in groups for p in group.rglob("*.md")]
    names = {}
    for doc in docs:
        if not doc.is_file():
            continue
        body = doc.read_text(encoding="utf-8")
        if doc.name == "MANUAL.md":
            match = re.match(r"---\s*\n(.*?)\n---", body, re.S)
            name = re.search(r"^name: (.+)$", match[1], re.M) if match else None
            if not name:
                errors.append(f"Missing manual name: {doc.relative_to(root)}")
            elif name[1] in names:
                errors.append(f"Duplicate manual name: {name[1]}")
            else:
                names[name[1]] = str(doc.relative_to(root))
        refs = set(re.findall(r"`([^`\n]+)`", body))
        refs.update(re.findall(r"\[[^]\n]*\]\(([^)\s]+)\)", body))
        refs.update(re.findall(r"\$\{COMMANDCODE_SKILL_DIR\}/([\w./-]+)", body))
        for ref in refs:
            ref = ref.removeprefix("${COMMANDCODE_SKILL_DIR}/")
            if ("/" not in ref or any(c in ref for c in " <>*{}")
                    or ":" in ref or ref.startswith("/")
                    or Path(ref).suffix not in {".md", ".py", ".webp", ".png"}):
                continue
            if Path(ref).suffix in {".png", ".webp"} and not ref.startswith("assets/"):
                continue  # Render/report outputs are not installed resources.
            if (doc.parent / ref).is_file() or (root / ref).is_file():
                continue
            message = f"Missing resource in {doc.relative_to(root)}: {ref}"
            if ref.startswith("assets/"):
                warnings.append(message)  # Historical evidence is not executable guidance.
            else:
                errors.append(message)
    scripts = sorted(root.rglob("*.py"))
    for script in scripts:
        try:
            ast.parse(script.read_text(encoding="utf-8-sig"), filename=str(script))
        except SyntaxError as exc:
            errors.append(f"Invalid Python: {script.relative_to(root)}: {exc}")
    evals = sorted(root.rglob("evals.json"))
    for dataset in evals:
        try:
            json.loads(dataset.read_text(encoding="utf-8-sig"))
        except ValueError as exc:
            errors.append(f"Invalid JSON: {dataset.relative_to(root)}: {exc}")
    return {"schema": "blender_handbook_audit.v2", "groups": len(groups),
            "manuals": len(manuals), "scripts": len(scripts), "eval_files": len(evals),
            "errors": sorted(set(errors)), "warnings": sorted(set(warnings)),
            "passed": not errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", "--plugin-root", dest="root", default=".",
                        help="Installed handbook root; --plugin-root is a legacy alias")
    parser.add_argument("--out", help="Optional JSON report; stdout otherwise")
    args = parser.parse_args()
    report = audit(args.root)
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print(text)
    raise SystemExit(0 if report["passed"] else 2)


if __name__ == "__main__":
    main()
