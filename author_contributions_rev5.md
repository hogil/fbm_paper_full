# 기여도 협의록 (Author Contribution Agreement)

본 문서는 단독 저자 논문에 대한 비저자 기여자 인정(non-author contributor acknowledgement)을 정리한 기록이며, 논문 author line(최호길 단독)과 충돌하지 않는다. 논문의 저자는 최호길 단독이고, 아래 현업 엔지니어는 저자가 아니라 연구 과정에 기여한 사람으로 인정한다. 본 연구의 AI 모델 설계와 구현, 데이터 파이프라인, 학습과 검증, 실험과 분석, 원고와 그림은 최호길이 단독으로 수행했다.

정리 기준은 CRediT(Contributor Roles Taxonomy)다. 학술 기여로 인정되는 11개 역할을 기준으로 누가 무엇을 수행했는지 정리했다. Resources / Supervision / Project administration 항목은 본 연구에 해당하는 별도 기여자(관리자 등)가 없으므로 표기하지 않는다.

## 기여자 표기

| 구분 | 인물 | 비고 |
|---|---|---|
| 제1저자 (논문 단독 저자) | 최호길 | 연구 기획, AI 모델 설계와 구현, 데이터 파이프라인, 학습과 검증, 실험과 분석, 원고와 그림 전반 |
| 기여자 (비저자) | 현업 엔지니어 (성명 기입 예정) | 현장 문제 정의, 요구사항 도출, 초기 labeling, 결과 확인 |

현업 엔지니어의 실명은 미정이며, 제출 전 확정해 기입한다.

## CRediT 역할 매핑

표기는 ●주도(Lead) / ○지원(Supporting) / −(없음)로 한다. Conceptualization은 현장 문제와 분석 방향을 엔지니어가 처음 제기(originate)하고, 최호길이 이를 AI 연구 문제로 정식화(formulate)해 모델과 학습 구조를 직접 설계, 구현했으므로 두 사람을 모두 주도(●)로 둔다. 나머지 AI 방법론, 모델 구현, 학습, 검증, 분석, 작성, 시각화는 최호길이 단독으로 주도했다.

| CRediT 인정 역할 | 최호길 | 현업 엔지니어 |
|---|:---:|:---:|
| Conceptualization (개념과 목표 수립) | ● | ● |
| Methodology (AI 방법론 개발과 모델 설계) | ● | − |
| Software (모델 코드와 알고리즘 구현, 테스트) | ● | − |
| Validation (재현성과 결과 검증) | ● | ○ |
| Investigation (실험 수행과 데이터 수집) | ● | ○ |
| Data curation (주석, 정리, 유지관리) | ● | ○ |
| Formal analysis (통계와 계산 분석) | ● | − |
| Analysis & conclusion (결과 비판적 검토) | ● | − |
| Writing-original draft (초고 작성) | ● | − |
| Visualization (시각화와 그림) | ● | − |
| Writing-review/editing (검토와 수정) | ● | − |

## AI 모델 설계와 구현 (제1저자 단독 핵심 기여)

본 연구의 AI 모델 전체를 최호길이 단독으로 설계, 구현, 학습, 검증했다. 단순한 공개 모델 적용이 아니라, 현업 Failbit Map 분석 문제에 맞춰 모델 구조와 학습 방식을 직접 설계한 것이 핵심 기여다.

- Known failure 분류: ConvNeXtV2-Base backbone 선정(FCMAE 사전학습)과 fine-tuning, 1차 분류 confidence가 낮은 sample에 한정한 ROI-YOLO 2-stage 보정 구조 설계, chip 좌표 기반 object-id map(chip-CNN) 대안 구현. class 비중을 반영한 weighted F1 score 0.95 달성.
- Unknown failure 군집화: 라벨에 종속되지 않는 self-supervised contrastive embedding(InfoNCE) 학습, MoCo queue와 grid 단위 global/local loss 설계, HDBSCAN 군집화로 신규 불량 후보 그룹 도출.
- chip multi-label 분류: 단일 불량 원천만으로 중복 불량 학습 신호를 만드는 FCM-PM(Full-Cover CutMix with Pair Mask) 설계, val_margin 기준 checkpoint 선택과 Gaussian Naive Bayes reject 게이트 구현. bit-F1 score 0.9927, False Alarm Rate 0.00% 달성.
- 학습 파이프라인: loss 함수 비교(Focal, ASL), hyperparameter optimization, 데이터 증강과 합성 평가셋 구성, 정량 지표 설계.
- 데이터와 시스템: Cython 파서(약 100배 가속)와 palette-indexed PNG 저장(약 80% 용량 절감) 기반 대량 데이터 파이프라인, 분석용 web viewer 구현.

## 합의 기여 비율(%)

기여 비율은 역할 점수를 기계적으로 환산한 값이 아니라, 위 CRediT 역할 매핑과 실제 수행 내용을 근거로 합의한 값이다. 최호길은 인정 역할 11개 전부를 단독 또는 주도적으로 수행했고, 특히 AI 모델 설계와 구현, 학습, 검증, 정량 분석, 원고와 그림을 단독으로 맡았다. 현업 엔지니어는 현장 문제 정의와 요구사항 도출, 초기 labeling, 결과 확인을 지원했다.

| 기여자 | 합의 기여율 | 합의 근거(요약) |
|---|---:|---|
| 최호길 | 80% | 연구 기획, AI 모델 설계와 구현, 데이터 파이프라인, 학습과 검증, 실험과 정량 분석, 원고와 그림 전반 단독 주도 |
| 현업 엔지니어 | 20% | 현장 문제 정의, 요구사항 도출, 초기 labeling, 결과 확인 |
| 합계 | 100% | |

## 기여 내용

- 최호길 (80%): 연구 기획과 AI 연구 문제 정식화, AI 모델 아키텍처 설계와 구현(Known 2-stage 분류, Unknown contrastive embedding 군집화, chip multi-label FCM-PM), 학습 파이프라인과 hyperparameter optimization, 데이터 파이프라인(Cython, palette PNG)과 web viewer 구현, 실험과 검증, 정량 분석, 시각화, 원고 작성과 수정을 단독으로 주도했다.
- 현업 엔지니어 (20%): 현장 문제 정의와 요구사항 도출에 기여하고, 초기 labeling과 결과 확인을 지원했다.
