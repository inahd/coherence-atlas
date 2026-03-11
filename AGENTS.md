# Coherence Atlas — Agent Orientation

This repository implements **Coherence Atlas**, a relational cosmology / knowledge graph environment.

## Core rule

`inputs -> graph -> projections`

The graph is the single source of truth.

## Graph data

- Nodes: `data/nodes.csv`
- Relations: `data/relations.csv`
- Graph snapshots: `memory/graphs/`

## Main domains

- jyotisha
- nakshatra
- graha
- rashi
- ritual
- agriculture
- symbolism
- Gaudiya theology
- cosmology

## Layers

1. Canonical ontology layer (stable entities and core relations)
2. Instance layer (chart/user-specific instantiations)
3. Activation layer (transits, dasha, temporal events)

## Common tasks

- stabilize broken scripts
- improve graph relation density
- add renderers that read graph nodes
- improve ncurses front gate
- generate docs from graph data

## Engineering rules

- Do not create duplicate sources of truth.
- UI/cards/visualizations must read from graph data.
- Prefer modifying existing files over creating parallel systems.
- Make small coherent patches with verification commands.

## North-star success condition

- `atlas node <id>` can inspect node + relations clearly.
- Projections (wiki/cards/mandalas/ncurses) derive from graph truth.
