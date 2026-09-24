# figure: 频域-奈氏-条件稳定.png
# figure: 频域-奈氏-结构不稳定.png
"""05-2-c 的两张示意图（条件稳定 / 结构不稳定）。

条件稳定：教材例5-8，$K=10$ 时曲线与负实轴有三个交点 $-2,-1.5,-0.5$，
交点横坐标随 $K$ 线性缩放，故稳定区间为 $(0,5)\\cup(20/3,20)$。
教材原图为示意。曲线用**参数样条**（x 不单调，不能插值成 y(x)）构造，沿 $\\omega$
增大方向依次经过：低频端 $(0.1,-2.3)$（画外，表现 $\\nu=1$ 时 $\\omega\\to0$ 沿 $-90^\\circ$
冲向无穷远）$\\to$ 交点 $-2$（自下而上＝负穿越）$\\to-1.5$（自上而下＝正穿越）
$\\to-0.5$（自下而上＝负穿越）$\\to$ 收于原点 $0\\angle-270^\\circ$。
（前一版峰谷封在 $\\pm1.1$ 内、两头都不出画，看着像一段小波浪而不像幅相曲线，
高频端也没回到原点——已改。）穿越方向、过零次数全部由断言把关。

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
from scipy.interpolate import CubicSpline

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
    # 参数样条（x 不单调，不能插值成 y(x)）：沿 ω 增大方向依次经过
    #   低频端 (0.10, -2.30) —— 画外，表现 ν=1 时 ω→0 沿 -90° 冲向无穷远；
    #   交点 -2（自下而上 = 负穿越）、-1.5（自上而下 = 正穿越）、-0.5（自下而上 = 负穿越）；
    #   高频端收于原点 0∠-270°（从正虚轴方向下来）。穿越方向与正文一致。
    knots_x = np.array([0.10, -1.55, -2.00, -2.50, -1.50, -1.05, -0.50, -0.10, 0.0])
    knots_y = np.array([-2.30, -1.05, 0.0, 0.72, 0.0, -0.62, 0.0, 0.38, 0.0])
    t = np.linspace(0.0, 1.0, knots_x.size)
    # 采样点要把控制点的参数值并进去，否则最近采样点可能落在陡峭处，
    # 断言会误判（如 x=-1.5 处取到 y=-1.13）
    tt = np.sort(np.concatenate([np.linspace(0.0, 1.0, 900), t]))
    cx, cy = CubicSpline(t, knots_x)(tt), CubicSpline(t, knots_y)(tt)
    # 语义自检：① 三个交点处确实 y=0；② 整条曲线只过零三次（样条不许在中间
    # 多拐出交点）；③ 穿越方向与正文一致（下→上为负、上→下为正）；
    # ④ 低频端伸到画面之下（表现 ω→0 冲向无穷远）。
    for xc in crossings:
        k = int(np.argmin(np.abs(cx - xc)))
        assert abs(cy[k]) < 0.03, (xc, cy[k])
    nz = np.where(np.abs(cy) > 0.05, np.sign(cy), 0)
    nz = nz[nz != 0]
    assert int(np.sum(nz[:-1] * nz[1:] < 0)) == 3, "过零次数应恰为 3"
    for xc, want in zip(crossings, (-1, 1, -1)):
        k = int(np.argmin(np.abs(cx - xc)))
        lo, hi = cy[k - 40], cy[k + 40]
        assert (-1 if lo < 0 < hi else 1) == want, (xc, lo, hi)
    assert cy[0] < -2.0, cy[0]
    ax.plot(cx, cy, color=fs.MAG, lw=2.3, zorder=4)

    ax.axvline(-1, color=fs.SUB, lw=1.1, ls=(0, (4, 3)), zorder=2)
    # 竖线标签放在线的右侧、顶部空白带里，不骑线
    ax.annotate(r"$-1$", (-1, 1.62), xytext=(8, 0),
                textcoords="offset points", color=fs.SUB, fontsize=11,
                ha="left", va="center", bbox=BOX, zorder=8)
    # 交点文字统一抬到曲线上方那条空带；引线取竖直方向，只在交点处与曲线相接，
    # 不会横穿曲线（曲线在每个 x 上只有一个 y）
    tag_x = (-2.95, -1.55, -0.45)
    for i, xc in enumerate(crossings):
        colour = fs.PHA if xc < -1 else fs.INK
        ax.plot(xc, 0, "o", ms=6, color=colour, zorder=7)
        ax.annotate(rf"$\omega_{i + 1}$: {xc:g}", (xc, 0),
                    xytext=(tag_x[i], 1.15), fontsize=10, color=colour,
                    ha="center", va="center", bbox=BOX, zorder=8,
                    arrowprops=dict(arrowstyle="-", lw=0.8, color=colour))
    ax.plot(-1, 0, marker="x", color=fs.INK, ms=10, mew=1.8, zorder=9)
    # (-1,j0)：曲线在这段最低到 -0.62，只能压到 -1.05 一带的下方空档；
    # 且框要整个留在竖线右侧，否则会压住 x=-1 那条竖虚线
    ax.annotate(r"$(-1,\,j0)$", (-1, 0), xytext=(-0.60, -1.05), fontsize=10,
                color=fs.INK, ha="center", va="center", bbox=BOX, zorder=9,
                arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.INK))
    ax.text(0.03, 0.95, r"$\mathrm{只有落在}-1\ \mathrm{左侧的交点}$"
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
