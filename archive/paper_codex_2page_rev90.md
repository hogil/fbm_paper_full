# DRAM Failbit Map 기반 Known·Unknown 불량 분석 AI 아키텍처

**An AI Architecture for Known/Unknown Defect Analysis Based on DRAM Failbit Maps**

홍길동¹, 김철수¹

¹ 반도체연구소, Samsung Electronics, 화성시, 대한민국

## 초록

Failbit Map은 반도체 EDS Test에서 생성되는 웨이퍼당 약 1,000만 pixel 수준의 초고해상도 공간 데이터로, 불량의 위치, 밀집도, 형상, 방향성을 정밀하게 보여주는 핵심 자료이다. 그러나 실제 현업에서는 대량의 Failbit Map을 생성·조회하고 전수 분석할 수 있는 환경이 부족하여, 엔지니어의 수작업 확인에 의존한 분석이 이루어지고 있다. 본 논문은 이를 해결하기 위해 Test Log를 변환하여 대규모 Failbit Map을 생성·저장하는 데이터 파이프라인과, Known 불량 및 Unknown 불량을 분석하는 AI 불량 분석 구조를 구현하였다.

Known 불량 분류는 ConvNeXtV2-Base를 주 모델로 사용하고, 신뢰도가 낮은 샘플에 한해 ROI 기반 YOLO를 선택적으로 적용하는 2단계 구조로 설계하였으며, 이를 통해 F1-score 0.95를 달성하였다. Unknown 불량 검출은 레이블 없이 SimCLR 계열 contrastive learning을 사용하였고, wafer의 zone 기반 불량 해석 특성을 반영하기 위해 grid structured local sampling을 적용하였다. 실제 양산 5일치 Failbit Map 10,000장을 학습한 뒤 1일치 2,000장에 대해 추론한 결과 13개 불량 그룹이 검출되었으며, 현업 분석 엔지니어의 검증 결과 이 중 7개가 실제 의미 있는 불량 그룹으로 확인되었다. 이를 통해 레이블이 없는 실제 운영 이미지에서도 Unknown 불량을 그룹 수준에서 검출하고, 전문가 검증을 통해 실제 불량으로 식별할 수 있음을 확인하였다.

Keywords: Failbit Map, Known Defect Classification, Unknown Defect Discovery, ConvNeXtV2, ROI-YOLO, Contrastive Learning, HDBSCAN

## 서론

Failbit Map은 EDS(Electrical Die Sorting) Test에서 각 Memory Cell Block의 불량 cell 개수를 Grade 0(정상)부터 7(최대 불량)까지로 표현한 데이터이다. Wafer 1장에는 약 1,000만 개의 block이 포함되므로, Failbit Map은 불량의 위치, 밀집도, 형상, 방향성을 반영하는 초고밀도 공간 데이터이자 수율 저하 원인 분석의 핵심 데이터이다. 그러나 현업 분석은 주로 Chip 단위 Measure(측정 항목별 집계값)의 발생 빈도를 기준으로 이상 여부를 판단하고 있어, Failbit Map 전체에서만 드러나는 불량 분포의 공간 패턴을 충분히 포착하지 못한다. 이로 인해 수율 저하 원인이 오분류되거나 미검출될 수 있다. 따라서 수율 저하 원인을 정밀하게 분석하기 위해서는 Measure 기반 접근만으로는 충분하지 않으며, Failbit Map 자체를 핵심 분석 단위로 삼아야 한다.

실제 현업 적용에는 두 가지 제약이 있다. 첫째, 대량 Map 생성이 어렵다. 설비 Log는 Wafer당 10~50MB 수준이며, 특정 제품군에서는 하루 약 2,000장의 Wafer가 발생한다. 그러나 기존 환경에서는 속도와 메모리 제약으로 한 번에 48매 이하만 처리할 수 있다. 둘째, Map이 생성되더라도 불량 여부와 유형 판단은 여전히 엔지니어의 직접 확인에 의존하고 있어 전수 분석이 어렵다. 따라서 본 논문은 대량 Raw Data를 처리하는 데이터 파이프라인과 Failbit Map 기반 Known 불량 분류 및 Unknown 불량 검출을 통합한 AI 아키텍처를 구현하여 실데이터에 적용·검증하였다. 본 논문의 주요 기여는 다음과 같다.

첫째, Test 부서와 협의하여 대량 Raw Data 적재 체계와 전수 Failbit Map 생성 파이프라인을 구축하였다. 또한 palette-indexed PNG를 적용해 이미지 용량을 약 75% 절감하고, 실시간 설비 Log 수집과 1시간 주기 Failbit Map 생성 체계를 구현하여 대량 분석이 가능한 운영 기반을 마련하였다.

둘째, Known 불량의 정밀 분류를 위해 ConvNeXt V2와 ROI 기반 YOLO를 결합한 2단계 분석 구조를 제안하였다. ConvNeXt V2로 Wafer 전역 패턴을 우선 분류하고, 신뢰도가 낮은 샘플에 한해 ROI 기반 YOLO로 불량 영역의 위치 정보를 추가 반영함으로써 전역 패턴과 국소 위치 정보를 함께 활용하는 정밀 분류를 구현하였다.

셋째, 기존 분류 체계에 등록되지 않은 상태에서 새롭게 발생하는 Unknown 불량을 검출하기 위해 SimCLR 계열 contrastive learning 기반 분석 구조를 구현하였다. 또한 grid structured local sampling을 적용하여 동일한 형태의 불량이라도 발생 위치에 따라 구분될 수 있도록 하였으며, 이를 통해 Unknown 불량을 유사 패턴 그룹 수준에서 검출하고 해석할 수 있도록 하였다.

## 제안 방법 및 결과

### 데이터 파이프라인

데이터 파이프라인은 설비 Log를 Storage에 실시간 적재하고, 이를 1시간 주기로 Failbit Map으로 변환·생성하도록 구성하였다. 핵심 병목은 raw hex stream을 2글자씩 읽어 grade로 변환하는 구간이다. 예를 들어 `09090909090A`와 같은 연속 데이터는 `09 09 09 09 09 0A`로 분할된 뒤 10진수 변환과 보정 연산을 거쳐 `0 0 0 0 0 1`의 grade row로 바뀐다. 이 연산이 웨이퍼당 약 1,000만 pixel 규모에서 반복되므로 Python 기반 반복문만으로는 주기적 생성이 어려웠다. 본 연구에서는 해당 루틴을 Cython으로 전환하여 바이트 배열을 직접 순회하고, 16진수 변환과 보정 연산을 C 레벨 루프에서 수행함으로써 핵심 데이터 변환 속도를 약 100배 향상시켰다.

```text
raw stream: 09090909090A
h_i:        09   09   09   09   09   0A
v_i:         9    9    9    9    9   10
g_i:         0    0    0    0    0    1
v_i = int(h_i, 16),    g_i = max(v_i - 9, 0)
```

즉, Python에서는 문자열 분할과 형변환이 pixel 수만큼 반복되지만, Cython 구현에서는 동일 연산을 typed loop로 처리하여 주기적 Map 생성이 가능하도록 하였다.

또한 Failbit Map은 grade와 boundary 등 제한된 색상 집합만 사용하므로 RGB PNG 대신 palette-indexed PNG를 적용하였다. 동일 색상은 palette에 1회만 정의하고 각 pixel에는 index만 저장하여 이미지 용량을 약 75% 절감하였다.

```text
Conventional RGB:
[(123,54,24), (123,54,24), (123,54,24), (123,54,24)]
[(123,54,24), (123,54,24), (123,54,24), (123,54,24)]
[(123,54,24), (123,54,24), (123,54,24), (123,54,24)]

Palette-indexed PNG:
P[1] = (123,54,24)
I = [[1, 1, 1, 1],
     [1, 1, 1, 1],
     [1, 1, 1, 1]]
```

즉, RGB PNG는 동일 색상을 픽셀마다 반복 저장하지만, palette-indexed PNG는 palette 정의 1회와 index 배열만 저장하므로 대량 Map에서 저장 효율이 높다.

### Known 불량 분류

Known 불량 분석은 16개 기등록 클래스를 대상으로 하며, 총 1,500개의 라벨된 Failbit Map을 사용하였다. 표 1과 같이 backbone 비교 결과 ConvNeXtV2-Base가 가장 안정적인 성능을 보여 주 모델로 선정되었다.

| 구성 | 사전학습 | Test F1 | 비고 |
|---|---|---:|---|
| ViT-Base/16 | IN-21k | 0.81 | fine-tuning |
| Swin-Base | IN-1k | 0.84 | fine-tuning |
| EfficientNetV2-M | IN-1k | 0.85 | fine-tuning |
| MaxViT-Base | IN-21k | 0.87 | fine-tuning |
| ConvNeXtV2-Base | FCMAE+IN-22k | 0.87 | 선택 backbone |
| ConvNeXtV2 + Optuna HPO | — | 0.92 | 하이퍼파라미터 최적화 |
| ConvNeXtV2 + Optuna + ROI-YOLO | — | 0.95 | 최종 2단계 구조 |

Baseline CNN의 weighted F1 0.78은 ConvNeXtV2-Base 적용으로 0.87까지 향상되었고, Optuna HPO로 0.92, ROI 기반 YOLO 보정으로 최종 0.95까지 개선되었다. 특히 center, edge, local 계열처럼 전역 형상만으로 구분이 어려운 저신뢰 샘플에 한해 ROI 기반 YOLO를 선택적으로 적용하여 유사 클래스 간 오분류를 효과적으로 보정하였다(Fig. 2).

![Fig. 2. Known 불량 2단계 분류 예시](_fig_yolo_roi.png)

**Fig. 2.** Known 불량 2단계 분류 예시. 좌측 두 패널은 혼동되는 Class A/B 예시이며, 우측은 CNN이 B로 오분류한 샘플을 ROI-YOLO가 A로 교정한 사례를 보여준다.

### Unknown 불량 검출

Unknown 불량은 사전에 정답 클래스를 정의하기 어려운 실제 운영 이미지를 대상으로 하므로, 본 연구에서는 이를 후보 grouping 문제로 정의하였다. 특정 제품의 5일치 운영 데이터 약 10,000장으로 SimCLR 계열 contrastive learning 기반 임베딩을 학습하고, 별도 1일치 2,000장에 HDBSCAN을 적용하여 유사 패턴을 그룹 단위로 압축하였다. 이때 wafer의 zone 기반 불량 해석 특성을 반영하기 위해 grid structured local sampling을 적용하였다. 그 결과 2,000장의 운영 이미지는 13개 후보 그룹으로 정리되었으며, 현업 분석 엔지니어 검증 결과 이 중 7개가 실제 불량 그룹으로 판정되었다(Fig. 3).

![Fig. 3. Unknown 불량 grouping 예시](_fig_cluster.png)

**Fig. 3.** Unknown 불량 grouping 예시. 실제 운영 이미지가 유사 패턴 기준으로 자동 압축된 후보 그룹을 보여주며, 이후 현업 분석 엔지니어 검증 대상으로 사용된다.

## 결론

본 연구는 대량 Failbit Map 조회가 불가능하고 일부 Map 분석이 엔지니어의 육안 판단에 의존하던 환경에서, 데이터 생성 파이프라인과 Known·Unknown 불량 분석 AI를 통합한 현업 적용형 구조를 제시하였다. 데이터 계층에서는 1시간 주기 Map 생성이 가능한 처리 성능과 저장 효율을 확보하였고, Known 경로에서는 높은 분류 성능을, Unknown 경로에서는 실제 검토 가능한 후보 그룹 발굴 성과를 확인하였다. 이를 통해 Failbit Map을 수작업 기반 시각 자료가 아니라 대량 운영 데이터 기반의 핵심 분석 단위로 전환할 수 있음을 보였다.

## 참고문헌

[1] T. Nakazawa and D. V. Kulkarni, "Wafer Map Defect Pattern Classification and Image Retrieval Using Convolutional Neural Network," IEEE Transactions on Semiconductor Manufacturing, vol. 31, no. 2, pp. 309-314, 2018.

[2] M. B. Alawieh, D. Boning, and D. Z. Pan, "Wafer Map Defect Patterns Classification Using Deep Selective Learning," in Proceedings of the 57th ACM/IEEE Design Automation Conference (DAC), pp. 1-6, 2020.

[3] J. Jang and G. T. Lee, "Decision fusion approach for detecting unknown wafer bin map patterns based on a deep multitask learning model," Expert Systems with Applications, vol. 215, art. 119363, 2023.

[4] S. Woo et al., "ConvNeXt V2: Co-Designing and Scaling ConvNets With Masked Autoencoders," in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 16133-16142, 2023.

[5] R. R. Selvaraju et al., "Grad-CAM: Visual Explanations From Deep Networks via Gradient-Based Localization," in Proceedings of the IEEE International Conference on Computer Vision (ICCV), pp. 618-626, 2017.

[6] T. Chen, S. Kornblith, M. Norouzi, and G. Hinton, "A Simple Framework for Contrastive Learning of Visual Representations," in Proceedings of the 37th International Conference on Machine Learning (ICML), PMLR 119, pp. 1597-1607, 2020.

[7] R. J. G. B. Campello, D. Moulavi, and J. Sander, "Density-Based Clustering Based on Hierarchical Density Estimates," in Advances in Knowledge Discovery and Data Mining, PAKDD 2013, pp. 160-172, 2013.

[8] Hugging Face, "facebook/convnextv2-base-22k-384," model card, accessed Apr. 15, 2026. Available: https://huggingface.co/facebook/convnextv2-base-22k-384

[9] Hugging Face timm, "maxvit_base_tf_384.in21k_ft_in1k," model card, accessed Apr. 15, 2026. Available: https://huggingface.co/timm/maxvit_base_tf_384.in21k_ft_in1k

[10] Z. Tu et al., "MaxViT: Multi-Axis Vision Transformer," in Proceedings of the European Conference on Computer Vision (ECCV), pp. 459-479, 2022.
