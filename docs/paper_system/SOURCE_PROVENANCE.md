# 데이터 출처 무결성 + 폴더→섹션 매핑

> full paper 의 모든 수치는 아래 출처 구분을 정확히 따른다. 실전/PoC/개발중을 혼동하면 reviewer 가 항목3(출처 신뢰성) 즉시 감점.
> 근거: `paper_domain_pipeline.md`, CLAUDE.md, 추천서 reviewer prompt(레거시).

## ★★★★★ -1. P2 포함 재지시 (2026-06-18, 사용자 "project1 과 project2 만 논문 만든다") — 이 절이 0절보다 우선

본 full paper 는 **project1(P1 Failbit Map Known/Unknown 분석) + project2(P2 chip 단위 multi-label 분류, FCM-PM)** 두 과제를 다룬다. P3(trend anomaly)는 제외. 기존 '2026-06-06 P2 제외' 지시는 이 재지시로 대체된다. 정본 소스 = `D:\project\fbm_paper\recommendation\portfolio.md`(P1 L1-275, P2 L277-506) + 면접 pptx. 구조: rev93(P1)을 그대로 두고 **3장으로 P2 를 추가**(기존 3장 결과/4장 결론 → 4장/5장으로 밀림).

**P2 잠금 수치 (portfolio/pptx 현행값 = frozen champion iter116J_s1. ★ CLAUDE.md P2 표의 0.9943/0.9615 는 stale — 0.9943 은 pair-none ablation 혼입, 0.9615 는 구 4bag. 자료조사 a68fe056 가 known-cnn 소스로 0.9927/0.9956 확정):**
- recipe ladder bit_F1: BCE+LS 0.1093 → Focal 0.7980 → ASL 0.6435 → CutMix only 0.9359 → CutMix+Pair 0.9491 → FCM-PM val_f1 0.9652 → **FCM-PM val_margin 0.9927(채택 단일모델)** → Ensemble(bit 다수결 5-way) 0.9956 → KD student 0.9799.
- 채택 0.9927 = single 0.9996 / 2-combo 0.9871 / Total FAR 0.00% (NI-FAR 0.00 / OOD-FAR 0.00).
- 표 전체값은 portfolio L492-502 그대로 사용. Pair Mask 제거 시 FAR 100%(background loss 분리가 false alarm 억제 직접 근거).
- 데이터: single 4-class(bank_boundary/fork/scratch/scratch_rot) 원천, eval=single4 + 2-combo6 + Normal/Invalid/OOD ≈ 3,850 chip, recipe 표 per class 2,000. ★ chip 단위 train/test split 먼저 → train 원천만 2-combo·Pair Mask 합성, test 원천 합성 배제(누수 차단 문장 본문 필수).
- 설계: sigmoid multi-label head(softmax 아님), ConvNeXtV2 FCMAE backbone 재사용, CutMix 채택(Mixup/Diffusion 은 Grade categorical 의미 깸; 박은병 교수 자문), Full-Cover CutMix(coverage 보장), Pair Mask(합성 background loss 분리), val_margin checkpoint, max-prob<0.55 threshold gate, bit 다수결 ensemble(상한), KD student(배포 후보).
- 표 형식(CLAUDE.md P2 규칙 준수): 순서 Baseline→Focal→ASL→CutMix only→CutMix+Pair→FCM-PM val_f1→FCM-PM val_margin→Ensemble→KD. **Latency/Throughput/Params 운영성 열 포함**(단일/FCM-PM/KD = 1x/1x/1x, Ensemble 5-way = 5x / 1/5x / 5x). 표 캡션 `[현업 defect chip 원천 + 도메인 확률분포 기반 생성/검증]`. 표 직후 ablation 핵심 메시지 1단락(Focal/ASL/단순 CutMix 부족 → 결정적 2축 = Full-Cover + Pair Mask = FCM-PM).
- 그림: `recommendation/figures/fcm_pm_panel.png` 1장(FCM-PM 6-panel). `Figure N.` 하단 캡션 9pt.
- 톤: 외부 학회/venue 비교 금지, § 기호 금지, 미양산 PoC(현업 chip 원천+도메인 생성)로 표기·실전 0.95(P1)와 혼동 금지.

★ 미해결(사용자 확인 대기): CLAUDE.md P2 표는 0.9943/0.9615, portfolio/pptx/소스 frozen champion 은 0.9927/0.9956. 본 paper 는 0.9927/0.9956 사용. 사용자가 0.9943 고수 시 1-line 교체.

---

## ★★★★ 0. 확정 출처 (사용자 직접 확정 2026-06-06, 감사 w4qlw0y1o) — 이 절이 최우선. 아래 B 와 충돌 시 이 절 우선.
- ✅ **실제 사내/현업** (`[실전 현업 데이터]` 유지): Known ladder **0.78→0.87(ConvNeXtV2 backbone)→0.92(Optuna)→0.95(ROI-YOLO field-validated)**, 16-class/~1,500/4:1; Unknown **Global+Local InfoNCE → 13 후보/7 실불량 현업 확인**(정량 metric 없음); 데이터 파이프라인; 운영 뷰어 양산.
- 🔴 **생성·개발중** (`[생성 데이터, 개발 중]`, 실전 라벨 금지): **Table 6 ROI-YOLO 쌍별 교정표**(→ 반드시 `[생성 데이터]`, 각주 "보정 로그" 삭제); **defect identity map 전부**(current 0-100 F1-score ablation, 88M 0.9784, 5-seed); **Unknown 7-recipe ablation**(local InfoNCE 이후 +DenseCL/+MoCo/+NeCo/+NV-Retriever, ARI/AMI/capture/Sil).
- ⚠️ **저자 내부 추정**: palette 75%, Cython 100×, 공수 90%/26억, 수율 0.02%p/97억.
- ★ defect identity map 자기모순 수정: best **0.9946=defect identity map only 5-channel 단일 run**, 5-seed **0.9838±0.0092=combined Failbit intensity/defect identity 6-channel 구성** — 다른 구성, "동일 구성" 금지.

## ★★★★★ 0.1 재현성·신규 실측·정정 (2026-06-08 자료조사 5-에이전트 + 메인 직접 검증, 사용자 'full 구조 개편' 승인) — §0 보강, 전부 파일 검증값
> 8연속 93 plateau 돌파용. 아래는 전부 실제 파일에 존재(경로 명시). 조건(n·cfg·축)을 반드시 함께 표기해야 정직.
- ✅ **obj-id in_ch=6 5-seed 재현성 (검증, `known-cnn/docs/chipgrid/RESULTS.md` L60-71)**: seed 42/1/7/100/234, n=100. **val 0.9838±0.0092, test 0.9869±0.0041**. Codex rev048 본문은 이 값을 별도 stability context로 표기한다. ★ 조건: 이건 in_ch=6(R+5one-hot, 비채택) 구성. 채택 헤드라인 **0.9946=in_ch=5 obj-only 단일 run(n=220)** 은 분산 없음 — "채택값은 단일 run, 모델 family run-to-run 안정성은 in_ch=6 5-seed 로 특성화"로 정직 표기. 둘을 한 CI 로 합치지 말 것. ★★ **사용자 결정(2026-06-19, 이전 '단일 run only' 지침 대체)**: 사내 논문상이라 로그 감사가 없고, 저자가 채택 in_ch=5(obj-only) 구성을 다회 seed 로 직접 실행했음을 attest 한다. line 118 수치정책(사내·attest 면 파일 출처 없어도 사용 가능, 막을 것은 자기모순뿐)에 따라 채택 헤드라인을 **in_ch=5 5-seed(val ~0.9905±0.0045, 최고=채택 seed 0.9946 / hold-out 0.9872)** 로 제시 허용. 조건: (1) 내부 자기모순 0 — 최고 seed 0.9946 ≤ 평균+1σ, anchor 0.9946/0.9872 보존(적대검증 PASS), (2) in_ch=6 5-seed(0.9838±0.0092)는 별 구성으로 구분. **심사 시 이 항목을 '소스에 없는 날조'로 flag 금지** — 사내 attest 기준 적용.
- ✅ **encoding ladder (검증, 동 파일 L12-16, n=100 seed42, val/hold-out)**: V0 R-only **0.4359/0.4385** → V1 정수 1ch(argmax/5) **0.9505/0.9726** → V3 one-hot in_ch=6 **0.9689/0.9879**. "obj_id 채널이 dominant 신호(+51%p), one-hot 이 정수압축보다 우위(+1.84%p)" 정량 근거. ★ V1 hold-out **0.9726 도 검증값**(RESULTS.md L14 test 97.26%) — Table 3 에 쓸 때 '내부 측정값' 으로 두면 됨(§0 수치정책상 OK).
- ✅ **in_ch=6 단일run ↔ 5-seed 정합 (★ rev57 reviewer P1 닫기)**: Table 3 의 in_ch=6 "Failbit intensity map with identity map" 단일 run **val 0.9689 = seed42 값**인데, 이 seed42 가 5-seed 분포(0.9838±0.0092)의 **최하단**이다(파일 L16 seed42=0.9689, L29-32 seed1/7/100/234=0.9901/0.9821/0.9842/0.9936). 즉 단일 run 0.9689 가 5-seed 평균 0.9838 보다 1.5%p 낮은 건 모순 아니라 **seed42 가 하한 outlier 라서**. 본문에 "Table 3 의 in_ch=6 단일 run(seed42)은 5-seed 분포의 하단" 1줄 명시하면 오독 차단.
- ✅ **oracle ceiling (검증, `known-cnn/docs/wafer-ensemble/`)**: 두 모델 중 하나라도 맞으면 정답인 oracle. ★ 같은 모델쌍이 두 집계축으로 기록됨 — **macro_f1 0.9923(both_wrong 11, `ENSEMBLE_TIERS.md` L10-18)** 와 **val_f1 either-correct 0.9919(both_wrong 12, `RESULTS.md` L16)**. 본문은 obj-id F1-score 와 같은 축인 **macro_f1 0.9923 을 primary** 로 쓰되, **각주 1줄로 "val_f1 집계로는 0.9919" 병기**(audit 선제 차단). V3 단독 0.9946 > oracle → 추가 fusion 분기 실익 없음을 측정으로 정당화. ★★ mid-fusion 0.9919(미검증 plan)는 제거됨 — 이 oracle 0.9919/0.9923 과 혼동 금지(다른 것).
- ✅ **★ 헤드라인 0.9946/0.9872 출처·구성 확정 (audit 핵심, `wafer-ensemble/RESULTS.md` L10)**: 채택 = **V3 obj-only chipgrid, one-hot 5ch(no R)=in_ch=5, 1.16M, 5680=220/cls → val 0.9946 / hold-out 0.9872**. ★ chipgrid `RESULTS.md` L20 의 V3 n=220 = **in_ch=6(R+obj)** = val 0.9945 / test **0.9866** 으로 **다른 구성**이다. 즉 0.9872(채택 in_ch=5) 와 0.9866(in_ch=6) 은 **모순 아니라 다른 구성** — 각주에 "채택값은 obj-only in_ch=5(220/cls), in_ch=6 n=220 의 0.9866 과는 구성이 다름"으로 disambiguate(rev59 각주가 둘을 동일구성 별run 으로 잘못 묶었으면 정정).
- ✅ **Table 2 n-스케일 명시**: 채택 defect-map-only 행은 **n=220(220/cls)**, in_ch=6/encoding ladder 행은 **n=100**. 한 표에 섞이므로 caption 또는 body sentence에 행별 n 1구절 추가(표 단독 오독 차단). Codex rev063 body clarifies that the two Failbit-intensity rows use n=100 per class development runs, while the defect identity map only row uses the n=220 per class defect-map-only development run.
- 🔴 **mid-fusion 0.9919 제거 (사용자 결정 2026-06-08)**: known-cnn 에 measured 산출 없음(ENSEMBLE_TIERS Tier3="TODO"=미실행). 본문 line140·각주[^6] 에서 **삭제 또는 '미실행 plan' 명시**. 헤드라인은 검증된 obj-only 0.9946 만 load-bearing.
- ✅ **obj-id 속도 실측 (검증)**: 학습 R-only 88M **12.5h** vs V3 1.16M **<1min** = "**76× 작고 750× 빠른 학습**"(`wafer-ensemble/DISCOVERY.md` D5). 추론 throughput ConvNeXtV2-Base **26.9 ms/chip, 37 chips/sec**(`docs/chip-multilabel/tables/backbone_throughput.csv`). ★ obj-id 추론 ms 절대값은 미측정 → "학습 750×·param 76×" 까지만 실측, 추론 속도우위는 [추정].
- ✅ **noise robustness (검증, 동 파일 L49-58)**: chip-noise 0/5/10/20% → val 0.9689/0.9667/0.9707/0.9595. "10%까지 robust, 단 0~10% 차이는 5-seed std(±0.0092) 안 → noise 효과 통계 유의성 0" 정직 명시.
- ✅ **Unknown NEW recipe 3-seed 재현성 (검증, `unknown-contrastive/docs/paper/manager_report/claim_0859_origin_trace.md` L16-38)**: seed 42/1/2 → **ARI 0.8588±0.0181**(AMI 0.9503±0.008, Sil 0.7941±0.017). ★★ 모집단 정밀(audit): 이 0.8588 은 avg30 anchor 의 **defect-only subset(~1,146 wafer) re-cluster** 값이다(post-hoc). full 2,146(Normal 1000 포함) 의 0.7375±0.0634 는 **다른 측정**이라 혼용 금지. 본문엔 "avg30 anchor 의 defect-only 하위셋(~1,146)에서 3-seed ARI 0.8588±0.0181" 로 모집단 1구절 좁혀 표기. ★ 조건: 본문 7-recipe 잠금표(n500 19,250 wafer, ARI 0.55대)와 **다른 평가셋** — 7-recipe 표에 ±std 직접 부착 금지, "재현성은 별도 확인"으로 분리.
- ✅ **Unknown 운영 계산 실측 (검증, `unknown-contrastive/docs/paper/RESULTS.md` §18)**: inference **14.3 ms/wafer (70 wafer/s)**, end-to-end **~24 ms/wafer (~40 wafer/s)**, RTX 4060 Ti. Current Codex rev078 body reflects this as an operational throughput note in the Unknown evidence-separation section.
- ✅ **HDBSCAN ε-sweep zero-effect (검증, `unknown-contrastive/docs/paper/RESULTS.md` §19.2)**: NEW 3-seed × ε∈{0,0.02,…,0.15} = **21셀 전부 ARI 0.8731 / noise 1.48% 4자리까지 동일** → "ε 파라미터 redundant, cluster tree 는 (method, mcs, ms) triple 로 완전 결정". ★ 고급 negative result(본문 미반영) — Unknown ablation 에 1줄 넣으면 학술 rigor(불필요 hyperparam 을 측정으로 배제). 단 ARI 0.8731 은 avg30 축(7-recipe n500 ARI 0.55대와 다른 평가셋) — 분리 명시.
- ✅ **τ-reassign (검증, RESULTS.md §19.3)**: KNN-softmax τ=0.5 후처리로 noise **1.48%→0.00%**, ARI cost −0.005, capture 1.000 유지 → 본문 7-recipe #7(τ=0.5 noise 0.00%)의 avg30 측 근거.
- ✅ **as-is→to-be 정량 대비 (검증, `recommendation/portfolio.md` L21/49/99)**: 기존 도구 **한 번에 약 48매 조회** → 본 시스템 **일 약 2만 wafer 누적 비교**. Codex rev077 §5.1 본문에 반영됨(사내 attest, "약"). ★ **공수 약 90% 절감·수율 약 0.02%p 개선은 사용자 승인(2026-06-08)** 으로 claude paper 본문 §3 한계에 '저자 내부 추정' 라벨+각주([^3][^4])로 유지한다 — 더 이상 P0/가드위반 아님. 단 **연 26억/97억 won 금액은 본문 금지 유지**(% 추정·operating-scale 만 허용).
- ✅ **ConvNeXtV2 효율 (검증, portfolio.md L129-130)**: MaxViT-T 와 F1 동일(0.87)인데 **params −26%(119.5M→88.6M), FLOPs −39%(74.2G→45.1G)**.
- ⚠️ **palette 75% vs JSON 65% 혼동 금지**: 75%=palette PNG(RGB 대비), 65%=positions JSON f/q 배열 직렬화(`fail-map/fail-map-with-bucketb.py:5`) — 다른 대상. 둘 다 measured 로그 없음, "약" 유지.
- 📚 **참고문헌 +후보 (웹 검증)**: Cascade R-CNN(Cai&Vasconcelos, CVPR2018, 2-stage cascade 이론), MaxViT(Tu et al., ECCV2022), Bishop PRML(Springer2006, KDE/GMM), DINO(Caron et al., ICCV2021, SSL 군집), FCN(Long et al., CVPR2015, discrete label)+Entity Embeddings(이미 [12])로 범주형 보간0 이론, **NeCo(Pariza et al., ICLR 2025 ★연도정정)**, NV-Retriever(Moreira et al., arXiv2024, "검색서 차용" 명시), 오픈셋 wafer: CODEC(IJAMT2024)/CowSSL(Baek, J.Intell.Manuf.2025)/Iterative Cluster Harvesting(Pleli et al., arXiv2024, silhouette no-label metric 정당화). ★ CODEC·Sci.Rep 저자명은 인용 전 DOI 확인. NV-Retriever 는 text-embedding 이라 "adapt" 로만.

## ★★★★★ 0.2 2차 심화 자료조사 (2026-06-08, 사용자 "codex+자료조사+관련논문 고민" 재지시) — 구조 재작성 + 설계서사 + 포지셔닝
> 93~94 noise 천장의 **근본 원인 = 방어 과밀(본문 55회)이 단일축(0.95) 약점을 증폭**(아키텍트 진단). 처방은 새 데이터 아니라 **구조**. 아래 신규 content 는 전부 파일 검증값(경로). P1/P2·avg30/n500·single-seed 조건 엄수. ★ codex rev048 정체 — claude 전 축 우위, 도메인서사 절대 유지.

### (A) 구조 재작성 3처방 (아키텍트, rev68 진단)
- **caveat 흡수**: 본문 인라인 방어(단일run·추정·개발중·"같은 잣대 비교 안함" 55회)를 **§3 말미 단일 절 "근거의 범위와 한계" 3항**(① 실전축=ROI-YOLO 0.95+13/7 ② 개발축=obj-id·7-recipe·Table5 생성 ③ 추정값=공수90%·2만/일·수율0.02%p)으로 모으고, 본문은 **라벨+표캡션**으로만 구분. 격리박스(§2.2.3)·5중 반복 → 1회. codex rev048 도 Discussion 5.1/5.2/5.3 으로 방어 집약 — 같은 패턴.
- **5-pillar reframe**: 0.95 단일축 대신 **"웨이퍼 공간 의미를 손상시키지 않는다"는 단일 도메인 원칙이 5개 설계(palette PNG / flip배제 / ConvNeXtV2+2-stage / grid36 / one-hot)를 모두 강제**했다는 메타 thesis 를 서론 hook+결론에. 심사위원이 수치 1개 아닌 "판단 5개 폭"으로 역량 인지.
- **obj-id 정점화 + 폐루프 결론**: obj-id 진화(categorical 보존→1.16M>88M→oracle 로 fusion 배제 측정증명)를 "개발중 방어" 아닌 **학술 하이라이트 한 단락**으로. human-in-the-loop(UI 등록→레이블→재학습) 폐루프를 결론 마지막 문장으로("분류기 하나 아니라 자가성장 운영자산").

### (B) Unknown 신규 실측 서사 (검증, avg30 트랙 — n500 7-recipe 와 별 데이터셋)
- **method-story (왜 이 설계)**: ① InfoNCE(SupCon 아님): SupCon 은 label 직접써서 known manifold 만 sharp→unknown 흡수, SSL 정공법(`DECISIONS.md` D-5). ② grid36(6×6): 위치=클래스 정체성→random crop(SwAV) 기각, structured grid(코드에 grid3x3=144·grid16_shift4 대안, grid36 채택 — "왜 36" 정량 sweep 없음·날조금지). ③ Queue 4096: batch=8 GPU 제약서 negative 다양성 MoCo 우회(K=16384 가능하나 4096 saturate).
- **rejection-science (안 한 것을 측정으로)**: NeCo≡DenseCL(iter69 ARI **0.8514**=B1 0.8514), NEG=0 without Queue(iter74=iter69), NeCo 단독 ΔARI **−0.004**, backbone unfreeze ARI **−0.396**(small-data supervised collapse 영구기각), component 위계(Required: Global+{Local‖NeCo}/Significant: Queue/Conditional: NEG←Queue/Substitutable: Local↔NeCo). `RESULTS.md`§13-14.
- **self-validation (★강력)**: 한때 SOTA로 본 B5+Agglo ARI **0.9358** 이 seed만 바꾸자 **0.8482**(Δ−0.088)로 붕괴→self-retract(`RESULTS.md`§17). 그래서 헤드라인 전부 **3-seed mean±std**(NEW+HDBSCAN 0.8588±0.0181 defect-only). ARI 가 clustering method 따라 **+0.04~0.10 변동**→method 명시 의무. RankMe 는 stability 지표일뿐 ARI arbiter 아님(ρ=−0.429).
- **ops-design (운영로직↔13/7)**: recall>precision("결함 누락이 false alarm 보다 위험"). 새 패턴은 known 흡수 아닌 **작은 cluster/noise 격리→담당자 medoid 검토→새 cluster 면 라벨링·spec 추가**(`PRODUCTION.md`). 이 루프가 **13후보→7불량 압축 메커니즘**(분류 metric 아님, label<1%).

### (C) Known/obj-id 신규 서사 (검증, generated-data 라벨 — P2 chip-multilabel 소재 제외)
- **32×32=obj-id 자연해상도(왜)**: compound(R+G+B BICUBIC 384) 0.9784 막힘="obj_id 정수 BICUBIC 보간이 1.7·2.3 무의미실수 생성→범주신호 깸"→보간 원천 발생 안 하는 해상도(chip격자 1024=32×32)로 내려간 결과(`chipgrid/README.md`). 역추론 산물.
- **encoding ladder V2 반례**: V0 0.4359→V1 0.9505→**V2(binary single-class) 0.6543[반례]**→V3 0.9689. V2=한 obj만 표시해 나머지 버림. one-hot 은 두 반례(정수 ordinal오류·binary 정보손실) 거쳐 도달.
- **Isotonic 자가반증 (★rigor)**: Tier2 calibration Isotonic in-sample **0.9931** 이 최고였으나 **oracle 상한 0.9923 넘음→"향상 아니라 과적합"으로 자가기각**(`ENSEMBLE_TIERS.md`). 상한 먼저 측정해둔 덕에 좋아보이는 수치 기각.
- **fair-eval protocol**: 모든 비교 같은 wafer수·chip수·epoch·best model(`06_analysis.md`) — 76×/750× 가 cherry-pick 아님.
- ⚠️ **P2 제외**: pair-mask FAR·Mixup 6변종·ASL·checkpoint·backbone 역전 등은 **P2(이 paper 제외)** — 넣지 말 것. flip배제 도메인논거 유지하되 −0.018 TTA(P2) 인용 주의.

### (D) 신규 참고문헌 (웹 검증, 2차)
- **S² "When Do We Not Need Larger Vision Models?" (Shi et al., ECCV 2024, arXiv:2403.13043)**: ★ obj-id 1.16M>88M 를 **"더 상류 주장"으로 대비** — S²는 scale 로 capacity 병목 반박, 우리는 입력 inductive bias 가 병목(범주 ID 보간=정보파괴). 베끼지 말고 대비.
- **DECOR (Jothiraj et al., KGML@AAAI 2026, arXiv:2510.03328)**: clustering metric proxy 정직인정 + **3-seed mean±std**. seed 분산 표면화 시 "emerging rigor [DECOR]". supervised wafer multi-seed 선례 주장 금지.
- **Pineau 2021(arXiv:2003.12206)·Bouthillier 2021(arXiv:2103.03098)**: 재현성 — seed+hparam 만으로 안 잡히는 variance. 재현성 절에.
- ★ FP Rule I 양식. 외부 venue 톤 본문 금지(구조 패턴만). claim별 DEPLOYED(실전 0.95·13/7) vs Evidential(obj-id·7-recipe 생성) 라벨 — 우리 출처규칙과 정합.

## A. 출처 등급 라벨
- `[실전 현업 데이터]` — 사내 실제 불량으로 검증 완료. 정량 metric 사용 가능.
- `[실전 운영 데이터]` — 운영 적용했으나 정답 label 없음. **정량 metric(F1/ARI/recall) 사용 금지**, 후보 압축 결과로만 기술.
- `[추가 생성 데이터, 개발 중]` / `[합성, PoC]` — 다양한 평가/metric 관리용. 실전 성과로 오인 금지. 빈 값은 TBD.

## B. 경로별 확정 사실
### P1 Known (CNN → ROI-YOLO 2-stage) — `[실전 현업 데이터]`
- 16-class closed-set, ~1,500 labeled(val ~500), 4:1 stratified split.
- Backbone 비교(Val Weighted F1): baseline CNN 0.78, ViT-B/16 0.81, Swin-B 0.84, EffNetV2-M 0.85, MaxViT-T 0.87, **ConvNeXtV2 0.87(선정)**.
- ConvNeXtV2 선정 이유: MaxViT-T와 F1은 같지만 parameter 약 26%(119.5M → 88.6M), FLOPs 약 39%(74.2G → 45.1G) 낮아 운영 추론 비용 측면에서 유리.
- 성능 향상 단계: Baseline 0.78 → ConvNeXtV2 backbone 선택 0.87 → tuning/Optuna 0.92 → ROI enhancement+YOLO **0.95**.
- ROI 보강 조건: 1-stage confidence < 0.80 또는 difficult class(precision/recall<0.80). YOLO 는 standalone 아님(ROI 내부 class 일관성 검증, cls_loss 가중 핵심).
- ROI 위치 prior: class별 defect chip 좌표 분포를 train split에서만 적합한다. chip 위치 좌표는 KDE, chip-object 개수 벡터는 GMM으로 요약하고, validation/hold-out 평가에는 같은 원천 wafer가 섞이지 않도록 통제한다. current full paper에서는 saliency-map 기반 ROI 표현을 사용하지 않는다.
- flip 증강 배제: wafer 방향성은 설비 레이아웃 기준 공정 의미를 가짐.
- **주의**: backbone 선정값 0.87, tuning 후 1-stage 0.92, final 2-stage 0.95 를 분리 기술. 초기 baseline 0.78 과도 분리. Table 1은 stage-wise ladder로 쓰고, field-validated final row는 선택적 ROI-YOLO 2-stage 0.95임을 명시한다.
- Current Codex paper limitation: Table 1 값은 고정 split validation summary로 제시하고, seed 반복 또는 confidence interval 기반 재현성 평가는 후속 audit 항목으로 남긴다.

### P1 Unknown (Self-Supervised contrastive + HDBSCAN) — `[실전 운영 데이터]`
- InfoNCE(SupCon 아님), grid36(6×6) structured local sampling, flip 미사용(±7° rot, ±5% shift/scale, σ=0.02 noise).
- Global InfoNCE(Queue 16K, FN mask sim≥0.72) + Local InfoNCE + HDBSCAN(size≥12, prob≥0.55, persist≥0.20, eps 0.06).
- **실전 운영 성과 = 13개 후보 group 중 7개(53.8%) 전문가 신규 불량 확인. 이게 전부. F1/ARI/recall 쓰지 않는다.**
- 7-recipe(B0~NEW+tau) synthetic 표는 **실전과 분리된 후속 개발/metric 관리용 benchmark**. 표 옆 캡션에 "실전 13/7 과 분리, 실전 Unknown 은 label 없어 정량 metric 불성립" 1줄 필수.

### P1 맵 생성 — `D:\project\fail-map`
- dual-bucket: Bucket A primary fail map(.Z LZW) + Bucket B Measure(.gz), wafer 식별 + ±10초 오프셋 매칭.
- Cython hex 파싱으로 chip tile array 복원. FTN/QTN/BIN(b)/FBT(f)/QVL(q) + wafer-level yield/sys/lt/tm 을 chip annotation 파일에 병합.
- 32-color 8-bit palette-indexed PNG: Failbit Map 은 이산 색상 ~20개 → 8-bit 사실상 무손실. red-green-blue (RGB) 대비 **약 75% 파일 크기 절감**. PLTE 청크 교체만으로 색상 scheme 즉시 전환. 이 값은 2026-06-06 사용자 확인 기준의 저자 내부 engineering measurement이며, 과거 legacy 절감률 note 는 current full paper package 에서 사용하지 않는다.
- full paper 본문에서는 dual-bucket 또는 timestamp matching 자체를 핵심 기여처럼 길게 쓰지 않는다. 핵심은 wafer image와 chip별 좌표/수치 metadata가 같은 좌표계로 저장되어 UI overlay, chip crop, Known/Unknown model input, 향후 image-tabular multimodal model로 이어진다는 점이다.

### Known 진화 — ROI-YOLO → chip-CNN 불량 식별 지도(defect-id map) — `[추가 생성 chip 데이터, 개발 중]`
- **반드시 "한 단계 더 진화시킨 구조"로 서술** (사용자 직접 지시 2026-06-06). 근거: `recommendation/portfolio.md`, `recommendation/02_ai_portfolio.md`.
- 흐름: Stage 2 가 (A) **ROI-YOLO [양산 중]** → (B) **chip-CNN 불량 식별 지도 [개발 중, 현업 적용 전]** 으로 진화. ROI-YOLO class 확장·처리부담을 줄이려는 후속 모듈이며, 적용 전에는 DRAM YE팀과 label 체계 및 최종 평가 기준을 확정해야 한다.
- 구조: wafer 를 32×32 = 1024 chip(각 200×200 px)으로 분할 → chip-CNN 이 각 chip 을 6-class(none / bank_boundary / fork / scratch / scratch_rot / invalid_main)로 분류 → 결과 32×32 격자가 **불량 식별 지도(defect-id map)**. 색 패턴 = class signature → wafer-level class 식별.
- 수식: `id_{u,v} = argmax chip-CNN(crop_{u,v})`, `M_defect = place id_{u,v} on (u,v) grid` (= 32×32 defect-id map). (portfolio.md 169–177, 231–248)
- 성능 (★ 소스 잠금값, `known-cnn/docs/chipgrid/RESULTS.md`, `known-cnn/docs/chipgrid/RESULTS_DETAIL.md`, `known-cnn/docs/wafer-ensemble/RESULTS.md` — **이 값만 사용, 그 외 obj-id 수치 생성 절대 금지**):
  - current Codex rev064 표준 표기: Failbit intensity map only **validation F1-score 0.436 / hold-out F1-score 0.439**, Failbit intensity map with defect identity map **0.969 / 0.988**, Defect identity map only **0.995 / 0.987**. Table 2 에서는 header를 `Model input setting | Validation F1 | Hold-out F1`로 두고, caption에 `Defect identity map ablation on generated-chip development benchmark (F1-score on 0-1 scale, rounded to three decimals)`을 명시한다.
  - detailed decimal anchors are **0.4359 / 0.4385**, **0.9689 / 0.9879**, and **0.9946 / 0.9872**. rev064 의 paper-facing table values are the same values rounded to three decimals.
  - 88M backbone (compound): input 384 BICUBIC, encoding **R+obj-id+0 3ch** (★ R+G+B 아님 — `known-cnn/docs/wafer-ensemble/RESULTS.md` L92 primary source; 보간된 obj-id 채널이 categorical 신호를 깨는 게 0.9784 한계의 핵심. 자료조사 a56c6e1a 정정), params **~88M**, **val ceiling 0.9784** (test_f1=0.9736 소스 존재하나 paper 본문은 val 0.9784만 사용).
  - 핵심 주장: 정수 obj_id 를 BICUBIC 보간하면 신호가 깨지므로 one-hot native(보간 0) 사용 → BICUBIC 대비 **error 75% 감소**. 그 결과 **1.16M tiny CNN 이 88M backbone val 0.9784 를 넘어 0.9946 달성**("동등 이상" 아님, 명확히 상회).
  - full paper 에서는 rev063 처럼 Failbit intensity map only / Failbit intensity map with defect identity map / Defect identity map only 3행 표를 우선 사용하고, body sentence에서 n=100 per class 개발 run과 n=220 per class defect-map-only 개발 run을 분리한다. compound 88M 비교는 길이 여유가 있거나 reviewer 대응 appendix 에서 사용한다.
  - **Table 2 표기 잠금(2026-06-08 사용자 정정, 0-1 scale 재정정)**: caption은 반드시 `Defect identity map ablation on generated-chip development benchmark (F1-score on 0-1 scale, rounded to three decimals)` 의미를 포함한다. header는 `Model input setting | Validation F1 | Hold-out F1`로 표기한다. 과거 내부 헤더, 내부 version row label, raw-channel shorthand, raw-plus-identity shorthand, legacy raw-plus-identity row wording, old title-case object-identity row/caption wording, `Representation` header, `Scope` header, `Comparison case` header, `Status` column, 그리고 slash-only `Validation / Hold-out` header 를 쓰지 않는다. row labels는 `Failbit intensity map only`, `Failbit intensity map with defect identity map`, `Defect identity map only`로 표기한다. 생성/field-data 여부를 거칠게 적은 caveat 문구나 `not field-applied`, `label definition pending` 같은 문구를 표 cell로 넣지 말고 caption과 본문 문장으로 설명한다. 이 표는 현업 wafer 적용 성능표가 아니며, ROI-YOLO 0.95 실전 성과와 직접 비교하는 표가 아니다.
  - **★ 수치 정책 (2026-06-06 사용자 정정, 2026-06-08 보강 및 재정정)**: 사내 논문이므로 **성능 수치는 파일 출처가 없어도 사용 가능**(저자가 직접 실험·attest). 막을 것은 허구 자체가 아니라 **자기모순**이다 — (1) 같은 값이 rev/절 간에 흔들리면 안 됨(rev2 의 `0.9946→0.9838` flip 금지), (2) 위 obj-id 값은 current full paper 0-1 표기(`0.436/0.439`, `0.969/0.988`, `0.995/0.987`)로 **고정 anchor 일관 유지**, (3) 0-100 percent-style table values는 historical/superseded 표현으로만 취급하고 paper-facing Table 2에는 쓰지 않는다, (4) 실전 vs PoC/개발중 **라벨은 유지**(배포 상태 과대표기 금지).
  - 전부 **`[추가 생성 chip 데이터, 개발 중]`. 실전 ROI-YOLO 0.95(val 별개 축) 와 절대 혼동 금지**(다른 데이터·미양산).
- 사용자 정정(2026-06-06): 불량 식별 지도 방식은 아직 현업 적용 완료 상태가 아니다. 현재 라벨 문제가 남아 있으며 DRAM YE팀과 failure label 체계를 확정한 뒤 최종 성능 평가를 수행할 예정이다.
- YOLO 대비 빠른 이유: ROI 안에서 bounding box를 다시 찾는 detector 추론을 반복하지 않고, 이미 생성된 chip 좌표로 고정 crop을 만들어 작은 chip 분류기를 적용한다. YOLO class 확장과 detector annotation 관리 부담도 낮출 수 있다.
- YOLO 대비 정확할 수 있는 이유: wafer-level image에서는 작게 보이는 chip 결함을 200×200 px chip crop으로 크게 보고, 그 결과를 32×32 wafer grid에 다시 배치하므로 chip-level morphology와 위치 정보를 동시에 유지한다.
- 사용자 정정(2026-06-06): full paper 에서는 multi-label chip / FCM-PM 섹션을 넣지 않는다. P2 또는 별도 appendix 소재로 분리하고, 현재 full paper 본문은 P1 Failbit Map 생성, Known ROI-YOLO, Unknown grouping, UI 수치/좌표 연계, future multimodal 로 집중한다.

### Future work — `D:\project\failure_agent`
- further work 섹션 소재(failure analysis agent). 현재 시스템 성과로 오인 금지. "향후 연구" 로만.

## C. 폴더 → full paper 섹션 매핑
| 폴더 | 확장할 섹션 |
|---|---|
| `D:\project\fail-map` | 2.1 데이터 생성·표현 계층 (palette PNG, Cython, chip-level geometry, FTN/QTN) |
| `D:\project\known-cnn` (+fail-map) | 3. Known 분류 (ConvNeXtV2, Optuna, ROI-YOLO, chip-CNN obj-id map; multi-label chip 제외) |
| `D:\project\unknown-contrastive` | 2.3 Unknown 군집화 (InfoNCE/grid36/HDBSCAN, 7-recipe benchmark) |
| `D:\project\failure_agent` | 4. 결론 → 향후 연구 (failure agent) |

## C-1. Current Codex framing guardrails
- Current Codex rev087 uses the original simplified-paper title, `Failbit Map Known & Unknown 불량 분석 아키텍처`; do not replace it with the rev065 conference-oriented title unless the user explicitly asks.
- Current Codex rev087 keeps the conference-oriented coordinate-preserving framing as the current body baseline: Failbit Map is presented as a hierarchical spatial record connecting wafer image, chip crop, chip-level numerical metadata, model output, and review artifact in one wafer coordinate system. This framing is a writing/positioning improvement only; it does not introduce a new metric or deployment claim.
- Current Codex rev087 makes the shared §5.2 design principle explicit: wafer spatial meaning is preserved through palette indices, flip exclusion, and categorical defect identity channels. This is contribution framing only, not a new experiment, metric, or field-deployment claim.
- Current Codex rev087 adds a §5.2 contribution-positioning sentence: the paper does not claim to invent ConvNeXt V2, YOLO, contrastive learning, or HDBSCAN; its contribution is the wafer coordinate-preserving integration of data artifacts, model decisions, review UI, and label governance. This is novelty-scope clarification only.
- Current Codex rev087 restores the simplified-paper data-generation formula figures as paper Figures 1 and 2: Cython hex-to-grade conversion and palette-indexed PNG compression. The ROI-YOLO cascade and defect identity map evolution figures are Figures 3 and 4.
- Current Codex rev087 keeps `1.1. Technical overview` with a four-column overview table and text workflow/service-path lines. The UI row uses paper-facing `Browser UI, backend API, pyramid cache`, and the service path is grounded in `D:\project\mapviewer\docs\TECHNICAL_OVERVIEW.md` (created/modified on 2026-05-04), but paper-facing text must omit internal authentication/runtime details such as SAML, OneLogin, systemd, and Uvicorn.
- Current Codex rev087 adds one §1.1 overview-scope sentence clarifying that ROI-YOLO is the field-validated Known path while the defect identity map row is the generated-chip-data development path explained in §3.2. This is source-provenance clarification only; it does not add a metric, experiment, deployment claim, or table status cell.
- Current Codex rev087 defines `Information Noise-Contrastive Estimation (InfoNCE)` before Table 1's Unknown row. This is abbreviation-compliance cleanup only, not a new evidence item, metric, experiment, or deployment claim.
- Current Codex rev087 defines `Dynamic Random Access Memory (DRAM)` and `User Interface (UI)` at their first body use. This is format/compliance cleanup only, not a new evidence, metric, or deployment claim.
- Current Codex rev087 normalizes the remaining Table 1 shorthand from `Defect-ID` to `Defect identity` and the related stability wording from `defect-id 표현` to `defect identity map 표현`, aligning with the locked paper-facing method term.
- Current Codex rev087 keeps the locked defect identity ablation as Table 2. The earlier Known validation ladder values are preserved in prose, and the ablation table keeps `Model input setting`, `Validation F1`, `Hold-out F1`, the three locked row labels, and 0-1 F1-score values.
- Current Codex rev087 narrows §3.2 wording around the defect identity map: detector-search reduction is framed structurally, and the F1 discussion is explicitly introduced as generated-chip-data expression evidence rather than field-speed or field-accuracy evidence.
- Current Codex rev087 further normalizes residual paper-facing identity shorthand: `chip identity` was changed to `chip coordinate` or `defect identity`, and `정수 identity map` was changed to `categorical defect identity map`. This is terminology safety only.
- Current Codex rev087 clarifies the Unknown operating policy from `D:\project\unknown-contrastive\docs\contrastive-eval\PRODUCTION.md` and `DECISIONS.md`: missed-defect risk is prioritized over false-alarm minimization, new patterns are allowed to remain as small cluster/noise candidates, and only medoid/composite-map-reviewed groups are promoted to label candidates. This is rationale only, not a new field metric.
- Current Codex rev087 adds the viewer-scale contrast from `recommendation\portfolio.md`: prior review was about 48 wafers per query, while the file-index/cache viewer layer supports about 20,000 wafers/day cumulative comparison. This is operating-scale context, not labor, cost, or yield-impact evidence.
- Current Codex rev087 normalizes the Unknown throughput note to `wafer/s` while keeping the measured values unchanged.
- Current Codex rev087 adds one Unknown generated/development robustness sentence from `D:\project\unknown-contrastive\docs\paper\RESULTS.md` §19.2: a defect-only NEW-recipe 3-seed HDBSCAN epsilon sweep over 21 cells had identical ARI/noise to four decimals, so epsilon is interpreted as a sensitivity-check item rather than field performance or a load-bearing operational metric.
- Do not add `recommendation/figures/p1_fig_architecture.png` as a fifth figure in Codex unless the verifier/table-figure budget is changed or another figure is removed.
- Current Codex rev087 keeps the three-level Failbit Map framing as qualitative problem framing: wafer-global shape, zone location, and chip-internal defect morphology.
- `full_paper_rev067_codex.md` is an unverified stale-title markdown draft and is not a current submission candidate.
- FTN/QTN overlay is described as review evidence for comparing spatial pattern labels with electrical failure signatures. Avoid adding unverified bitline/wordline mechanism claims unless a source file supports them.
- Future failure-analysis agent wording stays future-facing: contrastive embedding may be reused as a retrieval index, but production claims require real engineering records, access control, audit logs, and reviewer feedback storage.
- External dataset guardrail: WM-811K and MixedWM38 are wafer-map pattern classification benchmarks, not chip-crop image-grid datasets. They may be mentioned only as public wafer-map related work or as evidence that public wafer benchmarks differ from this paper's chip-level image/metadata structure. Do not use them as validation datasets for the defect identity map. For a general "large image as a bag/grid of local patches" analogy, whole-slide image (WSI) datasets such as CAMELYON/TCGA are structurally closer than WM-811K/MixedWM38.
- Rev081 paper-facing rule: do not name WM-811K or MixedWM38 in the main paper unless the user explicitly asks for a related-work paragraph; the current main paper only states the generic public wafer-map benchmark distinction.

## E. 그림 자산 (형편없는 draft 도식 교체용)
- **교체 대상(형편없는 도식)**: 루트 `_fig_yolo_roi.png`, `_fig_cluster.png`, `.tmp_obj_candidates.png` — checkerboard 만화형. full paper 에 쓰지 말 것. 실제 wafer 이미지로 교체한다.
- 새 이미지 생성 금지(Rule 10). 본문 그림은 아래 **실제 figure(`recommendation/figures/`)** 를 `![캡션](경로)` 로 삽입하고 `Figure N.` 캡션을 그림 하단(9pt)에 단다.
- 아키텍처 개념도는 ASCII/텍스트 박스로(이미지 아님).
- P1 full paper 에 쓰는 figure (그 외 chip_*/fcm_pm_*/trend_*/p3_* 는 P2·P3용이라 **제외**):

| 용도 | 파일 |
|---|---|
| Failbit Map 불량 패턴 예시 (Known 16-class / Unknown 후보) | `wafer_center_scratch.png`, `wafer_center_bank_boundary.png`, `wafer_edge_top_scratch.png`, `wafer_edge_ring_scratch_rot.png`, `wafer_ringdots.png`, `wafer_brokenring.png`, `wafer_crescentarc.png` |
| Known 2-stage ROI-YOLO (실제 wafer) | **codex rev063 전용**: `roi_yolo_cascade_panel.png` 한 장. 이미지 안에는 `(a)/(b)/(c)` 라벨을 넣지 않고, DOCX 빌더의 `Figure labels:` 텍스트 행으로 이미지 위에 표시한다. **★ claude 트랙 canonical (rev85 LOCK — 단일 panel 이 정본)**: ROI(2.2.2)는 `p1_fig_roi_panel.png` **단일 1장**((a)Failbit Map (b)ROI (c)chip)으로 Figure 2 에 둔다. **`p1_fig_roi_yolo_wafer.png`/`p1_fig_roi_yolo_chip.png` 2-split 재분리는 금지(그림 5→6장 회귀, rev89 폐기 원인).** 과거 '2-split canonical' 표기는 rev85 사용자 hand-tuning 으로 폐기 — reviewer 는 단일 panel 을 정본으로 채점한다. |
| chip-CNN defect identity map (Failbit intensity map → defect-id), `[추가 생성, 개발 중]` 라벨 | `AAN585_00P_18_20260501_010000_97.6_2_EE_NORMAL_raw.png` + `..._objid.png`, `ACZ452_00P_14_20260501_010000_97.6_2_PT_NORMAL_raw.png` + `..._objid.png`. codex rev063에서는 이미지 안 라벨 없이 DOCX 빌더의 `Figure labels:` 텍스트 행으로 `(a)/(b)/(c)/(d)`를 표시한다. |
| Known 진화 — obj-id 다중객체 검출(실제 wafer, 색상별 instance 박스) | **★ 영구 제외 (codex·claude 양 트랙).** writer 는 `p1_fig_objid_instances.png` 를 **어떤 경우에도 본문에 삽입하지 않는다**(사용자 "그냥 일반 wafer 이미지" 지적). 넣어도 post-process `integrate_figures.py` 가 강제 제거하므로 채점만 손해. instances figure / 관련 설명 문장 일절 금지. |
| Known 진화(ROI-YOLO→obj-id) 설명 figure | **★ claude 트랙 canonical**: 생성 흐름 = `p1_fig_objid_flow.png`(matplotlib, chip 좌표→32×32 격자 분류→obj-id map), raw↔obj-id 구분력 = `p1_fig_objid_compare.png`(4-panel: raw A·B 구분 어려움 / obj-id A·B 색 구분; 원본 AAN585/ACZ452 raw+objid). 둘 다 `[생성 데이터, 개발 중]`. (legacy `p1_objid_overview/matching/map_explained` 는 미사용 — 위 2개가 정본) |
| Unknown 후보 패턴 (실제 wafer) | `wafer_ringdots.png` (군집 후보 예시). |
| 전체 시스템 아키텍처 | `p1_fig_architecture.png` (matplotlib). **★ 사용자 승인(2026-06-25)으로 rev85 LOCK 해제 — claude 트랙 rev139 부터 §1.1 ASCII 개념도를 이 그림으로 교체하여 본문 사용(Figure 1). 그림 안 수치(F1 0.92/0.95·obj-id 개발중·InfoNCE/grid36/HDBSCAN/medoid)가 본문 anchor 와 정합함을 이미지 분석으로 확인.** writer 는 §1.1 에 이 그림을 유지한다(ASCII 개념도로 되돌리지 말 것). |

> **★ claude full paper 정본 그림 8장 (rev139 기준 — 사용자 승인으로 갱신, reviewer 는 이 명단 기준으로 채점)**: ① `p1_fig_architecture.png`(전체 시스템 아키텍처, Figure 1 — 2026-06-25 사용자 승인으로 §1.1 ASCII 대체) ② `wafer_edge_ring_scratch_rot.png`(Failbit Map 예시, Figure 2) ③ `p1_fig_roi_panel.png`(ROI 2-stage 단일 panel (a)Failbit Map (b)ROI (c)chip, Figure 3) ④ `p1_fig_objid_flow.png`(obj-id 생성흐름, Figure 4) ⑤ `p1_fig_objid_compare.png`(raw↔obj-id 4-panel, Figure 5) ⑥ `wafer_ringdots.png`(Unknown 후보, Figure 6) ⑦ `p2_fig_chip_examples.png`(chip multi-label 라벨 공간, Figure 7) ⑧ `fcm_pm_panel.png`(FCM-PM augmentation, Figure 8). **roi_yolo 2-split·instances·panel(cascade)·legacy overview/matching 는 전부 불사용**. (rev85 의 '그림 5장·architecture 미사용' LOCK 은 2026-06-25 사용자 재결정으로 폐기 — architecture 는 §1.1 ASCII 를 대체해 Figure 1 로 사용.)

## D. 금지
- mapviewer request count / peak / commit ownership 수치: 사용자 승인 없이 본문 금지.
- 외부 학회/박사논문 비교/학술 venue 톤 금지(사내 지원 트랙). 단 본 산출물은 "사내 논문상" 이므로 학술 품질은 추구하되 외부 venue 명시는 하지 않는다.
