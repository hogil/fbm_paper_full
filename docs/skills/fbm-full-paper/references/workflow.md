# Full Paper Workflow

## Revision naming

Scan for existing files:

```powershell
Get-ChildItem -Name full_paper_rev*_codex.*
```

Use the next numeric revision. If none exist, start with `full_paper_rev001_codex.md`.

## Controlled cycle

1. Research update
   - Inspect `D:\project\fail-map`, `D:\project\unknown-contrastive`, `D:\project\known-cnn`, and `D:\project\failure_agent`.
   - Update `docs/memory/full_paper_memory.md`.

2. Draft update
   - Expand from `paper_codex_2page_rev167.md`.
   - Keep only claims that have evidence or are explicitly framed as future work.

3. Reviewer pass
   - Apply `references/reviewer_rubric.md`.
   - Save score and blockers in memory.

4. Format pass
   - Check `PAPER_FULL_RULES.md`.
   - Verify page range, two-column intent, caption positions, citation format, references, fonts, margins, and title length.

5. Export pass
   - Generate `.docx` only after draft content is stable.
   - Render/check layout when possible.

## Writing order

Recommended paper structure:

1. Title and authors
2. Abstract
3. Introduction
4. Problem setting and data pipeline
5. Known defect recognition
6. Unknown candidate grouping
7. Full-paper evidence table and results
8. Discussion and future work
9. Conclusion
10. References

Use section numbering compatible with `PAPER_FULL_RULES.md`.

## Stop conditions

Ask the user before proceeding when:

- A key metric cannot be traced to a source file.
- The paper would need a new long experiment.
- Page count cannot be controlled without removing a major claim.
- The requested edit conflicts with the absolute rules.
