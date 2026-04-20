# Hybrid Failbit Map Analysis Architecture for Known Classification and Unknown Discovery

Gildong Hong¹, Cheolsu Kim¹

¹ Semiconductor Research Center, Samsung Electronics, Hwaseong-si, Republic of Korea

(Abstract)

Failbit Maps are ultra-high-resolution data generated in semiconductor EDS tests, with roughly 10 million pixels per wafer, and are a key source for defect-pattern analysis. However, in practical operations, large-scale retrieval and inspection of Failbit Maps has been impractical, and even limited analysis has depended heavily on manual inspection by engineers. This work addresses that limitation by building a large-scale Failbit Map data pipeline and implementing an architecture in which Known defects are handled by two-stage supervised classification and Unknown defects are discovered by self-supervised learning. Data transformation speed was improved by about 100x through Cython, while image size was reduced by about 75% through Palette PNG. For Known defects, a ConvNeXtV2-based first-stage classifier was combined with a second-stage ROI (Region of Interest)-based YOLO classifier for low-confidence samples, achieving an F1-score of 0.95. For Unknown defects, a SimCLR-family model was trained without labels, and contrastive learning was performed with grid structured local sampling to reflect wafer zone-based defect interpretation. After training on 10,000 Failbit Maps collected over five production days, application to 2,000 maps from an additional day detected 13 defect groups, and 7 were confirmed as real defect groups by domain engineers, demonstrating practical applicability in production.

Keywords: Failbit Map, Wafer Failure Analysis, ConvNeXtV2, YOLO, Contrastive Learning, HDBSCAN

## 1. INTRODUCTION

A Failbit Map represents defect severity at the memory-cell-block level in EDS testing using grades from 0 to 7. Because a single wafer contains roughly 10 million blocks, it is an ultra-high-resolution representation of defect location and morphology. In current practice, Measure-based analysis alone cannot capture this information, making exhaustive Failbit Map analysis necessary.

Two limitations have prevented practical deployment. First, the existing system did not have sufficient processing performance to transform equipment logs into large numbers of Failbit Maps and to store and browse them at scale. Equipment logs are typically 10 to 50 MB per wafer, and some products generate about 2,000 wafers per day. Under the previous environment, large-volume processing was limited by speed and memory constraints, and the number of maps that could be checked at once was restricted to about 48. Second, even when maps were generated, defect judgment and type identification still depended on manual inspection by engineers, making full analysis difficult. To address these limitations, this paper proposes an integrated analysis architecture composed of a data pipeline for continuously generating, storing, and serving large volumes of Failbit Maps from raw data, a two-stage supervised framework for Known defects, and a self-supervised framework for Unknown defects. The main contributions are as follows.

First, we implemented a data-processing foundation capable of real-time ingestion of large equipment logs and hourly Failbit Map generation, enabling sustained large-scale map creation and operational use. Second, for Known defects, we used ConvNeXt V2 to classify, in the first stage, the types and distribution patterns of defective chips at the wafer level, then applied ROI-based YOLO to samples prone to confusion because of similar distribution patterns for chip object detection and second-stage refinement. Third, for newly emerging defects not registered in the existing taxonomy, we implemented a SimCLR-family contrastive-learning framework for Unknown defect discovery. In addition, grid structured local sampling was introduced to also encode spatial occurrence information, enabling more precise Unknown defect detection.

## 2. PROPOSED METHOD

The architecture consists of a data pipeline, a two-stage Known classifier, and a self-supervised Unknown detector, deployed as a dedicated analysis web application[1].

### 2.1 DATA PIPELINE

The data pipeline was designed to ingest equipment Raw Logs in real time and generate Failbit Maps on an hourly cycle. The main bottlenecks were the hex-to-grade conversion speed for roughly 10 million encoded test values per wafer and the storage of ultra-high-resolution images; the former was accelerated about 100x with Cython (Fig. 1), and the latter was reduced by about 75% with palette-indexed PNG (Fig. 2).

<table>
<tr><td>
<div align="center"><b>Hex-to-grade conversion</b></div>

```text
    Raw:
        090B0C0D0E0F090A0B0C

    Decoding:
        "0C" -> "C" -> 12 (hex to decimal) -> 3


    Python:
        interpreter-based loop execution

    Cython:
        compiled integer loop execution

    Grade:
        0 2 3 4 5 6 0 1 2 3
```
</td></tr>
</table>

**Fig. 1.** Hex-to-grade conversion accelerated by Cython

<table>
<tr><td>
<div align="center"><b>RGB PNG vs Palette-indexed PNG</b></div>

```text
    RGB PNG:
        [(123,54,24), (123,54,24), ..., (123,54,24)],
        [(123,54,24), (123,54,24), ..., (123,54,24)]

    Palette-indexed PNG:
        P[3] = (123,54,24)
        [(3), (3), ..., (3)],
        [(3), (3), ..., (3)]

    RGB_to_Palette:
        (123,54,24) -> (3)
```
</td></tr>
</table>

**Fig. 2.** Palette-indexed PNG for failbit map compression.

### 2.2 Known Defect Classification

Known-defect analysis targeted 16 registered classes and used 1,500 labeled Failbit Maps to design a two-stage structure combining a ConvNeXtV2[2]-based wafer-level first-stage classifier and a second-stage ROI (Region of Interest)-based YOLO for low-confidence samples.
While the ConvNeXtV2-based wafer-level classifier showed high overall accuracy and throughput, its performance degraded on classes with similar wafer-level distributions of defective chips. To compensate for this, a two-stage design was introduced in which ROI-based YOLO further inspects low-confidence samples and evaluates defect-chip morphology and appearance patterns within the ROI (Fig. 3).

![Fig. 3. Two-stage known-defect classification with ROI-YOLO.](_fig_yolo_roi.png)

**Fig. 3.** Representative patterns of Class A(a) and Class B(b), and a true Class A sample(c) misclassified as Class B by the first-stage CNN but corrected to Class A by the second-stage ROI-YOLO. The blue circle indicates the ROI, and the red boxes denote YOLO detections of chip-level defect patterns within the ROI.


**Table 1.** Backbone comparison and staged improvements for known-fail classification (16-class, test Weighted F1)

| Configuration | Pre Train | Test F1 | Note |
|---|---|---:|---|
| ViT | IN-21k | 0.81 | fine-tune |
| Swin | IN-1k | 0.84 | fine-tune |
| EffNetV2 | IN-1k | 0.85 | fine-tune |
| MaxViT | IN-21k | 0.87 | fine-tune |
| ConvNeXtV2 (Ref) | IN-22k | 0.87 | selected |
| Ref + Optuna | IN-22k | 0.92 | HPO |
| Ref + Optuna + ROI | IN-22k | 0.95 | 2-stage |

MaxViT[3] and ConvNeXtV2 (Ref) achieved the same test Weighted F1 of 0.87, but ConvNeXtV2 was selected as the final backbone because it was more efficient, with about 26% fewer parameters (119.5M -> 88.6M) and about 39% fewer FLOPs (74.2G -> 45.1G). This choice reflects the operational environment in which more than 20,000 wafer Failbit Maps are generated per day. Optuna was then used to optimize fine-tuning hyperparameters such as learning rate, weight decay, focal loss, and class weight, improving test Weighted F1 to 0.92, and ROI-YOLO refinement further increased the final score to 0.95.

### 2.3 Unknown Defect Discovery

Unknown defect discovery was defined as the task of grouping similar patterns and identifying candidate defect groups. Using 10,000 production maps from five days, contrastive learning was performed on a SimCLR[4]-family model by applying grid structured local sampling to reflect wafer zone-based defect interpretation, and HDBSCAN[5] was then applied to a separate set of 2,000 maps from one additional day to group similar patterns.

![Fig. 4. Unknown-defect grouping on production images.](_fig_cluster.png)

**Fig. 4.** Unknown-fail grouping on production images.


For Unknown defects, grouping on 2,000 production images yielded 13 candidate groups, and domain-engineer validation confirmed 7 of them as real defect groups. The remaining 6 groups were interpreted as lot-specific warning-level noise patterns or patterns that did not lead to actual chip defects.

## 3. CONCLUSION

This study implemented an integrated architecture for full Failbit Map generation and automated defect analysis. Cython optimization and palette-indexed PNG enabled large-scale map generation, while the combination of Known two-stage classification and Unknown self-supervised discovery automated and advanced the analysis workflow.

## REFERENCES

[1] FBM, https://www.failbitmap.com

[2] S. Woo et al., "ConvNeXt V2: Co-Designing and Scaling ConvNets With Masked Autoencoders," in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 16133-16142, 2023.

[3] Z. Tu et al., "MaxViT: Multi-Axis Vision Transformer," in Proceedings of the European Conference on Computer Vision (ECCV), pp. 459-479, 2022.

[4] T. Chen, S. Kornblith, M. Norouzi, and G. Hinton, "A Simple Framework for Contrastive Learning of Visual Representations," in Proceedings of the 37th International Conference on Machine Learning (ICML), PMLR 119, pp. 1597-1607, 2020.

[5] R. J. G. B. Campello, D. Moulavi, and J. Sander, "Density-Based Clustering Based on Hierarchical Density Estimates," in Advances in Knowledge Discovery and Data Mining, PAKDD 2013, pp. 160-172, 2013.
