
# Full Paper 작성 절대규칙 — Samsung Best Paper Awards

> 별도 deliverable(추천서와 분리). **양식·분량 미준수 시 심사에서 제외**되므로 아래는 전부 절대규칙이다.
> 상세 정본: `PAPER_FULL_RULES.md`. 본 섹션은 항상-로드되는 enforced 요약본이며, 두 문서는 항상 동기화한다.

## FP Rule A — 구성·분량 (심사 제외 직결)
- 공식 템플릿 사용 필수. 국/영문 허용(언어 가점·불이익 없음).
- 초록 2매(extended abstract: `제목 → abstract → 본문(서론/본론/결론) → 참고문헌`). 논문 4~10매(참고문헌 등 모든 내용 포함).
- 단순 아이디어/컨셉만 제출 시 심사 제외. 본문 인용은 문장 오른쪽 `[]` 번호.
- 모든 단위 SI. 약어 첫 등장 시 전부 풀어쓰고, 미표준 약어는 명확히 정의.

## FP Rule B — 레이아웃
- A4(21×29.7cm), 여백 사방 1.5cm, 머리글 1cm / 바닥글 0.5cm.
- 머리글 "Samsung Best Paper Awards" 12pt bold, 바닥글 쪽번호.
- 본문 2단(단 간격 0.5cm). 목차: 장 `1.` `2.` / 절 `1.1.` `2.1.`.

## FP Rule C — 글꼴·정렬
- 영문 Times New Roman / 국문 바탕체, 줄간격 1.0. 제목·저자 좌측정렬 / 본문 양쪽정렬.

## FP Rule D — 글자 크기
- 제목 20 bold / 저자 12 bold / 섹션제목 12 bold / 소제목 10 bold / 본문 10 / Abstract 10 bold / 참고문헌 10 / 그림·표 9 / 각주 9.

## FP Rule E — 제목·저자
- 제목 2줄 이내. 저자명 제목 아래, 소속은 첫 페이지 하단 별도 표기.
- 제1저자 먼저 → 기여도 순. first name → last name 권장(이름 이니셜 금지, 중간 이니셜 허용).
- 제목·섹션제목은 고유명사(BLEU 등) 외 전부 대문자 금지. 소속은 부서 → 소속사 순. 저자명 뒤·바닥글 소속 앞 위첨자 1,2,3.

## FP Rule F — Abstract
- 굵은 글씨, 단락 구분 없이 15줄 이내.

## FP Rule G — 본문
- abstract 바로 아래 시작, 2단 단락 형식.

## FP Rule H — 그림·표
- 모든 그림 캡션·순차번호. `Figure 1. 캡션`(그림 하단) / `Table 1. 캡션`(표 상단), 9pt. "Fig" 약어, 번호 뒤 마침표. 캡션에 중요성 설명 권장.
- 표는 3선 테이블: 위·아래 가로선 진하게 + 헤더 행 밑줄만, 세로선·내부선 전부 없음.

## FP Rule I — 참고문헌
- 성 먼저 + 콤마 + 이름 이니셜. 2인↑은 1저자명 + 'et al.'. Article Title 첫 자 대문자.
- Journal/단행본 제목 이탤릭 + 모든 단어 첫 자 대문자(저널명 약어 가능). Vol. bold. 단행본은 (출판사명, 발행연도).

## FP Rule J — 전체 구성 재확인
- `제목 → abstract → 본문(서론/본론/결론) → 참고문헌`. 길이·형식 미준수 = 심사 제외.

## FP Rule K — 출력은 Word(.docx), 양식 자동 적용 (★ 절대규칙 2026-06-06)
- full paper 최종 산출은 반드시 **`.docx`** 로 만든다. md(`full_paper_rev{N}_claude.md`)는 정본/작성용이고, 제출본은 docx.
- 변환기: **`tools/build_fullpaper_docx_claude.py`** (`python tools/build_fullpaper_docx_claude.py [입력.md]`). 이 빌더가 FP Rule A~J(A4·여백 1.5cm·머리글 "Samsung Best Paper Awards" 12pt bold·바닥글 쪽번호·2단·바탕체/Times·글자크기·3선표·표상단/그림하단 캡션 9pt)를 자동 적용한다.
- 빌더는 codex `tools/build_full_paper_docx.py` 의 양식 함수를 import 재사용한다 — **그 codex 파일은 수정 금지**. `*_codex*` 산출물 전부 불가침.
- **best rev 가 갱신될 때마다 그 rev 의 `.docx` 를 재생성**한다(메인 thread 에서 python 1회, 창 안 뜸).

## FP Rule L — 관리자 가이드 반영: 배경·현장문제·용어 (★ 절대규칙 2026-06-26)
- Introduction은 심사위원이 EDS, wafer/bin map, FBM, chip-level measure 업무를 모른다는 전제로 재구성한다. 최신 wafer/chip-level 불량 분석 연구 흐름을 먼저 설명하고, 그 다음 실제 현장 분석 흐름과 연구 gap을 설명한다.
- 삼성그룹 단위 심사에서는 평가자가 삼성전자/메모리 반도체 업무를 모를 수 있으므로, Introduction과 method 첫 등장부는 비전공 평가자도 이해할 수 있는 정의를 먼저 제공한다.
- 사내 공용어가 아니거나 저자가 새로 정의한 기술어는 약어만 먼저 쓰지 않는다. EDS, FBM, bin map, measure value, Known/Unknown failure, ROI-YOLO, object-id map, chip multi-label, FCM-PM, val_margin, Naive Bayes reject 등은 첫 등장 시 "무엇을 입력으로 받고, 무엇을 구분/제어하며, 왜 필요한지"를 설명한 뒤 약어를 사용한다.
- FCM-PM처럼 논문 내부에서 정의한 방법명은 표/캡션/키워드에만 맡기지 않고, 본문에서 먼저 "chip 전체 coverage를 보장하는 CutMix와 원천 영역별 mask view를 결합해 positive probability를 올리고 negative-tail false alarm을 낮추는 학습 구성"처럼 기능을 설명한다.
- 실제 현장 흐름은 `chip별 EDS fail/양호 확인 → chip별 measure value 기반 고질 불량 분류 → FBM/TEM 등 물리 확인 → 공정 structure/layout 원인 해석 → 공정 불량 제어` 로 정리한다.
- DRAM cell, cell block, EDS, failbit, Failbit Map, measure value를 비전공 심사위원도 이해하도록 그림 또는 텍스트 도식으로 정의한다. Bin map 또는 chip fail/양호 map도 추가 후보로 둔다.
- 논문 본문/표/캡션/키워드/그림 텍스트/metadata에서는 `defect` 용어를 쓰지 않고 `failure`, `fail`, 또는 `불량`을 쓴다. 참고문헌 원문 제목은 정확 표기 규칙이 우선한다.

## FP Rule M — 관리자 가이드 반영: 구성·기여·결과 섹션 (★ 절대규칙 2026-06-26)
- FBM 기반 Known/Unknown failure 정의와 엔지니어 활용 난점을 명확히 설명한다. Known은 등록/label 존재 불량, Unknown은 아직 label 합의가 없는 신규/미분류 불량 후보로 둔다.
- workflow architecture를 포함한다: `measure value / FBM / bin map → Known classification → 등록 불량 filtering → contrastive embedding / clustering → 신규 불량 등록 여부 담당자 확인 → web app 기능 제공`.
- Contribution에는 web app 구현을 4번째 기여로, 실제 적용/평가 범위를 5번째 기여로 포함한다. 단, 과장 없이 source path 또는 사용자 제공 공식 근거 범위에서만 쓰며, HBM 적용/평가는 직접 근거가 제공되기 전까지 제외한다.
- Method는 이론적 근거와 구조 설명 중심, Result는 그림/표/시스템 캡처/web app 화면/bin map/FBM 예시 중심으로 재배치한다.
- wafer map, FBM, 반도체 불량 분석 관련 연구는 약 20편 수준으로 확장한다. 사용자가 준 H. Lee et al. 2024 chip-level wafer bin map 논문은 후보로 두되, title/venue/year는 원문 확인 후 정확히 반영한다.
- 한계와 future work를 마지막에 분리해 쓰고, 추가 figure/reference를 넣더라도 4~10매 제한을 넘기지 않도록 기존 문단·표·그림을 압축/교체한다.

## FP Rule N — 공식 심사 기준 (★ 절대규칙 2026-06-26, 채점 정본)
- 심사 기준은 `기술의 우수성 30점 / 독창성 30점 / 파급효과 10점 / 논문 질적 수준 30점`이다.
- 기술의 우수성: 세계 최초 또는 원천 기술 수준의 과장 claim을 억지로 만들지 않는다. 기존 공개 연구와 현장 분석 흐름 사이에서 어떤 새로운 기술 방향을 제시했는지, 왜 단순 모델 적용이 아닌지 명확히 쓴다.
- 독창성: 좌표 보존형 FBM 분석 단위, Known/Unknown 분리, field review와 generated benchmark의 분리, chip-level object-id map, chip multi-label probability control, web review/label feedback loop 결합을 기존 기술과의 차별점으로 설명한다.
- 파급효과: 제품 적용, 현업 이슈 해결, 운영/미래 가치를 근거 범위 안에서 쓴다. 48매 단위 검토에서 일 단위 약 2만 wafer 누적 비교 구조로 바뀐 점은 model throughput이 아니라 viewer/data pipeline 운영 파급효과로 설명한다.
- 논문 질적 수준: 명확한 근거에서 결론을 도출해야 한다. field / generated / internal engineering measurement / future work 범위를 분리하고 unsupported claim은 넣지 않는다.
- 게이트(FP Rule A~K 양식·10매·약어·금지 표현)는 채점 이전의 통과 조건으로 유지한다.

---

# 사내 AI Specialist 추천서 작성 절대 규칙

## Rule -1 (Rule 0 위 최상위 절대규칙, 2026-05-16): 창 / cmd / popup 절대 안 뜸
- 10분 주기 cycle 무한 루프 돌더라도 **cmd 창 / PowerShell 창 / OS notification / popup 절대 띄우지 않는다**.
- background agent 들에게 다음 금지 규칙을 매 dispatch 마다 prompt 안에 명시한다:
  - Bash tool 호출 금지
  - PowerShell tool 호출 금지
  - PushNotification 호출 금지
  - 외부 알림 / SendMessage / cmd 실행 금지
  - 작업은 Read / Grep / Glob / Edit / Write tool 만 사용
- cron prompt 도 동일 규칙 박은 채 등록한다.
- 사용자가 "창 뜬다" 보고 시 즉시 CronDelete 로 중단하고 원인 추적.

## Rule 0 (최상위 절대규칙): AI 문체 금지
- 결국 내가 사내 AI 전문가로 인정받기위해 반도체역량을 바탕으로 AI 모델을 어떻게 설계하고 개밣했고 추가로 성능을 올리기위해 어떤 방법들을 적용시켰냐 이런게 중요
- 심사위원이 어떤 기법들인지도 느끼고 전체 설계도 이해하게 그리고 역량이 뛰어나구나 느낄 수 있게해서 합격하도록 만들자
- 추천서 문장은 절대 AI가 자동 작성한 것처럼 보이면 안 된다.
- 사람이 직접 쓴 지원서처럼 자연스럽고 담백하게 쓴다.
- 수치나 로그를 억지로 끼워 넣지 않는다. 심사자가 읽었을 때 "왜 이 말이 여기 나오지?" 싶은 문장은 삭제한다.
- 같은 문장 구조, 과한 요약체, 홍보 문구, 근거 없는 성과 포장은 전부 금지한다.
- 사용자가 직접 거부한 표현이나 어색하다고 지적한 문장은 이후 루프에서 다시 살리지 않다.
- **★ 절대 금지 기호 (2026-05-20)**: `§` (절 기호) — 본문, 표, ASCII 박스, inline 참조 어디에도 사용 금지. inline 참조는 `**[참조]**` 굵은 대괄호 형식만.
- **★ 호칭 (2026-05-20)**: 추천서에서 "운영자" 표현 금지. 현업에서 도구를 다루는 사람은 모두 "담당자" 로 통일.

## 절대 규칙



**★ 형식 절대 규칙**:
- 대괄호 `[...]` 와 대시 `-` 사이에는 어떤 텍스트도 쓰지 않는다. 대괄호 라인 바로 다음 줄에 대시 bullet 이 와야 한다.
- 양식 spec 의 항목 설명 ("데이터 수집 경로, 전처리 기법 및 피처 엔지니어링 근거" 등) 은 대시 bullet 옆에 그대로 적되, 본문 내용은 대시 bullet **아래**로 옮긴다.
- 대시 bullet 항목 (데이터 / 알고리즘 / 최적화 / 기술 지표 / 현업 임팩트 등) 을 `**[데이터]: ...**` 같은 sub-bracket header 로 변환하지 않는다. 항상 `- 데이터: ...` 대시 bullet 형식 유지.
- 이 양식 외 추가 ㅁ section (예: 표지 / Executive Summary / 핵심 요약 / 종합 평가 / 부록) 절대 신설 금지.
- 양식 내부에서 가독성용 sub-heading (bold label, 짧은 소제목, 표 안 제목) 은 허용. 단 `##` / `###` / `####` markdown heading 으로 새 section 신설은 금지.




### Rule 6: 팀 에이전트 4개 구조
1. **Master Orchestrator**: 모든 것 관장 + 최종 승인 (본 대화의 메인 thread)
2. **지원서 작성 agent**: .md 파일 작성/수정
3. **냉정한 평가 심사위원 agent**: 부족한 점 지적 + 합격률 추적
4. **자료조사 agent**: 폴더별 독립 병렬 + 이미지 분석 (하위 에이전트 폴더별 분리)

### Rule 7: 참조 폴더 6개 (모두 활용)
- `D:/project/known-cnn`
- `D:/project/mapviewer`
- `D:/project/unknown-contrastive`
- `D:/project/anomaly-detection`
- `D:/project/fail-map`
- `D:/project/fbm_paper`



#### ★ 자문 교수 실명 표기 규칙 (역전 — 사용자 재결정 2026-06-19) ★
사용자 재결정: **"사내 논문이라도 본문에 교수 자문 inline 표기는 수준이 떨어진다 — 빼라."** (과거 "교수실명은 그냥 적는거다" 지시는 이 재결정으로 폐기. full paper 본문에 `(연세대 인공지능학과 전해곤/박은병 교수 자문)` 류 개인 자문 표기를 넣지 않는다. 기술 정당화는 저자 본인 판단으로 서술; 참고문헌 [N] 인용은 가능하되 개인 자문 inline은 금지.)
- backbone 선정 근거(자문 표기 없이): 약 1,500 규모라 전역 attention(ViT/Swin) 학습 부족, 결함이 국소 zone/chip에 몰려 CNN 국소 수용장 적합, FCMAE 가 국소 패턴 복원 강화 + 384 해상도 미세구조 보존, ConvNeXtV2 가 MaxViT 와 F1 0.87 동급이며 params −26%·FLOPs −39% 로 운영 효율 우위.
- CutMix 선정 근거(자문 표기 없이): Mixup 은 픽셀을 중간값으로 섞어 존재하지 않는 중간 Grade 생성→categorical 의미 깨짐 / Diffusion 은 실제 2-combo 데이터(라벨) 부족으로 양질 생성 분포 확보 어려움(라벨·연산 부담) → 영역 단위 원값 보존 CutMix 계열 적합.



#### ★ P1 Unknown 서술 순서 절대 규칙 — 실전 운영 확인 후 생성 데이터 metric 개발 ★
사용자 직접 정정: **"실전 운영은 지표가 없다. 13후보 7실제 불량밖에 없고, 데이터 생성해서 metric 보면서 개발중이다"**
- 제출본에서 Unknown contrastive 추가 생성 데이터 성능표를 넣을 때는 아래 skeleton 을 사용합니다. 이는 실전 현업 성과가 아니라 **추가 개선 및 metric 측정을 위한 생성 데이터 개발 관리표**입니다. 빈 칸은 `TBD` 또는 `학습 후 채워짐` 으로 둡니다.
- **★★★ 표 캡션 필수 1줄 (사용자 직접 명시 2026-05-16)**: 7-recipe 표 직전 또는 직후 캡션에 "이 표는 P1 Unknown 실전 운영 성과 (13 후보 중 7 실제 불량 현업 확인) 와는 분리된 후속 개발 / metric 관리용 synthetic benchmark 결과다. 실전 운영 Unknown 에는 정답 label 이 없어 F1 / ARI / recall 같은 정량 metric 이 성립하지 않고, 13/7 운영 검증은 후보 압축 결과이지 분류 metric 이 아니다" 식 한 줄을 박는다. 이 구분 없이 표만 두면 심사자가 "실전 Unknown 에도 ARI 가 있었던 것처럼 쓴 것 아니냐" 라고 의심한다.

| # | Recipe | P1 | P2 | P3 | P4 | ARI | AMI | Sil |
|---|--------|----|----|----|----|-----|-----|-----|
| 1 | B0 Global InfoNCE only | 학습 후 채워짐 | 학습 후 채워짐 | 학습 후 채워짐 | 학습 후 채워짐 | 학습 후 채워짐 | 학습 후 채워짐 | 학습 후 채워짐 |
| 2 | + Local DenseCL (LW=0.5) | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 3 | + MoCo Queue 4096 | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 4 | + NV-Retriever NEG 0.72 | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 5 | + NeCo 0.2 (B5 5-tool full) | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 6 | NEW (B5 - Local, 4-tool) | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 7 | NEW + tau=0.5 post-reassign | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

#### ★ P1 Known 2-stage 서술 절대 규칙 — 실전 검증 구조와 생성 데이터 추가 개발 구조 분리 ★
사용자 직접 정정: **"P1 known 은 2 stage 실전데이터로 검증 한거고 cnn -> roi-yolo 에서 현재 다양한 평가를 위해 생성한 데이터셋으로 cnn->chip-cnn obj id map 으로 분류하려한다"**

- P1 Known 의 **실전 검증 완료 성과**는 반드시 **CNN → ROI-YOLO 2-stage** 로 씁니다.
- 해당 실전 검증 성과는 추천서 제출본에서 **[실전 현업 데이터] 사내 실제 불량 이미지 데이터, 16-class · 1,500 labeled samples · 4:1 stratified split, weighted F1 0.95** 로 중립 표기합니다. BBD/Overlay/CD 경험 근거처럼 오독되지 않도록 P1 Known 데이터 출처 설명에서 BBD 표현을 반복하지 않습니다.
- 현재 추가 개발 중인 구조는 기존 **CNN → ROI-YOLO** 구조를 대체/확장하기 위한 **CNN → chip-CNN obj-id map** 구조입니다.(**CNN → chip-CNN obj-id map** 확장하는이유도 설명)
- `known-cnn` 폴더의 chip-CNN / obj-id map / chip 단위 결함 분류 수치는 **다양한 평가를 위해 생성한 데이터셋 기반의 추가 개발값**입니다.
- 추천서 본문에서는 P1 Known 을 `실전 데이터로 검증된 CNN → ROI-YOLO 2-stage 성과 → 생성 데이터셋 기반 CNN → chip-CNN obj-id map 추가 개발` 순서로 씁니다.
- chip-CNN obj-id map 수치를 ROI-YOLO 0.95 와 동일한 실전 현업 성과처럼 쓰거나, 실전 검증 완료 수치로 표현하면 안 됩니다.
- chip-CNN obj-id map 라벨은 반드시 `[추가 생성 chip 데이터, 개발 중]` 로 둡니다.

#### ★ P2 Multi-label — 현업 defect 원천 + 도메인 생성/검증 표기 규칙 ★
- P2 성능표는 단순 생성 PoC 표가 아니라, **현업 defect chip 원천을 기반으로 2-combo 부족 문제를 보완한 도메인 생성/검증 관리표**로 둡니다.
- P2 표는 `Baseline → Focal loss → ASL → CutMix only → CutMix + Pair → FCM-PM best val_f1 → FCM-PM best val_margin → Ensemble → KD` 순서로 둡니다.
- P2 표에는 `Latency / Throughput / Params` 운영성 열을 추가합니다. Ensemble은 `4x / 1/4x / 4x`, KD student는 성능 미확정이면 `1x / 1x / 1x`와 `TBD`를 함께 둡니다.
- 표 제목이나 본문에 `추가 생성 chip 데이터 기반 PoC`만 단독으로 쓰지 않습니다. 필요하면 **[현업 defect chip 원천 + 도메인 확률분포 기반 생성/검증]**으로 씁니다.
- `bit_F1 0.9927 / Total FAR 0.00%`(portfolio.md 정본)는 현업 defect 원천과 도메인 생성 평가셋 위에서 FCM-PM 구조가 2-combo 학습 신호와 false alarm 억제를 만든 검증 지표로 씁니다. 추천서 본문에서는 방어적 한계 설명을 반복하지 말고, 단순 생성 PoC보다 높은 수준의 방법론 검증으로 다룹니다.
- **★★★★ data leakage 방지 chip 단위 split 문장 필수 (사용자 직접 명시 2026-05-16)**: P2 §데이터 또는 §수행 업무 본문에 "single defect chip 원천을 chip 단위로 먼저 train / test 로 split 한 뒤, 2-combo 와 Pair Mask 합성은 train 원천 chip 만 사용했고, test 원천 chip 은 합성 과정에서 완전히 배제했다" 식 한 줄을 반드시 박는다. 이 문장이 없으면 면접 / 사후 검증에서 train ↔ test 누수 의심에 약해진다.
- **★★★★ ablation 핵심 메시지**: 표 직후 narrative 에 "Focal / ASL 처럼 loss 만 바꾸는 접근도, 단순 CutMix 도 본 과제 Grade 0-7 양자화 chip 이미지에서는 부족했고, 결정적 두 축은 defect coverage 보장 (Full-Cover Mixup) 과 합성 background 의 loss 분리 (Pair Mask) 다. 이 두 축을 한 학습 구조에 결합한 것이 FCM-PM" 톤을 한 단락 박는다.
- **외부 학회 / 박사논문 비교 / 학술 venue 톤 본문 금지 (Rule 1 보강)**: "KDD ADS", "AAAI IAAI", "WACV", "IEEE TSM", "ASMC", "박사논문급" 같은 외부 학술 venue / 비교 표현은 본문에 쓰지 않는다. 사내 지원서 톤 유지. 외부 논문화는 별도 트랙.
- **누수 의심 6 항목 점검표** (편집 시 매번): (1) chip 단위 split 무결성, (2) 2-combo 생성 방식 train / test 차이, (3) Normal / Invalid / OOD 가 너무 쉬운 negative 인지, (4) FAR 0 이 threshold 과도 인지, (5) class 별 n=2000 이 독립 sample 인지 augmentation copy 인지, (6) run116J val_margin 이 test 에 맞춘 것 아닌지. 본문에서 직접 또는 간접 반증되어야 함.

| # | Recipe | bit_F1 | single | 2combo | FAR | NI-FAR | OOD-FAR | Latency | Throughput | Params | Note |
|---|--------|--------|--------|--------|-----|--------|---------|---------|------------|--------|------|
| 1 | Baseline (BCE+LS=0.30, no cutmix) | 0.1093 | 0.1896 | 0.0668 | 99.47 | 99.65 | 98.91 | 1x | 1x | 1x | ladder BG |
| 2 | Focal loss (T9 sigmoid_focal, no cutmix) | 0.7980 | 0.8724 | 0.7050 | 45.72 | 35.55 | 77.50 | 1x | 1x | 1x | ladder BG |
| 3 | ASL (T4 asymmetric, no cutmix) | 0.6435 | 0.5379 | 0.7320 | 100 | 100 | 100 | 1x | 1x | 1x | ladder BG |
| 4 | CutMix only (random rect, no pair) | 0.9359 | 0.9566 | 0.9070 | 42.05 | 37.00 | 57.81 | 1x | 1x | 1x | ladder BG |
| 5 | CutMix + Pair (random rect + masked) | 0.9491 | 0.9728 | 0.9281 | 24.62 | 21.55 | 34.22 | 1x | 1x | 1x | ladder BG |
| 6 | FCM-PM best val_f1 | 0.9652 | 1.0000 | 0.9517 | 0.15 | 0.00 | 0.62 | 1x | 1x | 1x | val_f1 best |
| 7 | FCM-PM best val_margin (채택) | 0.9927 | 0.9996 | 0.9871 | 0.00 | 0.00 | 0.00 | 1x | 1x | 1x | portfolio 정본 단일 SOTA |
| 8 | Ensemble (vote_majority_bits 5-way) | 0.9956 | 1.0000 | 0.9921 | 0.00 | 0.00 | 0.00 | 5x | 1/5x | 5x | teacher / 상한 |
| 9 | KD distill (single student) | 0.9799 | 1.0000 | 0.9638 | 0.00 | 0.00 | 0.00 | 1x | 1x | 1x | deployable student 후보 |

### Rule 10: 다이어그램은 텍스트 (이미지 새로 생성 X)
- workflow / architecture flow 는 ASCII 또는 텍스트 박스
- 너무 단순하게하지마라 자세하게 만들고 어떻게 성능올렸는지와 성능올린 방식 초보자도 이해할 수 있게 작성
- 새 이미지 생성 시도 금지 ("이미지는 잘 못 만드네" — 사용자 평가)


### Rule 16: fail-map vs mapviewer 역할 분리 + 사내 인프라 노출 금지
- **fail-map** = FBM 이미지 데이터 **생성** 파이프라인 (Cython 100x, palette PNG, positions JSON, 이중 원천 병렬 처리).
 (`positions_module.py` / `cython_functions.pyx` / palette 생성).
- **web app** = FBM 이미지 **뷰어/검색** 시스템 (Vanilla JS + FastAPI + pyvips). commits 수가 많아도 본인 ownership 으로 과장하지 말고 "운영 뷰어 기여" 톤으로 조절. 면접에서 commit 비중 검증 시 위험.


### Rule 15: 팀 에이전트 4 분리 (사용자 첫 메시지 명시)
1. **Master Orchestrator**: 모든 것 관장 + 최종 승인 (메인 thread)
2. **지원서 작성 agent**: .md 작성/수정
3. **냉정한 평가 심사위원 agent**: 부족 점 지적 + 합격률 추적
4. **자료조사 agent**: 폴더별 독립 병렬 + **이미지 분석 에이전트** 포함

이미지 분석 에이전트 (자료조사 하위):
- 실제 이미지 찾고 복사
- 추천서 삽입 위치 결정
- 캡션 작성

## 사용자 핵심 평가 메시지 (영구 박을 anchor)
> "회사에서는 반도체 역량을 AI 에 어떻게 적용해서 현업 문제 개선을 해내나 그걸 합격으로 볼 것이다. AI 기술 역량 뛰어난 것도 물론이고."
