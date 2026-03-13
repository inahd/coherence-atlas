# 008 — Spectral Ontology Canonization Layer

Status: proposed

## Purpose
Formalize the spectral ladder discussed in recent work:

S0 metaphysical meaning
S1 archetype / deity
S2 sound / mantra
S3 rhythm / cycle
S4 geometry / symbol
S5 natural phenomena
S6 human experience

This offering defines the spectral ladder as an explicit model_v1 layer inside Atlas.

## Why now
The crawler, graph, and portal concepts need a stable shared ontology.
Without this, categories drift and growth becomes uneven.

## Deliverables
- ontology/spectral_layers.json
- mappings from node types to spectral layer
- relation guidance for cross-layer links
- validation rule for allowed / expected transitions

## Example transitions
- deity → mantra
- mantra → meter
- cycle → geometry
- geometry → plant symbolism
- plant → ritual use
- ritual → human experience

## Acceptance criteria
- Every major node type can be assigned a spectral layer
- Cross-layer relations can be grouped and queried
- Visual layers / portal can read the spectral model
- No existing canon overwritten

## Canon handling
Status:
- model_v1
- not yet fully canonical ontology
- can be promoted after successful use across domains

## Notes
This offering stabilizes the "where does this concept belong?" problem.
