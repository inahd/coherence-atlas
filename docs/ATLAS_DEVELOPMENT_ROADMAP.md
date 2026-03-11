# Coherence Atlas Development Roadmap

## Project trajectory

Coherence Atlas is evolving into a relational cosmology engine that supports:

- knowledge graphs
- symbolic systems
- documentation exploration
- card archetype systems
- cosmological visualization
- ecological simulation
- research prompt generation

Development should proceed in layers so each stage strengthens the graph.

## Phase 1 — Graph Stabilization

Goal: ensure one canonical graph and reliable ingestion.

Tasks:

- canonical graph convergence: `memory/graphs/canonical_graph.json`
- dataset loaders for: nakshatra, graha, rashi, plant guild data, symbol correspondences
- deduplication and normalization for: `id`, `label`, `type`, `attributes`

## Phase 2 — Resonance Engine

Goal: generate relations automatically.

Create module:

- `atlas/inference/resonance_engine.py`

Functions:

- shared attribute edges
- hierarchical edges
- symbol correspondence edges
- cosmology inference edges

Expected outcome:

- nodes ~1200
- edges ~10000+

## Phase 3 — Atlas Explorer

Goal: explore graph interactively via Atlas Commander.

Features:

- node search
- relation expansion
- attribute view
- backlink navigation

## Phase 4 — Visualization Layer

Goal: visual graph exploration.

Suggested stack:

- FastAPI
- Sigma.js / D3.js

Features:

- zoom
- node click
- relation display
- cluster detection

## Phase 5 — Card System

Goal: generate symbolic decks from graph nodes.

Deck types:

- Nakshatra
- Graha
- Deities
- Archetypes

Outputs:

- markdown
- image
- html

## Phase 6 — Documentation Wiki

Goal: graph-driven knowledge browser.

Features:

- node pages
- relation pages
- concept explanations
- source citations

## Phase 7 — Research Prompt Engine

Goal: system-generated maturation questions.

Examples:

- Which nodes have few relations?
- Which cosmology areas are underdeveloped?
- Which symbolic correspondences are missing?

Output file:

- `docs/research_prompts.md`

## Phase 8 — Game Layer

Goal: demonstrate graph relationships driving simulation.

Game:

- Gopala Field (pastoral cosmology roguelike)

Systems:

- herding
- plant guild ecology
- sky cycles
- yuga scale

Simulation loop:

- player action
- dogs move
- cows react
- plants grow
- sky updates

## Phase 9 — Ecological Knowledge Layer

Integrate:

- PFAF plant data
- permaculture guild logic
- soil and water cycles

Nodes include:

- plants
- soil types
- guild relationships

## Phase 10 — Self-Maturing Atlas

Goal: Atlas guides its own development.

Generate:

- research seeds
- missing relations
- dataset suggestions
- ontology proposals

## Architectural principle

Every subsystem reinforces the graph:

`graph -> projections -> simulation -> research prompts -> new graph data`

## Final direction

Atlas is becoming a living relational cosmology environment combining:

- ontology
- symbol systems
- ecology
- simulation
- documentation
- research generation

Development should always move toward greater relational coherence.
