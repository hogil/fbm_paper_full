"""
논문용 Figure 생성 스크립트
- fig1_architecture.png  : 전체 시스템 파이프라인
- fig2_data_pipeline.png : Failbit Map 데이터 생성 파이프라인
- fig3_palette_png.png   : Palette PNG 구조 및 활용
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# ── 공통 스타일 ──────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.linewidth": 0.8,
})

C = {
    "supervised":   "#2563EB",   # 파랑 - 지도학습
    "unsupervised": "#16A34A",   # 초록 - 비지도학습
    "data":         "#7C3AED",   # 보라 - 데이터
    "human":        "#EA580C",   # 주황 - Human-in-the-loop
    "input":        "#374151",   # 회색 - 입력
    "output":       "#0F766E",   # 청록 - 출력
    "arrow":        "#4B5563",
    "bg":           "#F9FAFB",
}

def box(ax, x, y, w, h, text, color, fontsize=8.5, alpha=0.92, textcolor="white", radius=0.04):
    fancy = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        linewidth=1.1, edgecolor=color,
        facecolor=color, alpha=alpha, zorder=3
    )
    ax.add_patch(fancy)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, color=textcolor, fontweight="bold",
            zorder=4, wrap=True, multialignment="center")

def arrow(ax, x1, y1, x2, y2, color="#4B5563", lw=1.4):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=12),
                zorder=2)

def label(ax, x, y, text, fontsize=7.5, color="#374151", style="normal"):
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, color=color, fontstyle=style, zorder=5)


# ════════════════════════════════════════════════════════════════
# FIG 1 — 전체 시스템 아키텍처
# ════════════════════════════════════════════════════════════════
def make_fig1():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7.5)
    ax.set_facecolor(C["bg"]); fig.patch.set_facecolor(C["bg"])
    ax.axis("off")
    ax.set_title("Fig. 1  전체 시스템 파이프라인", fontsize=12,
                 fontweight="bold", pad=10, color="#111827")

    # ── 입력 ──────────────────────────────────────────────────
    box(ax, 5.5, 6.9, 4.2, 0.55,
        "Failbit Map 입력 이미지  (Wafer-Level, 384×384)",
        C["input"], fontsize=8.5)

    # ── 두 갈래 분기 레이블 ───────────────────────────────────
    arrow(ax, 5.5, 6.62, 2.7, 6.0)
    arrow(ax, 5.5, 6.62, 8.3, 6.0)
    label(ax, 2.0, 6.2, "등록 불량", 8, C["supervised"])
    label(ax, 9.0, 6.2, "미등록 불량", 8, C["unsupervised"])

    # ════ 왼쪽 : 지도학습 파이프라인 ═════════════════════════
    sup_boxes = [
        (2.7, 5.65, "Stage 1\nConvNeXtV2-Base\n9-class 분류", C["supervised"]),
        (2.7, 4.60, "Grad-CAM ROI 추출\n공간 사전 정보(spatial prior)\nα-블렌딩·선택적 적용", C["supervised"]),
        (2.7, 3.35, "Stage 2\nYOLO 이차 검증\n(ROI crop 입력)", C["supervised"]),
        (2.7, 2.25, "라벨 오류 후보 탐지\n→ 학습 데이터 교정", C["supervised"]),
        (2.7, 1.25, "분류 결과\nWeighted F1 = 0.95", C["output"]),
    ]
    for i, (x, y, t, c) in enumerate(sup_boxes):
        box(ax, x, y, 3.6, 0.70, t, c, fontsize=7.8)
        if i < len(sup_boxes) - 1:
            arrow(ax, x, y - 0.35, x, sup_boxes[i+1][1] + 0.35)

    # Optuna 사이드 노트
    fancy_opt = FancyBboxPatch((0.12, 4.25), 1.55, 1.55,
        boxstyle="round,pad=0.05", linewidth=0.9,
        edgecolor="#9333EA", facecolor="#F5F3FF", alpha=0.9, zorder=3)
    ax.add_patch(fancy_opt)
    ax.text(0.89, 5.02,
            "Optuna\nTPE Sampler\nLR · WD\nScheduler\nAugment",
            ha="center", va="center", fontsize=7, color="#6B21A8", zorder=4)
    arrow(ax, 1.67, 4.90, 0.92, 5.65, color="#9333EA", lw=1)

    # ════ 오른쪽 : 비지도학습 파이프라인 ══════════════════════
    uns_boxes = [
        (8.3, 5.65, "ConvNeXtV2 백본 (동결)\n지도학습 가중치 재사용\n+ MLP Proj. Head (128-d)", C["unsupervised"]),
        (8.3, 4.55, "Global InfoNCE + Queue(16K)\n+ Local InfoNCE (Grid-36)\nNO flip 증강", C["unsupervised"]),
        (8.3, 3.40, "HDBSCAN 군집화\n품질 필터(size·prob·persist)\nmedoid 대표 이미지 저장", C["unsupervised"]),
        (8.3, 2.25, "군집 요약 & 대표 이미지\n전문가 검토 인터페이스", C["unsupervised"]),
        (8.3, 1.25, "평가 지표\nSilhouette · 전문가 동의율\n→ F1 개선(재학습 후)", C["output"]),
    ]
    for i, (x, y, t, c) in enumerate(uns_boxes):
        box(ax, x, y, 3.6, 0.70, t, c, fontsize=7.8)
        if i < len(uns_boxes) - 1:
            arrow(ax, x, y - 0.35, x, uns_boxes[i+1][1] + 0.35)

    # ════ 하단 : Human-in-the-loop ════════════════════════════
    box(ax, 5.5, 0.38, 5.0, 0.55,
        "Human-in-the-loop  →  신규 클래스 등록  →  지도학습 재학습",
        C["human"], fontsize=8.2)
    arrow(ax, 2.7, 1.25 - 0.35, 3.4, 0.38 + 0.27)
    arrow(ax, 8.3, 1.25 - 0.35, 7.6, 0.38 + 0.27)

    # ── 범례 ──────────────────────────────────────────────────
    legend_items = [
        mpatches.Patch(color=C["supervised"],   label="지도학습 (Supervised)"),
        mpatches.Patch(color=C["unsupervised"], label="비지도학습 (Self-supervised)"),
        mpatches.Patch(color=C["output"],       label="출력 / 평가"),
        mpatches.Patch(color=C["human"],        label="Human-in-the-loop"),
        mpatches.Patch(color="#9333EA",         label="Optuna 하이퍼파라미터 최적화"),
    ]
    ax.legend(handles=legend_items, loc="lower right",
              fontsize=7.5, framealpha=0.9, edgecolor="#D1D5DB",
              bbox_to_anchor=(1.0, 0.0))

    fig.tight_layout()
    fig.savefig("fig1_architecture.png", dpi=200, bbox_inches="tight",
                facecolor=C["bg"])
    print("✅ fig1_architecture.png 저장")
    plt.close(fig)


# ════════════════════════════════════════════════════════════════
# FIG 2 — Failbit Map 데이터 생성 파이프라인
# ════════════════════════════════════════════════════════════════
def make_fig2():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.set_facecolor(C["bg"]); fig.patch.set_facecolor(C["bg"])
    ax.axis("off")
    ax.set_title("Fig. 2  Failbit Map 데이터 생성 파이프라인", fontsize=12,
                 fontweight="bold", pad=10, color="#111827")

    # ── Bucket A / B ──────────────────────────────────────────
    box(ax, 2.5, 7.3, 3.2, 0.65,
        "Bucket A  (.Z / .gz)\n주 Failbit 로그 (S3)", "#1D4ED8", fontsize=8.2)
    box(ax, 7.5, 7.3, 3.2, 0.65,
        "Bucket B  (.gz)\nFBT / QVL 설비 계측 로그 (S3)", "#1D4ED8", fontsize=8.2)

    # 병렬 다운로드 표시
    for cx in [2.5, 7.5]:
        arrow(ax, cx, 6.97, cx, 6.45)
    ax.text(5.0, 6.72, "병렬 다운로드  (최대 256 연결)",
            ha="center", va="center", fontsize=7.8,
            color="#1D4ED8", style="italic")

    # ── 압축 해제 ──────────────────────────────────────────────
    box(ax, 5.0, 6.15, 6.5, 0.58,
        "LZW / gzip / 7z 압축 해제  (재귀 6단계, 멀티스레드)", C["data"], fontsize=8.2)
    arrow(ax, 5.0, 5.86, 5.0, 5.40)

    # ── Cython 파싱 ────────────────────────────────────────────
    box(ax, 5.0, 5.10, 6.5, 0.65,
        "Cython 초고속 Hex 파싱  (Python 대비 3~5× 속도)\n"
        "0x00/09→G0  0x0A/0B→G1  ···  0x0E/0F→G6", C["data"], fontsize=8.0)
    arrow(ax, 5.0, 4.77, 5.0, 4.28)

    # ── 두 경로 분기 ───────────────────────────────────────────
    arrow(ax, 5.0, 4.28, 2.5, 3.80)
    arrow(ax, 5.0, 4.28, 7.5, 3.80)
    ax.text(3.0, 4.08, "Chip Grid 구성", ha="center", fontsize=7.5, color="#374151")
    ax.text(7.0, 4.08, "시간 매칭 (±10s)", ha="center", fontsize=7.5, color="#374151")

    box(ax, 2.5, 3.48, 3.6, 0.60,
        "Chip Grid  [x,y] → Grade\n회전(rot_code) 적용", "#374151", fontsize=8.0)
    box(ax, 7.5, 3.48, 3.6, 0.60,
        "Bucket B 칩별 FBT/QVL\n좌표 기준 정합", "#374151", fontsize=8.0)

    arrow(ax, 2.5, 3.18, 5.0, 2.72)
    arrow(ax, 7.5, 3.18, 5.0, 2.72)

    # ── Palette PNG 생성 ───────────────────────────────────────
    box(ax, 5.0, 2.42, 6.5, 0.65,
        "8-bit 팔레트 인덱스 PNG 생성\n"
        "idx 0~7: Grade  |  idx 8~11: BG·텍스트·경계  |  idx 12~31: BIN 색상",
        C["output"], fontsize=8.0)

    # Palette 구조 미니 시각화 ──────────────────────────────────
    pal_x0, pal_y0 = 1.2, 1.65
    colors_pal = [
        "#111827","#1E3A5F","#1D4ED8","#2563EB","#3B82F6","#60A5FA","#93C5FD","#BFDBFE",
        "#F3F4F6","#374151","#6B7280","#9CA3AF",
        "#EF4444","#F97316","#EAB308","#22C55E","#14B8A6","#3B82F6","#8B5CF6","#EC4899",
    ]
    cell_w, cell_h = 0.30, 0.22
    grade_labels = [f"G{i}" for i in range(8)]
    extra_labels = ["BG","Txt","Bdr","Inv"] + [f"B{i}" for i in range(8)]
    all_labels = grade_labels + extra_labels
    for i, (c, lbl) in enumerate(zip(colors_pal, all_labels)):
        px = pal_x0 + i * cell_w
        rect = mpatches.FancyBboxPatch(
            (px, pal_y0), cell_w - 0.02, cell_h,
            boxstyle="square,pad=0", linewidth=0.6,
            edgecolor="#9CA3AF", facecolor=c, zorder=3)
        ax.add_patch(rect)
        ax.text(px + cell_w/2 - 0.01, pal_y0 + cell_h/2,
                lbl, ha="center", va="center",
                fontsize=5.5, color="white" if i < 12 else "#111827", zorder=4)
    ax.text(pal_x0 + len(colors_pal)*cell_w/2, pal_y0 - 0.12,
            "32색 팔레트 (Grade 인덱스 0~7 고정 → PLTE 교체만으로 즉시 색상 변경)",
            ha="center", fontsize=7.2, color="#374151")
    ax.annotate("", xy=(pal_x0 + 0.01, pal_y0 + cell_h + 0.05),
                xytext=(5.0, 2.09),
                arrowprops=dict(arrowstyle="-|>", color=C["output"], lw=1.2))

    # ── 최종 출력 ──────────────────────────────────────────────
    box(ax, 5.0, 1.20, 6.5, 0.60,
        "칩 좌표 JSON  |  FBT/QVL 칩별 계측값  |  웨이퍼 yield·systematic 불량률\n"
        "(f/q 배열화 → ~65% 용량 절감)", C["human"], fontsize=8.0)
    arrow(ax, 5.0, 2.09, 5.0, 1.50)

    fig.tight_layout()
    fig.savefig("fig2_data_pipeline.png", dpi=200, bbox_inches="tight",
                facecolor=C["bg"])
    print("✅ fig2_data_pipeline.png 저장")
    plt.close(fig)


# ════════════════════════════════════════════════════════════════
# FIG 3 — ROI Enhancement 교정 사례 (플레이스홀더)
# ════════════════════════════════════════════════════════════════
def make_fig3():
    fig, axes = plt.subplots(2, 4, figsize=(12, 5.5))
    fig.patch.set_facecolor(C["bg"])
    fig.suptitle(
        "Fig. 3  ROI Enhancement 교정 사례\n"
        "(Stage 1 오분류 → Stage 2 ROI 보강으로 정답 교정)",
        fontsize=11, fontweight="bold", color="#111827", y=0.98
    )

    pairs = [
        ("edge_loc → edge_ring\n(외곽 경계 집중)",  "#2563EB", "#16A34A"),
        ("local → random\n(군집 위치 확인)",         "#7C3AED", "#16A34A"),
        ("edge_ring → edge_loc\n(위치 패턴 구분)",   "#2563EB", "#16A34A"),
        ("near_full → donut\n(중심 공백 확인)",       "#EA580C", "#16A34A"),
    ]
    panel_titles = ["원본 이미지", "Grad-CAM Heat", "ROI BBox", "YOLO 검출"]

    for col, (desc, c_wrong, c_right) in enumerate(pairs):
        for row in range(2):
            ax = axes[row][col]
            ax.set_facecolor("#E5E7EB")
            ax.set_xticks([]); ax.set_yticks([])

            if row == 0:
                # 상단 패널 타이틀
                ax.set_title(panel_titles[col % 4] if col < 4 else "",
                             fontsize=8, color="#374151", pad=3)

            # 간단한 wafer 원 시각화
            theta = np.linspace(0, 2*np.pi, 200)
            ax.fill(0.5 + 0.42*np.cos(theta), 0.5 + 0.42*np.sin(theta),
                    color="#D1D5DB", zorder=1)
            ax.set_xlim(0, 1); ax.set_ylim(0, 1)

            if row == 0:  # Stage 1 (오분류)
                # 랜덤 불량 패턴
                np.random.seed(col * 7)
                xs = np.random.uniform(0.25, 0.75, 15)
                ys = np.random.uniform(0.25, 0.75, 15)
                ax.scatter(xs, ys, s=18, color=c_wrong, alpha=0.7, zorder=3)
                ax.text(0.5, 0.07, f"Stage 1 예측: 오분류",
                        ha="center", fontsize=6.5, color=c_wrong, fontweight="bold")
            else:  # Stage 2 (교정)
                np.random.seed(col * 7)
                xs = np.random.uniform(0.25, 0.75, 15)
                ys = np.random.uniform(0.25, 0.75, 15)
                ax.scatter(xs, ys, s=18, color=c_right, alpha=0.7, zorder=3)
                # ROI box
                roi = mpatches.FancyBboxPatch((0.22, 0.22), 0.56, 0.56,
                    boxstyle="square,pad=0", linewidth=2,
                    edgecolor="#EF4444", facecolor="none", zorder=4)
                ax.add_patch(roi)
                ax.text(0.5, 0.07, f"Stage 2 교정: 정답",
                        ha="center", fontsize=6.5, color=c_right, fontweight="bold")

        # 교정 설명
        axes[0][col].set_xlabel(desc, fontsize=7, color="#374151", labelpad=2)

    # 행 레이블
    for row, lbl in enumerate(["Stage 1  (오분류)", "Stage 2  (ROI 교정 후 정답)"]):
        axes[row][0].set_ylabel(lbl, fontsize=8, fontweight="bold",
                                 color=C["supervised"] if row==0 else C["unsupervised"],
                                 labelpad=4)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig("fig3_roi_correction.png", dpi=200, bbox_inches="tight",
                facecolor=C["bg"])
    print("✅ fig3_roi_correction.png 저장")
    plt.close(fig)


# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import os
    os.chdir(r"D:\project\image_classification")
    make_fig1()
    make_fig2()
    make_fig3()
    print("\n🎉 모든 Figure 생성 완료")
    print("   fig1_architecture.png")
    print("   fig2_data_pipeline.png")
    print("   fig3_roi_correction.png")
