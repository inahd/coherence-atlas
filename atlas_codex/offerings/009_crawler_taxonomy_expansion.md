# 009 — Crawler Taxonomy Expansion

Status: proposed

## Purpose
Expand Atlas crawler/source categories beyond mostly Jyotish material.

## Why now
The corpus currently appears heavily weighted toward astrology / nakshatra texts.
To realize the full cosmology engine, the crawler needs category-aware source acquisition.

## New category domains
- veda
- vedanga
- upanga
- jyotisha
- mantra
- ritual
- geometry
- yantra
- botany
- herbology
- music
- kala_64
- deity_theology
- gaudiya_vedanta
- temple_architecture

## Deliverables
- research source registry grouped by category
- crawler source manifests per category
- tagging rules so ingested texts carry category metadata
- gap report showing weak ontology layers

## Suggested directories
- research/sources/jyotisha
- research/sources/mantra
- research/sources/botany
- research/sources/geometry
- research/sources/ritual
- research/sources/kala_64

## Acceptance criteria
- crawler can pull from multiple ontology-relevant domains
- ingested texts are labeled by category
- state report shows more than astrology-heavy coverage
- graph growth begins populating S2/S4/S5/S6 layers more evenly

## Canon handling
Crawler outputs are raw or seed-level only.
No direct canon insertion.

## Notes
This offering is critical for balancing the graph.
