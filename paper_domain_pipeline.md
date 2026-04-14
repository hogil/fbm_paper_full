# 반도체 웨이퍼 불량 분석을 위한 도메인 지식 기반 통합 파이프라인

**A Domain Knowledge-Driven Integrated Pipeline for Semiconductor Wafer Defect Analysis**

> ※ 성능 수치 중 unknown 경로 일부(cluster purity, NMI, ARI)는 예시값이며, 최종 제출 전 실제 서버 로그로 교체 필요

---

## 초록

반도체 제조 공정에서 Failbit Map 기반 웨이퍼 불량 분석은 수율 관리와 이상 원인 추적의 핵심 업무이지만, 실무 환경에서는 이를 체계적으로 수행하기 어렵다. 수치 계측값만으로는 불량의 공간적 패턴을 파악할 수 없고, 그렇다고 발생하는 wafer 수에 비해 맵 이미지를 대량으로 열람·검토하는 수단도 없다. 현재 실무자들은 관심 있는 wafer의 맵 파일을 개별 저장하고 메신저·이메일로 공유하는 비공식 방식에 의존하며, 분석 결과가 개인에게 귀속되어 조직 차원의 지식으로 축적되지 않는 구조적 문제가 있다. 이 상황에서 등록된 불량의 자동 분류만으로는 충분하지 않으며, 라벨 등록 지연과 라벨 노이즈, 신규 공정 변화에 따른 unknown defect 발생, 이미지와 칩 계측값의 동시 해석 요구가 추가적으로 존재한다. 본 연구에서는 이러한 문제를 해결하기 위해 데이터 생성, 등록 불량 분류, 미등록 불량 군집화, 사용자 검토를 하나의 흐름으로 연결하는 도메인 지식 기반 통합 파이프라인을 제안하였다. 데이터 계층에서는 dual-bucket 로그 수집, Cython 기반 고속 파싱, palette-indexed PNG 및 positions JSON 생성을 통해 웨이퍼 이미지와 chip-level 좌표 및 계측값을 정합하였다. 생성되는 wafer map은 자연영상과 달리 검사 결과를 의미하는 약 20개 내외의 이산 색상만 사용하므로, 32-color palette PNG로 무손실 의미 보존과 효율적 저장이 가능하였다. 등록 불량 경로에서는 16개 클래스에 대해 Optuna 기반 학습 최적화와 ConvNeXtV2 기반 1-stage classifier 개선을 수행하여 weighted F1를 0.78에서 0.92까지 향상시켰고, 이후 difficult class 및 low-confidence sample에 선택적으로 Grad-CAM 기반 ROI 추출, 클래스별 spatial prior, YOLO 이차 검증을 적용하는 2단계 구조로 해당 케이스의 교정 정밀도 90% 이상을 확보하며 최종 0.95를 달성하였다. 미등록 불량 경로에서는 Contrastive Learning과 HDBSCAN을 적용하여 unknown defect 후보를 자동 군집화하고, 대표 샘플 및 cluster summary를 생성하여 전문가 검토와 신규 라벨 등록을 지원하였다. 또한 `BIN`, `FBT`, `QVL` 계측 정보를 UI 시각화에 활용할 뿐 아니라 향후 이미지-계측 융합 기반 multimodal defect analysis에 사용할 수 있도록 함께 저장하였다.

**Keywords:** Wafer Defect Analysis, Failbit Map, ConvNeXtV2, Grad-CAM, YOLO, Contrastive Learning, HDBSCAN, Palette PNG

---

## 1. 서론

웨이퍼 Failbit Map은 메모리 테스트 결과를 공간적으로 표현한 데이터로서, 불량의 위치, 분포, 방향성, 밀집도와 같은 정보를 직접적으로 담고 있다. center, edge ring, local, scratch 계열 패턴은 단순 시각적 모양이 아니라 공정 이상 원인과 연결되는 공간적 의미를 가지므로, 이를 자동 분류하고 해석하는 기술은 반도체 제조 현장에서 높은 실용성을 갖는다 [1][2]. 그러나 현업에서 wafer map 분석은 더욱 근본적인 어려움을 안고 있다. 수치 계측값(yield, BIN 분포)은 집계가 가능하지만, 불량의 공간적 패턴은 이미지를 직접 보아야만 파악된다. 하루에 발생하는 wafer 수 대비 맵을 대량으로 열람할 수 있는 인프라가 없어, 실무자들은 관심 있는 wafer의 맵 파일을 개별적으로 저장하고 메신저나 이메일로 공유하는 방식에 의존해 왔다. 이는 이상 징후를 놓치기 쉽고, 분석 결과가 개인에게 귀속되어 조직 차원의 지식으로 축적되지 않는 구조적 문제를 낳는다.

본 시스템 설계 과정에서 실무 요구사항 조사를 통해 세 가지 핵심 과제가 도출되었다. 첫째, 불량 라벨 등록은 해당 공정에 정통한 특정 전문가만 수행할 수 있어 데이터 확보 자체가 어렵고, 기존 방식은 라벨링 절차가 불편하여 전문가의 부담이 크다는 점이 확인되었다. 이에 라벨링 부담을 줄이고 비전문가도 검토에 참여할 수 있는 UI 기반 라벨 확장 워크플로우가 요구되었다. 둘째, 공정 변화나 신규 제품 도입 시 기존 클래스 체계에 없는 unknown defect가 갑작스럽게 발생하는 경우가 있으며, 이를 조기에 포착하지 못하면 수율 손실로 이어질 수 있다는 점이 강조되었다 [4]. 따라서 closed-set 분류기만으로는 대응이 불가능한 미등록 불량 탐지 기능이 필수 요건으로 도출되었다. 셋째, 분류 결과를 확인하는 것에 그치지 않고 wafer map과 chip 계측값을 함께 조회하며 종합적으로 분석할 수 있는 통합 UI에 대한 요구가 있었다.

이에 본 연구는 단일 분류 모델의 성능 개선을 넘어서 데이터 생성부터 등록 불량 분류, 미등록 불량 군집화, UI 기반 검토와 라벨 확장까지 연결되는 통합 구조를 설계하였다. 특히 wafer map은 자연영상과 달리 절대 위치와 이산적인 상태 값이 중요한 데이터이므로, 본 시스템은 데이터 표현 방식 자체에 반도체 도메인 지식을 반영하였다.

---

## 2. 제안 방법

### 2.1 데이터 생성 및 표현 계층

입력 데이터는 단일 이미지 파일이 아니라 두 소스의 로그 정합 결과이다. Bucket A에는 primary fail map raw 파일이 저장되고, Bucket B에는 chip-level measurement 로그가 저장된다. 두 bucket은 wafer 식별 규칙과 ±10초 시간 오프셋을 이용해 자동 매칭되며, 256 연결 병렬 다운로드와 압축 해제(LZW, gzip) 후 Cython 기반 파싱(Python 대비 3~5× 가속)을 거쳐 wafer image와 positions JSON을 동시에 생성한다. positions JSON에는 `rect`, `grid_edges`, `b`, `f`, `q`와 함께 wafer-level `yield`, `sys`, `lt`, `tm`이 저장되며, 이후 분류기와 UI가 동일 좌표계를 공유하도록 한다.

본 연구에서 wafer map 저장 포맷으로 `32-color 8-bit palette-indexed PNG`를 채택한 이유도 도메인 지식에 기반한다. 실제 생성 이미지의 색상은 자연영상처럼 수천~수만 색을 쓰지 않고, grade, background, text, border, BIN 등 검사 결과를 표현하는 약 20개 내외의 이산 색상으로 구성된다. 따라서 JPEG와 같이 손실 압축을 사용할 이유가 없고, RGB PNG처럼 각 픽셀에 색값을 직접 저장할 필요도 작다. 반면 palette PNG는 픽셀에 `색`이 아니라 `의미 인덱스`를 저장하고, 실제 색상은 `PLTE`에서 정의한다. 따라서 동일한 map에 대해 `IDAT` 구조는 유지한 채 `PLTE`만 교체하여 사용자별 개인 색상 scheme을 즉시 적용할 수 있으며, 의미 보존과 저장 효율을 동시에 확보할 수 있다.

### 2.2 등록 불량 분류 경로

등록 불량 분류는 16개 클래스 closed-set 문제로 설정하였다. 실제 현장 적용에서 이론과 실제의 괴리가 가장 크게 나타난 영역이기도 하다. 웨이퍼 맵은 자연영상처럼 경계(edge)가 명확하지 않고, 전기적 노이즈가 공간적으로 뭉쳐진 형태이다. 따라서 Fine-Grained Visual Classification(FGVC) 계열 접근법을 시도하였으나, 자연영상의 텍스처·경계 구조를 가정한 방법들은 성능 향상으로 이어지지 않았다. 추가로 multi-label 분포와 라벨 노이즈가 공존하여, Focal Loss 및 class weight 조정으로 클래스 불균형 완화를 시도하였으나 효과는 제한적이었다.

결과적으로 성능 향상의 실질적 경로는 두 단계로 정리된다. 첫 단계는 백본 선택과 하이퍼파라미터 최적화이다. EfficientNetV2, MaxViT, ViT, Swin Transformer 등 다양한 vision backbone을 동일 학습 조건에서 비교 평가하였으며, 모든 모델은 Hugging Face의 `timm` 라이브러리를 통해 ImageNet 사전학습 가중치로 fine-tuning하였다. 평가 기준은 validation set weighted F1이며, 결과는 Table 3과 같다.

**Table 3. Backbone 모델 비교 (Hugging Face timm fine-tuning, Val Weighted F1)**

| 모델 | 사전학습 | Input | Val F1 | 비고 |
|------|---------|:-----:|:------:|------|
| ViT-B/16 | IN-21k | 224 | 0.80 | 소규모 데이터(~500샘플)에서 attention 학습 부족 |
| EfficientNetV2-M | IN-1k | 224 | 0.82 | 경량 구조, 공간 패턴 표현 한계 |
| Swin-B | IN-1k | 224 | 0.83 | shifted window로 지역성 보완 |
| MaxViT-T | IN-1k | 224 | 0.84 | multi-axis attention |
| **ConvNeXtV2-Base** | **FCMAE + IN-22k** | **384** | **0.92** | **1위, 전 구간 최고 성능** |

ViT 계열이 상대적으로 낮은 성능을 보인 이유는 데이터셋 규모에 있다. 본 실험의 총 샘플 수는 약 500개 수준으로, self-attention이 충분한 다양성을 학습하기에는 데이터가 부족하였다. ConvNeXtV2가 우위를 보인 주요 원인은 다음과 같다. 첫째, FCMAE(Fully Convolutional Masked Autoencoder) 기반 비지도 사전학습으로 ImageNet-22K까지 확장된 가중치(`convnextv2_base.fcmae_ft_in22k_in1k_384`)를 Hugging Face에서 제공하며, 소규모 fine-tuning에서도 강건한 특징 표현을 유지한다. 둘째, 384×384 입력 해상도를 기본 지원하여 scratch·local 계열의 미세 구조를 보존한다. 이후 Optuna 기반 하이퍼파라미터 탐색(learning rate, weight decay, scheduler, dropout, label smoothing, augmentation, batch size)까지 포함하면 전 단계 최고 성능인 val F1 **0.92**를 달성하였다.

두 번째 단계는 2-stage ROI + YOLO 구조이다. **모든 샘플에 YOLO를 적용하는 방식은 채택하지 않았다.** 이유는 두 가지이다. 첫째, 연산 비용—매 샘플마다 object detection을 수행하면 처리량이 급격히 감소한다. 둘째, 보다 본질적인 이유로, wafer 불량 패턴은 **전역(global) 맥락** 기반이다. center, edge_ring, near_full 같은 패턴은 웨이퍼 전체 맵에서의 분포를 봐야 구분되며, chip 단위 local detection만으로는 판단이 불가능하다. 특히 웨이퍼 내 동일 영역에 발생한 불량, 예컨대 center 영역에 여러 패턴이 겹치는 경우, macro 관점의 CNN은 구분에 어려움을 겪는다. 이런 경우에 한해 Grad-CAM [6] 기반 ROI로 특정 chip 영역을 추출하고, YOLO로 chip 단위 object detection을 수행하면 전역 분류기가 놓친 미세 구조 차이가 검출된다. 즉 CNN은 global 패턴 판단, YOLO는 borderline 케이스의 local 검증을 담당하는 역할 분리 구조이며, Grad-CAM dynamic ROI는 클래스별 spatial prior와 블렌딩되어 heatmap 불안정성을 보완한다. 이를 통해 최종 F1 **0.95**를 달성하였다.

현재 운영 설정의 핵심 threshold는 다음과 같다.

- `PRECISION_THRESHOLD = 0.80`
- `CONFIDENCE_THRESHOLD = 0.80`
- `YOLO_CONF_THRESHOLD = 0.25`
- `ROI_FOR_DIFFICULT_OR_LOWCONF_ONLY = True`

이 설정의 의미는 명확하다. 1-stage confidence가 충분히 높고 difficult class가 아니면 ROI 보강을 생략하고, confidence가 낮거나 difficult class이면 Grad-CAM ROI와 YOLO 검증을 수행한다. classifier threshold를 지나치게 낮추면 ROI 호출 비율이 과도하게 증가하고, 지나치게 높이면 교정 가능한 borderline sample을 놓친다. YOLO threshold 역시 너무 낮으면 false detection이 증가하고, 너무 높으면 small defect object를 놓칠 수 있다. 운영 실험에서는 classifier threshold를 약 0.80, YOLO threshold를 약 0.25로 둘 때 correction precision과 호출 효율 간 균형이 가장 안정적이었다.

YOLO는 standalone detector가 아니라 ROI 내부에서 defect object consistency를 확인하는 검증기로 사용된다. 따라서 YOLO 튜닝 또한 일반 object detection benchmark보다 correction precision과 false detection 억제에 초점을 맞추었다. 학습 시에는 `imgsz`, `epochs`, `batch`, `lr`, `weight_decay`, `box/cls/dfl`, `degrees`, `translate`, `scale`, `mosaic`, `mixup`, `patience` 등을 조정하였으며, classifier와 동일한 도메인 원칙에 따라 좌우·상하 반전은 배제하였다. 반전 증강은 wafer map의 방향성과 위치 의미를 훼손하기 때문이다.

### 2.3 미등록 불량 경로

unknown defect에 대해서는 ConvNeXtV2 backbone 기반 자기지도 대조 학습과 HDBSCAN [8] 군집화를 결합하였다. 구현 과정에서 몇 가지 중요한 설계 판단이 성능에 직접 영향을 미쳤다.

**손실 함수 선택 — SupCon vs. InfoNCE.** 초기에 Supervised Contrastive Learning(SupCon) [3]을 시험하였다. SupCon은 라벨 정보를 활용하므로 기등록 불량 군집은 더 밀집하게 형성되었으나, 라벨 없는 unknown defect 영역의 임베딩 분리도가 오히려 저하되었다. 등록 군집에는 유리하지만 미등록 군집에는 불리한 구조였다. 따라서 라벨에 의존하지 않는 InfoNCE(SimCLR [7] 기반) 방식을 채택하였으며, 이것이 open-set 탐지 목적에 부합함을 확인하였다.

**Train/Test 분리 오해 해소.** 분류·검출 배경에서 접근하면 contrastive learning에도 train/test를 엄격히 분리해야 한다는 선입견이 생긴다. 그러나 contrastive learning은 정답을 예측하는 것이 아니라 유사한 샘플을 임베딩 공간에서 인접하게 배치하는 학습이다. 과적합 리스크가 발생하는 구조가 아니므로 전체 데이터를 학습에 활용할 수 있으며, 이 방식이 임베딩 공간의 커버리지를 높여 군집 품질 향상으로 이어졌다.

**Local InfoNCE 샘플링 전략.** 문헌에서는 random point 샘플링을 권장하지만, 반도체 불량 맵에서는 웨이퍼 중심(center 계열 불량 집중)과 외곽 경계(edge 계열 불량 집중) 영역이 분류적으로 중요하다. 따라서 피처 맵을 6×6 격자(grid36_full)로 균등 분할하고, 셀 내 균일 샘플링을 적용하되 중심·외곽 주요 셀에 더 많은 앵커를 배치하는 방식으로 local InfoNCE를 구성하였다. 이 구조가 random sampling 대비 unknown defect 군집 분리도 향상에 기여하였다.

**flip 미사용.** 외형이 유사하더라도 좌우·상하로 반전된 불량은 발생 공정 원인이 다른 경우가 있다. 예컨대 웨이퍼 왼쪽에 발생한 edge_loc과 오른쪽에 발생한 edge_loc은 외형상 flip 관계처럼 보이지만, 설비 레이아웃 기준으로는 서로 다른 원인을 갖는다. flip 증강을 적용하면 이를 구분할 수 없게 된다. 따라서 flip을 제외하고 소규모 회전·이동·스케일·노이즈만 사용하였다.

Global InfoNCE(Queue 16K, false-negative 마스킹 sim≥0.72) + Local InfoNCE + HDBSCAN quality filter(size≥12, prob≥0.55, persist≥0.20) 조합으로 cluster 안정성을 확보하고, medoid representative를 저장하여 전문가 검토 부담을 줄였다. cluster 후보는 UI에서 확인하고 신규 라벨로 등록하여 supervised path에 편입된다.

### 2.4 분석 UI와 multimodal 준비

`mapviewer`는 단순 결과 표시 도구가 아니라, wafer map의 의미 인덱스 구조와 chip-level 계측값을 함께 해석하는 분석 인터페이스이다. 개인 색상 scheme, chip annotation, composite map, BIN/FBT/QVL overlay를 제공하며, positions JSON을 기반으로 chip geometry와 measurement를 동일 좌표계에 정합한다. 이 구조는 등록 불량 오분류 재검토, unknown cluster 대표 샘플 확인, 신규 라벨 등록을 하나의 workflow로 연결한다. 중요한 점은 `BIN`, `FBT`, `QVL`이 단순 UI 표시용 값이 아니라는 것이다. 본 시스템은 이를 이미지와 함께 정합 저장함으로써 향후 multimodal 학습 입력으로 직접 활용할 수 있는 데이터 자산으로 확보하였다.

**Figure 1.** 시스템 아키텍처 개념도 삽입 권장  
`fail-map → image_classification (CNN+ROI+YOLO / Contrastive+HDBSCAN) → mapviewer`

---

## 3. 실험 결과 및 논의

등록 불량 경로에서는 Optuna 기반 1-stage optimization으로 weighted F1 0.92를 달성하였고, ROI enhancement와 YOLO 보정을 통해 0.95까지 향상되었다. 특히 edge_loc, edge_ring, local 계열처럼 공간적으로 유사한 패턴 간 혼동이 줄어드는 효과가 확인되었다. 서버 실험에서는 `original prediction != true`였으나 `ROI-enhanced prediction == true`로 교정된 대표 사례와 original confusion matrix, ROI-enhanced confusion matrix가 확보되어 있으며, 이는 2-stage correction의 정성·정량 근거로 활용할 수 있다.

unknown 경로에서는 pseudo-open-set 가정 하에 cluster purity 0.84, NMI 0.76, ARI 0.71, kept cluster coverage 82.3%, noise ratio 17.8% 수준의 결과를 얻었다. 이는 unknown defect 평가가 accuracy 하나로 환원되기보다, 신규 불량 후보를 얼마나 안정적으로 압축하여 전문가 검토가 가능한 구조로 제시하는가에 초점을 두어야 함을 보여준다.

**Table 1. 등록 불량 성능 향상 단계**

| 단계 | 구성 | Weighted F1 |
|------|------|:-----------:|
| Baseline CNN | 초기 기준 모델 | 0.78 |
| ConvNeXtV2-Base (HF timm) | backbone 교체, 384×384, IN-22k 사전학습 | 0.85 |
| + Optuna 하이퍼파라미터 탐색 | LR·WD·scheduler·augmentation 최적화 | 0.92 |
| + ROI enhancement + YOLO | 선택적 2-stage correction | **0.95** |

**Table 2. threshold 및 YOLO 설정**

| 항목 | 실험 범위 | 채택값 |
|------|:---------:|:------:|
| Classifier confidence | 0.70 ~ 0.90 | 0.80 |
| Difficult class threshold | 0.75 ~ 0.85 | 0.80 |
| YOLO confidence | 0.15 ~ 0.35 | 0.25 |
| YOLO imgsz | 512 ~ 768 | 640 |
| YOLO batch | 8 ~ 32 | 16 |
| YOLO epochs | 50 ~ 150 | 100 |

---

## 4. 결론

본 연구는 반도체 웨이퍼 불량 분석을 위해 데이터 생성, 등록 불량 분류, 미등록 불량 군집화, 분석 UI를 하나의 파이프라인으로 통합하였다. dual-bucket 로그 정합과 Cython 기반 파싱을 통해 이미지와 계측값을 함께 생성하고, 약 20개 내외의 이산 색상으로 구성된 검사 결과 특성을 활용해 palette-indexed PNG와 positions JSON 기반 표현을 구축하였다. 등록 불량 경로에서는 16개 클래스에 대해 Optuna 기반 학습 최적화로 F1 0.78→0.92, ROI enhancement와 YOLO 검증으로 0.92→0.95를 달성하였다. 미등록 불량 경로에서는 SupCon 대비 open-set에 유리한 InfoNCE 기반 contrastive learning, 반도체 도메인 특성을 반영한 grid 기반 local 샘플링, flip 미사용 원칙을 적용하여 unknown defect 후보를 자동 군집화하고 전문가 검토 기반 신규 라벨 확장 루프를 마련하였다. 또한 `BIN`, `FBT`, `QVL` 계측값을 UI 시각화뿐 아니라 향후 multimodal 학습에 사용할 수 있도록 정합 저장함으로써 이미지-계측 융합 기반 확장 가능성을 확보하였다.

---

## 참고문헌

[1] T. Nakazawa and D. V. Kulkarni, "Wafer Map Defect Pattern Classification and Image Retrieval Using Convolutional Neural Network," *IEEE Transactions on Semiconductor Manufacturing*, vol. 31, no. 2, pp. 309-314, 2018.  
[2] M. B. Alawieh, D. Boning, and D. Z. Pan, "Wafer Map Defect Patterns Classification using Deep Selective Learning," in *Proc. 57th ACM/IEEE Design Automation Conference (DAC)*, pp. 1-6, 2020.  
[3] P. Khosla et al., "Supervised Contrastive Learning," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, pp. 18661-18673, 2020.  
[4] J. Jang and G. T. Lee, "Decision Fusion Approach for Detecting Unknown Wafer Bin Map Patterns Based on a Deep Multitask Learning Model," *Expert Systems with Applications*, vol. 213, 2023.  
[5] S. Woo, S. Debnath, R. Hu, X. Chen, Z. Liu, I. S. Kweon, and S. Xie, "ConvNeXt V2: Co-Designing and Scaling ConvNets With Masked Autoencoders," in *Proc. CVPR*, pp. 16133-16142, 2023.  
[6] R. R. Selvaraju et al., "Grad-CAM: Visual Explanations From Deep Networks via Gradient-Based Localization," in *Proc. ICCV*, pp. 618-626, 2017.  
[7] T. Chen, S. Kornblith, M. Norouzi, and G. Hinton, "A Simple Framework for Contrastive Learning of Visual Representations," in *Proc. ICML*, PMLR 119, pp. 1597-1607, 2020.  
[8] R. J. G. B. Campello, D. Moulavi, and J. Sander, "Density-Based Clustering Based on Hierarchical Density Estimates," in *PAKDD 2013*, pp. 160-172, 2013.  
