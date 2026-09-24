# figure: 自控-频域-例530-K范围.png
"""例5.30（习题5-31 燕山大学2018）第(2)问：交点随 K 线性缩放 → 三个临界增益 → 稳定区间。

K = 5 时三个负实轴交点为 −10、−5、−0.2；由 G(jω) = K/(jω)·G1(jω)（ν = 1，lim G1 = 1）
可知交点横坐标与 K 成正比：

    x1(K) = −2K,   x2(K) = −K,   x3(K) = −0.04K

三者各自撞上 −1 的临界增益 K1 = 0.5、K2 = 1、K3 = 25。沿曲线的三个交点依次是
负、正、负穿越，落在 −1 左侧的个数：0 → 稳定；1 → 不稳定；2 → 稳定；3 → 不稳定。
稳定区 K ∈ (0, 0.5) ∪ (1, 25)。

面板 (a) 用**双对数**画三条轨迹（斜率 1 的直线），水平参考线 |x| = 1 即 −1 点；
面板 (b) 是「落在 −1 左侧的交点数」阶梯。图内文字一律「纯文本 + Unicode 数学」，
不与 $…$ 混排（mathtext 接管整串会掉汉字字形）。

Build: ..\\build.ps1 -File .\\ch5-ex530-krange.py
"""
from __future__ import annotations

import numpy as np

import matplotlib.pyplot as plt

import figures_style as fs

STABLE = "#E3EFE3"
UNSTABLE = "#F8E7E3"
GREEN = "#2F6B3A"

K_INF, K_SUP = 0.12, 300.0
CRIT = [0.5, 1.0, 25.0]
SLOPES = [2.0, 1.0, 0.04]          # 交点 −10、−5、−0.2 的 |x|/K
TRACKS = [("交点 −10：|x| = 2K", SLOPES[0], fs.MAG, "0"),
          ("交点 −5：|x| = K", SLOPES[1], fs.PHA, "1"),
          ("交点 −0.2：|x| = 0.04K", SLOPES[2], GREEN, "2")]
BANDS = [(K_INF, 0.5, STABLE, "稳定", 0),
         (0.5, 1.0, UNSTABLE, "不稳定", 1),
         (1.0, 25.0, STABLE, "稳定", 2),
         (25.0, K_SUP, UNSTABLE, "不稳定", 3)]


def verify() -> None:
    """三处硬核对：临界增益、各区间的交点计数、奇偶与稳定性的对应。"""
    for slope, kc in zip(SLOPES, CRIT):
        assert abs(1.0 / slope - kc) < 1e-12, (slope, kc)
    for lo, hi, _, tag, n in BANDS:
        rep = np.sqrt(lo * hi)                      # 区间几何中点代表该区间
        left = sum(1 for sl in SLOPES if sl * rep > 1.0)
        assert left == n, (lo, hi, left, n)
        assert (tag == "不稳定") == (n % 2 == 1), (lo, hi, tag, n)
    print("k-range check ok: 临界增益 %s（由交点 -10/-5/-0.2 反求）；"
          "稳定区 (0,0.5)∪(1,25)；计数 0→稳定,1→不稳,2→稳定,3→不稳" % CRIT)


def main() -> None:
    fs.use_style()
    fig, (ax, ax2) = plt.subplots(
        2, 1, figsize=(9.6, 6.0), sharex=True,
        gridspec_kw=dict(height_ratios=[3.0, 1.0], hspace=0.17))
    # 显式排版：本图是 GridSpec 双面板 + 图级文字，tight_layout 会直接拒绝执行
    fig.subplots_adjust(left=0.088, right=0.986, top=0.885, bottom=0.160)

    for a in (ax, ax2):
        a.set_xscale("log")
        for lo, hi, c, _, _ in BANDS:
            a.axvspan(lo, hi, color=c, lw=0.0, zorder=0)
    ax.set_yscale("log")          # 双对数：三条轨迹才真是斜率 1 的直线
    ax2.tick_params(labelbottom=True)

    # ---------- (a) 三条交点轨迹 ----------
    kk = np.array([K_INF, K_SUP])
    for _, slope, color, _ in TRACKS:
        ax.plot(kk, slope * kk, color=color, lw=2.4, zorder=4)
    ax.axhline(1.0, color=fs.INK, lw=1.6, ls=(0, (6, 3)), zorder=5)

    for kc in CRIT:
        ax.axvline(kc, color=fs.SUB, lw=1.0, ls=(0, (2, 2)), zorder=3)
        ax.text(kc, 1080.0, f"K = {kc:g}", ha="center", va="center", fontsize=11,
                color=fs.INK, zorder=9,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.4))
    for lo, hi, _, tag, _ in BANDS:
        ax.text(np.sqrt(lo * hi), 590.0, tag, ha="center", va="center", fontsize=12,
                color=GREEN if tag == "稳定" else fs.PHA, zorder=9,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.4))

    ax.axvline(5.0, color=fs.INK, lw=1.2, ls=(0, (1, 2.4)), zorder=6)
    ax.text(5.0, 250.0, "题给 K = 5", ha="center", va="center", fontsize=11,
            color=fs.INK, zorder=9,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.6))
    ax.text(0.135, 1.62, "|x| = 1 即 −1 点\n线段落在它上方 → 交点在 −1 左侧、计入穿越",
            ha="left", va="bottom", fontsize=10.5, color=fs.INK, zorder=9,
            linespacing=1.6,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.8))

    handles = [plt.Line2D([], [], color=c, lw=2.4, label=lb) for lb, _, c, _ in TRACKS]
    leg = ax.legend(handles=handles, loc="lower right", fontsize=10.5, frameon=True,
                    facecolor="white", edgecolor=fs.GRID, framealpha=1.0,
                    borderpad=0.55, labelspacing=0.45, handlelength=1.9)
    leg.set_zorder(10)

    ax.set_xlim(K_INF, K_SUP)
    ax.set_ylim(0.02, 1400.0)
    ax.set_yticks([0.1, 1.0, 10.0, 100.0, 1000.0])
    ax.set_yticklabels(["0.1", "1", "10", "100", "1000"])
    ax.minorticks_off()
    ax.tick_params(labelbottom=False)      # 横轴与下面板共用，刻度只画一份
    ax.set_ylabel("交点距原点的距离  |x|")
    ax.set_title("(a) 三个交点随 K 线性缩放（双对数图上是斜率 1 的直线）",
                 fontsize=13, pad=8)
    ax.grid(True, which="major", color=fs.GRID, lw=0.6, alpha=0.9)
    ax.spines[["top", "right"]].set_visible(False)

    # ---------- (b) 落在 −1 左侧的交点数 ----------
    edges = [b[0] for b in BANDS] + [K_SUP]
    vals = [b[4] for b in BANDS]
    ax2.step(edges, vals + [vals[-1]], where="post", color=fs.INK, lw=2.2, zorder=5)
    for lo, hi, _, tag, n in BANDS:
        col = GREEN if tag == "稳定" else fs.PHA
        ax2.plot([np.sqrt(lo * hi)], [n], "o", ms=7, color=col, zorder=6)
        ax2.text(np.sqrt(lo * hi), n + 0.34, f"{n} 个 → {tag}", ha="center",
                 va="bottom", fontsize=11, color=col, zorder=8,
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.4))
    ax2.set_ylim(-0.35, 4.15)
    ax2.set_yticks([0, 1, 2, 3])
    ax2.set_ylabel("−1 左侧\n交点数", fontsize=11.5, linespacing=1.4)
    ax2.set_title("(b) 数穿越：奇数个 → Z ≠ 0 不稳定，偶数个 → Z = 0 稳定",
                  fontsize=13, pad=8)
    ax2.grid(True, which="major", axis="y", color=fs.GRID, lw=0.6, alpha=0.9)
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.set_xticks([0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 25.0, 100.0])
    ax2.set_xticklabels(["0.2", "0.5", "1", "2", "5", "10", "25", "100"])
    ax2.set_xlabel("开环增益 K")

    fig.suptitle("例5.30（习题5-31）交点随 K 线性缩放 → 条件稳定的两个窗口",
                 fontsize=14, y=0.968)
    fig.text(0.5, 0.036, "闭环稳定：0 < K < 0.5 或 1 < K < 25（K = 0.5、1、25 处临界稳定）",
             ha="center", va="bottom", fontsize=11.5, color=fs.INK)
    fs.save(fig, "自控-频域-例530-K范围.png")


if __name__ == "__main__":
    verify()
    main()
