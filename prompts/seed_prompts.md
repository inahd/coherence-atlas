# Atlas Seed Prompts (Test Pack)

Paste this into ChatGPT (or your local model) along with any excerpts you want processed.

## Contract
- Do NOT hallucinate citations. If evidence is not present: output `NO EVIDENCE FOUND`.
- IDs must be `type:slug_or_int` (lowercase, underscores).
- Output MUST be file patches: each begins with `FILENAME: ...` and then a clean CSV/YAML/JSON block.

## Input you should assume I can paste next
- `atlas factcheck` output
- `datasets/relations_*.csv` files or relevant slices
- excerpts from `Journey with the Moon` (or other PDFs)

## Task A — Fill missing to_id
Given factcheck + relation rows missing to_id:
- propose `to_id` candidates and mark confidence HIGH/MED/LOW
- HIGH only if widely standard; MED if tradition-dependent; LOW if speculative (overlay-only)

## Task B — Fill missing evidence
Given relation rows with to_id but missing evidence:
- propose `source_title`, `source_locator` (page/section), and `excerpt`
- if evidence not available from pasted excerpts, say `NO EVIDENCE FOUND`

## Task C — New seed rows from Journey with the Moon
From pasted excerpts:
- produce new rows into `datasets/relations_ritual_calendar.csv` using `ritual_prescribed_on`
- include locator + excerpt in every new row
- confidence must be `seed_unverified` unless explicitly attested
