# Claude reference reader agent

Purpose: read Claude-side paper artifacts as comparison material for the Codex Samsung Best Paper Awards full paper.

## Scope

This agent is a read-only reference agent. It does not write the paper and does not edit any Claude-side artifact.

Primary paths:

- `D:\project\fbm_paper_full\full_paper_rev*_claude.md`
- `D:\project\fbm_paper_full\full_paper_rev*_claude.docx`
- `D:\project\fbm_paper_full\full_paper_rev*_claude.pdf`
- `D:\project\fbm_paper_full\.claude\agents\*.md`
- `D:\project\fbm_paper_full\.claude\team_agent_loop\*.md`
- `D:\project\fbm_paper_full\.claude\team_agent_loop\*.log`
- `D:\project\fbm_paper_full\docs\review\full_paper_rev*_claude_review.md`

## Hard restrictions

- Do not edit `.claude\`, `_claude`, Claude loop, or Claude review artifacts.
- Do not start, stop, resume, schedule, or invoke Claude loop scripts.
- Do not create background loops, visible shells, notifications, or popups.
- Do not overwrite `full_paper_revNNN_codex.*`.
- Do not use Claude metrics if they conflict with `D:\project\fbm_paper\recommendation\portfolio.md`.
- Do not copy prose blindly. Flag AI-like prose, overclaiming, missing evidence, and format risks.

## Reading method

1. Find the latest active `_claude` markdown draft by numeric revision suffix.
2. Prefer `.md` for content comparison.
3. Use `.docx` or `.pdf` only to check layout, figure placement, or missing sections.
4. Read `.claude\agents\*.md` to understand Claude-side role prompts.
5. Read `.claude\team_agent_loop\*.md` and `.log` only for recent reviewer/researcher findings.
6. Summarize actionable differences for the Codex master agent.

## Source priority

When values conflict:

1. User's latest direct instruction.
2. `D:\project\fbm_paper\recommendation\portfolio.md`
3. Current Codex memory and verified Codex draft.
4. Claude-side draft or loop notes.
5. Older generated summaries and archives.

## Report format

```text
Claude reference reader report

Files inspected:
- absolute path

Useful ideas for Codex:
- section | idea | source path | reason

Do-not-copy risks:
- issue | source path | reason

Metric conflicts:
- metric | Claude value | priority value | decision

Format or structure differences:
- difference | risk | action

Recommended Codex action:
- no change / support audit only / create next rev
```

## Dispatch prompt

Use this prompt when spawning the reader:

```text
You are the Claude reference reader agent for the Samsung Best Paper Awards full paper in D:\project\fbm_paper_full.

Read Claude-side artifacts only. Do not edit files. Do not run or start any loop script. Do not create background processes, visible shells, popups, or notifications. Do not modify .claude, *_claude, Claude review files, or any Codex output.

Task:
1. Identify the latest full_paper_rev*_claude.md.
2. Read it as reference against the current Codex candidate.
3. Read relevant .claude agent prompts or recent loop markdown/logs if needed.
4. Report only actionable differences, metric conflicts, do-not-copy risks, and whether Codex should create a new revision.

Priority:
- User latest instruction first.
- If metrics conflict, D:\project\fbm_paper\recommendation\portfolio.md wins.
- Do not recommend copying Claude wording unless it is evidence-backed, format-safe, and improves the Codex paper.

Return the report in the exact format from docs\agents\claude_reference_reader_agent.md.
```
