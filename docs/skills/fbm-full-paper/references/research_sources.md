# Research Sources

Use this file to route folder research. Record findings in `docs/memory/full_paper_memory.md`.

## `D:\project\fail-map`

Mission:

- Map generation.
- Raw failure data to Failbit Map representation.
- Visual assets, JSON, chip coordinates, map pipeline, and any operational integration evidence.

Search targets:

- README or docs.
- Scripts that generate maps, images, labels, or JSON.
- Result folders, sample images, logs, and notebooks.
- Any link to Known or Unknown flows.

## `D:\project\unknown-contrastive`

Mission:

- Unknown defect grouping.
- Contrastive embedding, clustering, candidate reduction, field validation, and synthetic benchmark separation.

Critical rule:

- Field operation evidence is `13` candidate groups and `7` confirmed defects.
- Do not present synthetic benchmark metrics as field operation metrics.

Search targets:

- Training/evaluation scripts.
- HDBSCAN or clustering code.
- Embedding exports.
- Metrics tables, logs, generated benchmark configs.
- Figures showing clusters or candidate examples.

## `D:\project\known-cnn`

Mission:

- Known defect recognition.
- CNN, ROI-YOLO, chip/object identification, FCM-PM or multi-label evidence if present.

Search targets:

- Model definitions.
- Training logs and evaluation results.
- Ablation tables.
- Figures showing chip classes, ROI boxes, or multi-label examples.
- Dataset split logic, especially source-chip split rules.

## `D:\project\failure_agent`

Mission:

- Future work.
- Automation, agentic failure analysis, deployment direction, monitoring, or follow-up architecture.

Use rule:

- Treat this folder as future work unless a result is clearly implemented and evidenced.

## Reporting template

```text
Folder:
Files inspected:
Strong evidence:
- claim | source path | why it matters
Weak or unsafe evidence:
- claim | source path | risk
Paper insertion candidates:
- section | proposed content | source path
Open questions:
- ...
```
