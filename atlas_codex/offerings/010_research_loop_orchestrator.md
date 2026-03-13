# 010 — Research Loop Orchestrator

Status: proposed

## Purpose
Unify the now-fragmented Atlas research cycle into one repeatable orchestrated loop:

gap detection
→ research task generation
→ corpus ingestion
→ concept extraction
→ relation proposals
→ graph rebuild
→ integrity check
→ coherence scoring
→ visualization

## Why now
Atlas has many working scripts but they remain scattered.
The system needs a single research growth loop.

## Deliverables
- one orchestrator shell or python script
- stable ordering of pipeline stages
- logging to status/events.log
- safe failure handling so one stage does not destroy the cycle

## Candidate command
- atlas grow
or
- bash scripts/atlas_research_loop.sh

## Acceptance criteria
- one command runs the full cycle
- system reports progress clearly
- graph rebuilds after loop
- visual outputs regenerate automatically
- event log records each stage

## Canon handling
Growth loop may only generate:
- seed_unverified
- auto_proposed
Canon promotion remains separate.

## Notes
This offering turns Atlas from a script collection into a living research instrument.
