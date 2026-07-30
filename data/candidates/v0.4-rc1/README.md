# Dataset v0.4-rc1

Status: **research release candidate**.

This candidate applies the reviewed corrections from the first two source-audit batches. It is structurally valid but is not yet ready for authoritative public citation.

## Main changes

- Corrected TSMC Arizona's current planned investment total to USD 165 billion.
- Separated operational and planned TSMC Arizona facilities.
- Reworked Israel's energy node to include gas-storage and long-term resilience constraints.
- Expanded Israel's semiconductor capability into design, metrology and inspection, fabrication and an aggregate ecosystem.
- Added Chips JU as allied R&D and funding access.
- Added line-audited U.S. data-center electricity metrics.
- Kept future Micron U.S. HBM packaging in planned status.
- Replaced AI21's strict domestic-control classification with an explicit unverified-control state.
- Marked Government Decision 4255 as partially corroborated while the stable official full text remains pending.

## Loading the dataset

Read `manifest.json`, concatenate the listed base64 parts, decode them, verify the compressed and decoded SHA-256 checksums, and decompress the gzip payload.

Run the repository validator:

```bash
python scripts/validate_candidate.py data/candidates/v0.4-rc1/manifest.json
```

## Current validation result

- 7 ecosystems
- 13 capability layers
- 57 nodes
- 67 edges
- 61 sources
- 0 structural errors
- 0 isolated nodes

## Open research items

See `validation-report-v0.4-rc1.json` and `CHANGELOG.md`. The main blockers are the full official text of Government Decision 4255, Tower Semiconductor's primary-source audit, private-company control verification and Israel's data-center grid, water, cooling and backup-power constraints.
