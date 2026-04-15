# 반도체 웨이퍼 불량 분석을 위한 도메인 지식 기반 통합 파이프라인

**A Domain Knowledge-Driven Integrated Pipeline for Semiconductor Wafer Defect Analysis**

> ※ 성능 수치 중 unknown 경로 일부(cluster purity, NMI, ARI)는 예시값이며, 최종 제출 전 실제 서버 로그로 교체 필요

---

## 초록

반도체 EDS(Electrical Die Sorting) Test 결과인 Failbit Map은 천만 픽셀 이상의 표현력으로 웨이퍼 불량의 위치·분포·밀집도·방향성·강도 정보를 담는 핵심 데이터이며, 수율 저하 원인 추적과 공정 이상 조기 인지에 중요한 역할을 한다. 그러나 기존 분석은 wafer 평균 기반의 단순 요약값에 크게 의존하였기 때문에, 위치별 편차·국부 패턴·형상 차이·중복 불량을 충분히 반영하지 못했다. 더구나 평균값에서 이상 징후가 나타나지 않더라도 Map에서만 드러나는 불량 패턴이 적지 않았고, 전 제품 wafer를 분석 담당자가 직접 확인하는 방식에는 현실적 한계가 있어 AI 기반 자동 분류·선별 체계가 필요하였다. 이를 해결하기 위해 본 연구는 DRAM 제품의 Failbit Map을 1시간 주기로 자동 적재하고, Known 불량 분류, Unknown 불량 검출, UI 기반 wafer·chip 단위 불량 유형 및 sample 등록을 하나의 흐름으로 통합한 운영형 분석 체계를 구축하였다. Failbit Map과 chip 특성 이미지를 초고속으로 제공하고 overlay 및 composite map 형태로 함께 분석할 수 있는 환경도 함께 구현하였다. Failbit Map은 자연영상처럼 보이지만 실제로는 Grade 0~7과 chip 경계 등 제한된 수의 색상만 사용하므로, 본 연구에서는 이를 palette-indexed PNG로 재구성하였다. 이를 통해 RGB 대비 파일 크기를 약 65% 줄여 기존 방식으로는 불가능하였던 전 제품 대규모 적재와 AI 활용을 실현하였으며, 불량 유형별 색상 scheme 변경도 palette table 교체만으로 즉시 처리할 수 있게 되었다. 또한 기존 약 22조 row DB 반복 조회 방식을 사전 생성 chip 정보 파일 기반 즉시 참조로 전환하였다. Known 불량 분류에서는 wafer 전역의 위치·형상·배치 문맥을 해석하는 ConvNeXtV2-Base CNN을 주 모델로 사용하여 F1 0.92를 달성하였고, 국부 재확인에 강점을 가지는 ROI-YOLO는 전역 문맥만으로 분리가 어려운 저신뢰 샘플에 한해 선택적으로 추가 적용하여 최종 F1 0.95를 달성하였다(기준 0.78). Unknown 불량 검출에서는 자기지도 contrastive learning과 HDBSCAN 군집화를 결합하였으며, 웨이퍼 내 위치와 형상 배치가 공정 원인 분석의 중요한 단서라는 도메인 지식을 반영한 6×6 grid 기반 structured local sampling을 설계하였다. 실제 운영 적용 결과 13개 후보 그룹 중 7개(53.8%)가 전문가 검토에서 유효한 신규 불량 패턴으로 확인되었다. UI에서 검토·등록한 결과를 학습 데이터에 반영할 수 있도록 하여, 현업 분석이 모델 개선으로 이어지는 운영 체계를 완성하였다.

**Keywords:** Wafer Defect Analysis, Failbit Map, EDS Test, ConvNeXtV2, Grad-CAM, YOLO, Contrastive Learning, HDBSCAN, Palette PNG

---

## 1. 서론

반도체 Fab 공정 완료 후 수행되는 EDS(Electrical Die Sorting) Test는 웨이퍼 내 각 셀의 전기적 불량 여부를 개별 측정한다. 그 결과를 공간적으로 표현한 것이 Failbit Map이며, 천만 픽셀 이상의 표현력으로 불량의 위치·분포·밀집도·방향성·강도를 담은 수율 관리와 불량 원인 분석의 핵심 데이터이다 [1]. center, edge ring, local, scratch 계열 패턴은 단순한 시각적 모양이 아니라 공정 이상 원인과 직접 연결되는 공간적 의미를 가지므로, 이를 체계적으로 분류하고 해석하는 기술은 반도체 제조 현장에서 높은 실용성을 갖는다 [2].

그러나 기존 운영 환경에서 Failbit Map 분석은 구조적 한계를 안고 있었다. 수치 계측값(yield, BIN 분포)은 집계·모니터링이 가능하지만, 불량의 공간적 패턴은 Map 이미지를 직접 보아야만 파악된다. 기존 시스템에서는 Map 조회 시마다 설비 로그를 서버에서 수신하고 암호화 해제 후 이미지를 생성하는 온디맨드 방식만 지원되어 소량 조회에도 상당한 시간이 소요되었다. 대량의 Map을 초고속으로 열람하거나 다양한 measure composite를 생성하는 것도 불가능하였고, 하루에 발생하는 전 제품 wafer에 대한 대량 Map 열람은 사실상 불가능하였다. 이로 인해 불량 감지는 wafer 평균값 또는 특정 chip의 수치가 임계치를 벗어난 경우에 한해 사후 대응하는 방식에 머물렀으며, 임계치를 초과하지 않더라도 Map 상에 이미 이상 패턴이 형성되고 있는 경우를 조기에 포착할 수 없는 구조적 공백이 존재하였다. 실무자들은 관심 있는 wafer의 Map 파일을 개별 저장하고 메신저·이메일로 공유하는 비공식 방식에 의존하였으며, 분석 결과가 개인에게 귀속되어 조직 차원의 지식으로 축적되지 않는 문제도 있었다.

본 시스템 설계 과정에서 실무 요구사항 조사를 통해 네 가지 핵심 과제가 도출되었다. 첫째, 대량 Map 열람 인프라의 부재이다. 기존에는 Map 조회 시마다 설비 로그 수신→암호화 해제→이미지 생성 과정을 거치는 온디맨드 방식만 가능하여 소량 조회에도 시간이 오래 걸렸고 전 제품 wafer를 체계적으로 관찰할 수 없었다. 이에 전 제품 데이터를 주기적으로 자동 적재하고 누구나 즉시 열람·검색할 수 있는 웹 기반 분석 UI가 필요하였다. 둘째, 불량 라벨 등록의 전문가 의존성이다. 기존 라벨링 절차가 불편하여 전문가 부담이 크고 라벨 지연·오류가 누적되었다. UI 내에서 누구나 불량을 직접 등록하고, 등록된 정보가 AI 모델 학습 레이블로 자동 연결되는 워크플로우가 요구되었다. 셋째, 공정 변화나 신규 제품 도입 시 기존 클래스 체계에 없는 Unknown fail이 갑작스럽게 발생하는 경우가 있으며, closed-set 분류기만으로는 이에 대응할 수 없었다 [4]. 넷째, 분류 결과만 확인하는 것이 아니라 wafer map과 chip 계측값을 함께 조회하며 종합 분석할 수 있는 통합 UI에 대한 요구가 있었다.

초기 설계 단계에서는 Known fail 분류 모델 성능 향상이 핵심 과제라고 판단하였다. 그러나 현업 분석 담당자와의 인터뷰를 통해 실제 현장에서 더 시급한 요구사항은 전 제품 Map을 대량으로 빠르게 열람하고 자유롭게 분석할 수 있는 인프라, 그리고 기존 분류 체계에 없는 Unknown 불량을 탐지하는 기능임을 확인하였다. 이에 본 연구는 단일 분류 모델의 성능 개선을 넘어서, (1) DRAM 전 제품 Failbit Map의 1시간 주기 자동 적재 파이프라인과 웹 기반 분석 UI 구축, (2) Known fail Supervised 분류, (3) Unknown 불량 Self-Supervised 군집화, (4) UI 기반 불량 등록·검토와 AI 모델 레이블 확장을 하나의 흐름으로 연결하는 통합 구조를 설계하였다.

본 연구의 핵심 차별점은 각 설계 단계에 반도체 공정 불량 분석 지식을 직접 반영한 데 있다. Failbit Map이 전기적 검사 결과를 나타내는 이산 색상으로만 구성된다는 특성은 무손실 palette 압축의 근거가 되었고, 불량의 발생 위치와 패턴 형태가 공정 원인과 직결된다는 사실은 분류 경계 설정과 임베딩 학습 전략 설계에 반영되었다. 웨이퍼 내 방향성이 설비 레이아웃 기준으로 공정 원인을 달리한다는 점은 flip 증강을 배제하는 근거가 되었으며, 패턴 분류 이후 공정 원인을 역추적하는 데 FTN·QTN 계측값이 필수적이라는 현장 지식은 annotation 파일 설계에 반영되었다. 이는 공개 AI 모델을 wafer 데이터에 단순 적용한 것과 구별되는 본 시스템의 핵심 기여이다.

---

## 2. 제안 방법

### 2.1 데이터 생성 및 표현 계층

본 계층의 목적은 단순히 이미지를 생성하는 것이 아니라, wafer의 공간 패턴 정보와 chip-level 계측 정보를 동일 좌표계에서 결합한 공통 표현을 구축하는 데 있다. Bucket A의 raw fail-map 로그는 불량의 공간 분포를 정밀하게 담고 있지만 Measure를 포함하지 않고, Bucket B의 Measure 데이터는 FTN(Fail Total Number), QTN(Qualified Test Number), BIN, FBT, QVL과 같은 수치 정보를 제공하지만 공간 패턴 자체를 직접 보여주지 않는다. 두 소스를 정합하여 wafer image와 chip annotation 파일을 동시에 생성하면, 동일 wafer를 Known fail 분류 입력, Unknown fail 군집 검토, UI overlay, 향후 이미지-계측 multimodal 학습의 공통 샘플 단위로 재사용할 수 있다.

**FTN**과 **QTN**은 이미지 분류 이후 근인 분석을 위한 핵심 Measure 수치이다. Failbit Map 분류(CNN/YOLO)가 불량의 공간 패턴 유형을 확정하면, 엔지니어는 다음 단계로 "어떤 전기적 불량이 어떤 구조적 결함을 유발했는가"를 규명해야 한다. Failbit Map은 이 질문에 답하지 못한다 — 공간 분포만 보여줄 뿐, 전기적 원인은 담고 있지 않기 때문이다. FTN·QTN이 이 공백을 채운다. 엔지니어는 UI에서 분류 결과로 패턴 유형을 확인한 직후, chip별 FTN·QTN 값을 overlay하여 bitline 단선·wordline 단락 등 어떤 전기적 실패 메커니즘이 해당 패턴을 유발했는지 역추적한다. 즉, 본 시스템의 분석 흐름은 **Failbit Map 패턴 분류 → FTN·QTN 기반 전기적 불량 특정 → 구조적 결함 근인 확정**으로 이어진다. 이를 실시간으로 지원하기 위해 데이터 생성 단계에서 chip별 FTN·QTN·BIN·FBT·QVL을 chip annotation 파일에 사전 적재하여 DB 조회 없이 수 ms 이하 접근을 보장한다.

구현 측면에서는 Bucket A의 primary fail map raw 파일(.Z LZW 압축)과 Bucket B의 Measure 로그(.gz 압축)를 wafer 식별 규칙과 ±10초 시간 오프셋으로 자동 매칭한다. 이후 Bucket A 로그의 `X=, Y=, b=` 헤더와 뒤따르는 hex grade block을 Cython 기반 Hex 파싱으로 변환하여 chip tile array를 복원하고, Bucket B에서 읽은 FTN·QTN·BIN(`b`)·FBT(`f`)·QVL(`q`) 및 wafer-level `yield`, `sys`, `lt`, `tm`을 chip annotation 파일에 병합한다. 이 결과 분류기와 UI는 동일한 wafer 좌표계와 동일한 chip 인덱스를 공유하게 된다.

wafer map 저장 포맷으로 `32-color 8-bit palette-indexed PNG`를 채택한 배경에도 도메인 지식이 있다. 자연영상은 수천~수만 가지 색을 포함하여 palette 양자화 시 색 손실이 크지만, Failbit Map은 전기적 테스트 결과인 Grade 등급, BIN 경계, 배경, 텍스트 등 검사 결과를 표현하는 약 20개 내외의 이산 색상만 사용한다. 따라서 8-bit palette(256색) 양자화가 사실상 무손실이다. 용량 절감 원리는 픽셀 표현 방식의 차이에서 비롯된다. RGB 방식은 픽셀 1개에 3바이트를 소비한다(예: edge_loc 불량 → `(255, 0, 0)`). palette 방식은 색상표(PLTE)에 색을 한 번만 등록하고, 픽셀에는 해당 인덱스 1바이트만 저장한다(예: `1`). 픽셀 데이터가 1/3로 줄고, DEFLATE 압축 단계에서도 작은 정수 반복 스트림이 더 높은 압축률을 내므로 24-bit RGB 대비 약 65% 파일 크기 절감과 화질 완전 보존을 동시에 달성한다. PLTE 청크만 교체하면 IDAT 재압축 없이 사용자별 색상 scheme 즉시 전환도 가능하다.

### 2.2 Known fail 분류 경로 (Supervised Learning)

Known fail 분류는 16개 클래스(arc, center, cluster, donut, edge_loc, edge_ring, h_line, line, local, near_full, none, random, ring, scratch, spot, v_line) closed-set 문제로 설정하였다. 웨이퍼 맵은 자연영상처럼 경계(edge)가 명확하지 않고, 전기적 노이즈가 공간적으로 뭉쳐진 형태이다. Fine-Grained Visual Classification(FGVC) 계열 접근법을 시도하였으나, 자연영상의 텍스처·경계 구조를 가정한 방법들은 wafer map에서 성능 향상으로 이어지지 않았다. 또한 클래스 간 샘플 수 불균형이 존재하여 Focal Loss 및 class weight 조정을 시도하였으나 효과는 제한적이었다.

#### 2.2-1 CNN 기반 global classifier

EfficientNetV2, MaxViT, ViT, Swin Transformer 등 다양한 vision backbone을 동일 학습 조건에서 비교 평가하였으며, 모든 모델은 Hugging Face `timm` 라이브러리를 통해 ImageNet 사전학습 가중치로 fine-tuning하였다. 총 약 1,500개(validation 약 500개) 규모의 데이터에서 평가 결과는 Table 1과 같다.

**Table 1. Backbone 모델 비교 (Hugging Face timm fine-tuning, Val Weighted F1)**

| 모델 | 사전학습 | Input | Val F1 | 비고 |
|------|---------|:-----:|:------:|------|
| ViT-B/16 | IN-21k | 224 | 0.80 | attention 학습에 데이터 규모 부족 |
| EfficientNetV2-M | IN-1k | 224 | 0.82 | 경량 구조, 공간 패턴 표현 한계 |
| Swin-B | IN-1k | 224 | 0.83 | shifted window로 지역성 보완 |
| MaxViT-T | IN-1k | 224 | 0.84 | multi-axis attention |
| **ConvNeXtV2-Base** | **FCMAE + IN-22k** | **384** | **0.92** | **1위, 소규모 fine-tuning에서 강건** |

ViT 계열의 상대적 저성능은 데이터 규모에 기인한다. self-attention은 다양한 샘플을 통해 전역 관계를 학습해야 하나, 약 1,500개 수준의 데이터는 이를 충족하기 어렵다. 반면 ConvNeXtV2는 두 가지 이점을 가진다. 첫째, FCMAE(Fully Convolutional Masked Autoencoder)는 패치를 무작위로 마스킹하고 복원하는 자기지도 사전학습 방식으로, 전역 구조보다 국소 공간 패턴을 복원하는 능력을 강화한다 [5]. 이는 불량의 공간적 위치와 형태가 핵심 변별 요소인 wafer map에 적합한 특징 표현을 제공한다. 둘째, 384×384 입력 해상도를 기본 지원하여 scratch·local·edge 계열의 미세 구조를 보존하기에 유리하다. Optuna 기반 하이퍼파라미터 탐색(learning rate, weight decay, scheduler, dropout, label smoothing, augmentation, batch size)까지 포함한 최종 결과가 val F1 **0.92**이다. 이 단계의 역할은 wafer 전체 배치, 중심/에지 분포, 다중 영역 간 상대 위치와 같은 global spatial context를 우선적으로 해석하는 것이다.

#### 2.2-2 YOLO 기반 ROI enhancement

전역적인 배치와 공간 문맥은 CNN이 보고, chip 단위 미세 패턴은 ROI 내부 object detection으로 다시 확인하는 구조이다. 모든 샘플에 YOLO를 적용하지 않은 이유는 두 가지이다. 첫째, 연산 비용 — 매 샘플마다 object detection을 수행하면 처리량이 급격히 감소한다. 둘째, center, edge_ring, near_full 같은 패턴은 웨이퍼 전체 맵에서의 분포를 보아야 구분되며, chip 단위 local detection만으로는 판단이 불가능하다.

CNN 단계의 오분류 패턴을 분석하면 두 유형의 취약 구간이 두드러진다. 첫째, 웨이퍼 중심부에서 발생하는 center·donut·ring·spot 계열은 발생 위치가 서로 겹치고 외형도 유사하여 전역 배치만으로는 혼동이 집중된다. 둘째, edge_loc과 edge_ring, local과 random, h_line과 v_line처럼 형태가 유사하거나 발생 영역이 겹치는 클래스 쌍은 웨이퍼 전체 문맥만으로 분리하기 불충분하다. 두 경우 모두 chip 단위 미세 패턴을 별도로 확인해야 분류 정확도가 결정되며, ROI enhancement의 주요 타깃이다.

ROI 보강 적용 조건은 두 가지 중 하나를 충족할 때이다. (1) 1-stage classifier confidence < 0.80, (2) precision 또는 recall < 0.80인 difficult class로 자동 식별된 경우. 특히 낮은 confidence 구간은 실제 오분류 비율이 높은 영역이므로, 전역 패턴만으로는 class 분리가 충분하지 않은 신호로 해석하였다. 이 조건을 충족한 샘플에 대해서만 Grad-CAM [6] 기반 dynamic ROI를 추출하고, 클래스별 학습 데이터에서 사전 학습한 평균 ROI 좌표(spatial prior)와 α-블렌딩하여 heatmap 불안정성을 보완한다.

YOLO는 standalone detector가 아닌 ROI 내부의 fail 클래스 일관성을 검증하는 역할로 사용된다. 학습 손실 항목 중 `cls_loss`의 영향이 가장 결정적이었다. ROI 내부에는 fail 객체가 통상 1~2개 수준으로 존재하므로 `box_loss`(위치 회귀)와 objectness 항은 비교적 빠르게 수렴한다. 핵심 과제는 scratch, local, arc, edge 계열처럼 형태가 유사한 객체를 올바른 class로 구분하는 것이며, `cls` 가중치를 강화하였을 때 ROI correction precision과 최종 F1이 안정적으로 상승하였다.

학습 시 CNN과 YOLO 모두 좌우·상하 반전 증강을 배제하였다. wafer map에서 방향성은 공정 의미를 가지기 때문이다. 예컨대 웨이퍼 좌측에 발생한 edge_loc과 우측에 발생한 edge_loc은 외형상 flip 관계처럼 보이지만, 설비 레이아웃 기준으로 서로 다른 공정 원인을 가진다. flip 증강을 허용하면 이 구분이 불가능해진다.

**Table 2. Threshold 및 YOLO 설정**

| 항목 | 실험 범위 | 채택값 | 비고 |
|------|:---------:|:------:|------|
| Classifier confidence | 0.70 ~ 0.90 | 0.80 | 이하 시 ROI 보강 적용 |
| Difficult class threshold | 0.75 ~ 0.85 | 0.80 | precision/recall 기준 |
| YOLO cls gain | 0.5 ~ 3.0 | 1.5 | correction precision 최적 |
| YOLO confidence | 0.15 ~ 0.35 | 0.25 | false detection 억제 |
| YOLO imgsz | 512 ~ 768 | 640 | — |
| YOLO epochs | 50 ~ 150 | 100 | — |

**Table 3. Known fail 분류 성능 향상 단계**

| 단계 | 구성 | Weighted F1 |
|------|------|:-----------:|
| Baseline CNN | 초기 기준 모델 | 0.78 |
| ConvNeXtV2-Base (HF timm) | backbone 교체, 384×384, IN-22k 사전학습 | 0.85 |
| + Optuna 하이퍼파라미터 탐색 | LR·WD·scheduler·augmentation 최적화 | 0.92 |
| + ROI enhancement + YOLO | 선택적 2-stage correction | **0.95** |

### 2.3 Unknown fail 군집화 경로 (Self-Supervised Learning)

Unknown fail에 대해서는 ConvNeXtV2 backbone 기반 자기지도 대조 학습과 HDBSCAN [8] 군집화를 결합하였다. 구현 과정에서 몇 가지 설계 판단이 군집 품질에 직접 영향을 미쳤다.

**[손실 함수 선택 — SupCon vs. InfoNCE]**
초기에 Supervised Contrastive Learning(SupCon) [3]을 시험하였다. SupCon은 라벨 정보를 활용하므로 Known fail 군집은 더 밀집하게 형성되었으나, 라벨이 없는 Unknown fail 영역의 임베딩 분리도가 오히려 저하되었다. Known fail에는 유리하지만 Unknown fail에는 불리한 구조이다. 따라서 라벨에 의존하지 않는 InfoNCE(SimCLR [7] 기반) 방식을 채택하였으며, 이것이 open-set 탐지 목적에 부합함을 확인하였다.

**[Train/Test 분리에 대한 오해 해소]**
분류·검출 배경에서 접근하면 contrastive learning에도 train/test를 엄격히 분리해야 한다는 선입견이 생긴다. 그러나 contrastive learning의 목표는 클래스 정답 예측이 아니라, 유사한 샘플을 임베딩 공간에서 인접하게 배치하는 것이다. 과적합 리스크가 구조적으로 발생하지 않으므로 전체 데이터를 학습에 활용할 수 있으며, 이 방식이 임베딩 공간의 커버리지를 높여 군집 품질 향상으로 이어졌다.

**[Local InfoNCE 샘플링 전략]**
문헌에서는 random point 샘플링을 권장하지만, wafer map에서는 웨이퍼 중심(center 계열 불량 집중)과 외곽 경계(edge 계열 불량 집중) 영역이 분류적으로 중요하다. 피처 맵을 6×6 격자(grid36_full)로 균등 분할하고, 중심·외곽 주요 셀에 더 많은 앵커를 배치하는 structured sampling을 적용하였다. wafer map에서 위치 자체가 공정 의미를 가지기 때문이다. 이 구조가 random sampling 대비 Unknown fail 군집 분리도 향상에 기여하였다.

**[flip 미사용]**
외형이 유사하더라도 좌우·상하로 반전된 불량은 발생 공정 원인이 다를 수 있다. 2.2절과 동일한 원칙으로 flip 증강을 배제하고, 소규모 회전(±7°)·이동(±5%)·스케일(±5%)·가우시안 노이즈(σ=0.02)만 사용하였다.

Global InfoNCE(Queue 16K, false-negative 마스킹 sim≥0.72) + Local InfoNCE + HDBSCAN quality filter(size≥12, prob≥0.55, persist≥0.20) 조합으로 cluster 안정성을 확보하고, medoid representative를 저장하여 전문가 검토 부담을 줄였다. 최종적으로 cluster 후보를 UI에서 확인하고 신규 라벨로 등록하여 Supervised 경로에 편입하는 human-in-the-loop 루프를 구성하였다.

### 2.4 분석 UI와 불량 등록 워크플로우

본 연구의 핵심 기여 중 하나는 DRAM 전 제품 Failbit Map을 1시간 주기로 자동 적재하고, 웹 기반 분석 UI(L3 Tracker)를 통해 누구나 즉시 열람·등록·검색할 수 있는 운영 환경을 구축한 것이다. 기존에는 Map 조회 시마다 설비 로그를 수신하여 암호화 해제 후 이미지를 생성하는 온디맨드 방식만 가능하여 소량 조회에도 시간이 오래 걸렸고, measure composite 생성이나 대규모 Map의 초고속 열람도 불가능했던 것을, 1시간 주기 자동 적재와 피라미드 렌더링 기반 고속 뷰어를 통해 전 DRAM 제품의 Map을 지연 없이 확인할 수 있는 인프라로 전환하였다.

L3 Tracker는 단순 결과 표시 도구가 아니라, wafer map의 의미 인덱스 구조와 chip-level 계측값을 함께 해석하는 운영형 분석 인터페이스이다. 주요 기능은 다음과 같다. 피라미드 기반 렌더링으로 수천×수천 픽셀 wafer map을 즉각적으로 줌·팬할 수 있으며, PLTE patch 방식으로 사용자별 개인 색상 scheme을 빠르게 적용한다. chip overlay 기반 BIN/FBT/QVL 계측값 시각화와 composite map 생성을 통해 LOT 단위 또는 제품 단위의 분포 패턴을 집계 분석할 수 있다. 특히 비전문가를 포함한 모든 사용자가 UI에서 직접 wafer map 상의 불량 패턴을 선택하고 클래스를 지정하여 등록할 수 있으며, 등록된 불량 정보는 AI 분류 모델의 학습 레이블로 직접 활용된다. 이로써 사용자 검토 → 불량 등록 → 모델 레이블 확장 → 재학습으로 이어지는 human-in-the-loop 순환 구조가 완성된다.

중요한 점은 BIN, FBT, QVL이 단순 UI 표시용 값이 아니라는 것이다. 본 시스템은 이를 이미지와 함께 정합 저장함으로써 향후 이미지-계측 융합 기반 multimodal fail 분석의 학습 데이터로 직접 활용할 수 있는 자산으로 확보하였다.

**[Figure 1 삽입 권장]** 시스템 아키텍처 개념도
`EDS Test → 1시간 주기 자동 적재 → Failbit Map 생성 → image_classification (CNN+ROI+YOLO / Contrastive+HDBSCAN) → L3 Tracker UI (열람·등록·레이블 확장)`

---

## 3. 실험 결과 및 논의

**[Known fail 분류 (Supervised)]**
ConvNeXtV2-Base backbone 채택과 Optuna 기반 최적화만으로 validation weighted F1 0.92를 달성하였으며, 선택적 ROI enhancement와 YOLO 보정을 통해 0.95까지 향상되었다. YOLO 보정은 전체 샘플이 아닌 difficult class 및 low-confidence sample에만 선택적으로 적용하였다. edge_loc과 edge_ring, local과 random처럼 공간적으로 유사한 패턴 간 혼동이 주로 교정되었으며, center 부근에 밀집한 패턴 간 혼동도 chip-level YOLO 검증으로 해소되었다.

**Table 4. Confusion Matrix 개선 주요 클래스 쌍 (1단계 → 2단계)**

| Stage1 예측 | 실제 클래스 | 교정 건수 | 교정률 |
|:-----------:|:-----------:|:---------:|:------:|
| arc | ring | 35건 | 71% |
| edge_loc | edge_ring | 47건 | 68% |
| edge_ring | edge_loc | 39건 | 63% |
| local | random | 31건 | 55% |
| h_line | v_line | 19건 | 52% |

**[Unknown fail 군집화 (Self-Supervised)]**
Known fail 경로(CNN+YOLO)는 사전에 등록된 불량 클래스만을 대상으로 하는 closed-set 문제이므로 F1 등 표준 지표로 명확히 측정할 수 있다. 반면 실제 운영 환경에는 무수히 많은 유형의 Map이 존재하고 노이즈가 극심하여, 어떤 패턴이 "유효한 신규 불량"인지에 대한 Ground Truth 자체를 사전에 정의하기 어렵다. 본 시스템을 실제 운영 환경에 적용한 결과 13개 군집이 발굴되었으며, 이 중 7개에서 기존 Known fail 클래스 체계에 없는 신규 불량 패턴이 전문가에 의해 확인되었다(Figure 2). 나머지는 lot 단위 공정 이상에 의한 일시적 패턴으로 판별되어 라벨 편입 대상에서 제외되었다. 이는 본 시스템이 노이즈와 일시적 이상을 걸러내고 실질적인 신규 불량 후보만을 압축하여 전문가에게 제시하는 기능을 수행함을 보여준다.

**Table 5. HDBSCAN 파라미터 구성 비교**

| 구성 | min_cluster_size | epsilon | 군집 수 | 무시 비율 |
|------|:----------------:|:-------:|:-------:|:---------:|
| 세분화 (aggressive) | 5 | 0.02 | 多 | 낮음 |
| **채택 (기본)** | **12** | **0.06** | **적정** | **적정** |
| 보수적 (conservative) | 25 | 0.15 | 少 | 높음 |

채택된 구성(min_cluster_size=12, epsilon=0.06)은 군집 수와 무시 샘플 비율 간의 균형을 최적화한 결과이며, 현업 검토 부담과 탐지 커버리지를 동시에 고려하였다.

**Table 6. 방법론 비교**

| 항목 | 단일 CNN | CNN + K-means | 본 연구 |
|------|:--------:|:-------------:|:-------:|
| 전 제품 자동 적재 (1시간 주기) | X | X | O |
| 웹 UI 즉시 열람 | X | X | O |
| UI 기반 불량 등록 → AI 레이블 연결 | X | X | O |
| Known fail 분류 | O | O | O |
| Unknown fail 탐지 | X | △ | O |
| 라벨 오류 탐지 | X | X | O |
| 군집 수 자동 결정 | — | X | O |
| 설명 가능성 (Grad-CAM) | X | X | O |
| Weighted F1 | 0.92 | 0.92 | **0.95** |

---

## 4. 결론

본 연구는 EDS Test 결과인 Failbit Map 기반 웨이퍼 불량 분석을 위해, DRAM 전 제품 데이터의 1시간 주기 자동 적재 파이프라인 구축과 웹 분석 UI(L3 Tracker) 개발, Known fail Supervised 분류, Unknown fail Self-Supervised 군집화를 하나의 통합 구조로 연결하였다. Failbit Map이 약 20개 내외의 이산 색상만 사용한다는 도메인 특성을 활용하여 32-color palette PNG와 chip annotation 파일 기반 표현을 구축하였고, dual-bucket 로그 정합과 Cython 파싱으로 wafer image와 chip 계측값을 함께 생성하였다. L3 Tracker UI는 피라미드 렌더링 기반 고속 열람, 개인 색상 scheme, BIN/FBT/QVL overlay, composite map과 함께, 누구나 UI에서 직접 불량을 등록하고 등록된 정보가 AI 모델 학습 레이블로 자동 연결되는 human-in-the-loop 워크플로우를 제공한다. Known fail 분류 경로에서는 ConvNeXtV2와 Optuna 최적화로 F1 0.78→0.92를, 선택적 ROI enhancement와 YOLO 검증으로 0.92→0.95를 달성하였다. Unknown fail Self-Supervised 경로에서는 InfoNCE, grid36 structured local sampling, flip 미사용 원칙을 적용하여 Unknown fail 후보를 자동 군집화하고 UI 기반 전문가 검토와 신규 라벨 등록 루프를 마련하였다. 또한 BIN, FBT, QVL 계측값을 UI 시각화뿐 아니라 향후 multimodal 학습의 학습 데이터로 정합 저장함으로써 이미지-계측 융합 기반 확장 가능성을 확보하였다. 이로써 기존에 온디맨드 소량 조회에 머물던 Failbit Map 분석을 조직 차원에서 체계적으로 적재·열람·등록·분류할 수 있는 운영 기반으로 전환하였다.

향후 연구로는 칩 레벨 다중 라벨 분류 확장, Failbit Map+Measure multimodal fail 분석 모델 설계, 전체 제품군으로의 일반화 검증을 계획하고 있다.

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
