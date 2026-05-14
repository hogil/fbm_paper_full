## 1. 기술 분야

| 기술 분야 | 대표 적용 기법 / 방식 |
|-----------|------------------------|
| 반도체 이미지 AI 모델링 | Failbit Map wafer/chip 이미지 분류, ConvNeXtV2 기반 wafer classification, ROI YOLO 2-stage 보정, chip-CNN object-id map 보정 구조 |
| Unknown / Unsupervised Detection | label 없는 신규 defect 후보 탐지를 위한 contrastive representation learning, clustering 기반 후보 grouping |
| Synthetic Data Engineering | wafer-class 생성 평가셋, chip multi-label synthesis, FCM-PM 합성 및 손실 마스킹, trend episode synthesis generator |
| AI 모델 최적화 | Bayesian Hyperparameter Optimization (Optuna), Focal Loss, Label Smoothing, Temperature Scaling, val_margin / best-margin checkpoint selection, Knowledge Distillation |
| Data / MLOps Engineering | EDS Test raw log → S3 → fail-map → mapviewer 적재, FastAPI backend, JavaScript frontend, WebGL2 rendering, RBAC, SAML Single Sign-On |
| High-Performance Image Pipeline | Cython hex-to-grade conversion, pyvips / Numba 기반 이미지 처리, 32-color palette-indexed PNG encoding |

## 2. 업무경력

본인의 결정적 차별성은 **반도체 분석 현장에서 쌓은 이해를 AI 모델 구조와 학습 데이터 생성 체계에 직접 반영해 현업 문제를 개선** 하는 데 있습니다. 아래 3개 과제는 모두 이 기준에 맞춰 수행했습니다.

ㅁ **P1. Failbit Map AI 분류 시스템 (Known 2-stage + Unknown contrastive)**

본 과제는 Failbit Map 데이터 파이프라인부터 Web App, Known 2-stage 분류, Unknown 검출까지 하나의 운영 흐름으로 구성한 시스템 과제입니다.

- 과제 개요 및 규모: DRAM 전제품 라인의 Failbit Map 데이터 파이프라인, mapviewer Web App, Known single-label 2-stage AI 분류기, Unknown self-supervised 검출기 통합 시스템입니다.
- 운영 상태:
  - 데이터 파이프라인 / Web App: **[양산 운영]**
  - Known 2-stage 분류: **[실전 현업 데이터, 검증 완료]**
  - Unknown 검출: **[실전 운영 적용 및 현업 확인]**
  - chip-CNN object-id map 보정 구조: **[추가 생성 데이터, 개발 중]**
- 담당 역할: 본인 70% / 현업 엔지니어 20% / 관리자 10% 입니다.
- 수행 업무: Cython hex-to-grade 변환, 32-color palette-indexed PNG 저장, mapviewer 운영, ConvNeXtV2 backbone 선정 및 hyperparameter optimization, ROI YOLO 2-stage 보정, Unknown self-supervised embedding 및 HDBSCAN grouping, chip-CNN → wafer 좌표계 object-id map 기반 Stage 2 보정 구조 개발을 수행했습니다.
- 성과: **[실전 현업 데이터]** Known weighted F1 **0.95** (16 class / 1,500 labeled samples / 4:1 stratified split) 를 달성했습니다.
- 성과: **[실전 현업 데이터]** Unknown 은 5일 운영 데이터 10,000장 학습 + 별도 1일 운영 데이터 2,000장 적용 결과 13 후보 중 7개 실제 불량을 현업 확인받은 운영 검증 근거입니다.
- 성과: **[양산 운영]** EDS Test → S3 → fail-map → mapviewer 1시간 주기 적재, 일 약 2만 장 wafer 처리, Cython hex-to-grade 약 **100배** 가속, 32-color palette PNG 저장 용량 약 **75%** 절감, 사내 failbitmap 서비스 12일 누적 **2,317 요청** (peak 1,801, 2026-03-07) 을 확인했습니다.
- 보조 개발: **[추가 생성 데이터, 개발 중]** Unknown metric 고도화와 chip-CNN object-id map 보정 구조는 실전 운영 성과와 분리해 후속 고도화로 진행 중입니다.

**과제 관련 도메인 / AI 기술 / 모델 / 방법론**

본 과제 도메인은 Failbit Map, DRAM EDS Test Grade 0-7 양자화 이미지, wafer-level defect zone 해석, 대량 wafer 이미지 양산 운영 파이프라인입니다. 이 도메인 위에 wafer 분류, ROI 보정, unknown 후보 grouping, Web App 운영 흐름을 결합했습니다. 핵심은 AI 모델이 신규 불량 후보를 현업 검토 대상으로 올리고, 엔지니어가 대량 Failbit Map 을 빠르게 조회·비교·확인할 수 있게 만든 점입니다.

Backbone 선정 과정에서는 Transformer 계열이 wafer 전체 구조를 보는 데 강점이 있으나, 본 과제의 결함이 특정 zone 또는 국소 영역에 나타나는 경우가 많다는 점을 고려해 CNN 계열 ConvNeXtV2 의 sliding-window 기반 지역 특징 추출이 더 적합하다고 판단했습니다. 실제 비교 (ViT 0.81 / Swin 0.84 / EffNetV2 0.85 / MaxViT 0.87 / ConvNeXtV2 0.87 / +Optuna 0.92 / +ROI 0.95) 에서 ConvNeXtV2 는 MaxViT 와 동일한 weighted F1 0.87 을 보이면서 파라미터 **26% 감소 (119.5M → 88.6M)** 와 FLOPs **39% 감소 (74.2G → 45.1G)** 로 효율이 높아 최종 backbone 으로 선정했습니다.

ㅁ **P2. Chip Multi-label Classification (CutMix → CutMix + Pair Mask → FCM-PM)**

본 과제는 chip 단위 multi-label classification 의 합성 데이터 한계를 단계적으로 풀어가며, 본 과제 데이터 특성에 맞춰 FCM-PM 합성 구조와 손실 마스킹 구조를 신규 적용한 PoC 입니다.

- 과제 개요 및 규모: chip multi-label classification PoC 입니다. 학습은 single 4 class 에서 시작하고, 평가는 single 4 + 2-combo 6 + Normal + Invalid + OOD 4 로 구성한 **16+ class × 약 3,850 chip** 추가 생성 chip 데이터 기반 controlled synthetic benchmark 로 수행했습니다.
- 운영 상태: **[추가 생성 chip 데이터, PoC, 양산 적용 후보 검증 중]** 입니다.
- 담당 역할: 본인 90% / 관리자 10% 입니다.
- 수행 업무: CutMix 계열 선정, CutMix + Pair Mask background loss masking, FCM-PM (Full-Cover Mixup + Pair Mask) 합성 및 손실 마스킹 구조의 본 과제 신규 적용, val_margin / best-margin checkpoint selection, Label Smoothing, Temperature Scaling, Knowledge Distillation single-model compression 을 수행했습니다.
- 성과: **[추가 생성 chip 데이터, PoC]** FCM-PM 대표 모델 bit F1 **0.9943**, Normal / Invalid / OOD negative false-positive **0건**을 확인했습니다.
- 성과: **[추가 생성 chip 데이터, PoC]** Pair Mask 제거 시 FAR **100%** 로 전면 오판되어, FCM-PM 의 background loss masking 이 성패를 가르는 핵심 장치임을 확인했습니다.
- 성과: **[추가 생성 chip 데이터, PoC]** KD single student 는 bit F1 **0.9872** / FAR **0.5%** / **1× inference cost (단일 모델 1회 추론 부하)** 의 운영 후보를 확보했습니다.

**과제 관련 도메인 / AI 기술 / 모델 / 방법론**

본 과제 도메인은 Grade 양자화 chip image, chip 내부 defect 위치를 사전에 알 수 없는 특성, multi-label defect co-occurrence 입니다. 이에 따라 Multi-label Image Classification, Synthetic Data Engineering, Machine Learning Optimization, Knowledge Distillation 을 결합했고, 구체 모델·방법론으로 CutMix 와 CutMix + Pair Mask 를 거쳐 FCM-PM (Full-Cover Mixup + Pair Mask) 을 본 과제에 신규 적용했으며, Pair Mask background loss masking, val_margin / best-margin checkpoint selection, Label Smoothing, Temperature Scaling, single student distillation 까지 함께 구성했습니다.

기술 판단으로는 일반 CutMix 가 일부 영역만 잘라 붙이는 방식이라 chip 내부 defect 위치를 사전에 알 수 없는 본 과제에서는 defect signal 이 잘릴 수 있다는 점을 인지했고, chip 전체 grid 를 cover 하는 Full-Cover Mixup 으로 확장하면서 합성 background 를 loss 에서 제외하는 Pair Mask 를 결합해 multi-label 오탐을 억제했습니다.

ㅁ **P3. Trend Episode 데이터 생성 기반 Anomaly-detection 검증 PoC**

본 과제는 BBD/Overlay/CD 현업에서 형성한 trend 도메인 지식을 합성 episode generator 로 코드화하여 AI 학습이 가능한 데이터 자산으로 만드는 데이터 생성 중심 과제입니다.

- 과제 개요 및 규모: **데이터 생성이 주 성과인 과제**입니다. BBD/Overlay/CD 현업 경험에서 형성된 trend 도메인 지식을 episode synthesis generator 로 코드화하고, Region 5종 / Noise 3종 / trend 불량 5종 (mean_shift / std / spike / drift / context) / Fleet enforcement floor 를 직접 설계했습니다.
- 운영 상태: **[합성 trend chart, PoC]** 이며, 실전 label 부족을 전제로 한 합성 데이터 기반 검증 단계입니다.
- 담당 역할: 본인 90% / 관리자 10% 입니다.
- 수행 업무: Region 5종 계측 밀도 코드화, Noise 3종 설비 모드 매핑, trend 불량 5종 형상 카탈로그, fleet_std 비례 anomaly 강도 하한 보정, 정상 / 이상 trend episode 생성, 생성 데이터 검증용 baseline 학습 안정화를 수행했습니다.
- 성과: **[합성 trend chart, PoC]** normal 750 + abnormal 5종 각 150 = 총 **1,500 sample** 합성 trend chart 평가셋을 생성했습니다.
- 성과: **[합성 trend chart, PoC]** 1차 Binary gate 는 Binary F1 **0.9967**, Abnormal Recall **0.9987** 로 안정 수렴해, 생성 데이터가 정상 / 이상 패턴을 학습 가능한 형태로 담고 있음을 확인했습니다. 2차 Type classifier 의 mean_shift ↔ drift 혼동 등 type-level accuracy 는 1차 binary 안정성과 분리해 **[합성 trend chart, PoC, 개발 중]** 으로 보고합니다.

**과제 관련 도메인 / AI 기술 / 모델 / 방법론**

본 과제 도메인은 BBD/Overlay/CD trend 해석 경험, 설비 산포, 설비 hunting, 미세 drift, baseline 평탄도, spec-in 변동 사고 가능성입니다. 이에 맞춰 Synthetic Data Engineering, Time-series / Trend Episode Simulation, Baseline Model Validation 을 결합했습니다. 구체적으로는 계측 밀도를 `dense` / `sparse` / `very_sparse` / `thin` / `missing` 5단계로 코드화하고, 설비 산포 / hunting / drift 를 `Gaussian` / `Laplacian` / `correlated drift` 3 가지 통계 분포로 매핑한 뒤, `mean_shift` / `std` / `spike` / `drift` / `context` 5종 trend 불량 형상을 구성했습니다. 여기에 fleet_std 기반 enforcement floor 로 이상 강도 하한을 보장했고, 검증용 baseline 학습은 val-F1 median smoothing 과 val-loss spike guard 로 수렴을 안정화했습니다.

BBD/Overlay/CD trend 판단 기준을 synthetic data generator 로 코드화해, 실전 label 부족 상황에서도 AI 검증을 시작할 수 있는 데이터 기반을 마련했습니다.
