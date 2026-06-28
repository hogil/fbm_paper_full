# Full Paper 멀티에이전트 시스템 — 아키텍처

> 목적: 간이 생성본 `paper_domain_pipeline.md`(= codex 2page docx `paper_codex_2page_rev167.docx` 의 md 마스터)를
> **삼성 Best Paper Awards full paper(4~10매)** 로 확장한다. 양식 정본은 `CLAUDE.md` 의 "Full Paper 작성 절대규칙" + `PAPER_FULL_RULES.md`.
> 본 문서가 시스템 단일 진실 소스다. agents / skill / workflow 는 모두 이 문서를 참조한다.

## 0. 절대 제약 (Rule -1 / Rule 0)
- **창/cmd/PowerShell/popup 절대 금지 (Rule -1)**. 모든 에이전트는 **Read / Grep / Glob / Edit / Write tool 만** 사용한다.
  - Bash · PowerShell · PushNotification · SendMessage · cron 창 · 외부 알림 호출 전부 금지.
- 루프는 **세션 내 Workflow** 로만 돈다(백그라운드 창을 띄우는 `.ps1` 절대 신규 생성 금지). 기존 `.claude/team_agent_loop/*.ps1` 은 추천서용 레거시이며 건드리지 않는다.
- **AI 문체 금지 (Rule 0)**: 사람이 직접 쓴 논문처럼. 반복 구조·과요약체·홍보 문구·근거 없는 포장 금지.

## 1. 출력 규약
- 산출물: `full_paper_rev{N}_claude.md` (루트). N 은 1부터 증가. **이전 rev 를 덮어쓰지 말고 새 번호로 저장**(결과물 삭제·덮어쓰기 금지).
- `*_codex*` 파일(예: `paper_codex_2page_rev167.docx`, `paper_domain_pipeline.md` 중 codex 산출분)은 **읽기 전용. 절대 수정 금지**.
- 1차 산출은 `.md` 마스터. docx 변환은 사용자 요청 시 별도(파이썬 foreground) 처리.
- 단위 SI, 약어 첫 등장 시 풀어쓰기, 본문 인용은 문장 우측 `[]`.

## 2. 에이전트 4종
| 에이전트 | 역할 | 허용 tool | 정의 파일 |
|---|---|---|---|
| **master** | 오케스트레이션 + 최종 승인. CLAUDE.md 절대규칙 판정. 루프 가동/중단 판단. (= 메인 세션 + Workflow 스크립트) | Read/Grep/Glob/Edit/Write/Agent/Workflow | `.claude/agents/paper-master.md` |
| **reviewer** | 냉정한 사내 심사위원. 현업 유용성 + 학술 우수성 + 양식 준수 + 출처 신뢰성 + 사람 문체를 비판적으로 채점. **파일 수정 금지** | Read/Grep/Glob | `.claude/agents/paper-reviewer.md` |
| **writer** | full paper 작성/수정. 양식 절대규칙 철저 준수, 사람이 쓴 문체 | Read/Grep/Glob/Edit/Write | `.claude/agents/paper-writer.md` |
| **researcher** | 프로젝트 폴더 자료조사. 폴더별 하위 에이전트 4개 병렬 | Read/Grep/Glob | `.claude/agents/paper-researcher.md` |

### researcher 하위(폴더별) 4
1. **map** — `D:\project\fail-map` (맵 생성 파이프라인: Cython, palette PNG, dual-bucket, positions JSON)
2. **unknown** — `D:\project\unknown-contrastive` (InfoNCE/DenseCL/MoCo/NV-Retriever/NeCo, HDBSCAN, 7-recipe)
3. **known** — `D:\project\known-cnn` (+ `D:\project\fail-map`) (ConvNeXtV2, ROI-YOLO 2-stage, chip-CNN obj-id map)
4. **future** — `D:\project\failure_agent` (further work: failure analysis agent)

## 3. 루프 (세션 내 Workflow, 창 안 뜸)
한 사이클 = `research(4 폴더 병렬) → write(rev{N} 생성) → review(채점) → master 판정`.
- master 가 reviewer 점수와 변화량을 보고 다음 사이클 실행 여부를 결정한다.
- 목표 점수 도달 또는 K회 연속 개선 없음(plateau) 이면 정지. 점수 rubric 은 `SCORING_RUBRIC.md`.
- 각 rev 는 새 파일. reviewer 코멘트는 `docs/paper_system/review_log/rev{N}.md` 에 누적.

## 4. 데이터 출처 무결성
- 실전 vs PoC vs 개발중 데이터를 절대 혼동하지 않는다. 상세는 `SOURCE_PROVENANCE.md`.
- 핵심: P1 Known 실전 CNN→ROI-YOLO weighted F1 0.95 / Unknown 실전은 metric 없음(13 후보→7 실불량) / chip-CNN obj-id map 은 개발중 생성데이터.
