# Atlas Architecture Principles

## Kernel Before Inference

The system must maintain a stable cosmological kernel before large-scale inference is allowed.

Without this, relations drift.

## Relations Over Pages

Information is stored as structured relations with evidence rather than free text pages.

Example relation structure:

subject | predicate | object | source | confidence

## Frame Awareness

Different philosophical traditions interpret concepts differently.

Atlas stores interpretive frames such as:

- Gaudiya
- Advaita
- Academic
- Comparative

Relations can be scoped to these frames.

## Sanskrit Root Layer

Where possible, Sanskrit terms serve as canonical concept identifiers.

English labels are treated as translations or explanatory aliases.

This preserves grammatical and philosophical nuance.

## Evidence First

All relations should ideally point to a source passage.

Inference layers are separated from canonical data.
