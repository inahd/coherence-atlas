# Atlas System Rules

## Purpose

This file defines non-negotiable architectural rules for development inside the Coherence Atlas project.

All contributors — human or AI — must follow these rules.

Atlas is not a conventional software project.
It is a relational cosmology engine built on a knowledge graph.

Every system must reinforce the graph.

## 📜 Rule 1 — The Graph Is Canonical

All knowledge ultimately belongs in the graph.

Canonical graph location:

`memory/graphs/canonical_graph.json`

Nodes represent entities.

Examples:

- nakshatra
- graha
- deity
- plant
- concept
- text
- practice

Edges represent relationships.

Examples:

- ruled_by
- presided_by
- associated_with
- symbolizes
- resonates_with

Interfaces must read from the graph, not invent independent data structures.

## 📜 Rule 2 — Projections Must Be Thin

User interfaces should project the graph, not replicate it.

Examples of projections:

- ncurses explorer
- visual graph interface
- card decks
- documentation wiki
- simulation engine

If a UI needs data, it should query the graph.

## 📜 Rule 3 — Inference Must Be Explicit

Generated relationships must be marked.

Example:

```json
{
  "source": "rohini",
  "target": "moon",
  "relation": "associated_with",
  "inferred": true
}
```

This prevents confusion between:

- canonical knowledge
- experimental inference

## 📜 Rule 4 — Symbol Systems Are First-Class

Atlas includes symbolic systems such as:

- jyotish
- archetypes
- mythology
- ritual systems
- sacred geometry

These are not decorative.

They are legitimate relational systems.

The graph must allow multiple interpretations of a node.

Example:

- Mars
- planet
- Mangala
- fire archetype
- war deity

## 📜 Rule 5 — Prefer Expansion Over Refactoring

Atlas is an exploratory system.

Avoid deleting structures prematurely.

Prefer:

- new nodes
- new relations
- new projections

Over:

- destructive rewrites
- premature simplification

Exploration precedes optimization.

## 🌾 Development Mindset

Atlas development follows a cycle:

seed data
→ build relations
→ explore patterns
→ generate research prompts
→ expand graph

The system grows organically.

## 🌌 Architectural Direction

Atlas is evolving into:

- knowledge graph engine
- symbolic cosmology explorer
- documentation wiki
- card archetype system
- ecological simulation
- research generator

Every contribution should move the project closer to this direction.
