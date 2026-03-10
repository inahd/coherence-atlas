# Coherence Atlas — Codex Instruction Pack

Use this document as the default instruction context for Codex runs in this repository.

## Primary Rule

Do not sprawl. Do not redesign the whole system unless explicitly asked.
Prefer one clean, testable change per cycle.

## Project Orientation

Coherence Atlas is a relational cosmology / knowledge graph environment.

- The graph is the truth layer.
- Everything else is a projection.

## Core Architectural Law

`inputs -> graph -> renderers`

### Inputs may include

- astro / jyotish calculation
- research seeds
- text ingestion
- canonical datasets
- manual ontology additions

### Renderers may include

- node explorer
- cards
- wiki pages
- constellation graphs
- mandalas
- ncurses views
- documentation sections

## Working Assumptions

- preserve difference
- assume inherence
- observe resonance, do not force it
- cards and views do not store knowledge
- the graph is the single source of truth
- canonical ontology, chart instance, and activation layers must remain distinct

## Development Priorities

1. stabilize broken code
2. improve graph relation density
3. improve one projection at a time
4. keep the repo understandable
5. prefer visible software outputs over abstract planning

## Workflow Rules

- Before changing files, inspect relevant files and summarize current reality briefly.
- Make the smallest coherent patch that moves the cycle forward.
- When possible, add or update verification steps.
- If a task is too large, produce a staged plan and execute only stage 1.
- Do not leave useful insights only in prose; capture them as one of:
  - `data/*.csv`
  - `atlas/*.py`
  - `docs/*.md`
  - `scripts/*.py`

## Output Modes

- **Vaidya**: diagnosis / repair / integrity
- **Shilpi**: implementation / file edits / code
- **Gopala**: prioritization / integration / next-step steering
- **Rishi**: compact conceptual clarification only when needed

## Response Style

Start responses with this shape:

1. `MODE: <Vaidya|Shilpi|Gopala|Rishi>`
2. `GOAL`
3. `FILES TO TOUCH`
4. `CHANGES`
5. `VERIFY`
6. `NEXT SEED`

## Editing Rules

- Prefer modifying existing project structure over inventing parallel structures.
- Keep the `atlas/` core small and legible.
- Put exploratory material in `docs/field`, `research/`, or `analysis/` unless asked to promote it.
- If introducing a new dependency, state it explicitly and update requirements if appropriate.
- Never paste Python into shell instructions; keep shell and file edits clearly separated.

## What Good Changes Look Like

- a working node explorer
- a graph densification report
- a renderer that reads from graph nodes
- a README section generated from real graph/data
- a small ncurses screen that exposes a real capability

## What Bad Changes Look Like

- large speculative rewrites
- duplicate sources of truth
- storing renderer-specific knowledge outside the graph
- giant option lists without one executed offering

## Default Task Behavior

When asked to help, default to:

`inspect -> patch -> verify -> summarize`

## Task Prompt Template

```text
Task:
<describe one concrete thing>

Constraints:
- Make one coherent change only.
- Keep the graph as single source of truth.
- Prefer existing files and patterns.
- Include verification commands.
- Do not redesign unrelated parts.

Success condition:
<what visible thing should work after this?>
```

## Recommended Operating Pattern

1. Give one concrete task.
2. Require touched files + verify commands.
3. Apply or review the patch.
4. Run the verification locally.
5. Commit only when visible behavior improves.
