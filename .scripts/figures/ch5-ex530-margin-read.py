# figure: 自控-频域-例530-读裕度.png
"""例5.30（习题5-31 燕山大学2018）第(1)问：由奈氏图直接读 γ 与 h。

K = 5 时曲线与单位圆交于 (-0.8, -0.6)（0.8²+0.6² = 1），与负实轴交于
-10、-5、-0.2（曲线由 _ex530_curve.py 的示意曲线给出）：
  * gamma = arctan(0.6/0.8) = 36.87°   —— 交点与 -180° 方向的圆心角
  * h     = 1/0.2 = 5（约 14 dB）      —— 只有 -0.2 这个交点在 -1 右侧
其余两个交点在 -1 左侧（增益下限那一侧），取它们会把 h 算成 0.2 < 1 而误判。

图内文字**不要**把中文与 $…$ 混在一串（mathtext 接管整串会让汉字掉字形），
一律用「纯文本 + Unicode 数学」；mathtext 也不认 \\lvert，且 `\\mathrm j` 的
空格写法在 3.11 上报 ParseFatalException，要写 \\mathrm{j}。

Build: ..\\build.ps1 -File .\\ch5-ex530-margin-read.py
"""
from __future__ import annotations

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch
from matplotlib.path import Path

import figures_style as fs
import _ex530_curve as ec

UNIT_HIT = ec.UNIT_POINT                  # (-0.8, -0.6)
W_CROSS = ec.CROSSINGS[2]                 # -0.2
H_RATIO = 1.0 / abs(W_CROSS)              # 5
GAMMA = np.degrees(np.arctan2(-UNIT_HIT[1], -UNIT_HIT[0]))


def verify() -> None:
    assert abs(UNIT_HIT[0] ** 2 + UNIT_HIT[1] ** 2 - 1.0) < 1e-12     # 恰在单位圆上
    assert abs(GAMMA - 36.8698976) < 1e-6, GAMMA
    assert abs(H_RATIO - 5.0) < 1e-12, H_RATIO
    assert abs(20 * np.log10(H_RATIO) - 13.9794) < 1e-3
    ec.check()
    print(f"verified: gamma={GAMMA:.2f}° |G|=1 @(-0.8,-0.6) | "
          f"h=1/0.2={H_RATIO:.1f} ({20 * np.log10(H_RATIO):.2f} dB)")


def path_arrow(ax, x, y, lo, hi, color=fs.MAG, ms=16):
    """沿曲线上 [lo, hi] 一段画方向箭头（ω 增大方向）。"""
    sel = (x >= lo) & (x <= hi)
    verts = np.column_stack((x[sel], y[sel]))
    ax.add_patch(FancyArrowPatch(path=Path(verts), arrowstyle="-|>",
                                 mutation_scale=ms, color=color, lw=1.8,
                                 zorder=5))


def draw():
    fs.use_style()
    fig, ax = plt.subplots(figsize=(7.0, 6.8))
    fig.suptitle("例5.30（习题5-31）奈氏图上直接读 γ 与 h", fontsize=14, y=0.98)
    ax.set_title("K = 5：负实轴交点 −10、−5、−0.2；单位圆交点 (−0.8, −0.6)",
                 fontsize=13, pad=10)
    ax.set_xlim(-1.45, 1.05)
    ax.set_ylim(-1.45, 1.05)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color=fs.SUB, lw=0.85, zorder=1)
    ax.axvline(0, color=fs.SUB, lw=0.85, zorder=1)
    ax.grid(True, color=fs.GRID, lw=0.55, alpha=0.6)
    ax.set_xlabel(r"$\mathrm{Re}\,G(\mathrm{j}\omega)$")
    ax.set_ylabel(r"$\mathrm{Im}\,G(\mathrm{j}\omega)$")
    ax.spines[["top", "right"]].set_visible(False)

    # 单位圆（标注挪到右上角：曲线的弧斜穿第一象限，贴弧放必被压）
    th = np.linspace(0.0, 2.0 * np.pi, 721)
    ax.plot(np.cos(th), np.sin(th), color=fs.SUB, lw=1.0, ls=(0, (5, 4)), zorder=2)
    ax.text(1.02, 0.95, "单位圆  |G| = 1", color=fs.SUB, fontsize=11,
            ha="right", va="center", zorder=8)

    # 曲线（示意，K = 5）
    x, y = ec.curve()
    ax.plot(x, y, color=fs.MAG, lw=2.3, zorder=4)
    path_arrow(ax, x, y, -1.30, -1.12)

    # 临界点
    ax.plot([-1.0], [0.0], marker="*", ms=16, color=fs.PHA, zorder=9)
    ax.annotate("临界点 (−1, j0)", (-1.0, 0.0), xytext=(-9, 14),
                textcoords="offset points", ha="right", fontsize=11,
                color=fs.PHA, bbox=dict(facecolor="white", edgecolor="none", pad=1.5),
                zorder=10)

    # γ：单位圆上从 (−1, j0) 到 (−0.8, −0.6) 的圆心角
    ax.plot([0.0, UNIT_HIT[0]], [0.0, UNIT_HIT[1]], color=fs.SUB, lw=0.9,
            ls=(0, (4, 3)), zorder=3)
    ax.add_patch(Arc((0.0, 0.0), 2.0, 2.0, theta1=180.0, theta2=180.0 + GAMMA,
                     color=fs.PHA, lw=3.2, zorder=6))
    mid = np.radians(180.0 + 0.5 * GAMMA)
    # 半径 1.27（原 1.22）：让白框整体退到圆弧外侧，别让虚线圆擦过框角
    ax.text(1.27 * np.cos(mid), 1.27 * np.sin(mid), f"γ = {GAMMA:.2f}°",
            color=fs.PHA, fontsize=12, ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5), zorder=10)
    ax.plot([UNIT_HIT[0]], [UNIT_HIT[1]], "o", ms=6, color=fs.PHA, zorder=8)
    # 下移到 −1.03：白框顶边让开单位圆下半弧（圆在 y=−0.93 处已到 x=−0.37）
    ax.annotate("(−0.8, −0.6) 恰在单位圆上\n（0.8² + 0.6² = 1）", UNIT_HIT,
                xytext=(-1.42, -1.03), textcoords="data", ha="left", va="center",
                fontsize=11, color=fs.INK,
                bbox=dict(facecolor="white", edgecolor="none", pad=2.0), zorder=10,
                arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8,
                                shrinkA=4.0, shrinkB=3.0))

    # h：负实轴上的尺寸线（只有 −0.2 这个交点在 −1 右侧）
    ax.plot([0.0, W_CROSS], [0.0, 0.0], color=fs.PHA, lw=3.4, zorder=7,
            solid_capstyle="butt")
    ax.plot([W_CROSS, -1.0], [0.0, 0.0], color=fs.PHA, lw=1.6, ls=(0, (4, 3)), zorder=7)
    ax.plot([W_CROSS, W_CROSS], [-0.06, 0.06], color=fs.PHA, lw=1.4, zorder=7)
    # 抬到 y=0.30 并拆两行：曲线在原点左侧有个小钩（最高到 y≈0.11），原位置被白框盖住；
    # 拆行后框宽 0.6 < 0.66，右端才收在 y 轴竖线（x=0）左边、左端让开单位圆上弧
    ax.annotate(f"h = 1/0.2 = {H_RATIO:.0f}\n（约 {20 * np.log10(H_RATIO):.0f} dB）",
                (-0.60, 0.0), xytext=(-0.66, 0.30), textcoords="data",
                ha="left", va="center", fontsize=11, color=fs.PHA, linespacing=1.5,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5), zorder=10,
                arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8,
                                shrinkA=2.0, shrinkB=2.0))
    # 拆两行、落在单位圆**内侧**（|G|<1 那片空区）：单行太长会捅出右侧坐标轴、且斜穿圆弧
    ax.annotate("交点 −0.2\n（唯一在 −1 右侧）",
                (W_CROSS, 0.0), xytext=(0.04, -0.19), textcoords="data",
                ha="left", va="center", fontsize=11, color=fs.INK,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5), zorder=10,
                arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8,
                                shrinkA=2.0, shrinkB=3.0))
    ax.annotate("曲线向左还有交点 −5、−10\n（已越过 −1，取它们 h 会算成 0.2）",
                (-1.40, -0.62), xytext=(-1.42, -1.32), textcoords="data",
                ha="left", va="center", fontsize=11, color=fs.SUB,
                bbox=dict(facecolor="white", edgecolor="none", pad=2.0), zorder=10,
                arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8,
                                shrinkA=4.0, shrinkB=4.0))

    fig.text(0.5, 0.052,
             "γ 由曲线与单位圆的交点读出；h 由曲线与负实轴的交点读出（距离的倒数）。",
             ha="center", va="bottom", fontsize=10, color=fs.SUB)
    fig.text(0.5, 0.018,
             "按题目 K = 5 的图形示意重绘：三个交点与单位圆交点按题目给定。",
             ha="center", va="bottom", fontsize=10, color=fs.SUB)
    fig.tight_layout(rect=(0.005, 0.085, 0.995, 0.945))
    fs.save(fig, "自控-频域-例530-读裕度.png")


if __name__ == "__main__":
    verify()
    draw()
