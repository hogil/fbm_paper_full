# full_paper_rev211_codex final checklist

Date: 2026-06-29

Files:
- `D:\project\fbm_paper_full\full_paper_rev211_codex.md`
- `D:\project\fbm_paper_full\full_paper_rev211_codex.docx`
- `D:\project\fbm_paper_full\full_paper_rev211_codex.pdf`
- `D:\project\fbm_paper_full\full_paper_final.docx`

## Format gate

| Check | Result |
|---|---|
| 4-10 pages | PASS: 9 pages |
| Abstract 15 lines or fewer | PASS: 13 extracted lines |
| DOCX built with official builder | PASS |
| PDF exported from Word | PASS |
| Tables rendered as Word tables | PASS: 8 tables |
| Figure captions below figures | PASS |
| Table captions above tables | PASS |
| Figure 6/7 and Table 6/7 rendered check | PASS |

## Requested wording checks

| Check | Result |
|---|---|
| `map review` removed | PASS |
| `review label` removed | PASS |
| `chip measure` removed | PASS |
| `single-failure source 기반 2-combo controlled synthetic benchmark` removed | PASS |
| `검토군` / `불량군` not introduced | PASS |
| `false alarm 0.00` removed | PASS |
| `micro-F1(bit-F1)` removed | PASS |
| `candidate group` removed | PASS |
| Incorrect InfoNCE full name removed | PASS |
| Table 6 caption separated generated-development benchmark from field review result | PASS |

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
| `generated-chip development extension` not present | PASS |

Decision: `full_paper_rev211_codex` is the current final Codex candidate.
