# full_paper_rev210_codex final checklist

Date: 2026-06-29

Files:
- `D:\project\fbm_paper_full\full_paper_rev210_codex.md`
- `D:\project\fbm_paper_full\full_paper_rev210_codex.docx`
- `D:\project\fbm_paper_full\full_paper_rev210_codex.pdf`
- `D:\project\fbm_paper_full\full_paper_final.docx`

## Format gate

| Check | Result |
|---|---|
| 4-10 pages | PASS: 9 pages |
| Abstract 15 lines or fewer | PASS: 14 extracted lines |
| DOCX built with official builder | PASS |
| PDF exported from Word | PASS |
| Tables rendered as Word tables | PASS: 8 tables |
| Figure captions below figures | PASS |
| Table captions above tables | PASS |
| Figure 6/7 labels readable in rendered page check | PASS |
| Last page not blank | PASS: references are present |

## Requested wording checks

| Check | Result |
|---|---|
| `false alarm 0.00` removed | PASS |
| `micro-F1(bit-F1)` removed | PASS |
| `candidate group` removed | PASS |
| `한 점수처럼` removed | PASS |
| `review label` changed to `검토 라벨` | PASS |
| `chip measure` changed to `chip 계측값` | PASS |
| `generated-chip development extension` removed | PASS |
| Incorrect InfoNCE full name removed | PASS |
| Unknown field result uses 2,000 images -> 13 groups -> 7 real failures | PASS |
| `검토군` / `불량군` forced wording removed | PASS |

## Scope checks

| Scope item | Result |
|---|---|
| Known F1 0.95 = field validation | PASS |
| Unknown 13→7 = field review result, not classifier precision | PASS |
| object-id map = generated development | PASS |
| FCM-PM = controlled synthetic benchmark | PASS |
| KRW 12.3B = internally certified quantified contribution | PASS |
| Operation impact and model metrics are not summed | PASS |

## Text-integrity checks

| Check | Result |
|---|---|
| Soft hyphen / `￾` not present | PASS |
| `해 야`, `의 심`, `파 이프라인` not present | PASS |
| `P1` / `P2` not present | PASS |
| `Information Noise` not present | PASS |

Decision: `full_paper_rev210_codex` is the current final Codex candidate.
