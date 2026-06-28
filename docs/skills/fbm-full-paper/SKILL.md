---
name: fbm-full-paper
description: Use when researching, writing, reviewing, expanding, or formatting the Samsung Best Paper Awards full paper in D:\project\fbm_paper_full, especially from paper_codex_2page_rev167 and evidence folders fail-map, unknown-contrastive, known-cnn, and failure_agent. Enforces absolute paper rules, coordinates research-writer-reviewer cycles, and names outputs full_paper_revNNN_codex.
---

# FBM Full Paper

Use this skill for the full-paper workflow in `D:\project\fbm_paper_full`.

## Required reads

Before writing or editing the paper:

1. `PAPER_FULL_RULES.md`
2. Top full-paper section of `CLAUDE.md`
3. `docs/agents/full_paper_agents.md`
4. `docs/memory/full_paper_memory.md`

Do not modify `.claude/`, `_claude` files, or Claude loop artifacts unless the user explicitly asks.

## Workflow

1. Load the seed draft: `paper_codex_2page_rev167.docx` or `paper_codex_2page_rev167.md`.
2. Research source folders and update memory before adding claims.
3. Draft the next `full_paper_revNNN_codex.md`.
4. Review with the internal reviewer rubric.
5. Check template compliance before producing `.docx`.
6. Update `docs/memory/full_paper_memory.md` with evidence, score, and next actions.

## References

- Detailed loop: `references/workflow.md`
- Reviewer rubric: `references/reviewer_rubric.md`
- Source research map: `references/research_sources.md`

## Hard constraints

- Output names must follow `full_paper_revNNN_codex.*`.
- Page target is 4 to 10 A4 pages including references.
- Every technical claim needs a source path or must be marked as future work.
- Unknown field operation evidence and synthetic benchmark evidence must remain separated.
- The final paper should sound like a careful engineer wrote it, not an AI-generated brochure.
