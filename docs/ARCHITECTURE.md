# Atlas Architecture

Coherence Atlas is a graph-based relational knowledge environment.

## System flow

`sources -> seeds -> nodes -> relations -> graph -> projections`

## Inputs

- astro/jyotish engines
- research seeds
- text ingestion
- canonical datasets
- manual ontology additions

## Graph core

- Nodes
- Relations

Graph artifacts are produced in `memory/graphs/` and consumed by projections.

## Projections

- node explorer
- wiki-style outputs
- cards
- constellation graphs
- mandalas
- ncurses interface (`ac`)

## Key principle

Graph = truth layer.

Renderers never become independent truth stores; they are views over graph state.
