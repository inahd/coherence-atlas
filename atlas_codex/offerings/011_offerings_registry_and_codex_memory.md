# 011 — Offerings Registry and Codex Memory

Status: proposed

## Purpose
Create an official in-repo registry of all Codex offerings so future work remains transparent and aligned.

## Why now
The project now has multiple offerings, and new ones are emerging from discussion.
Without a formal registry, Codex and human operators lose context.

## Deliverables
- atlas_codex/offerings/INDEX.md
- atlas_codex/offerings/offerings.json
- AGENTS.md update pointing Codex to offerings registry
- optional status lifecycle for offerings

## Offering lifecycle
- proposed
- active
- implemented
- canonical
- superseded

## Acceptance criteria
- Codex can discover offerings from inside the repo
- every new offering gets a numbered file
- project can distinguish current vs obsolete offerings
- no duplicated architecture effort

## Notes
This is the memory layer for Codex-facing system intent.
