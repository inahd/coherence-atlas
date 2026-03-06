# Atlas Seed Prompts (Batch Processor Pack)

## Contract (read first)

```text

You are helping maintain Coherence Atlas: a local-first Vedic knowledge graph.

Hard rules:
- Do NOT hallucinate citations. If evidence is not present, output NO EVIDENCE FOUND.
- Keep canon clean: anything uncertain must remain auto_proposed or seed_unverified.
- Every canonical-eligible row MUST include: source_title, source_locator, excerpt, tradition, confidence.
- IDs must follow: type:slug_or_int (lowercase, underscores for spaces).
- Output MUST be files (with suggested filenames) containing clean blocks (CSV/YAML/JSON) only.
```

## Ontology + allowed relations

```yaml

id_format: "type:slug_or_int"
entity_types:
  - nakshatra
  - tithi
  - graha
  - rashi
  - deity
  - devi
  - nitya_devi
  - plant
  - weapon
  - ritual
  - raga
relations:
  - name: nakshatra_associated_deity
    from: nakshatra
    to: [deity, devi, nitya_devi]
  - name: nakshatra_ruling_graha
    from: nakshatra
    to: [graha]
  - name: nakshatra_sacred_plant
    from: nakshatra
    to: [plant]
  - name: devi_wields_weapon
    from: devi
    to: [weapon]
  - name: ritual_prescribed_on
    from: ritual
    to: [tithi, nakshatra]
  - name: ritual_uses_raga
    from: ritual
    to: [raga]
confidence_allowed: [seed_unverified, auto_proposed, attested_secondary, canonical]
evidence_required: [source_title, source_locator, excerpt]
```

## Current state

```text
Generated: 2026-03-06 07:21:00

Factcheck snapshot:
- total rows: 106
- missing to_id: 42
- missing evidence: 55

Per-file:
- relations_nakshatra_deity.csv: rows=27 missing_to_id=0 missing_evidence=11
- relations_devi_weapon.csv: rows=15 missing_to_id=15 missing_evidence=15
- relations_nakshatra_plants.csv: rows=27 missing_to_id=27 missing_evidence=27
- relations_ritual_calendar.csv: rows=10 missing_to_id=0 missing_evidence=0
- relations_raga_ritual.csv: rows=0 missing_to_id=0 missing_evidence=0
- relations_nakshatra_graha.csv: rows=27 missing_to_id=0 missing_evidence=2
```

## Available public research files (repo-safe)

```text
/opt/atlas/research_public/README.md
```

## Reports present

```text
aggregate.json
canon_guard.json
dashboard.html
evidence_todo.txt
gaps.json
gaps_top.txt
journey_moon_passages.csv
next_domain.txt
quality_report.json
research_fingerprint.txt
stability_report.json
```

## Task A — Fill missing to_id (safe structural completion)

```text

For each row below:
- propose to_id (type:slug) and confidence (HIGH/MED/LOW).
- HIGH only if mapping is widely standard; MED if tradition-dependent; LOW if speculative.
- Output a CSV file patch that updates ONLY to_id + confidence + notes.
Queue:
- relations_devi_weapon.csv	devi:bhagamalini	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:bherunda	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:chitra	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:jvalamalini	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:kameshvari	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:kulasundari	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:mahavajreshvari	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:nilapataka	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:nitya	devi_wields_weapon	(to_id missing)
- relations_devi_weapon.csv	devi:nityaklinna	devi_wields_weapon	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:1	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:2	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:3	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:4	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:5	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:6	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:7	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:8	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:9	nakshatra_sacred_plant	(to_id missing)
- relations_nakshatra_plants.csv	nakshatra:10	nakshatra_sacred_plant	(to_id missing)
```

## Task B — Attach evidence to evidence-missing rows

```text

For each row below (to_id present; evidence missing):
- Find/construct evidence ONLY from provided sources/excerpts (if included in the pasted bundle).
- If you cannot, output NO EVIDENCE FOUND for that row.
- Output a CSV file patch that updates source_title, source_locator, excerpt, tradition, confidence, notes.
Queue:
- relations_nakshatra_deity.csv	nakshatra:1	nakshatra_associated_deity	deity:ashwini_kumaras
- relations_nakshatra_deity.csv	nakshatra:10	nakshatra_associated_deity	deity:pitrs
- relations_nakshatra_deity.csv	nakshatra:12	nakshatra_associated_deity	deity:aryaman
- relations_nakshatra_deity.csv	nakshatra:13	nakshatra_associated_deity	deity:savitar
- relations_nakshatra_deity.csv	nakshatra:14	nakshatra_associated_deity	deity:vishvakarma
- relations_nakshatra_deity.csv	nakshatra:16	nakshatra_associated_deity	deity:indraagni
- relations_nakshatra_deity.csv	nakshatra:17	nakshatra_associated_deity	deity:mitra
- relations_nakshatra_deity.csv	nakshatra:19	nakshatra_associated_deity	deity:nirriti
- relations_nakshatra_deity.csv	nakshatra:21	nakshatra_associated_deity	deity:vishvadevas
- relations_nakshatra_deity.csv	nakshatra:25	nakshatra_associated_deity	deity:ajaekapada
- relations_nakshatra_graha.csv	nakshatra:18	nakshatra_ruling_graha	graha:mercury
- relations_nakshatra_graha.csv	nakshatra:19	nakshatra_ruling_graha	graha:ketu
```

## Task C — Generate new relation rows from a single source (Journey-with-the-Moon etc.)

```text

Given a pasted excerpt bundle from one source, propose new seed rows into:
- relations_ritual_calendar.csv (ritual_prescribed_on)
- relations_raga_ritual.csv (ritual_uses_raga)
Rules:
- include source_title + locator + excerpt in every new row
- confidence must be seed_unverified or auto_proposed unless explicitly attested
Output new CSV files with correct headers.
```

## Output format (strict)

```text

Return results as multiple files.

For each file:
1) A line: FILENAME: <path/filename>
2) Then the exact file content as a clean block (CSV/YAML/JSON)
3) No extra commentary.

CSV headers must match existing dataset headers exactly.
```

