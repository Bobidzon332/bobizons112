# 09 — Quality Gates

**Open this when** work is believed finished and needs a verdict before it ships. These are gates, not tutorials: run them and act on the result.

Paths below are relative to this file's own directory.

| Manual | Use when | Path |
|--------|----------|------|
| `qa-review` | Production QA gate for an asset — viewport screenshots, validation checklists, naming audit, and an explicit ship/no-ship verdict | `qa-review/MANUAL.md` |
| `animation-quality-gate` | Validating an animation before accepting it — contact sheets, silhouette stability, flicker, framing, subject dominance, layer separation, export compatibility, motion-design coherence | `animation-quality-gate/MANUAL.md` |

## Related

- A gate that fails repeatedly is a symptom, not a bug → `quality-refinement-autoloop` in `../01-orchestration/INDEX.md`
- The always-on visual check that runs much earlier than a full gate → `${COMMANDCODE_SKILL_DIR}/references/output-and-reporting.md`
