# Dataset v0.4-rc2

Status: **research release candidate**.

This candidate applies the reviewed corrections from the first three source-audit sprints. It is structurally valid but is not ready for authoritative public citation.

## Snapshot

- 7 ecosystems
- 13 capability layers
- 60 nodes
- 75 edges
- 66 sources
- 0 structural errors

## Front-end loading

The simplest front-end path is:

```text
data/candidates/v0.4-rc2/ai-ecosystem-v0.4-rc2.json
```

The multipart gzip representation remains available for integrity verification and archival use.

## Validation

```bash
python scripts/validate_candidate.py data/candidates/v0.4-rc2/manifest.json
```

See `validation-report-v0.4-rc2.json` and `CHANGELOG.md`.
