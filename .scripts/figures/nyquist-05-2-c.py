# figure: 频域-奈氏-条件稳定.png
# figure: 频域-奈氏-结构不稳定.png
"""05-2-c 的两张示意图（条件稳定 / 结构不稳定）。

条件稳定：教材例5-8，$K=10$ 时曲线与负实轴有三个交点 $-2,-1.5,-0.5$，
交点横坐标随 $K$ 线性缩放，故稳定区间为 $(0,5)\\cup(20/3,20)$。
教材原图为示意，这里用保形插值（PCHIP）构造一条**严格过三个交点**的曲线，
并把峰谷压在 $\\pm1.1$ 以内——目的一：曲线真的过"交点"（原来圆点画在实轴上、
曲线却在 $y\\neq0$ 处，是失真的）；目的二：上下各留出一条空白带专门放标注。

结构不稳定：$G(s)H(s)=K/[s^2(Ts+1)]$，$\\nu=2$ 使低频相角起步 $-180°$，
相频始终在 $-180°\\sim-270°$，曲线从第三象限冲向无穷远，$(-1,j0)$ 被围住，
增益无法挽救（画正频率支示意）。

**标注位置**（2026-09-24 重排）：两条硬规则——文字框不骑 $x=-1$ 竖线、不压曲线。
条件稳定图：交点文字一律下移到曲线够不到的底部空白带（$y\\approx-1.5$）再拉细引线
连回交点；$(-1,j0)$ 抬到曲线正峰之上；说明块走顶部空白带。
结构不稳定图：$(-1,j0)$ 与 $\\omega\\to\\infty$ 分居原点两侧；$\\omega\\to0^+$
改指曲线**可见左端**（原来指向画外，等于没标出来）；左下说明块每行压到 ~11 字，
否则一跨过纵轴就会压住纵轴线。
"""
from __future__ import annotations

import os
from pathlib import Path

import control as ct
import numpy as np
from scipy.interpolate import PchipInterpolator

import matplotlib.pyplot as plt

import figures_style as fs
from _nyquist_style import canvas, response, finish, BOX

OUT = Path(os.environ.get("FIGURE_OUT", fs.ATTACH_DIR / "unused.png")).parent


def fig_conditionally_stable():
    """条件稳定：三个交点随 K 线性缩放，只有 -1 左侧的才计数。"""
    crossings = np.array([-2.0, -1.5, -0.5])
    fig, ax = canvas(r"条件稳定系统 - 教材例5-8, K = 10",
                     r"$G(s)=K G_1(s)/s$" "\n"
                     r"$\mathrm{曲线与负实轴有三个交点}$",
                     (-3.4, 1.2), (-2.0, 2.0), figsize=(6.8, 5.4))
    # 保形插值：强制在 -2 / -1.5 / -0.5 处取零（真交点），峰谷控制在 ±1.1 内，
    # 于是 y>1.2 与 y<-1.1 各成一条空白带，专门用来放标注。
    knots_x = np.array([-3.25, -2.6, -2.0, -1.75, -1.5, -1.0, -0.5, 0.15, 0.65])
    knots_y = np.array([-1.05, -0.55, 0.0, 0.40, 0.0, -0.72, 0.0, 0.85, 1.10])
    x = np.linspace(knots_x[0], knots_x[-1], 900)
    ax.plot(x, PchipInterpolator(knots_x, knots_y)(x),
            color=fs.MAG, lw=2.3, zorder=4)

    ax.axvline(-1, color=fs.SUB, lw=1.1, ls=(0, (4, 3)), zorder=2)
    # 竖线标签放在线的右侧、顶部空白带里，不骑线
    ax.annotate(r"$-1$", (-1, 1.50), xytext=(8, 0),
                textcoords="offset points", color=fs.SUB, fontsize=11,
                ha="left", va="center", bbox=BOX, zorder=8)
    # 交点文字统一沉到底部空白带，再用细引线连回交点
    tag_x = (-2.90, -1.90, -0.42)
    for i, xc in enumerate(crossings):
        colour = fs.PHA if xc < -1 else fs.INK
        ax.plot(xc, 0, "o", ms=6, color=colour, zorder=7)
        ax.annotate(rf"$\omega_{i + 1}$: {xc:g}", (xc, 0),
                    xytext=(tag_x[i], -1.52), fontsize=10, color=colour,
                    ha="center", va="center", bbox=BOX, zorder=8,
                    arrowprops=dict(arrowstyle="-", lw=0.8, color=colour))
    ax.plot(-1, 0, marker="x", color=fs.INK, ms=10, mew=1.8, zorder=9)
    # (-1,j0)：抬到曲线正峰（0.40）之上，且整体留在竖线左侧
    ax.annotate(r"$(-1,\,j0)$", (-1, 0), xytext=(-60, 46),
                textcoords="offset points", fontsize=10, color=fs.INK,
                ha="right", va="bottom", bbox=BOX, zorder=9,
                arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.INK))
    ax.text(0.03, 0.94, r"$\mathrm{只有落在}-1\ \mathrm{左侧的交点}$"
                        "\n"
                        r"$\mathrm{才计入穿越}$",
            transform=ax.transAxes, fontsize=10, color=fs.SUB, bbox=BOX,
            va="top", zorder=9)
    finish(fig, OUT / "频域-奈氏-条件稳定.png",
           "形状示意（非教材真实曲线）；交点坐标随 K 线性缩放，"
           "故稳定区间为 (0,5)∪(20/3,20)。")


def fig_structurally_unstable():
    """结构不稳定的两条理由：相频永远够不到 -180° 以上，且环必然包住 (-1,j0)。"""
    s = ct.tf("s")
    system = 1 / (s * s * (s + 1))
    w = np.geomspace(6e-3, 3e1, 20000)
    z = response(system, w)
    fig, ax = canvas(r"结构不稳定系统 - 教材 §5-3 原文例子",
                     r"$G(s)H(s)=K/[s^2(Ts+1)]$",
                     (-6.5, 1.2), (-3.4, 3.4), figsize=(7.0, 5.0))
    ax.plot(z.real, z.imag, color=fs.MAG, lw=2.4, zorder=4)
    ax.plot(-1, 0, marker="x", color=fs.INK, ms=10, mew=1.8, zorder=9)
    # (-1,j0)：沉到曲线下方（此处曲线 y≈0.79），整体留在竖线左侧，
    # 并给左下说明块让出 x<-2.3 的位置（两框错开，避免 [压字]）
    ax.annotate(r"$(-1,\,j0)$", (-1, 0), xytext=(-4, -44),
                textcoords="offset points", fontsize=10, color=fs.INK,
                ha="right", va="top", bbox=BOX, zorder=9,
                arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.INK))
    # ω→0+：低频端早已跑到画外（实部 ~-2.8e4），必须指向曲线**可见左端**
    vis = int(np.argmax(z.real >= -6.5))
    ax.annotate(r"$\omega\to0^+$" "\n" r"$\to\infty\angle-180^\circ$",
                (z.real[vis], z.imag[vis]), xytext=(10, -40),
                textcoords="offset points", fontsize=10, color=fs.MAG,
                ha="left", va="top", bbox=BOX, zorder=9,
                arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.MAG))
    # ω→∞：曲线只走左半平面，原点右下整片是空的（注意别写成一行长串——
    # 上一版就是这样被顶出画布右边界，等于没标出来）
    ax.annotate(r"$\omega\to\infty$" "\n" r"$0\angle-270^\circ$", (0, 0),
                xytext=(7, -40), textcoords="offset points", fontsize=10,
                color=fs.PHA, ha="left", va="top", bbox=BOX, zorder=9,
                arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.PHA))
    # 说明块放左下（曲线只在第二象限，左下整片空着）；每行压到 11 字以内，
    # 否则框会跨过纵轴并压住纵轴线（这是上一版报 [压线] 的原因）。
    ax.text(0.03, 0.05,
            r"$\mathrm{正频率支全在第二象限}$" "\n"
            r"$(\angle-180^\circ\sim-270^\circ)$" "\n"
            r"$\mathrm{补}\ 180^\circ\mathrm{弧成环后,}$" "\n"
            r"$\mathrm{环必含}(-1,j0)$" "\n"
            r"$\mathrm{调}K\ \mathrm{只改变环的大小}$",
            transform=ax.transAxes, fontsize=9.5, color=fs.SUB, bbox=BOX,
            va="bottom", zorder=9)
    finish(fig, OUT / "频域-奈氏-结构不稳定.png",
           "仅正频率支；低频端沿 -180° 方向伸向无穷远（补弧半径 ∞，此处不画），"
           "与 180° 补弧闭合成环后必含 (-1, j0)。")


if __name__ == "__main__":
    fig_conditionally_stable()
    fig_structurally_unstable()
