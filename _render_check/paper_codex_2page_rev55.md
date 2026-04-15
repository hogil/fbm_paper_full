DRAM Failbit Map 기반 Known 불량 분석과 Unknown 불량 검출 운영
파이프라인

**Abstract**

반도체 EDS(Electrical Die Sorting) Test의 Failbit Map은 웨이퍼 불량의
위치·분포·밀집도·방향성·강도 정보를 담는 핵심 데이터이다. 그러나 기존
분석은 chip별 특성을 wafer 평균값으로 요약하는 방식에 크게 의존하였기
때문에 위치별 편차, 국부 패턴, 형상 차이, 중복 불량을 충분히 반영하지
못했고, Map에서만 드러나는 불량을 전 제품 wafer에 대해 사람이 직접
확인하기에도 한계가 있었다. 본 연구는 이러한 문제를 해결하기 위해 DRAM
Failbit Map 기반 Known 불량 분석, Unknown 불량 검출, UI 등록을 연결한
운영 파이프라인을 제안한다. UI에서는 Failbit Map과 chip 특성 이미지를
초당 50매 수준으로 제공하고, overlay 및 composite map 분석과 wafer·chip
단위 sample 등록을 지원한다. 데이터 생성 단계에서는 제한된 색상만
사용하는 Failbit Map 특성에 맞추어 palette-indexed PNG를 적용함으로써
RGB 대비 파일 크기를 약 65% 절감하였다. Known 불량 분석에서는
ConvNeXtV2-Base와 선택적 ROI-YOLO를 결합하여 16-class weighted F1을
0.78에서 0.95로 향상시켰다. Unknown 불량 검출에서는 contrastive
learning, HDBSCAN, 6×6 structured local sampling을 적용하였고, 운영 적용
결과 13개 후보 그룹 중 7개가 실제 불량 그룹으로 확인되었다.

Keywords: Failbit Map, Wafer Defect Analysis, ConvNeXtV2, YOLO,
Contrastive Learning, HDBSCAN

**1. 서론**

반도체 EDS(Electrical Die Sorting) Test 결과인 Failbit Map은 천만 픽셀
이상의 표현력으로 웨이퍼 불량의 위치·분포·밀집도·방향성·강도 정보를 담는
핵심 데이터이며, 수율 저하 원인 추적과 공정 이상 조기 인지에 중요한
역할을 한다. 그러나 기존 분석은 chip별 특성을 wafer 평균 기반의 단순
요약값으로 다시 압축하는 방식에 크게 의존하였기 때문에 위치별 편차, 국부
패턴, 형상 차이, 중복 불량을 충분히 반영하지 못했다. 평균값에서 이상
징후가 나타나지 않더라도 Map에서만 드러나는 불량이 발생하였고, 이는
chip별 특성값을 다시 wafer 평균값으로 요약하는 과정에서 위치 정보와 패턴
정보가 크게 소실되기 때문이다. 따라서 Failbit Map 기반의 직접 확인은
보조 절차가 아니라 불량 검출과 원인 분석에서 필수적인 과정이다.

기존 wafer map 조회 환경에서는 사용자가 map을 요청할 때마다 설비 로그를
불러온 뒤 압축을 해제하고, 설비 전용 포맷으로 인코딩된 테스트 결과를
해독·복원하여 wafer map 이미지로 변환해야 했기 때문에 응답 시간이 길고
소량 조회만 가능하였다. 또한 전 제품 wafer를 분석 담당자가 직접 확인하는
방식에는 처리량과 일관성 측면에서 현실적 한계가 있었다. 계측 연계 분석
역시 약 22조 row 규모의 DB를 반복 조회해야 했기 때문에 Failbit Map과
함께 즉시 확인하거나 chip 단위로 종합 해석하기 어려웠다. 이에 본 연구는
DRAM Failbit Map을 기반으로 Known 불량 분석, Unknown 불량 검출, UI 기반
등록을 연결한 human-in-the-loop 운영 파이프라인을 구축하고, UI에서
Failbit Map과 chip 특성 이미지를 overlay 및 composite map 형태로 함께
분석하면서 wafer·chip 단위의 불량 유형과 sample을 즉시 등록할 수 있도록
하였다.

**2. 제안 방법**

2.1 데이터 생성 및 표현

입력 데이터는 failbit map 로그와 Measure 로그의 정합 결과이다. Bucket A
로그로부터 wafer 내 각 chip의 failbit map tile을 복원하고, Bucket B의
주요 Measure 값을 동일 chip 인덱스로 매칭하여 Chip Information 파일을
생성하였다. 이를 통해 Failbit Map과 chip 특성 이미지를 동일 좌표계에서
overlay 및 composite map 형태로 함께 분석할 수 있도록 하였다.

Failbit Map은 일반 영상과 달리 Grade 0-7과 chip 경계 등 제한된 수의
색상만 사용하므로 RGB 방식으로 저장할 필요가 없다. 이에 palette-indexed
PNG를 적용하여 RGB 대비 파일 크기를 약 65% 절감하였고, 대량 이미지
저장·처리와 AI 적용이 현실적으로 가능하도록 하였다. 또한 기존 RGB 기반
방식이 색상 scheme 변경 시 전 픽셀 재변환이 필요한 것과 달리,
palette-indexed PNG는 palette table만 교체하면 되므로 사용자별 색상
설정을 초고속으로 적용할 수 있다. Chip 특성 데이터 역시 약 22조 row
규모의 DB 반복 조회 대신 Chip Information 파일로 저장하여 wafer map과
함께 즉시 확인할 수 있도록 하였다.

![](media/image1.png){width="3.05in" height="0.650667104111986in"}

Fig. 1. Failbit Map, FTN, QTN 연계 분석 예

2.2 Known 불량 분석

Known 불량 분석에서는 ConvNeXtV2-Base 기반 CNN을 주 모델로 사용하였다.
CNN은 wafer 전역의 위치·형상·배치 문맥을 함께 해석하는 데 가장 높은
성능을 보였으며, 기존에 등록된 16개 불량 클래스를 1차 분류하는 역할을
담당한다. 이는 일부 불량이 chip 단위 국소 정보보다 wafer 전체 배치와
상대 위치에 의해 더 잘 구분되기 때문이다.

![](media/image2.png){width="3.05in" height="0.650667104111986in"}

Fig. 2. ROI-YOLO 기반 오분류 교정 예

2.3 ROI-YOLO 기반 선택적 재확인

ROI-YOLO는 전체 분류 성능에서는 CNN보다 우세하지 않았지만, 국부 영역을
다시 확인하는 데 강점이 있어 전역 패턴만으로는 혼동이 큰 저신뢰 샘플에서
보정 효과를 보였다. 이에 본 연구에서는 CNN이 1차 분류를 담당하고,
ROI-YOLO는 혼동이 집중되는 저신뢰 샘플에 대해서만 선택적으로 적용하는
2단계 구조를 설계하였다.

2.4 Unknown 불량 검출

Unknown 불량 검출은 미리 정답 클래스가 정해져 있지 않은 실제 운영
이미지를 다루기 때문에, 임의로 정제한 고정 클래스 데이터셋만으로는 현장
조건을 충분히 반영하기 어렵다. 이에 자기지도 contrastive learning과
HDBSCAN 군집화를 결합하고, 6×6 grid 기반 structured local sampling을
적용하여 유사 이미지를 그룹화하였다. 이때 structured local sampling은
위치와 형상 정보가 중요한 wafer 데이터 특성을 반영하기 위한 설계이다.

3\. 실험 결과 및 논의

Known 불량 분석에서는 ConvNeXtV2-Base와 Optuna 기반 최적화를 통해
weighted F1을 0.78에서 0.92까지 향상시켰고, low-confidence subset에 대한
선택적 ROI-YOLO 재확인을 통해 최종 0.95를 달성하였다. Table 1은 단계별
성능을 요약한 결과이다.

Unknown 불량 검출 경로는 정답 기반 accuracy가 아니라 실제 운영
데이터에서의 grouping 유효성 관점에서 평가하였다. 분석 담당자를 통한
확인 결과, 도출된 13개 후보 그룹 중 7개가 실제 불량 그룹으로
확인되었으며, 이는 신규 라벨 확장과 검토 대상 축소에 활용될 수 있음을
보여준다.

  Configuration            Weighted F1   Note
  ------------------------ ------------- ---------------------------
  Baseline CNN             0.78          initial model
  ConvNeXtV2 + Optuna      0.92          global classifier
  \+ ROI-YOLO refinement   0.95          low-confidence correction

4\. 결론

본 연구는 DRAM Failbit Map을 기반으로 데이터 생성, Known 불량 분석,
Unknown 불량 검출, UI 기반 등록을 하나의 운영 파이프라인으로 연결하였다.
이를 통해 Failbit Map과 chip 특성을 함께 해석하고, 기존 불량은 자동
분석하며, 미등록 불량은 그룹화 기반으로 검출하여 현업 검토와 후속 학습
데이터 확장까지 연결할 수 있는 기반을 마련하였다.

참고문헌

\[1\] T. Nakazawa and D. V. Kulkarni, \"Wafer Map Defect Pattern
Classification and Image Retrieval Using Convolutional Neural Network,\"
\*IEEE Transactions on Semiconductor Manufacturing\*, vol. 31, no. 2,
pp. 309-314, 2018.

\[2\] M. B. Alawieh, D. Boning, and D. Z. Pan, \"Wafer Map Defect
Patterns Classification using Deep Selective Learning,\" in \*Proc. 57th
ACM/IEEE Design Automation Conference (DAC)\*, pp. 1-6, 2020.
