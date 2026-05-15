## 1. 기술 분야

| 기술 분야 | 대표 적용 기법 / 방식 |
|-----------|----------------|
| Computer Vision | Image Classification, Object Detection, Multi-label Classification, Feature Representation Learning, Image-based Defect Detection |
| Deep Learning | CNN Backbone Modeling, Transfer Learning, Task-specific Fine-tuning, Loss Function Design, Regularization |
| Self-Supervised Learning | Contrastive Learning, Self-supervised Representation Learning, Embedding Learning |
| Unsupervised Learning | Clustering, Novelty Detection, Anomaly Detection, Out-of-Distribution Detection |
| Synthetic Data Generation / Data Augmentation | Synthetic Dataset Generation, Data Augmentation, Mixup, CutMix, Noise Injection |
| Model Optimization / Model Selection | Hyperparameter Optimization, Model Selection, Threshold Optimization, Calibration, Ensemble, Knowledge Distillation |
| Data Engineering / MLOps | ETL Pipeline, Batch Processing, Object Storage Integration, Model Evaluation Pipeline, Experiment Tracking |
| Software Engineering / API Service | Backend API, Web Application, Data Visualization, Access Control, Single Sign-On |

---

## 2. 업무경력

> 세 과제 모두 현업 데이터가 바로 모델 학습에 쓰이기 어려운 상황에서 시작했습니다. 본인은 데이터를 모델이 학습할 수 있는 형태로 바꾸고, 모델 결과가 현업 검토로 이어지도록 운영 흐름까지 함께 만들었습니다.

**ㅁ P1. Failbit Map Known & Unknown 불량 분석 아키텍처**

양산 Failbit Map 처리 흐름과 AI 불량 후보 검출을 하나의 운영 구조로 연결한 과제입니다.

(1) 과제 개요 및 규모 / 담당 역할 / 수행 업무 / 성과

- 과제 개요 및 규모: 2024년 10월부터 현재까지 Failbit Map raw log 를 이미지와 chip 좌표 데이터로 변환해 Web App 에서 조회하고, Known 분류와 Unknown 후보 검출까지 연결한 양산 운영 과제입니다. DRAM 전제품 라인에서 운영 중이며, 일 약 2만 장 wafer 를 1시간 주기로 적재합니다.
- 담당 역할: 본인 60% (서버 환경 구축, 데이터 처리, Web App 운영, Known/Unknown 모델 설계, 개발 및 검증) / 현업 엔지니어 20% (현업 문제정의 및 불량 교육) / 관리자 20% (방향성, 일정 및 리뷰 매니징)
- 수행 업무: Failbit Map 변환 파이프라인, Web App, ConvNeXtV2 task-specific fine-tuning 및 모델 설정값 튜닝, ROI YOLO 2-stage 보정, Unknown 자기지도 임베딩, Local InfoNCE, HDBSCAN grouping, chip-CNN 기반 object-id map 구조 개발
- 성과: Known은 평가용 hold-out set 기준 weighted F1 0.95(16 class / 1,500 labeled samples, 운영 적용 결과와 별도)입니다. Unknown은 운영 데이터 후보 13건 중 7건을 현업이 실제 불량으로 확인했고, Web App은 12일 누적 2,317 요청까지 사용되었습니다.
- 추가 개발: [추가 생성 chip 데이터, 개발 중] object-id map 구조는 별도 생성 chip 데이터 기준으로 검증 중입니다. Unknown 후속 생성 데이터 평가는 same-anchor defect-class capture 43/43, ARI 0.859±0.018 입니다.

(2) 과제 관련 도메인 / AI 기술 / 모델 / 방법론

- 도메인: EDS Failbit Map, wafer 불량 패턴 분석, 현업 불량 검토 Web App
- AI 기술: ConvNeXtV2 fine-tuning, ROI YOLO 2-stage, 대조학습 임베딩, Local InfoNCE, HDBSCAN, chip-CNN 기반 object-id map(chip 위치별 불량 chip id로 제작한 map)
- 방법론: wafer 단위 분류 모델로 전체 분포를 먼저 보고, center scratch / scratch_rot 처럼 헷갈리는 class 는 ROI YOLO 로 chip 단위 판단 근거를 재확인했습니다. 등록 class 밖 패턴은 대조학습 임베딩과 HDBSCAN 으로 후보화했습니다.

**ㅁ P2. Chip Multi-label Classification**

현업에서 바로 모으기 어려운 multi-label 조합을 single-label 불량 chip 기반으로 풀어본 과제입니다.

(1) 과제 개요 및 규모 / 담당 역할 / 수행 업무 / 성과

- 과제 개요 및 규모: 2025년 3월부터 현재까지 실제 환경에서 multi-label 불량 조합 label 을 충분히 모으기 어렵다는 조건을 두고, single-label 불량 chip 을 조합해 multi-label 불량 학습 및 검증을 진행한 과제입니다. single 4 class 기반으로 2-combo, Normal, Invalid, OOD 를 포함한 16+ class × 약 3,850 chip 통제 합성 평가셋을 구성했습니다.
- 담당 역할: 본인 80% / 관리자 20%
- 수행 업무: CutMix 계열 선정, FCM-PM(Full-Cover Mixup + Pair Mask) 합성 구조 적용, single 4 → 16+ multi-label / OOD 평가 구성, val_margin 기반 모델 선택 기준 도입, Label Smoothing, Temperature scaling, 4-bag ensemble, KD 단일 모델 압축 검토
- 성과: [추가 생성 chip 데이터, PoC] 최신 per-class 2,000 갱신 평가 기준 bit F1 0.9964, Total FAR 0.83% 입니다. 기존 요약 평가셋 기준으로는 bit F1 0.9943, Normal/Invalid/OOD 오탐 0건이었습니다. 운영 적용 전 PoC 수치입니다.
- 추가 확인: [추가 생성 chip 데이터, PoC] FCM-PM 구성요소 제거 비교 실험에서 Full-Cover Mixup 이 없거나 Pair Mask 구성이 빠진 변형은 Normal/Invalid/OOD 평가 오탐 억제가 실패했습니다. 4-bag ensemble 은 bit F1 0.9909 / FAR 0.00%, KD 단일 모델은 bit F1 0.9872 이지만 가혹 조건 평가에서 FAR 12.86% 로 추가 보정 대상입니다.

(2) 과제 관련 도메인 / AI 기술 / 모델 / 방법론

- 도메인: chip 단위 불량 이미지, Grade 0~7 양자화 이미지, single-label 기반 multi-label defect 조합
- AI 기술: Multi-label chip classification, CutMix, CutMix + Pair Mask, FCM-PM, Pair Mask 기반 배경 영역 loss 제외, val_margin / best-margin 모델 선택, asymmetric pos/neg target, Label Smoothing, Temperature scaling, 4-bag ensemble, Knowledge Distillation
- 방법론: Grade 값을 보존하기 위해 CutMix 계열을 선택했고, defect 위치를 미리 알 수 없는 조건은 Full-Cover Mixup 으로 반영했습니다. 합성 배경 영역이 defect 로 학습되는 문제는 Pair Mask 로 loss 에서 제외했습니다.

**ㅁ P3. Domain Knowledge 기반 Trend Anomaly 데이터 생성 및 불량 검증**

BBD(현업 trend 항목) / Overlay(정렬 계측) / CD(선폭 계측) 업무에서 보던 trend 판단 기준을 생성 데이터 구조로 옮긴 과제입니다.

(1) 과제 개요 및 규모 / 담당 역할 / 수행 업무 / 성과

- 과제 개요 및 규모: 2026년 1월부터 현재까지 실전 abnormal label 이 부족한 상태에서 detector 를 먼저 고도화하기보다, 학습 가능한 trend abnormal 데이터를 먼저 만드는 과제입니다. normal 3,500 + 불량 5종 각 700 = 불량 3,500, 총 7,000 sample 합성 trend chart 평가셋을 만들었습니다.
- 담당 역할: 본인 80% / 관리자 20%
- 수행 업무: Region 5종(정상 / 희소 / 공핍 / 얇은 계측 / 결핍), Noise 3종(Gaussian noise=설비 산포 / Laplacian noise=hunting, 목표값 주변 흔들림 / correlation noise=drift, 시간 방향 변화), 불량 5종 trend 합성 generator, 정상 산포 기준 anomaly 강도 하한 보정, 1단계 정상/이상 분류 기준 모델 검증, 2단계 5개 불량 유형 분류 규칙 보정
- 성과: [합성 trend chart, PoC] 1단계 정상/이상 분류에서 Binary F1 0.9967, Abnormal Recall 0.9987, 5개 seed 반복 평가 0.9944~0.9988 이 나왔습니다. 이 값은 실전 운영 성능 주장이 아니라, 생성 데이터에 정상/이상 구분 신호가 들어갔는지 확인한 기준 모델 결과입니다.
- 상태: 아직 실전 현업 데이터 검증 단계는 아니며, 생성 데이터와 기준 모델 결과를 분리해 관리하고 있습니다.

(2) 과제 관련 도메인 / AI 기술 / 모델 / 방법론

- 도메인: BBD(현업 trend 항목) / Overlay(정렬 계측) / CD(선폭 계측) trend chart, 계측 밀도 차이, 설비 산포, hunting(목표값 주변 흔들림), drift(시간 방향 변화), context pattern
- AI 기술: synthetic trend episode generation, 계측 밀도 코드화, statistical noise injection, trend anomaly shape catalog, 정상 산포 기준 anomaly strength calibration, 생성 데이터 확인용 기준 모델 학습 안정화
- 방법론: 실제 운영 chart 처럼 결핍 영역, 희소 영역, 공핍 영역을 만들고, Gaussian noise / Laplacian noise / correlation noise 로 설비 산포, hunting, drift 를 분리했습니다. 정상 산포에 묻히는 약한 이상은 최소 anomaly 강도를 보정했습니다.
