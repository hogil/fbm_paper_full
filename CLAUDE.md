# 사내 AI Specialist 추천서 작성 절대 규칙

## 작업 정의
- **목적**: 사내 AI Specialist 추천 서류 (Word 변환 예정 .md)
- **출력**: `D:/project/fbm_paper/recommendation/ai_specialist.md`
- **본질**: **사내 지원서 (논문 아님)** — 임원에게 직접 보고하는 형식

## 절대 규칙

### Rule 1 (최우선): 논문이 아닌 지원서다
- 학회 인용 (CVPR/ICCV/NeurIPS/arXiv/et al.) 본문에 금지
- "N1-N9 contributions" / "paper integrity" / "retract" / "84-iteration cycle" 같은 논문 운영 표현 금지
- "본 논문" / "투고" / "학술" 표현 금지 (단, Executive Summary 에서 "본 추천서는 학술 논문이 아닌 운영 시스템 보고서" framing 1회만 OK)
- 기법명 자체 (ConvNeXtV2, CutMix, HDBSCAN 등) 는 한글 + 영문 병기로 유지

### Rule 2: 톤 = 임원 보고 + 존댓말
- 종결구 `~합니다 / ~입니다 / ~했습니다 / ~드립니다 / ~됩니다`
- 본인 호칭: "본인"
- 표 / 코드 / ASCII 다이어그램 / 부제목은 평어 유지

### Rule 3: 합격 평가 기준 (사용자 명시)
> **"반도체 역량 → AI 적용 → 현업 문제 개선"**
> 
> AI 기술 역량은 필수 조건이지만 결정적 차별성은 위 3-step 인과 chain.

이 메시지는 Executive Summary / 강점 #1 / 결론 3곳에 echo.

### Rule 4: 3개 프로젝트 구조
1. **P1**: FBM(Fail-Bit Map) 이미지 데이터 생성 + Known-CNN 2-stage 분류 + Unknown-contrastive 검출
2. **P2**: Chip multi-label classification (CutMix → FCM-PM 신기법 + best-margin + temperature 등)
3. **P3**: Anomaly-detection (도메인 지식 기반 episode 합성 + noise 3종 매핑 + 4종 불량)

### Rule 5: 본인 기여도 (★ 사용자 정정, 최종 ★)
- **P1**: 본인 **70%** / 현업 엔지니어 (아이디어 발의 및 불량 분석 교육) **20%** / 관리자 매니징 **10%**
- **P2**: 본인 **90%** / 관리자 매니징 **10%**
- **P3**: 본인 **90%** / 관리자 매니징 **10%**

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

### Rule 8: 추천서 구조 (필수 sub-section)
1. 표지 (성명/부서/입사/13년차/학력/추천 분야)
2. Executive Summary
3. 경력 기술서 (보유 기술만 — 향후 계획 X, "도메인×AI 융합"은 기술 아님 X)
4. AI 주요 과제 요약 (3개 한 표)
5. 포트폴리오 (관리/설계/개발 비중 %)
6. 대표 과제 상세 기술서 × 3 (각 6 sub: 기본정보 / 참여 인력 / 개인 기여 / 문제 정의 / 기술 해결 / 구현 성과)
7. 종합 평가
8. 부록

### Rule 9: 사업부 채택 표현 (정확)
- **DRAM 전제품 라인 운영** + **PoC AI 모델 개발 중**
- "Flash YE" 표현 금지 (사용자 정정)
- "DRAM YE 팀장 의뢰" 는 2022 과제 발의 시점 역사적 사실로 유지 OK

### Rule 10: 다이어그램은 텍스트 (이미지 새로 생성 X)
- 기존 hybrid_fig 6개 (./figures/) 만 활용
- workflow / architecture flow 는 ASCII 또는 텍스트 박스
- 새 이미지 생성 시도 금지 ("이미지는 잘 못 만드네" — 사용자 평가)

### Rule 11: 잘못 박은 표현 (영구 금지)
- "overlay bit data 분석" — 논문에 없는 표현. **"Photo BBD/Overlay 측정·분석"** 으로 통일
- "wafer bit map (grade 0-7 + BIN) 의미 사전 인지" — 본인 photo 경력에 없는 표현. **"Failbit Map 의미 인지 (인접 부서 협업으로 자연 인지)"** 또는 **"본 과제 시작 시점에 현업 사용자로부터 수개월간 학습"**
- "도메인 × AI 융합" — 기술 분류표에 들어갈 항목 아님. 강점 narrative 에서만 사용
- "향후 계획 LLM / 강화학습 ▲" — 보유 기술표에 들어갈 항목 아님
- "Top 1 강점" / "★ 핵심 표 N ★" 같은 자기홍보 / 강조 인플레이션 — 학술 톤으로 정제

### Rule 12: 작업 진행 패턴
- 사용자 추가 정보 / 정정 → 즉시 반영 + push (commit 1회 / 사이클)
- 각 사이클: 자료조사 → draft/revise → 심사위원 검토 → 합격률 추적
- 자료조사 에이전트는 폴더별 독립 병렬 (서로 보지 말 것)
- 학술 인용 다수 금지 — 핵심 기법만 (사용자 평가: "추천서는 논문이 아니다 핵심 기법만")

### Rule 13: 이미지 활용 규칙 (★★ 사용자 절대 명시 ★★)

**Absolute Rule (위반 시 즉시 정정)**:
> "chip map이나 wafer map은 절대로 생성하지마라"
> "E:/data/images 여기서 가져와서 쓰는거다"

#### 13.1 Chip / Wafer 이미지 = E:/data/images 절대경로 직접 참조
- **합성 wafer 이미지**: `E:/data/images/unknown/<class>/*.png`
  - `Center_fork`, `Edge-Ring_bank_boundary`, `Donut_scratch`, `CrossScratch`, `Starburst`, `CenterDonut` 등 wafer-class 폴더
- **chip 단일 이미지**: `E:/data/images/classification_chips/<obj>/*.png`
  - `bank_boundary`, `fork`, `scratch`, `scratch_rot`, `invalid_main`
- **chip multi-label 평가**: `E:/data/images/chip_multilabel_v15direct/<class>/*.png`
  - single + 2-combo (`bank_boundary+fork`, `fork+scratch` 등) + Normal + Invalid + OOD (`Starburst`, `CenterDonut`, `CrossScratch`, `DiagonalSmear`)
- **chip multi-label mega eval**: `E:/data/images/chip_multilabel_mega_eval_n200/<class>/*.png`
  - 3-combo 까지 포함 (`bank_boundary+fork+scratch` 등)

#### 13.2 절대 금지
- **chip map / wafer map 새로 생성 절대 금지** (Python plot / matplotlib / PIL 등 어떤 방법으로도 X)
- **D 드라이브로 복사 금지** (D 가 100% 가득 참, 그리고 사용자가 "E 에서 가져와서 쓰는 거다" 명시)
- **manager_report 의 figs / heatmap / preview 등 보조 이미지를 wafer/chip 대체로 사용 금지**
- **이미지 파일 절대 삭제 금지** (★ 사용자 직접 명시: "이미지는 절대로 지우지마라")
  - 예외: 사용자가 특정 이미지를 직접 지시하여 삭제 요청한 경우만

#### 13.6 ★ hybrid_fig 6장 사용 절대 금지 ★
사용자 직접 명시 (이미지 6장 보여주며): **"이것들은 지우고 다시는 쓰지 마"**
- 금지: `hybrid_fig1_overview.png` / `hybrid_fig2_distribution.png` / `hybrid_fig3_matching.png` / `hybrid_fig4_flowchart.png` / `hybrid_fig5_zoomed_example.png` / `hybrid_fig6_confusion_pairs.png`
- 추천서 어떤 형식으로도 참조 X
- 이미 figures/ 에서 삭제됨
- 도식 대용 = ASCII 다이어그램 + 실제 wafer 이미지 (E:/data/images/unknown/)

#### 13.3 추천서에 삽입 방식
- 마크다운: `![캡션](E:/data/images/unknown/Center_fork/<filename>.png)`
- 또는 `<img src="E:/data/images/.../*.png" />` HTML
- Word 변환 시 절대경로 그대로 (사용자가 처리)

#### 13.4 다이어그램 / Workflow / Architecture Flow
- **텍스트(ASCII) 시각화** (이미지로 만들지 X)
- 사용자 평가: "이미지는 잘 못 만드네" — 새 이미지 생성 시도 절대 금지

#### 13.5 이미지 분석 에이전트 역할
- `E:/data/images/` 폴더 탐색해서 적절한 wafer / chip 이미지 식별
- 추천서 삽입 위치 결정 + 캡션 작성
- **복사 금지, 절대경로 직접 참조**

### Rule 14: 기술적 해결 방안 표현 규칙 (사용자 첫 메시지 명시)
사용자 첫 메시지 원문:
> "실제 코드를 제외한 **아키텍쳐 설계도, 플로우 차트 등으로 기술**"

- §6.X.4 (기술적 해결 방안) 에서 **실제 코드 인용 금지**
- 아키텍처 설계도 / 플로우 차트 / 의사결정 트리 = **텍스트 박스 / ASCII 다이어그램 / 표** 로 시각화
- Logic flow 중심 (코드 라인 X)
- 예시:
  ```
  [Input wafer] → [Stage 1: wafer-level CNN]
                    ↓ confidence < τ_gate
                  [Stage 2: chip-level CNN]
                    ↓
                  [obj_id map → G channel]
                    ↓
                  [Compound CNN → 33-class]
  ```

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

이게 본 추천서 평가의 메인 기준. 모든 결정은 이 메시지로 정렬.

---

## 사용자 첫 메시지 원문 (영구 보존, 빠짐없이)

> 자 사내 ai specialist 추천 서류를 작성할거다
>
> 총 3개 프로젝트 할거고
> 1. 현재 논문에도 나와있는 이미지 데이터 생성 및 known-cnn 2stage 그리고 unkown-contrastive
> 2. multi label classification- 이미지 cut mix부터 fcmpm    bestmodel margin 확정방식     temp 등 특히 새로운 방식들 만들어서 진행해나가는
> 3. anomaly-detection 이거는 데이터 생성에 주를 이루자 뒤에는 너무 식상하니까 domain kowlegde로 trend를 episode 방식으로 만들고 anomaly 값도 실제 불량 발생방식들 넣고
> noise 3종류 각각 설비 상태변동 산포 spike 에 매칭되는 것들 등 설명
>
> 팀 에이전트로 할거고
>
> 1. maser orchestrator
> 모든 것을 관장하고 이상 없는 지 확인하며 최종 승인한다
>
> 2. 지원서작성 agent
> .md 파일로 만들면 내가 word로 옮길게
> 경력 기술서 - 기술 분야     comuter vision llmnlp  강화학습 머신러닝 ai시스템 인지니어링 파이프라인구축 모델 최적화 등
>
> ai 주요 과제
>
> -과제명
> 과제 개요 및 규모 담당 역할 수행 업무 성과(정량지표 권장)
> 과제 관련 도메인 ai 기술 모델 방법론 등
>
> -포트폴리오
> ai 프로젝트 수행 전체이력
> 각 프로젝트별로
> 기간, 내용(과제명 리딩 규모 담당업무 과제관리, 설계 개발비중:
>
> 대표 과제 상세 기술서
> 나는 3개 프로젝트니까 다 적으면되는데
> 과제 기본정보(과제명:   수행기간:
>
> 과제 차며 인력 및 역할( 참여일력 구성 및 기여도)
>
> 개인별 기여 서술(본인이 독자적으로 수행한 핵심 모듈, 과제내에서 타 구성원과 차별되는 본인만의 구체적 담당영역, 본인의 기술적 해결책이 과제 성패에 미친 영향
> 문제정의 ( 현장 난제 및해결 목표, 기존 방식의 한계 및 ai 도입의 구체적 배경, 과제 수행 시 해결해야해썬 기술적 / 환경적 제약 조건
>
> 기술적 해결 방안( 본인이 직접 수행한 핵심 로직, 데이터 데이터 수집경로, 전처리 기법 및 피처엔지니어링 근거, 알고리즘 선정한 모델 아키텍쳐와 선택 사유(logicc flow 중심), 최적화 : 성능 향상을 위해본인이 직접 시도한 기술적 해법)
> **실제 코드를 제외한 아키텍쳐 설계도, 플로우 차트 등으로 기술**
>
> 구현성과(정량적/정성적 성과, 기술지표 모델 정확도 향상 추론속도 개선 등,       현업 임팩트 수율향ㅇ상 불량률 감소 tat 단축 등 실제 기여도)
>
> 심사위원 에이전트에게 전달하고 피드백 받고
> 자료조사 에이전트를활용해서 계속 자료들을 조사받아라
>
> 3. 냉정한 평가 심사위원 에이전트
> 너는 지원자들을 평가하는 에이전트로 부족한 점을 계속 지적해서 지원서 작성 agent에게 피드백해줘
>
> 4. 자료조사 에이전트
> 너는 아래의 파일과 폴더들읠 계속해서 조사해서 지원서 작성 agent에게 전달해줘
>
> 현재 프로젝트 폴더의 내용과
>
>   [OUT] D:/project/unknown-contrastive/docs/paper/manager_report/SUMMARY.md
>   [OUT] D:/project/unknown-contrastive/docs/paper/manager_report/cross_anchor_eval_260514.md
>   [OUT] D:/project/unknown-contrastive/outputs_contrastive_260514_001210/eval_E/eval_summary.json
>   [OUT] https://github.com/hogil/unknown-contrastive (commits 9c1873e, 0be76bf)
>
>  [OUT] D:/project/known-cnn/docs/chip-multilabel/manager_report/REPORT_beginner.md
>   [OUT] https://github.com/hogil/known-cnn/commit/3f3490e
>
>   [OUT] D:/project/known-cnn/docs/paper/figures/hybrid_fig1_overview.png
>   [OUT] D:/project/known-cnn/docs/paper/figures/hybrid_fig2_distribution.png
>   [OUT] D:/project/known-cnn/docs/paper/figures/hybrid_fig3_matching.png
>   [OUT] D:/project/known-cnn/docs/paper/figures/hybrid_fig4_flowchart.png
>   [OUT] D:/project/known-cnn/docs/paper/figures/hybrid_fig5_zoomed_example.png
>   [OUT] D:/project/known-cnn/docs/paper/figures/hybrid_fig6_confusion_pairs.png
>   [OUT] D:/project/known-cnn/docs/paper/02_method.md
>   [OUT] D:/project/known-cnn/docs/paper/00_abstract.md
>   [OUT] D:/project/known-cnn/docs/paper/CHANGELOG.md
>   [OUT] D:/project/known-cnn/hybrid_match/_paper_fig_hybrid.py
>
> D:\project\known-cnn D:\project\mapviewer D:\project\unknown-contrastive D:\project\anomaly-detection D:\project\fail-map D:\project\fbm_paper
> 이폴더들 ㅊ마조

위 첫 메시지는 본 작업의 절대 사양이다. 어떤 항목도 빠뜨리지 말 것.
