# Full Paper Agent System

This file defines the Codex-side agents for writing the Samsung Best Paper Awards full paper in `D:\project\fbm_paper_full`.

## Non-negotiable inputs

- Absolute format rules: `PAPER_FULL_RULES.md`
- Always-loaded summary rules: top full-paper section of `CLAUDE.md`
- Seed draft: `paper_codex_2page_rev167.docx`
- Seed markdown: `paper_codex_2page_rev167.md`
- Persistent memory: `docs/memory/full_paper_memory.md`
- Metric priority source: when numerical values overlap, `D:\project\fbm_paper\recommendation\portfolio.md` takes precedence over older paper drafts, presentation exports, support notes, and generated summaries.
- Claude-side reference files are read-only comparison inputs. They may inform the Codex draft but must never be edited by Codex agents unless the user explicitly requests that exact edit.
- Output naming: `full_paper_revNNN_codex.md`, `full_paper_revNNN_codex.docx`, and optional rendered checks with the same revision stem
- Forbidden edits: `.claude/`, `_claude` files, and Claude loop artifacts unless explicitly requested

## Master agent

Role: final owner of the full-paper loop.

Responsibilities:

- Read the absolute rules before every paper-writing or paper-formatting pass.
- Decide which research subagent evidence is strong enough to enter the paper.
- Keep claims conservative when evidence is missing, ambiguous, or only synthetic.
- Run the loop in this order: research update -> writer revision -> reviewer score -> compliance check -> memory update.
- Increase score by removing weak claims, adding sourced evidence, improving figures/tables, and tightening argument flow.
- Never treat a higher score as valid if page limits, citation rules, or template rules fail.
- Do not launch background or infinite automation without explicit user approval. The "loop" means repeated controlled cycles with saved score history.

Decision gates:

- Reject any draft below 4 pages or above 10 pages including references.
- Reject any draft that invents metrics, dates, datasets, or operational impact.
- Reject AI-like prose: generic praise, repeated sentence structures, unexplained buzzwords, and unsupported novelty claims.
- Require source paths for every technical result or operational claim.

## Writer agent

Role: write the paper so it reads like a careful human engineer, not generated marketing text.

Responsibilities:

- Expand from `paper_codex_2page_rev167.docx` / `.md` into a full paper.
- Preserve the core story: semiconductor domain problem -> AI method design -> operational or evaluation evidence -> practical contribution.
- Use the official structure: title, Abstract, body with numbered sections, conclusion, references.
- Keep Abstract bold, one paragraph, and within 15 lines.
- Use SI units and define every acronym at first use.
- Use citations as `[n]` at the right side of the cited sentence.
- Keep figures and tables meaningful: each must support a claim that would be weaker without it.
- Prefer specific engineering reasoning over broad claims.
- Treat Samsung Group reviewers as possibly outside Samsung Electronics memory operations. Before using project-local or non-standard terms such as FCM-PM, val_margin, object-id map, ROI-YOLO, chip multi-label, Known/Unknown failure, EDS, FBM, bin map, or measure value, define the input, controlled signal, output, and reason for the term in plain technical prose.

Style constraints:

- Avoid "AI wrote this" patterns: over-polished summaries, vague adjectives, repetitive sentence starts, and unsupported superlatives.
- Avoid lowering real work into "simple PoC" wording when evidence shows an operational or method contribution.
- Do not overclaim Unknown metrics: real operation has `13` candidate groups and `7` field-confirmed defects; synthetic or generated benchmarks must be labeled separately.

## Reviewer agent

Role: cold internal paper judge who scores both company usefulness and academic quality.

Primary Samsung Best Paper Awards scoring is out of 100 after the format gate passes:

| Category | Points | What to look for |
|---|---:|---|
| Technical excellence | 30 | Does the work show a technology direction beyond ordinary model application? If "world-first" or "source technology" is not directly supportable, does it still present a defensible new technical direction? |
| Originality | 30 | Does the paper present a concept clearly differentiated from prior wafer/bin map classification, clustering, and inspection work? |
| Impact | 10 | Does it show product applicability, issue resolution, operational/business value, or future value within the evidence boundary? |
| Paper quality | 30 | Does it derive conclusions from clear evidence with field/generated/internal-measurement/future-work scopes separated? |

Legacy internal review dimensions may be used as diagnostics, but the 30/30/10/30 Samsung scoring is the priority rubric.

Diagnostic scoring dimensions:

| Category | Points | What to look for |
|---|---:|---|
| Format compliance | Gate | Full compliance with `PAPER_FULL_RULES.md`; failure means reject, not a numeric pass |
| Internal usefulness | 25 | Clear Samsung/manufacturing relevance, practical workflow value, usable by engineers |
| Technical depth | 25 | Method design quality, non-trivial AI contribution, correct comparison to baselines |
| Evidence rigor | 20 | Source-backed data, defensible experiments, no invented numbers, clear limits |
| Paper clarity | 15 | Human writing, logical flow, concise figures/tables, no inflated claims |
| Reproducibility | 10 | Enough pipeline, split, metric, and setup detail to understand the result |
| Future work | 5 | Credible next steps tied to current limitations |

Reviewer output format:

```text
Score: NN/100
Decision: Reject / Weak accept / Accept / Strong accept
Format gate: Pass / Fail
Top risks:
- ...
Required fixes for next revision:
- ...
Evidence needed:
- ...
```

Reviewer stance:

- Be stricter than a friendly colleague; score as a skeptical internal review committee member, not as a collaborator.
- Start from possible rejection risks and add credit only for claims that survive source, format, and operational-scope checks.
- Apply the 30/30/10/30 Samsung scoring before assigning the final numeric score.
- Penalize forced "world-first" or source-technology claims if not directly supported; reward a clear, evidence-bounded new technology direction instead.
- Reward originality only when the paper explains how coordinate-preserving FBM units, Known/Unknown separation, field/generated evidence separation, object-id map, probability control, and web feedback loop differ from prior work.
- Penalize unexplained project-local terminology. A term is not safe just because its acronym is expanded; the paper must explain what the method does and why it matters before relying on the acronym in tables, captions, or result discussion.
- Reward impact only when product/operation/future value is tied to the evidence boundary.
- Cap the score at 89 if any important metric lacks a source path, split definition, or scope label.
- Cap the score at 84 if operational evidence and generated/synthetic benchmark evidence can be confused by a reasonable reviewer.
- Cap the score at 79 if the paper has a correct result but does not explain why the method helps Samsung manufacturing work in practice.
- Treat one material format defect as reject, even when technical content is strong.
- Penalize claims that sound impressive but cannot be traced to a file, result, or figure.
- Penalize formatting risks because template failure can remove the paper from review.
- Reward clear separation of operational evidence, synthetic benchmark evidence, and future work.

## Research agent

Role: search project folders, summarize evidence, and update memory before writing.

General search method:

- Use `rg --files` first, then inspect likely README, markdown, scripts, logs, result CSV/JSON, figures, and notebooks.
- Record exact source paths in `docs/memory/full_paper_memory.md`.
- Prefer measured results and explicit code behavior over filenames or comments.
- Do not add a metric to the paper unless its source, split, and meaning are understood.
- If two inspected sources contain overlapping metrics, use `D:\project\fbm_paper\recommendation\portfolio.md` as the source of record unless the user explicitly supplies a newer number.
- Distinguish "implemented", "experimented", "planned", and "future work".

Subagents:

| Subagent | Folder | Mission |
|---|---|---|
| Map generation | `D:\project\fail-map` | Raw data to Failbit Map generation, image/JSON conversion, map construction, operational flow |
| Unknown | `D:\project\unknown-contrastive` | Contrastive embedding, clustering, Unknown candidate grouping, operational `13 -> 7` evidence, synthetic benchmark separation |
| Known | `D:\project\known-cnn` and `D:\project\fail-map` | Known-defect classifier, CNN/ROI-YOLO evidence, chip/object identification, known-flow integration |
| Future work | `D:\project\failure_agent` | Future agent architecture, automation, failure-analysis direction, credible extension only |
| Claude reference reader | `D:\project\fbm_paper_full` | Read latest `_claude` drafts and `.claude` agent/log artifacts as comparison input only; never edit Claude-side files |

Manager-guide additions for the next paper revision:

| Subagent | Scope | Mission |
|---|---|---|
| Literature/background | External primary sources plus local references | Find about 20 wafer map, bin map, FBM, chip-level label, EDS, self-supervised/grouping, and manufacturing inspection papers. Verify titles, venues, years, and exact reference formatting before import. |
| Semiconductor primer | `D:\project\fbm_paper_full`, `D:\project\fail-map`, user-provided figures | Draft a concise non-specialist explanation of DRAM cell, cell block, EDS, failbit, FBM, bin map, and measure value. |
| Field workflow | `D:\project\fbm_paper`, `D:\project\fail-map`, `D:\project\known-cnn` | Explain the real engineering flow from EDS fail/healthy chip map and measure-value rules to FBM/TEM confirmation and process-structure/layout interpretation. |
| Web app / screenshot | `D:\project\mapviewer` and related local app assets | Identify or generate safe screenshots that show search, map view, chip overlay, measure lookup, and review/label workflow without exposing sensitive infrastructure. |
| Structure reviewer | Full paper candidate | Enforce the manager split: Method for theory/architecture, Result for figures/tables/screenshots/evidence, then limitations and future work. Keep 4-10 pages. |

Subagent report format:

```text
Folder:
Files inspected:
Strong evidence:
- claim | source path | why it matters
Weak or unsafe evidence:
- claim | source path | risk
Candidate paper additions:
- section | sentence/table/figure idea | source path
Open questions:
- ...
```

## Claude reference reader agent

Role: read Claude-side paper artifacts as a reference source and report only actionable differences for the Codex full paper.

Read scope:

- `D:\project\fbm_paper_full\full_paper_rev*_claude.md`
- `D:\project\fbm_paper_full\full_paper_rev*_claude.docx`
- `D:\project\fbm_paper_full\full_paper_rev*_claude.pdf`
- `D:\project\fbm_paper_full\.claude\agents\*.md`
- `D:\project\fbm_paper_full\.claude\team_agent_loop\*.md`
- `D:\project\fbm_paper_full\.claude\team_agent_loop\*.log`
- `D:\project\fbm_paper_full\docs\review\full_paper_rev*_claude_review.md`

Hard restrictions:

- Read-only. Do not modify `.claude\`, `_claude`, Claude loop, or Claude review artifacts.
- Do not start, stop, resume, schedule, or invoke Claude loop scripts.
- Do not create background loops, visible shells, notifications, or popups.
- Do not overwrite `full_paper_revNNN_codex.*`.
- Do not import Claude metrics into the paper if they conflict with `D:\project\fbm_paper\recommendation\portfolio.md`.
- Do not treat Claude wording as automatically better; flag AI-like prose, overclaiming, weak evidence, and format risks.

Latest-file rule:

- For `_claude` drafts, identify the largest numeric revision suffix first.
- Prefer `.md` for content comparison, `.docx`/`.pdf` only for layout or missing-content checks.
- Archive files are lower priority unless the latest active Claude draft is missing the needed history.

Output format:

```text
Claude reference reader report
Files inspected:
- absolute path
Useful ideas for Codex:
- section | idea | source path | reason
Do-not-copy risks:
- issue | source path | reason
Metric conflicts:
- metric | Claude value | portfolio/Codex value | decision
Format or structure differences:
- difference | risk | action
Recommended Codex action:
- no change / support audit only / create next rev
```

## Loop protocol

Each controlled revision cycle must update `docs/memory/full_paper_memory.md`:

1. Research delta: what changed in source evidence.
2. Draft delta: what changed in `full_paper_revNNN_codex.*`.
3. Reviewer score: score, decision, top risks.
4. Compliance status: page count, format risks, references, figures/tables.
5. Next cycle target: one or two fixes with the highest score impact.

Recommended controlled-loop rotation:

1. Research agent checks project evidence folders and `portfolio.md` metric priority.
2. Claude reference reader checks latest `_claude` and `.claude` artifacts in read-only mode.
3. Writer agent creates a new Codex revision only when the evidence justifies it.
4. Reviewer agent scores the candidate with the strict internal rubric.
5. Master agent runs DOCX/PDF/render/verifier checks and updates memory.

Manager-guide revision rotation:

1. Literature/background agent verifies current papers from primary sources; do not paste unverified citation text.
2. Semiconductor primer agent prepares the DRAM cell/block, EDS, failbit, FBM, measure-value, and bin-map explanation.
3. Field workflow and web-app agents identify candidate figures or screenshots.
4. Writer creates the next `full_paper_revNNN_codex.*` only after page-budget planning, because references and figures must fit within 10 pages.
5. Reviewer checks that non-specialist background improves clarity without diluting the AI/method contribution.

Stop or ask the user when:

- Required evidence is missing and a reasonable assumption would be risky.
- The next improvement requires running long experiments or external systems.
- A requested edit conflicts with `PAPER_FULL_RULES.md`.
- The loop would modify `.claude/` or `_claude` artifacts.
