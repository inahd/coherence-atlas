ATLAS CODEX TASK QUEUE

Codex should process tasks in order.
Each task must produce patch proposals only.
Never modify canon graph directly.

--------------------------------
TASK 1
--------------------------------

Implement transparency layer.

Create:

atlas_codex/status/
    atlas_status.md
    task_queue.md
    events.log

Create dashboard:

atlas_codex/dashboards/atlas_dashboard.py

CLI command:

atlas status

Dashboard reads:

memory/graphs/canonical_graph.json
atlas_codex/status/events.log

Output:

Atlas System Status
Nodes:
Relations:
Broken relations:
Missing evidence:

--------------------------------
TASK 2
--------------------------------

Create graph health scanner.

File:

scripts/graph_health.py

Command:

atlas graph-health

Detect:

missing node references
duplicate nodes
isolated nodes
missing evidence fields

--------------------------------
TASK 3
--------------------------------

Create Atlas field environment.

File:

scripts/atlas_field.py

Command:

atlas field

Output:

ATLAS FIELD

S0 metaphysical
S1 archetype
S2 sound
S3 rhythm
S4 geometry
S5 natural
S6 human

Display graph metrics.

--------------------------------
TASK 4
--------------------------------

Create seed prompt parser.

File:

atlas_codex/scripts/seed_prompt_parser.py

Goal:

scan seed_prompts.md
generate patch proposals

Outputs:

atlas_codex/patches/
atlas_codex/outputs/

--------------------------------
