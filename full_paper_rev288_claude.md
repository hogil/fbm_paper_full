# Failbit Map Known & Unknown 불량 분석 아키텍처

**Hybrid Failbit Map Analysis Architecture for Known Classification and Unknown Discovery**

최호길<sup>1</sup>, 홍지훈<sup>1</sup>, 김성호<sup>2</sup>

<sup>1</sup> 메모리사업부 메모리제조기술센터 QIE그룹, Samsung Electronics
<sup>2</sup> 메모리사업부 메모리제조기술센터 DRAM YE팀, Samsung Electronics

---

**Abstract** - **Failbit Map은 반도체 EDS Test에서 생성되는 웨이퍼당 약 1,000만 pixel 수준의 초고해상도 데이터로, 불량 패턴 분석의 핵심 자료이다. 그러나 실제 현업에서는 대량의 Failbit Map 조회가 어렵고, 조회 가능한 일부 Map의 분석도 엔지니어 수작업에 의존한다. 본 논문은 이를 해결하기 위해 대량 Failbit Map 데이터 파이프라인을 구축하고, 기존 고질 불량은 2-stage supervised classification으로 분류하고, 신규 후보 패턴은 self-supervised embedding과 HDBSCAN을 이용해 유사한 Failbit Map끼리 묶어 Unknown failure 후보 그룹을 도출하였다. 변환 속도는 Cython 적용으로 약 100배 향상되었고, 이미지는 24-bit RGB 대신 8-bit palette-indexed PNG로 저장해 실제 저장 파일 기준 용량을 약 80% 줄였다. 기존 불량 분류는 ConvNeXtV2 기반 1차 분류와 low confidence sample에 대한 ROI(Region of Interest) 기반 YOLO 2차 분류를 결합한 구조로 설계하였으며, weighted F1 score 0.95를 달성하였다. 신규 후보 패턴 검출에서는 작은 불량 영역이 wafer 전체 평균에 묻히지 않도록 대조학습(InfoNCE) embedding에 grid별 local loss를 추가하였다. 별도 1일치 2,000장의 실제 wafer 이미지에 적용한 결과, 13개 Unknown failure 후보 그룹이 도출되었고, 이 중 7개가 현업 엔지니어 확인에서 실제 불량 그룹으로 확인되었다. 실제 chip에서는 둘 이상의 불량이 겹치는 경우가 있어, 단일 불량 분류 방식으로는 충분히 구분하기 어렵다. 이를 보완하기 위해 chip multi-label 분류 구조를 추가하였다. 중복 불량 라벨을 충분히 확보하기 어려워, 단일 불량 chip 라벨을 학습 원천으로 사용했다. FCM-PM(Full-Cover CutMix with Pair Mask)은 별도 2-combo 합성 평가셋에서 bit-F1 score 0.9927과 FAR(False Alarm Rate) 0.00%를 얻었다.**

**Keywords:** Wafer Failure Analysis, Failbit Map, EDS Test, ConvNeXtV2, ROI-YOLO, Object-ID Map, Contrastive Learning, HDBSCAN, Palette PNG, Multi-label Classification, CutMix

## 1. 서론

### 1.1. 배경, 문제, 기여

DRAM(Dynamic Random Access Memory)은 데이터를 저장하는 최소 단위인 cell과, 다수 cell이 배열된 cell array로 구성된다. 양산 라인은 EDS(Electrical Die Sorting) 검사에서 cell array의 동작 여부와 전기적 특성을 측정한다. array 안에서 발생한 cell fail 수를 Grade 0(정상)부터 7(최대 불량)까지로 양자화하고, 이를 wafer 좌표에 배치한 것이 Failbit Map(FBM)이다. EDS는 chip별 measure value도 함께 산출하며, 현업에서는 이 수치로 chip 불량을 우선 분석한다. Failbit Map은 해당 불량의 wafer 내 위치와 공간 분포를 제공한다. cell에서 Failbit Map까지의 관계는 Figure 1에 정리하였다.

![DRAM cell에서 Failbit Map까지](figures/full_paper_rev260/fig01_dram_to_fbm.png)

**Figure 1.** From DRAM cell to Failbit Map. EDS counts failed cells in the cell array, converts the count into Grade 0-7, and places the grades on wafer coordinates.

Failbit Map은 불량률 숫자만으로는 보이지 않는 위치 정보를 담고 있다. 같은 불량률이라도 불량이 가장자리에 분포하는지, 중앙에 밀집하는지, 한 방향으로 편중되는지에 따라 우선 확인해야 할 설비와 공정 조건이 달라진다(Figure 2). measure value로 chip별 불량 일부는 빠르게 확인할 수 있지만, wafer 안에서 불량이 어디에 어떤 형태로 나타나는지는 Failbit Map을 분석해야 확인된다.

![Failbit Map examples](figures/full_paper_rev260/fig02_fbm_examples.png)

**Figure 2.** Examples of Failbit Map patterns. The same measure value level can correspond to different spatial patterns such as center cluster, edge ring, or broken ring.

당시 환경에서는 Failbit Map을 한 번에 소수만 조회할 수 있었고, 대량 이미지의 장기 저장이 어려워 이미지 기반 분석으로 이어지지 못했다. 기존에는 담당자가 chip별 measure value로 불량 여부를 확인하고, 수식과 임계값 기반 rule을 정의해 고질 불량을 분류해 왔다. 이 방식은 빠르고 근거가 분명했지만, 담당자가 정의한 rule에 의존하는 한계가 있었다. 또한 chip별 수치만 보면 주변 chip과의 관계, wafer 안의 위치, 불량 형태 같은 공간 정보를 함께 보기 어렵다. 이 정보가 없으면 우선 확인해야 할 공정 조건을 정하기 어렵다. 같은 fail rate라도 edge-ring, center-cluster, directional pattern은 원인이 다를 수 있어 Failbit Map 확인이 필요하다. 불량으로 분류된 wafer는 Failbit Map이나 TEM(Transmission Electron Microscopy)으로 시료를 잘라 CD(Critical Dimension)나 misalignment 같은 pattern을 확인하고 공정 structure와 layout 원인을 해석했다. 문제는 대량의 Failbit Map을 빠르게 생성하고 필요한 wafer를 즉시 조회하기 어렵다는 점이다.

Failbit Map의 불량은 두 종류로 나뉜다. 하나는 학습할 수 있는 기존 고질 불량(Known failure)이고, 다른 하나는 등록되지 않은 신규 발생 불량(Unknown failure)이다. 기존 불량은 16-class 라벨 체계 안에서 지도학습으로 분류할 수 있다. 신규 불량은 정답 라벨이 없으므로 지도학습을 적용할 수 없고, F1 score 같은 분류 성능 지표로 바로 평가하기도 어렵다.

본 논문은 대량 Failbit Map 처리의 병목과 수작업 불량 판정 의존 문제를 함께 다룬다. 이를 위해 raw log를 Failbit Map 이미지와 chip annotation으로 변환하고, chip별 measure value와 연계해 조회할 수 있는 데이터 구조를 구축하였다. 적용 후에는 1시간 주기로 FBM을 만들어 화면에서 확인할 수 있도록 구성하였다. 기존 불량은 1차 분류 결과의 confidence가 낮은 sample만 ROI-YOLO로 재확인하는 2-stage 구조로 검증했고, chip 좌표를 쓰는 Stage-2 대안은 생성 데이터에서 별도로 평가했다. HDBSCAN 군집화로 후보 그룹을 도출하고, 현업 엔지니어가 신규 불량 후보를 우선 확인할 수 있도록 구성하였다. 한 chip에 불량이 둘 이상 겹치는 경우는 chip multi-label 문제로 별도 정의하였다.

전체 작업은 데이터 파이프라인, Known failure 분류 및 재확인, Unknown 후보 그룹 도출, chip multi-label, web viewer로 나눌 수 있다. 첫째, 대량 Failbit Map을 빠르게 생성하고 필요한 wafer를 조회할 수 있는 데이터 파이프라인을 구축했다. 둘째, Known failure는 low confidence sample만 ROI-YOLO로 재확인하는 2-stage 구조로 검증했다. 셋째, Unknown failure는 self-supervised embedding과 HDBSCAN으로 후보 그룹을 도출하였다. 넷째, 중복 불량 chip을 위해 chip multi-label 구조를 추가했다. 다섯째, web viewer에서 map, chip overlay, measure value를 함께 확인하고 신규 불량 등록까지 이어지도록 구성했다.

### 1.2. 관련 연구

기존 연구에서도 wafer map image를 CNN으로 분류하거나 selective learning을 적용한 사례가 있었고 [1][2], wafer-level 라벨로 chip 불량을 추정하거나 혼합형 bin map을 분류한 연구도 있었다 [3][4]. 라벨 없는 패턴 탐색은 대조 학습, open-set recognition, deep clustering 계열로 이어졌다 [5]-[9]. 모델 규모와 효율 관점은 vision backbone 비교 연구를 참고했고 [10], 검출 기반 재확인은 Faster R-CNN과 Cascade R-CNN을 기본 참조로 두었다 [11][12]. HDBSCAN은 density-based clustering의 구현 기반이다 [13]. Known 분류 backbone은 ConvNeXtV2를 사용했고 [14], YOLO detector 계열과 최신 구현은 ROI-YOLO 비교 근거로 참고했다 [15][16]. object-id map의 categorical class 표현은 categorical embedding 연구를 참고했다 [17]. 이 논문은 공개 데이터셋 성능 비교보다 현업 Failbit Map 처리, wafer 조회, Known/Unknown 분석 연결에 초점을 둔다. 기존 연구와의 차이는 Table 1에 정리하였다.

**Table 1. Difference from prior wafer map studies.**

| 비교 축 | 기존 wafer map 연구 | 본 논문 |
|------|------|------|
| 데이터 단위 | wafer image 또는 bin map 중심 | Failbit Map, chip 좌표, measure value 연결 |
| 불량 분석 | 단일 분류 또는 군집화 중심 | Known 분류와 Unknown 후보 그룹 분리 |
| chip 재확인 | detector 또는 wafer-level 판정 중심 | ROI-YOLO와 object-id map 대안 비교 |
| 중복 불량 | 실제 mixed label 또는 단일 label 중심 | FCM-PM과 val_margin으로 2-combo 검증 |
| 현업 사용 | 실험 결과 중심 | web viewer와 운영 성과까지 연결 |

## 2. 본론

### 2.1. 제안 방법

전체 구조는 Failbit Map 생성, Known failure 분류, Unknown failure 후보 그룹화, chip multi-label, web viewer로 나누었다. Table 2는 전체 구조와 각 단계의 역할을 요약한다.

**Table 2. Main components of the proposed method.**

| Component | Method | Role |
|------|------|------|
| Failbit Map generation | raw log 변환, palette PNG 저장, chip 좌표 정렬 | map 생성과 chip 정보 정렬 |
| Known failure | ConvNeXtV2, selective ROI-YOLO | 기존 불량 분류와 재확인 |
| Stage-2 follow-up | object-id map | chip 좌표 fixed-crop 대체 가능성 확인 |
| Unknown failure | contrastive embedding, HDBSCAN | 신규 후보 그룹 도출 |
| Chip multi-label | FCM-PM, val_margin, NB reject | 중복 불량 chip 분류 |
| Web viewer | search, overlay, measurement view | 담당자 확인 화면 |

전체 데이터 흐름은 다음과 같다(Figure 3).

![좌표 보존 분석 파이프라인](figures/full_paper_rev260/fig02_pipeline_architecture.png)

**Figure 3.** Coordinate-preserving analysis pipeline. EDS raw logs and measure values are aligned with the Failbit Map and chip coordinates, then used by Known, Unknown, and chip multi-label paths. Confirmed cases can be stored as future training data.

Figure 3은 Failbit Map 생성 이후 Known, Unknown, chip multi-label 경로로 나뉘는 흐름을 보인다.


#### 2.1.1. 데이터 표현과 정합 적재

데이터 병목은 변환 속도와 저장 용량 두 곳에서 나타났다. wafer 한 장은 약 1천만 픽셀이고 하루 약 2만 매가 유입되므로, raw hex 페이로드는 Cython 파서로 복원해 순수 Python 대비 약 100배 빠르게 처리했다(Figure 4a). 저장 용량도 주요 제약이었다. Failbit Map에서 실제로 쓰는 색상은 약 20개 수준이지만 32-entry palette table 안에서 관리할 수 있다. 이에 24-bit RGB 대신 8-bit palette PNG로 저장했다(Figure 4b). 실제 저장 파일 기준으로는 RGB 저장 대비 약 80% 감소했다. 색상 scheme은 PLTE(PNG palette) 청크 교체만으로 변경할 수 있다. 압축률이 더 높은 무손실 방식도 검토할 수 있으나 처리 시간이 길어져 1시간 주기 생성에 불리하다. JPEG는 손실 압축 때문에 grade 색이 혼합될 수 있어 제외했다. 학습 입력에서도 grade 색이 그대로 유지되어야 모델이 실제 불량 패턴만 학습한다. Failbit Map raw log와 chip별 measure value는 wafer 식별자와 ±10초 오프셋으로 매칭하고, 같은 wafer와 chip 좌표 기준으로 저장했다. 이와 같이 적재한 데이터는 동일 wafer 기준의 화면 표시와 모델 입력에 함께 사용된다.

![Cython parser and palette PNG](figures/full_paper_rev260/fig04_cython_palette.png)

**Figure 4.** Cython parser and palette-indexed PNG. (a) Hex-to-grade conversion is accelerated by Cython. (b) Palette PNG stores grade colors as indices instead of RGB triples, reducing storage while preserving grade values.

#### 2.1.2. Known failure 분류 구조

**Backbone 선정 및 단계별 구성은 다음과 같다.** Known failure는 주요 반복 불량 16개 class, 약 1,500장의 labeled Failbit Map, 4:1 stratified split으로 학습했다. backbone은 ConvNeXtV2-Base를 사용했다. 이후 learning rate, weight decay, focal loss, class weight를 조정해 1-stage 분류기를 구성하고, 마지막에는 low confidence sample에만 ROI-YOLO 2-stage를 적용했다. 성능 변화는 Table 5에 따로 정리했다.

**ROI-YOLO 2-stage 보정.** 1차 CNN의 confidence가 낮은 sample은 class 경계가 애매하거나 불량 영역이 작아 wafer 전체 이미지에서는 근거가 약한 경우가 많았다. 해당 sample에 한해 ROI-YOLO로 재확인하였다(Figure 5). 모든 wafer에 검출 모델을 적용하지 않고, 1차 분류에서 low confidence인 경우만 2차 분류하도록 했다.

실제 적용 기준은 1-stage 예측 confidence 0.70 미만으로 두었다. 나머지 wafer는 Stage 2를 생략한다.

![ROI-YOLO 2-stage 검출](figures/full_paper_rev260/fig03_roi_yolo.png)

**Figure 5.** ROI-YOLO 2-stage check. Panels show (a) the Failbit Map, (b) the ROI region set by the class prior (blue circle) with YOLO detection boxes inside (red), and (c) the detected chip's scratch detail (confidence 0.91). Failures that look small and scattered globally become distinct under ROI-limited detection and chip-level inspection, while regions outside the ROI are skipped.

**chip-CNN object-id map.** 현재 검증된 Known failure 구조는 CNN 1차 분류 뒤 low confidence sample만 ROI-YOLO로 재확인하는 2-stage다. object-id map은 이 Stage-2를 detector가 아니라 chip 좌표 기반 fixed-crop 분류로 변경하는 개발 항목이다. ROI-YOLO는 ROI 안에서 object를 찾기 위해 여러 후보 box와 crop을 평가하고 NMS를 수행한다. 반면 object-id map은 제품 layout에 이미 있는 chip 좌표를 사용해 각 chip을 fixed crop으로 추출하고, class 예측 결과를 wafer grid에 표시한다(Figure 6). 생성 데이터에서는 raw Failbit Map보다 class 구분이 분명했고, 계산량은 ROI-YOLO 대비 낮았다.

![raw와 object-id map 구분력 비교](figures/full_paper_rev260/fig_objid_compare.png)

**Figure 6.** Class separability of raw Failbit Map vs object-id map. Generated examples show improved class separability in object-id maps, where each chip crop class is rendered as color. [Generated data only, under development]

Table 3은 ROI-YOLO와 object-id map의 Stage-2 연산량을 비교한다. object-id map은 Stage-2에서 detector 대신 chip 좌표 기반 fixed crop을 쓰도록 설계했다. 이 구조에서 chip-CNN은 약 1.16 million parameters, 약 0.31 GFLOPs로 계산되며, 공개 YOLO11x의 194.9 GFLOPs 대비 약 1/600 수준이다.[^1] 생성 평가셋의 분류 성능은 Table 6에 따로 정리했다.

**Table 3. Stage-2 computation of ROI-YOLO and chip-CNN object-id map. The table reports parameter count and calculated GFLOPs only; classification results are listed in Table 6.**

| Stage-2 method | Parameters | Operations |
|------|:--:|:--:|
| ROI-YOLO detector | 56.9 million | 194.9 GFLOPs |
| chip-CNN object-id map | 1.16 million | 0.31 GFLOPs |


#### 2.1.3. Unknown failure 군집화 구조

실제 데이터에서는 기존 16-class에 포함되지 않는 신규 불량이 드물게 나타나며 정답 라벨이 거의 없다. 지도 대조학습(SupCon[5])은 새 패턴을 기존 class로 흡수할 위험이 있어, 라벨에 종속되지 않는 contrastive embedding을 학습하였다(Figure 7). 초기 구현은 InfoNCE(Information Noise-Contrastive Estimation) loss와 MoCo(Momentum Contrast)[18] queue(4096)로 작은 batch의 negative 부족 문제를 보완했다.

학습된 embedding은 HDBSCAN으로 군집화한다. HDBSCAN 군집화 결과는 web viewer에 후보 그룹으로 표시하여, 현업 엔지니어가 신규 불량 후보를 우선 확인할 수 있도록 구성하였다. 최종 개발 구성에서는 queue 크기를 16K로 확장한 global/local contrastive loss를 쓰고, noise wafer는 최근접 이웃 투표가 임계를 넘을 때만 그룹에 포함했다. 불량 누락이 false alarm보다 위험하므로 누락을 줄이는 것을 우선 기준으로 두었다.

![Unknown failure embedding flow](figures/full_paper_rev260/fig05_unknown_flow.png)

**Figure 7.** Unknown failure embedding flow. Augmented views of the same FBM are kept close in the embedding space, while a different FBM is separated; HDBSCAN then groups the embeddings for engineer confirmation.

#### 2.1.4. chip 수준 multi-label 분류 구조

Failbit Map에서 잘라낸 chip 단위 이미지에는 둘 이상의 failure가 함께 나타나는 경우가 있다. 단일 failure class만 선택하는 단일-label 방식으로는 이런 chip을 제대로 분석하기 어렵다. 이에 따라 chip multi-label 분석 구조를 별도로 개발하였다. 학습과 평가는 bank_boundary, fork, scratch, scratch_rot 4개 class를 독립 sigmoid 출력으로 표현했다(Figure 8). 이때 한 chip 안에 두 class가 함께 나타나는 2-combo를 softmax 단일 class가 아니라 multi-label 문제로 정의했다. 다만 실제 2-combo 정답 라벨은 충분히 확보하기 어렵다.

원천 데이터는 현업 EDS Failbit Map에서 얻은 single failure 4종(bank_boundary, fork, scratch, scratch_rot) chip이다. 학습은 single failure chip 라벨만 사용했다. 2-combo 평가는 single failure chip에서 확인한 위치와 Grade 확률분포를 이용해 별도로 합성했고, 평가셋은 single 4종, 2-combo 6종, Normal, Invalid, OOD(out-of-distribution) noise chip으로 구성하였다. 학습 중에는 FCM-PM이 single 원천 chip으로 2-combo 학습 신호를 구성하고, 평가는 사전에 구성한 single 및 2-combo 합성 평가셋으로 수행한다. backbone은 ConvNeXtV2(FCMAE 사전학습)를 chip 이미지에 맞게 재학습했고, head는 클래스별 독립 sigmoid 확률을 출력한다.

![chip 라벨 공간 예시](figures/full_paper_rev260/fig05_chip_label_space.png)

**Figure 8.** Label space of chip-level multi-label classification. Top row: four single failures with distinct shapes (bank_boundary, fork, scratch, scratch_rot). Bottom row: a synthetic 2-combo example and negative samples used in the controlled benchmark (Normal, Invalid, OOD/Starburst). [Real chip source + domain synthesis]

합성은 원본 Grade를 보존하는 방식으로 한정하였다. Grade 0~7은 discrete value이므로 Mixup처럼 색상을 평균하면 실제로 존재하지 않는 중간 Grade가 생성된다. Diffusion은 충분한 라벨과 큰 연산 자원이 필요해 본 문제에 적합하지 않았다. 따라서 원래 Grade 값을 영역 단위로 보존하는 CutMix[19] 계열을 택했다. 다만 random rectangle CutMix만 쓰면 불량 영역이 잘리거나, 합성 후 남는 background가 false-positive 신호로 학습될 수 있다.

학습에서는 single-failure chip source만 사용하고, FCM-PM으로 두 failure가 함께 있는 학습 신호를 구성하였다. FCM-PM은 두 single-failure chip을 full-cover 방식으로 합쳐 A+B mixed chip을 만들고, 동시에 A-only와 B-only masked view를 함께 학습한다(Figure 9). mixed view는 두 failure가 함께 있을 때의 positive 학습 신호를 제공하고, masked view는 합성 과정에서 생긴 background가 false-positive signal로 학습되지 않도록 한다. false alarm rate(FAR)는 negative 중 오검출 비율(FP_neg/N_neg)로 계산하고, checkpoint는 validation에서 val_margin = mean(p_pos) - max(p_neg)이 가장 큰 epoch로 선택한다.

손실 함수 변경만으로는 충분하지 않았다. Focal과 ASL[20]은 일부 positive 반응을 유지했지만, negative sample tail을 충분히 억제하지 못했다. 특히 single-only 학습에서는 2-combo의 두 번째 bit의 positive probability가 낮게 유지되어 평균 0.42 수준까지 내려갔다. FCM은 두 single source가 chip 전체 영역을 덮도록 합성해 두 번째 bit의 평균 positive probability를 약 0.54까지 높였다. 반대로 Pair Mask는 합성 과정에서 생긴 background가 불량 신호로 학습되는 것을 막았다. 그 뒤에는 val_margin으로 positive와 negative 간격이 가장 넓은 checkpoint를 고르고(Figure 10a), Gaussian Naive Bayes reject로 4-bit probability shape가 등록 profile과 맞지 않는 OOD 형태의 probability profile을 제외하였다(Figure 10b). ensemble은 단일 모델 과적합 여부를 확인하기 위한 비교로 두었고, Knowledge Distillation student[21]는 경량화 후보로 두었다.

![FCM-PM augmentation](figures/full_paper_rev260/fig06_fcm_pm.png)

**Figure 9.** FCM-PM augmentation for chip multi-label learning. Full-Cover CutMix makes A+B mixed views, while Pair Mask trains A-only/B-only views to suppress synthetic-background false positives. [Real chip source + domain synthesis]


![val_margin selection and NB reject sidecar](figures/full_paper_rev260/fig07_probability_control.png)

**Figure 10.** Probability control in chip multi-label learning. (a) val_margin selects the checkpoint whose probability gap tracks hold-out bit-F1 score better than val-F1 score. (b) NB reject checks the whole 4-bit probability profile and rejects an OOD-shaped vector when no known profile matches. [Real chip source + domain synthesis]



#### 2.1.5. 분석 화면(web viewer) 구조

web viewer는 생성된 Failbit Map을 pyramid tile 형태로 불러와 대형 wafer map에서도 화면 이동과 확대/축소가 지연 없이 동작하도록 구성하였다. 담당자는 같은 화면에서 wafer map, chip overlay, chip별 measure value, 후보 그룹을 함께 확인한다. 신규 불량으로 남길 필요가 있는 경우에는 해당 wafer와 chip 정보를 등록해 이후 학습 데이터 구성에 사용할 수 있도록 했다.

### 2.2. 결과 및 운영 적용

#### 2.2.1. 결과 범위

Table 4는 각 수치의 산출 조건과 적용 범위를 구분하여 정리하였다. 운영 수치와 모델 성능 지표는 합산하지 않았다.

**Table 4. Validation scope of reported results.**

| Item | Value | Scope |
|------|------|------|
| Known | weighted F1 score 0.95 | 현업 데이터 검증 |
| Unknown | 13개 후보 그룹 / 7개 실제 불량 그룹 | 현업 엔지니어 확인 |
| object-id | val/hold-out F1 score 0.9946 / 0.9872 | 생성 데이터 기반 검증 |
| FCM-PM | bit-F1 score 0.9927 / Total FAR 0.00% | 조건을 통제한 합성 평가 |
| FBM gen./storage | ~100× / ~80% file-size reduction | 내부 측정 |
| Impact | KRW 12.3B | 내부 성과 인증 |

#### 2.2.2. Known failure 결과

Table 5는 같은 split에서 backbone, fine-tuning, selective ROI-YOLO를 순서대로 비교한 결과다. 표 안에 pre-train과 tuning을 함께 표기하여, fine-tuning과 2-stage 적용에 따른 F1 score 변화를 함께 표시했다.

**Table 5. Backbone comparison and staged improvements for Known failure classification (16-class, weighted F1 score on internal data split).**

| Model / stage | Setting | F1 score |
|------|------|:------:|
| Baseline CNN | ImageNet pretrain | 0.78 |
| ViT-Base/16 | IN-21k fine-tune | 0.81 |
| Swin-Base | IN-1k fine-tune | 0.84 |
| EfficientNetV2-M | IN-1k fine-tune | 0.85 |
| MaxViT-Base | IN-21k fine-tune | 0.87 |
| ConvNeXtV2-Base | FCMAE + IN-22k fine-tune | 0.87 |
| ConvNeXtV2 + HPO | lr, weight decay, focal loss, class weight | 0.92 |
| ConvNeXtV2 + HPO + ROI-YOLO | low confidence sample 2-stage | 0.95 |

MaxViT-Base와 ConvNeXtV2-Base는 같은 weighted F1 score 0.87을 보였지만, ConvNeXtV2-Base는 parameters가 119.5M에서 88.6M으로 약 26% 작고 FLOPs도 74.2G에서 45.1G로 약 39% 낮아 최종 backbone으로 선택했다. 이후 HPO로 0.92까지 향상되었고, ROI-YOLO는 confidence가 낮은 sample에만 적용해 최종 0.95를 얻었다.

Table 6은 object-id map의 생성 데이터 개발값만 정리한다.[^2]

**Table 6. Object-id map development metrics for Known Stage-2 follow-up. [생성 데이터 기반 검증]**

| 입력 구성 | 확인 값 | Scope |
|------|------|:------:|
| Selected obj-only | val F1 score 0.9946 / hold-out F1 score 0.9872 | 생성 데이터 기반 검증 |

#### 2.2.3. Unknown failure 결과

13개 후보 그룹 중 7개가 실제 불량으로 확인된 결과는 분류 정밀도로 해석하지 않았다. 정답 라벨이 없는 실제 wafer 이미지 2,000장에 self-supervised embedding과 HDBSCAN을 적용하여 13개 Unknown failure 후보 그룹을 도출하였다. 현업 엔지니어 확인 결과, 이 중 7개가 실제 불량 그룹으로 확인되었다(Table 4).

정답 라벨이 있는 별도 생성 데이터 기반 평가셋에서는 대조학습 구성과 queue, negative 보강을 단계적으로 적용해 성능을 확인했다(Table 7). 단순 backbone보다 불량 후보가 noise로 분리되는 비율이 줄었고, 최종 구성은 생성 평가셋에서 가장 높은 Completeness를 보였다. Completeness는 생성 데이터에서 군집 분리 정도를 평가하는 개발 지표이며, 운영 Unknown 결과와 합산하지 않는다.

**Table 7. Component-isolation benchmark for Unknown clustering. [생성 데이터 기반 검증]**

| Recipe | Capture | Noise(%) | Completeness | n_cluster |
|------|:------:|:------:|:------:|:------:|
| Global contrastive only | 0.9337 | 15.78 | 0.9468 | 40 |
| + Local DenseCL | 0.9361 | 13.87 | 0.9502 | 37 |
| + MoCo Queue | 0.9356 | 9.45 | 0.9474 | 41 |
| + NV-Retriever NEG | 0.9250 | 8.23 | 0.9485 | 40 |
| + NeCo (5-tool) | 0.9559 | 6.66 | 0.9660 | 35 |
| 최종 + tau=0.5 후처리 | 0.9619 | 0.00 | 0.9679 | 35 |

#### 2.2.4. chip multi-label 결과

Table 8은 위 설계 선택을 수치로 확인한 결과다. BCE+label smoothing, Focal[22], ASL[20]은 FAR를 안정적으로 억제하지 못했고, 단순 CutMix에서도 false alarm이 높은 수준으로 유지되었다. Pair Mask를 더하면서 FAR가 감소하였고, FCM-PM과 val_margin을 결합한 단일 모델을 조건을 통제한 합성 평가의 최종 recipe로 채택했다. ensemble은 단일 모델의 과적합 여부를 확인하는 비교군으로 두었다. 성능은 소폭 향상되었지만 비용이 약 5배여서 최종 구성에서는 제외했고, Knowledge Distillation student는 경량화 후보로 분류하였다.

**Table 8. Stage-wise performance of chip multi-label training recipes (2,000 per positive class). Evaluation uses real failure-chip sources and domain probability-distribution synthesis; not a production deployment result.**

| Recipe | bit-F1 / single / 2-combo | Total FAR |
|--------|:--:|:--:|
| BCE | 0.1093 / 0.1896 / 0.0668 | 99.47% |
| Focal | 0.7980 / 0.8724 / 0.7050 | 45.72% |
| ASL | 0.6435 / 0.5379 / 0.7320 | 100% |
| CutMix | 0.9359 / 0.9566 / 0.9070 | 42.05% |
| CutMix + Pair Mask | 0.9491 / 0.9728 / 0.9281 | 24.62% |
| FCM-PM + val_f1 | 0.9652 / 1.0000 / 0.9517 | 0.15% |
| FCM-PM + val_margin | 0.9927 / 0.9996 / 0.9871 | 0.00% |
| Ensemble | 0.9956 / 1.0000 / 0.9921 | 0.00% |
| Knowledge Distillation student | 0.9799 / 1.0000 / 0.9638 | 0.00% |

합성 평가 ablation에서 Pair Mask를 제거하면(다른 모든 설정, reject 게이트 동일) 합성 과정에서 남은 background를 불량으로 잘못 학습해 Total FAR가 0.00%에서 100%로 증가하였다. 이 비교에서는 reject 게이트가 아니라 Pair Mask가 false alarm 억제에 직접 기여했음을 확인하였다.

여기서 bit-F1 score는 한 chip 라벨을 클래스 수만큼의 bit vector로 보고 각 bit를 독립 측정해 micro-average한 값으로, positive 집합은 single 4종과 2-combo 6종을 포함한다. Total FAR 0.00%는 Normal, Invalid와 OOD 4종을 합한 negative 약 2,640 chip에서 오검출이 없던 값이다. 단일 불량 라벨만 있는 조건을 모사한 설정에서 중복 불량을 구분하며 FAR를 낮춘 방법론 검증이며, 본 수치는 조건을 통제한 합성 평가 범위로 한정한다.

#### 2.2.5. 시스템, 운영 결과

구축한 viewer/data pipeline은 2025년부터 DRAM D1a/b/c/d 전제품의 FBM을 생성하는 데 사용된다. 담당자는 이 화면에서 wafer ID를 검색하고, map overlay와 composite, chip별 계측값을 확인한다(Figure 11). 필요하면 신규 불량으로 등록한다. 여기서 사용 범위는 FBM 생성, 화면 조회, overlay, composite까지이며, Known/Unknown/chip model serving이나 object-id map 양산 적용 완료를 의미하지 않는다. 적용 후 확인 범위는 기존 약 48매 단위에서 하루 약 2만 wafer 수준으로 넓어졌다(Table 9). 이 전환으로 분석 공수가 약 90% 줄었고, HBM 제품 사례에서는 수율이 약 0.02%p 개선됐으며, 메모리제조기술센터 내부 성과 인정 기준 약 123억 규모의 성과로 인정받았다.[^3] 이 정량 기여는 DRAM viewer/data pipeline 기준으로 한정한다. 따라서 Table 5~8의 모델 성능 지표와 합산하지 않았다.

**Table 9. Change in FBM review after viewer/data pipeline deployment.**

| 항목 | 이전 방식 | 적용 후 |
|------|------|------|
| 조회 규모 | 약 48매 확인 | 하루 약 2만 wafer 확인 |
| 확인 항목 | map과 계측값 별도 확인 | overlay, composite, chip 계측값 동시 확인 |
| 신규 불량 관리 | 담당자별 기록 | web viewer에서 등록 이력 확인 |

![single wafer view](figures/full_paper_rev260/fig09_webapp_viewer.png) ![grid view](figures/full_paper_rev260/fig11b_webapp_grid.png)

**Figure 11.** Screenshot of the deployed web viewer. (a) single wafer view with chip overlay and measurement panel; (b) grid view of Unknown candidate clusters. Search, map view, overlay, measurement, and navigator thumbnails are integrated in one screen.

### 2.3. 논의 및 한계

본 연구의 독창성은 기존 모델을 단순히 적용한 데 있지 않다. Known failure 경로에서는 ConvNeXtV2의 전역 판정 결과를 그대로 끝내지 않고, low confidence sample만 ROI-YOLO로 재확인하는 selective 2-stage 구조를 구성하였다. 또한 object-id map은 ROI-YOLO를 작은 모델로 대체하려는 접근이 아니라, 제품 layout으로 이미 주어진 chip 좌표를 사용해 box search, regression, NMS 부담을 줄이고 chip class id를 wafer grid에 되돌리는 문제 정의 전환이다. chip multi-label에서는 실제 2-combo label이 부족한 조건에서 FCM-PM으로 single failure chip 원천만 사용해 중복 불량 학습 신호를 만들었고, val_margin과 NB reject로 weak positive와 false alarm을 함께 제어하였다.

생성 데이터와 합성 평가셋의 결과는 실제 wafer 적용 결과와 구분했다. 공개 wafer 데이터는 die 단위 bin map이어서 chip 안의 불량 모양과 계측값을 함께 보는 이 작업과 직접 비교하기 어렵다.

**제외한 설계와 근거.** 채택하지 않은 항목은 별도 측정 후 제외하였다. Unknown failure는 구성요소 제거 실험으로 불필요한 요소를 제외했고(2.1.3), 사전학습 backbone을 더 많이 fine-tuning하는 설정은 소규모 데이터에서 학습이 불안정해져 배제하였다. Isotonic 보정은 in-sample F1 score 0.9931로 높았으나 별도 검증 기준에서 과적합으로 판단했다.

**평가 조건.** 비교마다 입력 조건과 최적 모델 선정 기준을 동일하게 유지하였다.

### 2.4. 향후 연구

다음 단계는 적용 제품과 분석 단위를 확장하는 것이다. bin map과 chip multi-label 분석으로의 확장에 대해 Flash YE에서도 적용 가능성을 문의받았으며, 실제 적용은 데이터 권한과 제품 차이를 확인한 뒤 별도 과제로 진행한다. 원인 분석 측면에서는 wafer 이미지와 chip별 계측값을 한 화면에서 함께 보며 근거를 남기는 기능을 보강한다. 대조 임베딩은 과거 유사 사례와 엔지니어 기록을 찾는 검색 인덱스로 확장할 수 있다. 이미지, trend, 이력 정보를 요약하는 large language model 기반 기능은 담당자 승인과 이력 기록을 전제로 한 보조 기능으로 제한한다.

## 3. 결론

Failbit Map을 일회성 조회 이미지가 아니라, 엔지니어 확인과 학습 데이터 축적으로 이어지는 분석 흐름 안에 위치시켰다. Cython 변환과 palette PNG 저장으로 대량 Failbit Map을 1시간 주기로 생성하고, map과 chip별 계측값을 동일 화면에서 확인할 수 있도록 구성하였다. Known failure는 confidence가 낮은 sample에 한해 ROI-YOLO로 재확인하여 weighted F1 score 0.95를 얻었다. Unknown failure는 self-supervised embedding과 HDBSCAN을 이용해 후보 그룹을 도출하였고, 현업 엔지니어 확인에서 13개 중 7개가 실제 불량으로 확인되었다. 또한 chip multi-label 구조로 중복 불량 chip이 단일 불량 분석 방식으로 분류되지 않는 문제를 보완하였고, FCM-PM은 2-combo 합성 평가셋에서 bit-F1 score 0.9927과 FAR 0.00%를 얻었다. 핵심 기여는 개별 모델 성능이 아니라, Failbit Map 생성부터 현업 확인과 학습 데이터 축적까지 이어지는 흐름을 실제 분석 환경에서 동작하는 구조로 만든 점이다.

[^1]: 약 0.31 GFLOPs(307.9 million FLOPs)는 obj-id 분류기 ChipGridCNN(32×32 격자 입력, conv 6단 + 분류 head) 아키텍처에서 레이어별 MAC를 합산해 결정론적으로 산출한 값으로, 약 1.16 million parameters와 정합한다.

[^2]: object-id map은 동일 chip 원천 split에서 seed 5회(42/1/7/100/234)를 반복했다. 평균은 validation F1 score 0.9905±0.0045, hold-out F1 score 0.9831±0.0050이며, Table 6의 값은 가장 높았던 seed 결과다. chip-CNN 출력에 10% noise를 주입해도 wafer-level F1 score 변동은 5-seed 표준편차 안에 머물렀다.

[^3]: 약 90% 공수 절감은 현업 운영 성과이며, 약 0.02%p 수율 개선은 HBM 제품 단일 사례 기준(연환산 아님)이다. 약 123억은 메모리제조기술센터 성과 인증값이다.

## 참고문헌

[1] Nakazawa, T. et al., "Wafer map defect pattern classification and image retrieval using convolutional neural network," *IEEE Trans. Semicond. Manuf.*, Vol. **31**, no. 2, pp. 309-314, 2018.

[2] Alawieh, M. B. et al., "Wafer map defect patterns classification using deep selective learning," in *Proc. 57th ACM/IEEE Design Automation Conf. (DAC)*, pp. 1-6, 2020.

[3] Lee, H. et al., "Classification of chip-level defect types in wafer bin maps using only wafer-level labels," *J. Manuf. Sci. Eng.*, Vol. **146**, no. 7, article 070902, 2024.

[4] Kyeong, K. et al., "Classification of mixed-type defect patterns in wafer bin maps using convolutional neural networks," *IEEE Trans. Semicond. Manuf.*, Vol. **31**, no. 3, pp. 395-402, 2018.

[5] Khosla, P. et al., "Supervised contrastive learning," in *Advances in Neural Information Processing Systems (NeurIPS)*, Vol. **33**, pp. 18661-18673, 2020.

[6] Chen, T. et al., "A simple framework for contrastive learning of visual representations," in *Proc. Int. Conf. on Machine Learning (ICML)*, PMLR 119, pp. 1597-1607, 2020.

[7] Shin, J.-S. et al., "Enhanced detection of unknown defect patterns on wafer bin maps based on an open-set recognition approach," *Comput. Ind.*, Vol. **164**, article 104208, 2025.

[8] Baek, I. et al., "Contrastive deep clustering for detecting new defect patterns in wafer bin maps," *Int. J. Adv. Manuf. Technol.*, Vol. **130**, pp. 3561-3571, 2024.

[9] Jang, J. et al., "Decision fusion approach for detecting unknown wafer bin map patterns based on a deep multitask learning model," *Expert Syst. Appl.*, Vol. **215**, article 119363, 2023.

[10] Shi, B. et al., "When do we not need larger vision models?," in *Proc. European Conf. on Computer Vision (ECCV)*, pp. 444-462, 2024.

[11] Ren, S. et al., "Faster R-CNN: Towards real-time object detection with region proposal networks," *IEEE Trans. Pattern Anal. Mach. Intell.*, Vol. **39**, no. 6, pp. 1137-1149, 2017.

[12] Cai, Z. et al., "Cascade R-CNN: Delving into high quality object detection," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, pp. 6154-6162, 2018.

[13] Campello, R. J. G. B. et al., "Density-based clustering based on hierarchical density estimates," in *Proc. Pacific-Asia Conf. on Knowledge Discovery and Data Mining (PAKDD)*, pp. 160-172, 2013.

[14] Woo, S. et al., "ConvNeXt V2: Co-designing and scaling ConvNets with masked autoencoders," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, pp. 16133-16142, 2023.

[15] Redmon, J. et al., "You only look once: Unified, real-time object detection," in *Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)*, pp. 779-788, 2016.

[16] Jocher, G. et al., "Ultralytics YOLO11," Ultralytics, 2024.

[17] Guo, C. et al., "Entity embeddings of categorical variables," *arXiv preprint* arXiv:1604.06737, 2016.

[18] He, K. et al., "Momentum contrast for unsupervised visual representation learning," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, pp. 9729-9738, 2020.

[19] Yun, S. et al., "CutMix: Regularization strategy to train strong classifiers with localizable features," in *Proc. IEEE/CVF Int. Conf. on Computer Vision (ICCV)*, pp. 6023-6032, 2019.

[20] Ridnik, T. et al., "Asymmetric loss for multi-label classification," in *Proc. IEEE/CVF Int. Conf. on Computer Vision (ICCV)*, pp. 82-91, 2021.

[21] Hinton, G. et al., "Distilling the knowledge in a neural network," *arXiv preprint* arXiv:1503.02531, 2015.

[22] Lin, T.-Y. et al., "Focal loss for dense object detection," in *Proc. IEEE Int. Conf. on Computer Vision (ICCV)*, pp. 2980-2988, 2017.

