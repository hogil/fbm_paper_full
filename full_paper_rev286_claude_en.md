# Hybrid Failbit Map Analysis Architecture for Known Classification and Unknown Discovery

Hogil Choi<sup>1</sup>, Jihoon Hong<sup>1</sup>, Sungho Kim<sup>2</sup>

<sup>1</sup> QIE Group, Memory Manufacturing Technology Center, Memory Business, Samsung Electronics
<sup>2</sup> DRAM YE Team, Memory Manufacturing Technology Center, Memory Business, Samsung Electronics

---

**Abstract** - **A Failbit Map from semiconductor Electrical Die Sorting (EDS) holds about 10 million pixels per wafer and is central to failure-pattern analysis, but large-scale retrieval was difficult and the few retrievable maps were reviewed manually by yield engineers. We built a large-scale pipeline: Cython sped up conversion by about 100x, and 8-bit palette-indexed PNG (vs 24-bit RGB) cut the stored file size by about 80%. Known failures used a 2-stage classifier, ConvNeXtV2 with Region-of-Interest YOLO (ROI-YOLO) rechecking of low-confidence samples, reaching a weighted F1 score of 0.95. For Unknown failures, a grid-level local loss on a self-supervised contrastive (InfoNCE) embedding kept small regions from being diluted, and HDBSCAN grouped candidates by Failbit Map similarity; on 2,000 real wafer images from one day, 13 candidate groups were produced and yield engineers confirmed 7 as actual failures. For chips with overlapping failures that single-failure classification cannot separate, a chip multi-label structure was trained on single-failure labels, since overlapping labels are scarce; FCM-PM (Full-Cover CutMix with Pair Mask) reached a bit-F1 score of 0.9927 and a False Alarm Rate (FAR) of 0.00% on a 2-combo synthesis set.**

**Keywords:** Wafer Failure Analysis, Failbit Map, EDS Test, ConvNeXtV2, ROI-YOLO, Object-ID Map, Contrastive Learning, HDBSCAN, Palette PNG, Multi-label Classification, CutMix

## 1. Introduction

### 1.1. Background, problem, and contribution

Dynamic Random Access Memory (DRAM) is built from cells, the smallest units that store data, and from cell arrays that hold many cells. In a production line, EDS testing checks whether each cell array operates correctly and measures its electrical characteristics. The number of failed cells in each array is quantized into a Grade from 0 (normal) to 7 (maximum failure), and placing these grades on wafer coordinates yields the Failbit Map (FBM). EDS also produces a chip-level measure value, and yield engineers first analyze chip failures from this value. The Failbit Map then provides the location and spatial distribution of that failure within the wafer. The relationship from cell to Failbit Map is summarized in Figure 1.

![From DRAM cell to Failbit Map](figures/full_paper_rev260/fig01_dram_to_fbm.png)

**Figure 1.** From DRAM cell to Failbit Map. EDS counts failed cells in the cell array, converts the count into Grade 0-7, and places the grades on wafer coordinates.

The Failbit Map carries location information that a failure-rate number alone cannot reveal. For the same failure rate, the equipment and process condition to check first differ depending on whether the failures sit near the edge, cluster in the center, or lean in one direction. Measure values can quickly confirm some chip-level failures, but where a failure appears within the wafer and what shape it takes can be seen only by analyzing the Failbit Map.

![Failbit Map examples](figures/full_paper_rev260/fig02_fbm_examples.png)

**Figure 2.** Examples of Failbit Map patterns. The same measure value level can correspond to different spatial patterns such as center cluster, edge ring, or broken ring.

In the previous analysis environment, only a few Failbit Maps could be retrieved at once, and storing large image volumes long-term was difficult, so image-based analysis could not be routinely used. Yield engineers checked failure status from chip-level measure values and classified recurring failures using formula- and threshold-based rules. This approach was fast and well-founded, but it depended on the rules each yield engineer defined. Chip-level numbers alone also make it hard to see the relation to neighboring chips, the location within the wafer, and the failure shape as a whole. Without this spatial information, it is difficult to decide which process condition to check first. An edge-ring, center-cluster, or directional pattern can each point to a different cause, which is why the Failbit Map must be examined. For a wafer classified as a failure, yield engineers used the Failbit Map and Transmission Electron Microscopy (TEM) to section and inspect samples, examined features such as Critical Dimension (CD) shifts or misalignment, and interpreted the process structure and layout cause. The problem was that large numbers of Failbit Maps could not be generated quickly, and the needed wafers could not be retrieved immediately.

Failures in a Failbit Map are divided into Known and Unknown failures. Known failures are registered repeated patterns within the 16-class label set and can be trained with supervised learning. Unknown failures are newly occurring or unregistered patterns, so they have no ground-truth labels and cannot be evaluated directly with a classification metric such as the F1 score.

This work addresses two recurring operational problems: the bottleneck in large-scale Failbit Map processing and the dependence on manual failure judgment. For this, raw logs were converted into Failbit Map images and chip annotations, and a data structure was built so they could be retrieved together with chip-level measure values. After deployment, the pipeline generated FBMs on a one-hour cycle and enabled on-screen review. Known failure was validated with a 2-stage structure that rechecks only the samples whose first-stage confidence is low with ROI-YOLO, and a Stage-2 alternative that uses chip coordinates was evaluated separately on generated data. HDBSCAN clustering derived candidate groups for yield engineers to review first. Cases where two or more failures overlap on one chip were treated separately as a chip multi-label problem.

The overall work can be divided into the data pipeline, Known failure classification and recheck, Unknown candidate-group discovery, chip multi-label, and the web viewer. First, a data pipeline was built to generate large numbers of Failbit Maps quickly and to retrieve the wafers needed. Second, Known failure was validated with a 2-stage structure that rechecks only low-confidence samples with ROI-YOLO. Third, Unknown failure candidate groups were derived using self-supervised embeddings and HDBSCAN. Fourth, a chip multi-label structure was added for chips with overlapping failures. Fifth, the web viewer lets yield engineers review the map, chip overlay, and measure value together, and register a new failure when needed.

### 1.2. Related work

Earlier studies classified wafer map images with a CNN or applied selective learning [1][2], and others inferred chip failures from wafer-level labels or classified mixed-type bin maps [3][4]. The search for unlabeled patterns extended into contrastive learning, open-set recognition, and deep clustering [5]-[9]. For model size and efficiency, vision-backbone comparison studies were used as reference [10], and for detection-based recheck, Faster R-CNN and Cascade R-CNN were taken as base references [11][12]. HDBSCAN is the basis of the density-based clustering implementation [13]. ConvNeXtV2 was used as the Known classification backbone [14], and the YOLO detector family and recent implementations were referenced for the ROI-YOLO comparison [15][16]. The categorical-class representation of the object-id map draws on categorical-embedding work [17]. This paper focuses less on comparing scores on public datasets and more on processing in-house Failbit Maps, retrieving wafers, and connecting Known and Unknown analysis. The difference from prior work is summarized in Table 1.

**Table 1. Differences from prior wafer-map studies.**

| Comparison axis | Prior wafer-map studies | This paper |
|------|------|------|
| Data unit | Centered on wafer images or bin maps | Failbit Map linked with chip coordinates and measure value |
| Failure analysis | Centered on single classification or clustering | Known classification separated from Unknown candidate grouping |
| Chip recheck | Centered on a detector or wafer-level decision | Comparison of ROI-YOLO with the object-id map alternative |
| Overlapping failure | Centered on real mixed labels or single labels | 2-combo validation with FCM-PM and val_margin |
| Operational use | Centered on experimental results | Connected through the web viewer to operational impact |

## 2. Method, results, and discussion

### 2.1. Proposed method

The overall structure is divided into Failbit Map generation, Known failure classification, Unknown failure candidate grouping, chip multi-label, and the web viewer. Table 2 summarizes the overall structure and the role of each step.

**Table 2. Main components of the proposed method.**

| Component | Method | Role |
|------|------|------|
| Failbit Map generation | Raw log conversion, palette PNG storage, chip coordinate alignment | Generate maps and align chip information |
| Known failure | ConvNeXtV2, selective ROI-YOLO | Classify and recheck existing failures |
| Stage-2 follow-up | object-id map | Check a chip-coordinate fixed-crop alternative |
| Unknown failure | Contrastive embedding, HDBSCAN | Produce new candidate groups |
| Chip multi-label | FCM-PM, val_margin, NB reject | Classify overlapping-failure chips |
| Web viewer | Search, overlay, measurement view | Yield-engineering inspection screen |

The overall data flow is shown in Figure 3.

![Coordinate-preserving analysis pipeline](figures/full_paper_rev260/fig02_pipeline_architecture.png)

**Figure 3.** Coordinate-preserving analysis pipeline. EDS raw logs and measure values are aligned with the Failbit Map and chip coordinates, then used by the Known, Unknown, and chip multi-label paths. Confirmed cases can be stored as future training data.

Figure 3 shows the flow that branches into the Known, Unknown, and chip multi-label paths after Failbit Map generation.


#### 2.1.1. Data representation and coordinate-aligned loading

The data bottleneck appeared in two places: conversion speed and storage size. One wafer holds about 10 million pixels, and about 20,000 wafers are processed each day, so the raw hex payload was decoded with a Cython parser, about 100x faster than pure Python (Figure 4a). Storage was another major constraint. Although a Failbit Map uses only about 20 colors in practice, these fit within a 32-entry palette table. Images were therefore stored as 8-bit palette PNG instead of 24-bit RGB (Figure 4b). This reduced the stored file size by about 80% compared with RGB storage. The color scheme can be changed by replacing only the PLTE (PNG palette) chunk. A lossless method with higher compression could be considered, but its longer processing time is unsuitable for hourly generation. JPEG was excluded because lossy compression can blend grade colors. The grade colors must also stay intact in the training input so that the model learns only the actual failure pattern. The Failbit Map raw log and the chip-level measure value were matched by wafer identifier within a ±10 s offset and stored on the same wafer and chip-coordinate basis. The loaded data is used for both on-screen display and model input, linked by wafer ID and chip coordinates.

![Cython parser and palette PNG](figures/full_paper_rev260/fig04_cython_palette.png)

**Figure 4.** Cython parser and palette-indexed PNG. (a) Hex-to-grade conversion is accelerated by Cython. (b) Palette PNG stores grade colors as indices instead of RGB triples, reducing storage while preserving grade values.

#### 2.1.2. Known failure classification structure

**Backbone selection and staged design.** The Known failure classifier was trained on 16 major repeated-failure classes using about 1,500 labeled Failbit Maps with a 4:1 stratified split. ConvNeXtV2-Base was used as the backbone. Learning rate, weight decay, focal loss, and class weight were then tuned to build the 1-stage classifier, and finally ROI-YOLO 2-stage was applied only to low-confidence samples. The performance change is reported separately in Table 5.

**ROI-YOLO 2-stage correction.** Samples with low first-stage CNN confidence often had ambiguous class boundaries or failure regions too small to give strong evidence in the whole-wafer image. Only these samples were rechecked with ROI-YOLO. This avoided running the detector on every wafer.

Stage 2 was applied only when the first-stage prediction confidence was below 0.70.

![ROI-YOLO 2-stage detection](figures/full_paper_rev260/fig03_roi_yolo.png)

**Figure 5.** ROI-YOLO 2-stage check. Panels show (a) the Failbit Map, (b) the ROI region set by the class prior (blue circle) with YOLO detection boxes inside (red), and (c) the scratch detail of the detected chip (confidence 0.91). Failures that look small and scattered globally become distinct under ROI-limited detection and chip-level inspection, while regions outside the ROI are skipped.

**Chip-CNN object-id map.** The object-id map is a development item that reformulates the validated ROI-YOLO Stage-2 as chip-coordinate fixed-crop classification rather than detection. ROI-YOLO evaluates many candidate boxes and crops to find objects inside the ROI and performs non-maximum suppression (NMS). The object-id map, in contrast, uses the chip coordinates already present in the product layout to extract each chip as a fixed crop and displays the class prediction on the wafer grid (Figure 6). On generated data, class separation was clearer than in the raw Failbit Map, with lower computation than ROI-YOLO.

![Class separability comparison of raw and object-id map](figures/full_paper_rev260/fig_objid_compare.png)

**Figure 6.** Class separability of raw Failbit Map vs object-id map. Generated examples show improved class separability in object-id maps, where each chip crop class is color-coded. [Generated data only, under development]

Table 3 compares the Stage-2 computation of ROI-YOLO and the object-id map. Because Stage 2 here uses chip-coordinate fixed crops rather than a detector, the chip-CNN has about 1.16 million parameters and requires about 0.31 GFLOPs, which is about 1/600 of the 194.9 GFLOPs of public YOLO11x.[^1] The classification performance on the generated evaluation set is reported separately in Table 6.

**Table 3. Stage-2 computation of ROI-YOLO and chip-CNN object-id map. The table reports parameter count and calculated GFLOPs only; classification results are listed in Table 6.**

| Stage-2 method | Parameters | Operations |
|------|:--:|:--:|
| ROI-YOLO detector | 56.9 million | 194.9 GFLOPs |
| chip-CNN object-id map | 1.16 million | 0.31 GFLOPs |


#### 2.1.3. Unknown failure clustering structure

In real data, new failures outside the existing 16 classes appear rarely, and ground-truth labels are almost absent. Supervised contrastive learning (SupCon [5]) risks absorbing a new pattern into an existing class, so we trained a contrastive embedding that does not depend on labels. The initial implementation used the InfoNCE (Information Noise-Contrastive Estimation) loss and a MoCo (Momentum Contrast) [18] queue of size 4096 to compensate for the scarcity of negatives in small batches.

The learned embedding is clustered with HDBSCAN. The HDBSCAN clustering result is shown as candidate groups in the web viewer so that yield engineers can inspect new failure candidates first. The final development configuration uses a global/local contrastive loss with the queue size extended to 16K, and a noise wafer is included in a group only when nearest-neighbor voting exceeds the threshold. Because missing a failure is more critical than a false alarm, we prioritized reducing missed failures.

![Unknown failure embedding flow](figures/full_paper_rev260/fig05_unknown_flow.png)

**Figure 7.** Unknown failure embedding flow. Augmented views of the same FBM are kept close in the embedding space, while a different FBM is separated; HDBSCAN then groups the embeddings for yield-engineer review.

#### 2.1.4. Chip-level multi-label classification structure

A chip-level image cropped from a Failbit Map sometimes shows two or more failures together. A single-label approach that selects only one failure class cannot analyze such a chip properly. We therefore developed a separate chip multi-label analysis path. For training and evaluation, four classes, bank_boundary, fork, scratch, and scratch_rot, were expressed as independent sigmoid outputs. Here, a 2-combo in which two classes appear together in one chip was defined as a multi-label problem rather than a single softmax class. Actual 2-combo ground-truth labels, however, are hard to collect in sufficient quantity.

The source data consisted of four types of single-failure chips (bank_boundary, fork, scratch, scratch_rot) obtained from in-house EDS Failbit Maps. Training used only single-failure chip labels. The 2-combo evaluation set was synthesized separately from the locations and Grade probability distributions observed in single-failure chips, and it comprised 4 single types, 6 2-combo types, plus Normal, Invalid, and out-of-distribution (OOD) noise chips. During training, FCM-PM builds the 2-combo learning signal from single-source chips, and evaluation is performed on the prebuilt single and 2-combo synthesis evaluation set. The backbone, ConvNeXtV2 pretrained with a Fully Convolutional Masked Autoencoder (FCMAE), was retrained to fit chip images, and the head outputs an independent sigmoid probability per class.

![Example chip label space](figures/full_paper_rev260/fig05_chip_label_space.png)

**Figure 8.** Label space of chip-level multi-label classification. Top row: four single failures with distinct shapes (bank_boundary, fork, scratch, scratch_rot). Bottom row: a synthetic 2-combo example and negative samples used in the controlled benchmark (Normal, Invalid, OOD/Starburst). [Real chip source + domain synthesis]

Synthesis was limited to methods that preserve the original grade. Because Grade 0-7 is a discrete value, averaging colors as in Mixup creates intermediate grades that do not actually exist. Diffusion was not suitable here because it requires many labels and substantial compute resources. A CutMix [19] family method that preserves the original Grade value by region was therefore chosen. However, using random-rectangle CutMix alone can cut off the failure region or leave a residual synthetic background that gets learned as a false-positive signal.

To build a learning signal for two overlapping failures from single-failure sources, FCM-PM combines two single-failure chips in a full-cover manner to make an A+B mixed chip, and at the same time trains the A-only and B-only masked views (Figure 9). The mixed view supplies the positive learning signal, and the masked view keeps the synthetic background from being learned as a false positive. The FAR is computed as the false-detection ratio among negatives (FP_neg/N_neg), and the checkpoint is chosen at the epoch where val_margin = mean(p_pos) - max(p_neg) is largest on the validation set.

Changing the loss function alone was not enough. Focal and Asymmetric Loss (ASL) [20] preserved part of the positive response but did not sufficiently suppress the negative tail. Particularly in single-only training, the positive probability of the second bit in a 2-combo stayed low, down to about 0.42 on average. FCM raised the second bit's average positive probability to about 0.54 by synthesizing two single sources so that they cover the whole chip area. Pair Mask, in turn, blocked the background created during synthesis from being learned as a failure signal. After that, val_margin selected the checkpoint with the widest gap between positive and negative (Figure 10a), and a Gaussian Naive Bayes (NB) reject excluded OOD-shaped probability vectors that did not match any registered 4-bit profile (Figure 10b). The ensemble was used only as an overfitting check, and the Knowledge Distillation student [21] was retained as a lightweight candidate.

![FCM-PM augmentation](figures/full_paper_rev260/fig06_fcm_pm.png)

**Figure 9.** FCM-PM augmentation for chip multi-label learning. Full-Cover CutMix makes A+B mixed views, while Pair Mask trains A-only/B-only views to suppress synthetic-background false positives. [Real chip source + domain synthesis]


![val_margin selection and NB reject sidecar](figures/full_paper_rev260/fig07_probability_control.png)

**Figure 10.** Probability control in chip multi-label learning. (a) val_margin selects the checkpoint whose probability gap tracks held-out bit-F1 score better than val-F1 score. (b) NB reject checks the whole 4-bit probability profile and rejects an OOD-shaped vector when no known profile matches. [Real chip source + domain synthesis]



#### 2.1.5. Analysis screen (web viewer) structure

The web viewer loads the generated Failbit Map as pyramid tiles so that panning and zooming stay responsive even on a large wafer map. On the same screen, a yield engineer reviews the wafer map, chip overlay, chip-level measure value, and candidate group side by side. When a new failure candidate needs to be recorded, the wafer and chip information can be registered for later use in building training data.

### 2.2. Results and operational application

#### 2.2.1. Result scope

Table 4 summarizes the validation conditions and scope for each reported value. Operational values and model performance metrics were not combined.

**Table 4. Validation scope of reported results.**

| Item | Value | Scope |
|------|------|------|
| Known | weighted F1 score 0.95 | Real-wafer data validation |
| Unknown | 13 candidate groups / 7 actual failure groups | Yield-engineer review |
| object-id | val/hold-out F1 score 0.9946 / 0.9872 | Generated-data validation |
| FCM-PM | bit-F1 score 0.9927 / Total FAR 0.00% | Controlled synthesis evaluation |
| FBM gen./storage | ~100x / ~80% file-size reduction | Internal measurement |
| Impact | KRW 12.3B | Internal achievement certification |

#### 2.2.2. Known failure results

Table 5 compares backbone, fine-tuning, and selective ROI-YOLO in order on the same split. Pretraining and tuning are shown together in the table to show the change in F1 score from fine-tuning and 2-stage application.

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
| ConvNeXtV2 + HPO + ROI-YOLO | low-confidence sample 2-stage | 0.95 |

MaxViT-Base and ConvNeXtV2-Base both showed a weighted F1 score of 0.87, but ConvNeXtV2-Base was chosen as the final backbone because its parameters are about 26% smaller, from 119.5M to 88.6M, and its FLOPs are about 39% lower, from 74.2 GFLOPs to 45.1 GFLOPs. Hyperparameter Optimization (HPO) then raised the score to 0.92, and ROI-YOLO, applied only to low-confidence samples, gave the final 0.95.

Table 6 reports only the generated-data development value of the object-id map.[^2]

**Table 6. Object-id map development metrics for the Known Stage-2 follow-up. [Generated-data validation]**

| Input configuration | Reported value | Scope |
|------|------|:------:|
| Selected obj-only | val F1 score 0.9946 / hold-out F1 score 0.9872 | Generated-data validation |

#### 2.2.3. Unknown failure results

The finding that 7 of the 13 candidate groups were confirmed as actual failures was not interpreted as classification precision. Self-supervised embedding and HDBSCAN were applied to 2,000 real wafer images without ground-truth labels, producing 13 Unknown failure candidate groups. Yield engineers confirmed 7 of the 13 groups as actual failure groups (Table 4).

On a separate generated-data evaluation set with ground-truth labels, the contrastive-learning configuration, queue, and stronger negative sampling were applied step by step to check performance (Table 7). Compared with the plain backbone, fewer failure candidates were discarded as noise, and the final configuration achieved the highest Completeness on the generated evaluation set. Completeness is a development metric that evaluates the degree of cluster separation on generated data and is not summed with the operational Unknown result.

**Table 7. Component-isolation benchmark for Unknown clustering. [Generated-data validation]**

| Recipe | Capture | Noise (%) | Completeness | n_cluster |
|------|:------:|:------:|:------:|:------:|
| Global contrastive only | 0.9337 | 15.78 | 0.9468 | 40 |
| + Local DenseCL | 0.9361 | 13.87 | 0.9502 | 37 |
| + MoCo Queue | 0.9356 | 9.45 | 0.9474 | 41 |
| + NV-Retriever NEG | 0.9250 | 8.23 | 0.9485 | 40 |
| + NeCo (5-tool) | 0.9559 | 6.66 | 0.9660 | 35 |
| Final + tau=0.5 post-processing | 0.9619 | 0.00 | 0.9679 | 35 |

#### 2.2.4. Chip multi-label results

Table 8 quantifies the effects of these design choices. Binary Cross-Entropy (BCE) with label smoothing, Focal [22], and ASL [20] did not suppress FAR consistently, and false alarms stayed high even under plain CutMix. Adding Pair Mask reduced FAR, and the single model combining FCM-PM with val_margin was adopted as the final recipe of the controlled synthesis evaluation. The ensemble, kept as a comparison to check for overfitting, improved performance only slightly at about 5x the cost, so it was excluded from the final configuration. The Knowledge Distillation student was retained as a lightweight candidate.

**Table 8. Stage-wise performance of chip multi-label training recipes (2,000 per class). Evaluation uses real failure-chip sources and domain probability-distribution synthesis; not a production deployment result.**

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

In the synthesis-evaluation ablation, removing Pair Mask (with every other setting and the reject gate identical) led the residual background from synthesis to be learned as a false failure signal, raising Total FAR from 0.00% to 100%. This comparison confirmed that the false alarm suppression came directly from Pair Mask, not the reject gate.

Here, the bit-F1 score treats one chip label as a bit vector with as many bits as classes, measures each bit independently, and micro-averages them; the positive set includes the 4 single types and the 6 2-combo types. Total FAR 0.00% is the value with no false detection among about 2,640 negative chips combining Normal, Invalid, and the 4 OOD types. This is a methodology validation that distinguishes overlapping failures and lowers FAR under a setting that mimics having only single-failure labels, and the value is limited to the controlled synthesis-evaluation scope.

#### 2.2.5. System and operational results

The viewer/data pipeline built here has been used since 2025 to generate FBMs for all DRAM D1a/b/c/d products. On this screen, a yield engineer searches a wafer ID and reviews the map overlay, composite, and chip-level measure values. When needed, the yield engineer registers a new failure. The usage scope here covers FBM generation, on-screen review, overlay, and composite; it does not mean that serving of the Known, Unknown, or chip model, or the object-id map, is in full production. After deployment, the review scale increased from about 48 wafers per batch to about 20,000 wafers per day (Table 9). Analysis labor then dropped by about 90%. A single High Bandwidth Memory (HBM) product case showed a yield improvement of about 0.02%p, and the work was internally certified by the Memory Manufacturing Technology Center as a contribution of about KRW 12.3B.[^3] This quantitative contribution is limited to the DRAM viewer/data pipeline basis. It was therefore not summed with the model performance metrics in Tables 5-8.

**Table 9. Change in FBM review after viewer/data pipeline deployment.**

| Item | Previous method | After deployment |
|------|------|------|
| Retrieval scale | About 48 wafers checked | About 20,000 wafers checked per day |
| Checked items | Map and measure values checked separately | Overlay, composite, and chip measure values checked together |
| New failure management | Records kept by each yield engineer | Registration history checked in the web viewer |

![single wafer view](figures/full_paper_rev260/fig09_webapp_viewer.png) ![grid view](figures/full_paper_rev260/fig11b_webapp_grid.png)

**Figure 11.** Screenshot of the deployed web viewer. (a) single wafer view with chip overlay and measurement panel; (b) grid view of Unknown candidate clusters. Search, map view, overlay, measurement, and navigator thumbnails are integrated in one screen.

### 2.3. Discussion and limitations

The originality of this work does not lie in simply applying an existing model. In the Known failure path, the global decision of ConvNeXtV2 was not taken as final; instead, a selective 2-stage structure rechecks only low-confidence samples with ROI-YOLO. The object-id map is not an attempt to replace ROI-YOLO with a smaller model; it is a shift in problem definition. Because the product layout already fixes each chip's coordinates, the map avoids box search, regression, and NMS. It instead assigns a class id to each chip position on the wafer grid. For chip multi-label, under a condition where actual 2-combo labels are scarce, FCM-PM built the overlapping-failure learning signal using only single-failure chip sources, and val_margin with NB reject controlled weak positives and false alarms together.

Results from generated data and synthesis-based evaluation were kept separate from actual wafer results. Public wafer datasets are usually die-level bin maps, so they are hard to compare directly with this work, which views the failure shape inside the chip together with the measure value.

**Excluded designs and rationale.** Non-adopted design choices were ruled out through separate measurements. For Unknown failure, unnecessary elements were excluded through component-removal experiments (Section 2.1.3), and a setting that fine-tuned the pretrained backbone more heavily was excluded because training became unstable on the small dataset. Isotonic calibration reached a high in-sample F1 score of 0.9931 but was judged to overfit under a separate validation criterion.

**Evaluation conditions.** For each comparison, the input conditions and the criterion for selecting the best model were kept identical.

### 2.4. Future work

Future work will expand the product scope and the analysis granularity. Flash YE has also requested a feasibility review for applying this flow to bin-map and chip multi-label analysis, and any actual deployment will proceed as a separate task after checking data access rights and product differences. On the cause-analysis side, we will reinforce the function that shows wafer images and chip-level measure values on one screen and records the supporting evidence. The contrastive embedding can be extended into a search index that finds similar past cases and yield-engineering records. Any large-language-model-based function that summarizes image, trend, and history information will remain an assistant feature and will require engineer approval and history logging.

## 3. Conclusion

This work treats the Failbit Map not as a one-time image for lookup, but as part of an analysis flow that leads to yield-engineer review and training-data accumulation. With Cython conversion and palette PNG storage, Failbit Maps are generated every hour at scale, and the map and chip-level measure values can be reviewed on the same screen. Known failure reached a weighted F1 score of 0.95 by rechecking only low-confidence samples with ROI-YOLO. Unknown failure candidate groups were derived using self-supervised embeddings and HDBSCAN, and yield engineers confirmed 7 of the 13 candidate groups as actual failure groups. The chip multi-label structure also addressed the problem that overlapping-failure chips cannot be classified by a single-failure analysis approach, and FCM-PM reached a bit-F1 score of 0.9927 and FAR 0.00% on a 2-combo synthesis evaluation set. The core contribution is not the performance of any single model, but the implementation of an operational analysis workflow that connects Failbit Map generation, yield-engineer review, and training-data accumulation.

[^1]: About 0.31 GFLOPs (307.9 million FLOPs) is a deterministic value obtained by summing the layer-wise MACs in the obj-id classifier ChipGridCNN architecture (32x32 grid input, 6 convolution stages plus a classification head), and it is consistent with about 1.16 million parameters.

[^2]: The object-id map was repeated over 5 seeds (42/1/7/100/234) on the same chip-source split. The means were validation F1 score 0.9905±0.0045 and hold-out F1 score 0.9831±0.0050, and the value in Table 6 is the best-seed result. Even when 10% noise was injected into the chip-CNN output, the wafer-level F1 score change stayed within the 5-seed standard deviation.

[^3]: The approximately 90% labor reduction is an operational result, and the approximately 0.02%p yield improvement is based on a single HBM product case (not annualized). The approximately KRW 12.3B is an internally certified contribution amount from the Memory Manufacturing Technology Center.

## References

[1] Nakazawa, T. et al., "Wafer map defect pattern classification and image retrieval using convolutional neural network," *IEEE Trans. Semicond. Manuf.*, Vol. **31**, no. 2, pp. 309-314, 2018.

[2] Alawieh, M. B. et al., "Wafer map defect patterns classification using deep selective learning," in *Proc. 57th ACM/IEEE Design Automation Conf. (DAC)*, pp. 1-6, 2020.

[3] Lee, H. et al., "Classification of chip-level defect types in wafer bin maps using only wafer-level labels," *J. Manuf. Sci. Eng.*, Vol. **146**, no. 7, article 070902, 2024.

[4] Kyeong, K. and Kim, H., "Classification of mixed-type defect patterns in wafer bin maps using convolutional neural networks," *IEEE Trans. Semicond. Manuf.*, Vol. **31**, no. 3, pp. 395-402, 2018.

[5] Khosla, P. et al., "Supervised contrastive learning," in *Advances in Neural Information Processing Systems (NeurIPS)*, Vol. **33**, pp. 18661-18673, 2020.

[6] Chen, T. et al., "A simple framework for contrastive learning of visual representations," in *Proc. Int. Conf. on Machine Learning (ICML)*, PMLR 119, pp. 1597-1607, 2020.

[7] Shin, J.-S. et al., "Enhanced detection of unknown defect patterns on wafer bin maps based on an open-set recognition approach," *Comput. Ind.*, Vol. **164**, article 104208, 2025.

[8] Baek, I. and Kim, S. B., "Contrastive deep clustering for detecting new defect patterns in wafer bin maps," *Int. J. Adv. Manuf. Technol.*, Vol. **130**, pp. 3561-3571, 2024.

[9] Jang, J. et al., "Decision fusion approach for detecting unknown wafer bin map patterns based on a deep multitask learning model," *Expert Syst. Appl.*, Vol. **215**, article 119363, 2023.

[10] Shi, B. et al., "When do we not need larger vision models?," in *Proc. European Conf. on Computer Vision (ECCV)*, pp. 444-462, 2024.

[11] Ren, S. et al., "Faster R-CNN: Towards real-time object detection with region proposal networks," *IEEE Trans. Pattern Anal. Mach. Intell.*, Vol. **39**, no. 6, pp. 1137-1149, 2017.

[12] Cai, Z. and Vasconcelos, N., "Cascade R-CNN: Delving into high quality object detection," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, pp. 6154-6162, 2018.

[13] Campello, R. J. G. B. et al., "Density-based clustering based on hierarchical density estimates," in *Proc. Pacific-Asia Conf. on Knowledge Discovery and Data Mining (PAKDD)*, pp. 160-172, 2013.

[14] Woo, S. et al., "ConvNeXt V2: Co-designing and scaling ConvNets with masked autoencoders," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, pp. 16133-16142, 2023.

[15] Redmon, J. et al., "You only look once: Unified, real-time object detection," in *Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)*, pp. 779-788, 2016.

[16] Jocher, G. and Qiu, J., "Ultralytics YOLO11," 2024.

[17] Guo, C. and Berkhahn, F., "Entity embeddings of categorical variables," *arXiv preprint* arXiv:1604.06737, 2016.

[18] He, K. et al., "Momentum contrast for unsupervised visual representation learning," in *Proc. IEEE/CVF Conf. on Computer Vision and Pattern Recognition (CVPR)*, pp. 9729-9738, 2020.

[19] Yun, S. et al., "CutMix: Regularization strategy to train strong classifiers with localizable features," in *Proc. IEEE/CVF Int. Conf. on Computer Vision (ICCV)*, pp. 6023-6032, 2019.

[20] Ridnik, T. et al., "Asymmetric loss for multi-label classification," in *Proc. IEEE/CVF Int. Conf. on Computer Vision (ICCV)*, pp. 82-91, 2021.

[21] Hinton, G. et al., "Distilling the knowledge in a neural network," *arXiv preprint* arXiv:1503.02531, 2015.

[22] Lin, T.-Y. et al., "Focal loss for dense object detection," in *Proc. IEEE Int. Conf. on Computer Vision (ICCV)*, pp. 2980-2988, 2017.

<!-- rev273 changelog: rev272(EN) 위에 2~3차 검수 반영. 미번역 각주→빌더 분기(Footnotes), Known/Unknown 정의 동어반복 제거, 초록 Unknown/Known 2-stage 문장 정리, 'field' 13곳 제거(engineering confirmation/real-wafer/engineers/in-house/operational), negative reinforcement→stronger negative sampling, NMS 첫 등장 풀이, ±기호, HBM single 명시, 결론 마지막 문장 '동작하는 구조=working analysis flow' 의미 보존 재서술. 수치·표·figure·참고문헌 전부 보존. -->
