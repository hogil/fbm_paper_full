## 1. 기술 분야

| 기술 분야 | 적용 기술 / 방법론 |
|-----------|--------------------|
| Computer Vision / Image-based Defect Detection | Wafer map image classification, object detection, chip-level defect classification, image-based defect pattern analysis |
| Self-Supervised Representation Learning | Contrastive learning, Global / Local InfoNCE, embedding learning, unknown defect candidate grouping |
| Unsupervised Learning / Anomaly Detection | HDBSCAN clustering, novelty detection, out-of-distribution evaluation, trend anomaly validation |
| Synthetic Data Engineering / Data Augmentation | Full-Cover Mixup, Pair Mask, synthetic trend episode generation, controlled evaluation dataset construction |
| Machine Learning Optimization / Model Selection | Task-specific fine-tuning, hyperparameter optimization, threshold calibration, ensemble, knowledge distillation |
| MLOps / Data Pipeline Engineering | Raw log parsing, batch pipeline, object storage integration, model evaluation pipeline, experiment tracking |
| AI Systems Engineering / Web Application | Backend API, Web App operation, data visualization, access control, production monitoring |

## 2. 업무경력

**ㅁ P1. Failbit Map Known & Unknown 불량 분석 아키텍처**

(1) 과제 개요 및 규모 / 담당 역할 / 수행 업무 / 성과

- 과제 개요 및 규모: 2024년 10월부터 현재까지 Failbit Map raw log 를 이미지와 chip 좌표 데이터로 변환하고, Web App 조회와 Known / Unknown AI 분석까지 연결한 양산 운영 과제입니다. DRAM 전제품 라인에서 일 약 2만 장 wafer 를 1시간 주기로 적재합니다.
- 담당 역할: 본인 60% (서버 환경 구축, 데이터 처리, Web App 운영, Known / Unknown 모델 설계, 개발 및 검증) / 현업 엔지니어 20% (현업 문제정의 및 불량 분석 교육) / 관리자 20% (방향성, 일정 및 리뷰 매니징)
- 수행 업무: S3 raw log 수집, Cython hex-to-grade 변환, 32-color palette PNG 저장, chip 좌표 JSON 생성, Web App 운영, ConvNeXtV2 task-specific fine-tuning, ROI YOLO 2-stage 보정, Unknown 자기지도 임베딩, 6×6 local sampling, Local InfoNCE, HDBSCAN grouping, chip-CNN 기반 object-id map(chip 위치별 불량 chip id로 제작한 map) 구조 개발
- 성과: [실전 현업 라벨 데이터] Known 2-stage 는 16 class / 1,500 labeled samples / 평가용 hold-out set 기준 weighted F1 0.95 입니다. [양산 운영] Web App 은 12일 누적 2,317 요청까지 사용되었고, Cython 변환은 기존 Python 대비 약 100배 빠르게 처리했습니다. [실전 현업 데이터] Unknown 은 5일 10,000장 학습 + 별도 1일 2,000장 적용 결과 13개 후보 중 7개 실제 불량을 현업이 확인했습니다.

(2) 과제 관련 도메인 / AI 기술 / 모델 / 방법론 등

- 도메인: EDS Failbit Map, wafer 불량 패턴 분석, chip 좌표 기반 defect object 분석, 현업 불량 검토 Web App
- AI 기술 / 모델: ConvNeXtV2, ROI YOLO 2-stage, chip-CNN, self-supervised contrastive learning, Local InfoNCE, HDBSCAN
- 방법론: wafer 전체 분포는 ConvNeXtV2 로 먼저 보고, center scratch / center scratch_rot 처럼 map-level 에서 헷갈리는 class 는 ROI YOLO 로 chip 단위 증거를 다시 확인했습니다. 등록 class 밖 패턴은 global embedding 만 쓰지 않고 6×6 local sampling 과 Local InfoNCE 를 넣어 위치 정보를 보존한 뒤 HDBSCAN 으로 후보화했습니다.

**ㅁ P2. Chip Multi-label Classification**

(1) 과제 개요 및 규모 / 담당 역할 / 수행 업무 / 성과

- 과제 개요 및 규모: 2025년 3월부터 현재까지 single-label 불량 chip 만 비교적 확보되는 실제 환경을 기준으로, multi-label 불량 조합을 학습 및 검증한 과제입니다. single 4 class 기반으로 2-combo, Normal, Invalid, OOD 를 포함한 16+ class × 약 3,850 chip 통제 합성 평가셋을 구성했습니다.
- 담당 역할: 본인 80% (FCM-PM 합성 구조, loss masking, 모델 선택 기준, 학습 및 평가 운영) / 관리자 20% (방향성, 일정 및 리뷰 매니징)
- 수행 업무: CutMix 계열 선정, FCM-PM(Full-Cover Mixup + Pair Mask) 합성 구조 적용, single 4 class 기반 multi-label 조합 생성, Normal / Invalid / OOD 평가 구성, val_margin 기반 모델 선택, Label Smoothing, Temperature scaling, 4-bag ensemble, KD 단일 모델 압축 검토
- 성과: [추가 생성 chip 데이터, PoC] 최신 per-class 2,000 갱신 평가 기준 bit F1 0.9964, Total FAR 0.83% 입니다. 기존 요약 평가셋 기준으로는 bit F1 0.9943, Normal / Invalid / OOD 오탐 0건이었습니다. FCM-PM 구성요소 제거 비교에서는 Full-Cover Mixup 또는 Pair Mask 가 빠진 변형에서 오탐 억제가 실패해, 최종 구조 유지 근거를 확인했습니다.

(2) 과제 관련 도메인 / AI 기술 / 모델 / 방법론 등

- 도메인: chip 단위 불량 이미지, Grade 0~7 양자화 이미지, single-label 기반 multi-label defect 조합
- AI 기술 / 모델: Multi-label chip classification, CutMix, Full-Cover Mixup, Pair Mask, asymmetric positive / negative target, model calibration, ensemble, knowledge distillation
- 방법론: Grade 0~7 값 자체가 불량 의미를 가지므로 픽셀값을 섞는 방식보다 CutMix 계열을 선택했습니다. 일반 CutMix 가 불량 영역을 일부 잘라낼 수 있는 문제는 Full-Cover Mixup 으로 줄였고, 합성 background 가 defect 로 학습되는 문제는 Pair Mask 로 loss 에서 제외했습니다.

**ㅁ P3. Domain Knowledge 기반 Trend Anomaly 데이터 생성 및 불량 검증**

(1) 과제 개요 및 규모 / 담당 역할 / 수행 업무 / 성과

- 과제 개요 및 규모: 2026년 1월부터 현재까지 실전 abnormal label 이 부족한 조건에서 trend anomaly 검증용 합성 데이터를 먼저 만든 과제입니다. normal 3,500 + 불량 5종 각 700 = 불량 3,500, 총 7,000 sample 합성 trend chart 평가셋을 구성했습니다.
- 담당 역할: 본인 80% (domain knowledge 기반 데이터 합성 generator 설계, trend 불량 rule 코드화, AI 기준 모델 fine-tuning 및 성능 검증) / 관리자 20% (방향성, 일정 및 리뷰 매니징)
- 수행 업무: Region 5종(정상 / 희소 / 공핍 / 얇은 계측 / 결핍), Noise 3종(Gaussian noise=설비 산포 / Laplacian noise=hunting / correlation noise=drift), trend 불량 5종(mean_shift / std / spike / drift / context) 합성 generator 설계, 정상 산포 기준 anomaly 강도 하한 보정, 1단계 정상/이상 분류 기준 모델 검증, 2단계 5개 불량 유형 분류 규칙 보정
- 성과: [합성 trend chart, PoC] 1단계 정상/이상 분류에서 Binary F1 0.9967, Abnormal Recall 0.9987, 5개 seed 반복 평가 0.9944~0.9988 이 나왔습니다. 이 값은 실전 운영 성능 주장이 아니라, 생성 데이터에 정상/이상 구분 신호가 들어갔는지 확인한 기준 모델 결과입니다.

(2) 과제 관련 도메인 / AI 기술 / 모델 / 방법론 등

- 도메인: BBD(현업 trend 항목), Overlay(정렬 계측), CD(선폭 계측) trend chart, 계측 밀도 차이, 설비 산포, hunting, drift, context pattern
- AI 기술 / 모델: Synthetic trend episode generation, statistical noise injection, trend anomaly shape catalog, binary anomaly classification, type classification, anomaly strength calibration
- 방법론: 실제 운영 chart 에서 보이는 결핍 영역, 희소 영역, 공핍 영역을 Region rule 로 만들고, 설비 산포 / hunting / drift 를 각각 noise 조건으로 분리했습니다. 모델을 먼저 복잡하게 키우기보다, domain knowledge 가 반영된 데이터 생성 규칙과 기준 모델 평가를 반복해 생성 데이터의 학습 가능성을 확인했습니다.
