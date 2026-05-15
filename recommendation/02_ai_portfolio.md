## 1. AI 프로젝트 수행 전체이력

| 기간 | 내용(과제명) | 리딩 규모 | 담당업무 | 과제관리 | 설계 | 개발비중 |
|------|--------------|-----------|----------|----------|------|----------|
| 2024년 10월 ~ 현재 | P1. Failbit Map Known & Unknown 불량 분석 아키텍처 | 3인 협업, 본인 60% 담당<br>DRAM 전제품 라인<br>일 약 2만 장 wafer 운영 데이터 | S3 수집, Cython / Python 파싱, palette PNG 및 chip 좌표 JSON 생성, Web App 운영, Known / Unknown 모델 설계 및 검증 | 10% | 40% | 50% |
| 2025년 3월 ~ 현재 | P2. Chip Multi-label Classification | 2인 PoC, 본인 80% 담당<br>16+ class<br>약 3,850 chip 통제 합성 평가셋 | FCM-PM 합성 구조, loss masking, val_margin 모델 선택 기준, multi-label 학습 및 평가 운영 | 20% | 40% | 40% |
| 2026년 1월 ~ 현재 | P3. Domain Knowledge 기반 Trend Anomaly 데이터 생성 및 불량 검증 | 2인 PoC, 본인 80% 담당<br>총 7,000 sample<br>normal 3,500 + 불량 5종×700 | Domain Knowledge 기반 trend episode generator 설계, Region / Noise / trend 불량 rule 코드화, AI 기준 모델 fine-tuning 및 성능 검증 | 5% | 55% | 40% |

## 2. 대표 과제 상세 기술서

**ㅁ P1. Failbit Map Known & Unknown 불량 분석 아키텍처**

**ㅁ 과제 기본정보**

| 항목 | 내용 |
|------|------|
| 과제명 | Failbit Map Known & Unknown 불량 분석 아키텍처 |
| 수행기간 | 2024년 10월 ~ 현재 |
| 참여인원 | 본인 / 현업 엔지니어 / 관리자 |

**ㅁ 과제 참여 인력 및 역할**

| NO | 성명 | Knox Id | 소속 | 역할 | 기여도 |
|----|------|---------|------|------|--------|
| 1 | 본인 | 공식 과제기록 기준 | 공식 과제기록 기준 | 서버 환경 구축, 데이터 처리, Web App 운영, Known / Unknown 모델 설계, 개발 및 검증 | 60% |
| 2 | 현업 엔지니어 | 공식 과제기록 기준 | 공식 과제기록 기준 | 현업 문제정의 및 불량 분석 교육 | 20% |
| 3 | 관리자 | 공식 과제기록 기준 | 공식 과제기록 기준 | 방향성, 일정 및 리뷰 매니징 | 20% |

**ㅁ 개인별 기여 서술**

[본인이 독자적으로 수행한 핵심 모듈]

- 과제 안에서 타 구성원과 차별화되는 본인만의 구체적 담당영역: 현업 엔지니어가 불량 기준과 판독 기준을 정리하면, 본인은 설비 raw log 를 Web App 과 모델이 바로 쓸 수 있는 Failbit Map 이미지, chip 좌표 JSON, palette PNG 로 변환하는 흐름을 맡았습니다. 이후 Known 2-stage 분류, Unknown 후보 검출, chip-CNN 기반 object-id map(chip 위치별 불량 chip id로 제작한 map) 확장 구조까지 직접 설계했습니다.
- 본인의 기술적 해결책이 과제 성패에 미친 영향: raw log 를 매번 수작업으로 확인하던 흐름을 1시간 주기 자동 적재와 Web App 조회 구조로 바꾸고, map-level 판단이 흔들리는 class 는 ROI YOLO 로 chip 단위 근거를 다시 보게 했습니다. Unknown 쪽은 위치 정보가 사라지지 않도록 6×6 local sampling 과 Local InfoNCE 를 넣어 현업 검토 후보로 올릴 수 있는 수준까지 만들었습니다.

**ㅁ 문제정의**

| 항목 | 내용 |
|------|------|
| 현장 난제 및 해결 목표 | Failbit Map 은 wafer 당 약 1,000만 개 block 의 Grade 0~7 값을 가지는 초고해상도 데이터입니다. 수율, BIN(불량 bin 분류), FTN/QTN(검사 요약 지표) 같은 Measure 요약값만으로는 불량의 위치, 형상, 밀집도, 방향성을 확인하기 어려워, map 기반 전수 분석과 AI 후보 검출이 필요했습니다. |
| 기존 방식의 한계 및 AI 도입 배경 | 기존 방식은 요청 시점에 raw log 를 받아 변환하는 온디맨드 방식에 가까웠고, 전 제품 기준 일 약 2만 장 wafer 를 사람이 직접 확인하기 어려웠습니다. 또 center scratch / center scratch_rot 처럼 전체 map 만 보면 헷갈리는 class 가 있어 chip 단위 근거를 같이 확인해야 했습니다. |
| 기술적 / 환경적 제약 조건 | 1시간 주기 자동 적재, wafer 당 약 1,000만 grade 변환, 이미지 저장 용량, Web App 응답성, 16 class / 1,500 labeled sample 의 label 부족, low-confidence Known class 보정, 등록 class 밖 Unknown 후보 검출을 동시에 해결해야 했습니다. |

**ㅁ 기술적 해결 방안**

[본인이 직접 수행한 핵심 로직]

- 데이터 : EDS Test raw log 를 S3 적재 경로에서 수집하고, 압축 해제 후 Cython 기반 hex-to-grade 변환으로 Grade 0~7 Failbit Map 을 만들었습니다. 제한된 색상 체계라는 데이터 특성을 이용해 32-color palette PNG 로 저장 용량을 줄였고, chip 좌표 JSON 을 함께 생성해 Web App, 모델 입력, object-id map 재구성에서 같은 좌표계를 쓰도록 했습니다.
- 알고리즘: wafer 전체 분포는 ConvNeXtV2 task-specific fine-tuning 모델로 1차 판단하고, 저신뢰 또는 혼동 class 는 ROI YOLO 2-stage 로 chip 단위 defect box 와 class 를 다시 확인했습니다. 등록 class 밖 패턴은 self-supervised embedding, 6×6 grid local sampling, Local InfoNCE, HDBSCAN 순서로 후보화했습니다.
- 최적화: 변환 병목은 Cython 으로 줄이고, 저장 병목은 palette PNG 로 줄였습니다. 모델 쪽은 ConvNeXtV2 / MaxViT 비교 후 운영 부담이 낮은 ConvNeXtV2 를 선택했고, 모델 설정값 튜닝, focal loss / class weight 조정, confidence gate, ROI YOLO 보정, Local InfoNCE 를 직접 적용했습니다.

ㅁ 실제 코드를 제외한 아키텍쳐 설계도, 플로우차트 등으로 기술

```
[EDS Test raw log]
        ↓
[S3 적재 / 압축 해제]
        ↓
[Cython hex-to-grade 변환 + palette PNG + chip 좌표 JSON]
        ↓
[Web App 조회 / 비교 / 현업 검토]
        ↓
[Stage 1: ConvNeXtV2 wafer classifier]
        ↓ low confidence or confusion class
[Stage 2: ROI YOLO chip evidence 확인]
        ↓
[Known class 보정]
        ↓
[Unknown: global embedding + 6×6 local sampling + Local InfoNCE]
        ↓
[HDBSCAN 후보 grouping]
        ↓
[chip-CNN → object-id map 기반 후속 보정 구조]
```

| ROI YOLO 보정 예시 | object-id map 비교 예시 |
|:------------------:|:-----------------------:|
| <img src="./figures/p1_known_roi_yolo_real.png" width="360" /> | <img src="./figures/p1_wafer_center_scratch_obj.png" width="170" /> <img src="./figures/p1_wafer_center_scratch_rot_obj.png" width="170" /> |

**ㅁ 구현 성과**

[정량적/정성적 성과]

- 기술 지표: [실전 현업 라벨 데이터] Known 2-stage 는 16 class / 1,500 labeled samples / 평가용 hold-out set 기준 weighted F1 0.95 입니다. [양산 운영] Cython hex-to-grade 변환으로 처리 속도는 기존 Python 대비 약 100배 빨라졌고, 32-color palette PNG 적용 후 저장 용량은 약 75% 줄었습니다. [추가 생성 데이터, 개발 중] Unknown 후속 평가는 same-anchor defect-class capture 43/43, ARI 0.859±0.018, Completeness 0.994, Homogeneity 0.942 수준입니다.
- 현업 임팩트: DRAM 전제품 라인에서 일 약 2만 장 wafer 를 1시간 주기로 적재했고, Web App 은 12일 누적 2,317 요청까지 사용되었습니다. Unknown 은 [실전 현업 데이터] 5일 10,000장 학습 + 별도 1일 2,000장 적용 결과 13개 후보 중 7개 실제 불량을 현업이 확인했습니다. 이 값은 F1 같은 정량 metric 이 아니라, 신규 후보를 현업 검토 대상으로 압축한 운영 확인 결과입니다.

**ㅁ P2. Chip Multi-label Classification**

**ㅁ 과제 기본정보**

| 항목 | 내용 |
|------|------|
| 과제명 | Chip Multi-label Classification |
| 수행기간 | 2025년 3월 ~ 현재 |
| 참여인원 | 본인 / 관리자 |

**ㅁ 과제 참여 인력 및 역할**

| NO | 성명 | Knox Id | 소속 | 역할 | 기여도 |
|----|------|---------|------|------|--------|
| 1 | 본인 | 공식 과제기록 기준 | 공식 과제기록 기준 | FCM-PM 합성 구조, loss masking, val_margin 기준, KD 압축 검토, 학습 및 평가 운영 | 80% |
| 2 | 관리자 | 공식 과제기록 기준 | 공식 과제기록 기준 | 방향성, 일정 및 리뷰 매니징 | 20% |

**ㅁ 개인별 기여 서술**

[본인이 독자적으로 수행한 핵심 모듈]

- 과제 안에서 타 구성원과 차별화되는 본인만의 구체적 담당영역: 실제 운영 환경에서는 multi-label 불량 조합 label 을 충분히 모으기 어렵기 때문에, 본인은 확보 가능한 single-label defect chip 을 조합해 multi-label 학습 샘플을 만드는 FCM-PM(Full-Cover Mixup + Pair Mask) 구조를 설계했습니다.
- 본인의 기술적 해결책이 과제 성패에 미친 영향: 일반 CutMix 만 쓰면 불량 영역이 잘리거나 배경이 defect 로 학습되는 문제가 있어, chip 전체를 덮는 Full-Cover Mixup 과 배경 loss 를 제외하는 Pair Mask 를 같이 적용했습니다. 이 구조 덕분에 multi-label 조합 학습과 Normal / Invalid / OOD 오탐 검증을 같은 평가 흐름 안에서 볼 수 있었습니다.

**ㅁ 문제정의**

| 항목 | 내용 |
|------|------|
| 현장 난제 및 해결 목표 | 현장에는 single-label 불량 chip 은 비교적 쌓이지만, 두 개 이상 불량이 한 chip 안에 같이 들어간 multi-label label 은 의도적으로 모으기 어렵습니다. 목표는 single-label chip 을 기반으로 multi-label 조합을 만들고, 조합 안의 각 single class 를 빠짐없이 맞히도록 학습 및 검증하는 것입니다. |
| 기존 방식의 한계 및 AI 도입 배경 | single-label 불량을 단순 조합하면 defect 위치를 사전에 모르는 문제가 남습니다. 일반 CutMix 는 일부 영역만 잘라 붙이므로 불량 신호가 잘릴 수 있고, 합성 background 영역까지 defect 로 학습하면 Normal / Invalid / OOD 오탐이 늘어납니다. |
| 기술적 / 환경적 제약 조건 | single-label 기반 multi-label 조합 생성, chip 내부 defect 위치 사전 미지, 작은 검증셋, OOD 및 Normal / Invalid 오탐 억제, KD 단일 모델 압축 시 성능 저하 가능성을 함께 관리해야 했습니다. |

**ㅁ 기술적 해결 방안**

[본인이 직접 수행한 핵심 로직]

- 데이터 : multi-label chip label 대신 확보 가능한 single-label defect chip 을 원천 데이터로 사용했습니다. Grade 0~7 양자화 값이 불량 의미를 가지므로 픽셀값을 섞는 Mixup / Diffusion 계열보다, 원래 Grade 값을 보존하는 CutMix 계열을 기본 합성 방식으로 선택했습니다.
- 알고리즘: 판단 흐름은 `single-label chip 확보 → multi-label 조합 생성 → 조합 안의 각 single class 예측 → Normal / Invalid / OOD 오탐 확인`입니다. 일반 CutMix 한계를 줄이기 위해 chip 전체 grid 를 cover 하는 Full-Cover Mixup 을 적용했고, 합성 background 영역은 Pair Mask 로 loss 에서 제외했습니다.
- 최적화: 작은 검증셋에서는 val_f1 만으로 모델 저장 시점을 고르기 어려워, 정답 score 평균과 오답 최고 score 사이의 여유를 보는 val_margin 을 추가했습니다. FCM-PM 구성요소 제거 비교, 4-bag ensemble, KD student 모델 비교로 오탐 안정성과 추론 비용 절감 가능성을 같이 확인했습니다.

ㅁ 실제 코드를 제외한 아키텍쳐 설계도, 플로우차트 등으로 기술

```
[single-label defect chip]
        ↓
[Grade 0~7 보존을 위해 CutMix 계열 선택]
        ↓
[Full-Cover Mixup: chip 전체 grid cover]
        ↓
[Pair Mask: 합성 background loss 제외]
        ↓
[multi-label classifier 학습]
        ↓
[val_margin 기준 모델 선택]
        ↓
[Normal / Invalid / OOD 오탐 평가]
        ↓
[4-bag ensemble 및 KD student 비교]
```

| raw A | raw B | 2-combo |
|:-----:|:-----:|:-------:|
| <img src="./figures/chip_eval_bank_boundary_selected.png" width="130" /> | <img src="./figures/chip_eval_scratch_selected.png" width="130" /> | <img src="./figures/chip_combo_bb_scratch_selected.png" width="130" /> |

**ㅁ 구현 성과**

[정량적/정성적 성과]

- 기술 지표: [추가 생성 chip 데이터, PoC] single 4 + 2-combo 6 + Normal + Invalid + OOD 4 로 16+ class × 약 3,850 chip 통제 합성 평가셋을 만들었습니다. FCM-PM 대표 모델은 기존 요약 평가셋 기준 bit F1 0.9943, Normal / Invalid / OOD 오탐 0건이었습니다. per-class 2,000 갱신 평가에서는 bit F1 0.9964, Total FAR 0.83% 로 나왔고, 4-bag ensemble 은 bit F1 0.9909, Total FAR 0.00% 로 오탐 안정성을 확인했습니다.
- 현업 임팩트: single-label defect chip 만으로 multi-label 조합 학습과 검증을 시작할 수 있는 방법을 만들었습니다. Full-Cover Mixup 과 Pair Mask 구성요소 제거 비교에서는 일부 변형이 Total FAR 100.00% 로 실패했고, 이 결과를 보고 FCM-PM 조합을 유지했습니다. 아직 운영 적용 전 PoC 단계라 수율, 불량률, 검토 시간 개선 수치는 분리해 관리하고 있습니다.

**ㅁ P3. Domain Knowledge 기반 Trend Anomaly 데이터 생성 및 불량 검증**

**ㅁ 과제 기본정보**

| 항목 | 내용 |
|------|------|
| 과제명 | Domain Knowledge 기반 Trend Anomaly 데이터 생성 및 불량 검증 |
| 수행기간 | 2026년 1월 ~ 현재 |
| 참여인원 | 본인 / 관리자 |

**ㅁ 과제 참여 인력 및 역할**

| NO | 성명 | Knox Id | 소속 | 역할 | 기여도 |
|----|------|---------|------|------|--------|
| 1 | 본인 | 공식 과제기록 기준 | 공식 과제기록 기준 | Domain Knowledge 기반 trend episode generator 설계, Region / Noise / trend 불량 type 코드화, AI 기준 모델 fine-tuning 및 성능 검증 | 80% |
| 2 | 관리자 | 공식 과제기록 기준 | 공식 과제기록 기준 | 방향성, 일정 및 리뷰 매니징 | 20% |

**ㅁ 개인별 기여 서술**

[본인이 독자적으로 수행한 핵심 모듈]

- 과제 안에서 타 구성원과 차별화되는 본인만의 구체적 담당영역: 본인은 BBD(현업 trend 항목) / Overlay(정렬 계측) / CD(선폭 계측) 업무에서 보던 결핍, 희소, 공핍, 얇은 계측 영역을 Region rule 로 만들고, 설비 산포 / hunting / drift 를 noise 조건으로 분리했습니다.
- 본인의 기술적 해결책이 과제 성패에 미친 영향: 실전 abnormal label 이 부족한 상태에서 detector 부터 키우지 않고, 먼저 학습 가능한 trend abnormal 데이터를 만들었습니다. 정상/이상 기준 모델과 5개 불량 유형 분류를 분리해 보면서, 모델 성능보다 생성 규칙과 label 정의를 먼저 보정하는 흐름을 세웠습니다.

**ㅁ 문제정의**

| 항목 | 내용 |
|------|------|
| 현장 난제 및 해결 목표 | trend 이상은 단순 threshold 만으로 판정하기 어렵고, 설비 산포 / hunting / drift / baseline 평탄도 / spec-in 변동 가능성을 함께 봐야 합니다. 목표는 현업 trend 판단 기준을 합성 데이터 생성 rule 로 옮겨, anomaly detector 검증을 시작할 수 있는 데이터 기반을 만드는 것입니다. |
| 기존 방식의 한계 및 AI 도입 배경 | 실전 trend abnormal data 는 충분한 양과 균형 label 을 확보하기 어렵고, 수작업 chart 판독은 누락 가능성과 시간 소모가 큽니다. label 이 부족한 상태에서 detector 를 바로 고도화하면 모델 성능보다 데이터 편향을 먼저 학습할 수 있습니다. |
| 기술적 / 환경적 제약 조건 | 실제 운영 chart 처럼 결핍 영역, 희소 영역, 공핍 영역, 얇은 계측 영역을 반영해야 했고, Gaussian noise(설비 산포), Laplacian noise(hunting), correlation noise(drift)를 구분해야 했습니다. 정상 산포에 묻히는 약한 이상은 최소 anomaly 강도 보정이 필요했습니다. |

**ㅁ 기술적 해결 방안**

[본인이 직접 수행한 핵심 로직]

- 데이터 : normal 3,500 + 불량 5종 각 700 = 불량 3,500, 총 7,000 sample 합성 trend chart 평가셋을 만들었습니다. Region 은 정상 / 희소 / 공핍 / 얇은 계측 / 결핍 영역으로 나누고, Noise 는 Gaussian noise, Laplacian noise, correlation noise 로 분리했습니다.
- 알고리즘: 모델을 먼저 고도화하기보다 `domain knowledge → synthetic generator → 기준 모델 검증 → 생성 rule 보정` 흐름을 선택했습니다. 생성 chart 는 1단계 정상/이상 분류로 구분 신호를 먼저 확인하고, 2단계 5개 불량 유형 분류는 mean_shift / std / spike / drift / context rule 보정에 사용했습니다.
- 최적화: 생성 데이터가 너무 쉬운 문제가 되지 않도록 정상 산포 기준 최소 anomaly 강도를 보정했고, normal chart 가 과도하게 흔들리지 않도록 target_std 를 정상 wafer 내부 산포 범위 안에서 제한했습니다. 유형 혼동이 커지면 모델 구조보다 생성 규칙과 label 정의를 먼저 수정했습니다.

ㅁ 실제 코드를 제외한 아키텍쳐 설계도, 플로우차트 등으로 기술

```
[BBD / Overlay / CD 현업 trend 경험]
        ↓
[Region 5종: 정상 / 희소 / 공핍 / 얇은 계측 / 결핍 영역]
        ↓
[Noise 3종: Gaussian noise / Laplacian noise / correlation noise]
        ↓
[trend 불량 5종: mean_shift / std / spike / drift / context]
        ↓
[정상 산포 기준 최소 anomaly 강도 보정]
        ↓
[224×224 trend chart PNG rendering]
        ↓
[1단계 정상/이상 기준 모델 + 2단계 유형 분류 rule 점검]
```

| Normal | Spike | Drift |
|:------:|:-----:|:-----:|
| <img src="./figures/trend_normal.png" width="150" /> | <img src="./figures/trend_spike.png" width="150" /> | <img src="./figures/trend_drift.png" width="150" /> |

**ㅁ 구현 성과**

[정량적/정성적 성과]

- 기술 지표: [합성 trend chart, PoC] normal 3,500건과 불량 5종 각 700건으로 불량 3,500건, 총 7,000 sample 의 합성 trend chart 평가셋을 만들고 224×224 chart PNG 로 rendering 했습니다. 1단계 정상/이상 분류에서는 Binary F1 0.9967, Abnormal Recall 0.9987, 5개 seed 반복 평가 0.9944~0.9988 이 나왔습니다.
- 현업 임팩트: BBD / Overlay / CD 현업 trend 판단 기준을 synthetic data generator 로 옮겨, 실전 abnormal label 이 부족한 상태에서도 anomaly detector 검증을 시작할 수 있는 데이터 기반을 만들었습니다. 이 수치는 실전 운영 성능이 아니라 생성 rule 이 정상/이상 구분 신호를 담고 있는지 확인한 기준 모델 결과이며, 실제 chart 적용 전 단계입니다.
