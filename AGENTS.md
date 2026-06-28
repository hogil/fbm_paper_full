# Project Instructions

## Full Paper Absolute Rules

- For any Samsung Best Paper Awards abstract or full-paper writing, editing, formatting, export, or review task, read the full-paper section at the top of `CLAUDE.md` and treat `PAPER_FULL_RULES.md` as the detailed binding source of truth.
- Read `PAPER_FULL_RULES.md` before changing paper content, generating `.docx`/`.pdf` output, or checking compliance.
- Do not silently relax page limits, layout, typography, citation, figure/table, abstract, author, affiliation, or reference-format requirements.
- If a user request conflicts with `PAPER_FULL_RULES.md`, state the conflict clearly and ask before proceeding.
- Ignore older archived or generated rule files when they conflict with `PAPER_FULL_RULES.md`.

## Full Paper Agent System

- Use `docs/agents/full_paper_agents.md` as the project-level agent specification for full-paper work.
- Use `docs/memory/full_paper_memory.md` as the persistent Codex memory for current draft state, evidence queues, score history, and next actions.
- Use the local skill at `docs/skills/fbm-full-paper/SKILL.md` when the task is to research, write, review, expand, or format the full paper.
- The seed draft is `paper_codex_2page_rev167.docx` and the adjacent markdown extraction `paper_codex_2page_rev167.md`.
- Full-paper output names must follow `full_paper_revNNN_codex.*`, where `NNN` is the next available revision number.
- Do not modify `.claude/` files, `_claude` files, or Claude loop artifacts unless the user explicitly asks for that specific edit.
