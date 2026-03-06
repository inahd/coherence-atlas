# Coherence Atlas

<p align="center">
  <b>Local-first research backend → layered knowledge graph (Canon • Inference • Overlays)</b><br/>
  <i>Ingest sources → extract passages w/ locators → propose relations → resolve coherence over time</i>
</p>

<p align="center">
  <a href="https://github.com/inahd/coherence-atlas/actions"><img alt="Actions" src="https://img.shields.io/github/actions/workflow/status/inahd/coherence-atlas/ia_manifests.yml?branch=main"/></a>
  <a href="https://github.com/inahd/coherence-atlas"><img alt="Repo" src="https://img.shields.io/github/stars/inahd/coherence-atlas?style=social"/></a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue"/>
  <img alt="Local-first" src="https://img.shields.io/badge/local--first-yes-success"/>
</p>

---

## Vision (full system map)
➡️ **Read the full vision:** [](docs/vision.md)  
➡️ **North Star demo:** [](docs/north_star_demo.md)

---

## What this is
Coherence Atlas is a **research backend** that builds a structured, queryable knowledge graph from real sources (PDF/text/epub/html).
It is designed for domains where **coherence emerges from layered relationships** (e.g., time cycles, ritual calendars, arts, ecology).

Atlas outputs **three truth layers** so the system can grow fast *without lying*:
- **Canon (attested):** evidence-backed, stable, promotion-gated
- **Inference (coherence-derived):** fast growth, explicitly labeled 
- **Overlays (variants):** tradition/school mappings that preserve disagreement without mud

---

## Quickstart (3 commands)


**Outputs (local):**
- Dashboard: 
- Stability report: 
- Resolved layers:
  -  (should be non-empty early)
  -  (should be non-empty early)
  -  (may be empty early; canon is strict)

---

## Why this matters
Most knowledge graphs either:
1) stay tiny because evidence requirements block growth, or
2) grow fast and become **mud**.

Atlas is built to avoid both failure modes: **growth happens in inference**, and **canon matures over time** as evidence coverage improves.

---

## What you can explore today
- **Cluster exploration:** focus an entity like  and see its neighborhood across domains
- **Entity pages (wiki-style):** “Rohini page” views grouped by Canon / Inference / Overlays
- **Dashboards:** see what blocks canon (missing , missing evidence, conflicts)

---

## Repo layout
-  — pipeline + utilities (ingest/extract/harvest/evidence/resolve/graph/wiki)
-  — structured entities + relation tables (CSV/YAML)
-  — wget lists (auto-generated + curated)
-  — downloaded sources (local)
-  — extracted text stream (local)
-  — generated reports/graphs (local)
-  — documentation (vision, demo, architecture)

---

## Maturity model (honest)
- Early stage: inference + overlays grow first
- Canon grows later as evidence density rises
- Conflicts remain visible (not hidden) and can be scoped by overlays

If you’re evaluating the project: open  and  after a cycle.

---

## Contributing (high leverage)
If you want to help, the biggest wins are:
- Improve ingestion quality (text-first sources, OCR where needed)
- Improve evidence matching (better locators/snippets)
- Add resolver constraints (types/cardinality/conflict settling)
- Improve exploration UX (filters, collapsible clusters, entity pages)
- Add domain packs (panchanga, mantra metadata, ayurveda, yantra, music)

See  for a docs index.

---

## License
TBD (choose before broad distribution).

