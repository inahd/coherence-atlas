# Atlas Codex Proposal Bundle

This document consolidates the current game-layer proposal, README/front-page direction, ncurses environment direction, symbolic response layer, and additional architectural suggestions for the Coherence Atlas project.

It is written as a handoff file for Codex or any implementation-oriented agent already familiar with the project's basic context.

## 1. Project Identity

Coherence Atlas is a relational cosmology / knowledge graph environment.

It maps:

- entities
- relations
- symbols
- practices
- cycles
- texts
- cosmologies
- research seeds

The graph is the truth layer. Everything else is a projection.

Atlas is not merely an app. It is a living ecology of knowledge systems.

## 2. Core Axioms

1. Knowledge is relational.
2. Difference is preserved.
3. Inherence is assumed.
4. Resonance is observed, not forced.
5. The system grows by offerings.
6. Offerings create relations.
7. Relations create structure.
8. Structure reveals patterns.
9. The graph is the truth layer.
10. All interfaces are projections of the graph.
11. Atlas does not compute ultimate realization.
12. Atlas maps living relationships that shape understanding.
13. The map is not the territory.
14. Canonical traditions provide hypothesis structures.
15. Real-world observation may test resonance.
16. The system should generate prompts both for users and for its own maturation.

## 3. Three Cosmology Layers

Atlas should support three simultaneous cosmological graphs:

- eternal
- subtle
- material

These should not be collapsed into one graph. They should be able to resonate across layers.

### Eternal Layer

Examples:

- Krishna
- Radha
- Goloka
- Lila
- Rasa
- Bhakti

### Subtle Layer

Examples:

- Graha
- Nakshatra
- Yantra
- Mantra
- Archetypes
- Symbol systems
- Guna
- Karma patterns

### Material Layer

Examples:

- planets as observable bodies
- ecology
- agriculture
- weather
- human events
- bodies
- technologies

### Cross-Layer Relation

Use a relation like `resonates_with`.

This preserves difference while allowing structural coherence.

## 4. Atlas Commander Direction

Atlas Commander (`ac`) should become the front gate of the system.

It should not remain a toy debug menu. It should become a terminal knowledge sanctuary.

### Desired Front Screen

- Wiki Explorer
- Tarot / Card Decks
- Cosmology Mandala
- Graph Explorer
- Documentation
- Research Seeds
- Settings / State
- Quit

Purpose: one environment, many modes, same underlying graph.

The terminal should bootstrap the whole ecosystem before later web / desktop interfaces exist.

## 5. Projection Principle

Same graph, many views.

The graph remains canonical. The projection changes.

Projection types:

- wiki view
- card view
- mandala view
- constellation graph
- nakshatra wheel
- documentation browser
- research prompt panel
- timeline view

Principle: Atlas is a projection engine as much as a graph engine.

## 6. README Front Page Direction

The README should function like a navigation cosmogram rather than a linear developer README.

README front page should include:

- project identity
- system axioms
- graph principle
- offering model
- projection model
- Atlas Commander as front gate
- navigation tree into docs / systems / datasets
- emergent possibilities

Tone:

- avoid generic open-source template tone
- avoid defensive explanation
- avoid installation-first banality
- emphasize the field, axioms, environment, and growth

Front page entry paths:

- Cosmology Explorer
- Card Systems
- Knowledge Corpus
- Atlas Engine
- Research Seeds
- Documentation

## 7. Symbol Layer Guidance

Do not use symbols as decoration only. Use them as meaning-dense semantic markers.

Suggested symbol classes:

- 🪔 insight / offering / illumination
- 📜 canon / principle / schema
- 🌌 constellation / pattern / cluster
- ⚙ engine / implementation / mechanics
- 🌾 seed / growth / cultivation
- 🔍 inquiry / missing relation / investigation
- 🧭 direction / next cycle / navigation

Example response structure:

- 🪔 Insight: clear conceptual clarification
- ⚙ Implementation: concrete software action or architecture move
- 🌌 Pattern: structural observation emerging from graph/repository

## 8. Graph State and Maturation

Observed canonical graph state example:

- Nodes: 1253
- Edges: 145

Interpretation:

- architecture formation: passed
- corpus accumulation: passed
- graph convergence: passed
- next stage: relational densification

Main unfinished subsystem:

- inference / resonance engine

Missing transformation:

`nodes -> inferred relations -> dense relational field`

## 9. Self-Maturing Prompt Model

Atlas should generate two prompt streams.

### A. Outward Prompts

For users/researchers:

- missing canonical relations
- underdeveloped nodes
- weakly linked cosmology areas
- dataset needs

### B. Inward Prompts

For Atlas itself:

- which ontology gaps most limit coherence?
- which node classes remain weakly connected?
- which projections are unsupported?
- which canon layers are underrepresented?
- which inference families are untested?

## 10. Canonical Data Strategy

Prioritize canonical relational datasets over manual invention.

Priority domains:

- 27 nakshatras
- 9 grahas
- 12 rashis
- tithi / yoga / karana
- deity correspondences
- symbol correspondences
- plant guilds
- agricultural cycles
- ritual calendars
- Gaudiya theological entities
- 64 arts / Vedic sciences

## 11. Game Layer Direction

The game layer is a proof that Atlas can drive a living simulation.

Core concept:

- Player = herdsman
- Dogs = influence agents
- Cows = semi-autonomous herd
- Plants = ecological layer
- Sky = cosmological modifier

This proves `graph -> world rules -> living simulation`.

Candidate name: **Gopala Field**.

## 12. Gopala Field — Simulation Proposal

World elements:

Tiles:

- grass
- trees
- water
- village
- forest
- ruins

Entities:

- player
- cows
- dogs
- plants

Systems:

- day / night cycle
- moon phase
- nakshatra
- season
- weather
- grass regrowth
- herd movement
- plant guild interaction

Herding principle: player influences cows through position, dogs, terrain, and timing.

Dog commands:

- send left
- send right
- circle herd
- recall dog

Cow rules:

- seek grass
- avoid dogs
- stay near herd
- avoid water

## 13. Satya–Kali Scale

Global variable:

`yuga_index = 0.0 -> 1.0`

Meaning:

- 0.0 = Satya-like harmony
- 0.25 = Treta-like order
- 0.50 = Dvapara complexity
- 0.75 = Kali imbalance
- 1.0 = collapse / cyberpunk ruin

Effects:

- soil fertility
- weather volatility
- technological debris presence
- ecosystem health
- pasture richness
- atmospheric tone

Regenerative practices reduce imbalance:

- rotational grazing
- water harvesting
- plant guild cultivation
- soil restoration
- ritual timing
- ecological care

## 14. PFAF + Plant Guild Integration

Plant layer should support:

- soil preferences
- water needs
- companion plants
- productive guilds
- regenerative effects

Connect ecology/agriculture/cosmology/simulation via graph relations.

## 15. Why the Game Layer Matters

Game layer acts as:

- proof of relational coherence
- stress test for graph rules
- visible living system
- pedagogical interface for pattern recognition

If graph quality is high, simulation behavior becomes meaningful.

## 16. Codex Prompt — Game Layer

Design a minimal simulation layer for Coherence Atlas.

Requirements:

- terminal ASCII using Python curses
- title: Gopala Field
- pastoral cosmology simulation
- player is a herdsman
- dogs influence cow movement
- cows are semi-autonomous
- sky conditions affect world
- include nakshatra, moon phase, season
- support both turn-based and realtime modes
- include a yuga_index from Satya to Kali/collapse
- regenerative actions can improve world state
- use Atlas graph data where possible

Goal: demonstrate graph relations driving a living world.

## 17. Codex Prompt — Resonance / Inference Engine

Design `atlas/inference/resonance_engine.py`.

Requirements:

- read `canonical_graph.json`
- generate inferred edges automatically
- avoid duplicates
- mark inferred edges (`inferred: true`)
- support shared attribute resonance
- support cosmology hierarchy inference
- support symbolic correspondence inference
- support text-reference linking
- support deity–graha–nakshatra relation generation
- write updated graph back to `canonical_graph.json`

Goal: increase relational density dramatically.

## 18. Codex Prompt — Wiki Explorer

Design a wiki explorer inside Atlas Commander.

Requirements:

- node browsing
- search
- relation expansion
- attribute viewing
- backlink viewing

Display:

- node title
- node type
- layer
- attributes
- relations

Controls:

- arrow keys move
- enter expands
- backspace goes back
- slash searches

Read from `canonical_graph.json`.

## 19. Codex Prompt — README Devi Field

Construct `README.md` front page as navigation mandala.

Include:

- project identity field
- entry paths
- hyperlink tree
- core axioms
- documentation map
- Atlas Commander front gate
- architecture + projection principle

Avoid generic boilerplate.

## 20. Additional Suggestions

### A. One Canonical Graph Rule

Converge graph generation into:

`memory/graphs/canonical_graph.json`

Other graphs become source/snapshot/backup/experimental artifacts.

### B. One Canonical Capsule Standard

Each major chat/subsystem exports a capsule with:

- README
- axioms
- ecosystems
- datasets
- schemas
- rules
- seeds

### C. Naming Coherence

Prefer names aligned with project frame:

- `offer_seed.py`
- `manifest_constellation.py`
- `resonance_engine.py`
- `harvest_seeds.py`

### D. Front-Facing Proofs

Show living outputs:

- ncurses explorer screenshots
- graph counts
- mandala images
- sample cards
- research seed examples

### E. First Powerful Data Packs

Priority packs:

- full nakshatra attribute pack
- graha attribute pack
- rashi correspondences
- deity-symbol pack
- plant guild pack
- Gaudiya entity pack

### F. Long-Term Shape

Atlas evolving into:

- graph engine
- projection engine
- cosmology explorer
- symbolic card system
- wiki environment
- simulation world
- self-maturing research ecology

## 21. Final Direction

Do not flatten Atlas into a generic graph app.

Direction:

`living relational cosmology -> graph canon -> many projections -> regenerative simulation -> self-maturing ecology of knowledge`

Offering placed.
