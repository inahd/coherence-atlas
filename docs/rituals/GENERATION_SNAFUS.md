# Generation Snafus

## 2026-03-09 — Interrupted heredoc during renderer install

Symptom:
- shell remained in continued input mode
- pasted Python file truncated
- command did not complete

Cause:
- heredoc write was interrupted before terminator line was received

Ritual correction:
- always use one complete paste block
- if terminal shows repeated `>` continuation prompts, abort with Ctrl+C
- prefer verified write blocks that end with a visible success message
- add post-write syntax check before running

Architecture implication:
- generation tools should include:
  - safe write markers
  - syntax validation
  - README marker validation
  - clear completion messages
