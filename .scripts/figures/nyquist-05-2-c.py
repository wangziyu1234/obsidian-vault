# figure: 频域-奈氏-条件稳定.png
# figure: 频域-奈氏-结构不稳定.png
"""05-2-c 的两张示意图（条件稳定 / 结构不稳定）。

条件稳定：教材例5-8，$K=10$ 时曲线与负实轴有三个交点 $-2,-1.5,-0.5$，
交点横坐标随 $K$ 线性缩放，故稳定区间为 $(0,5)\\cup(20/3,20)$。
教材原图为示意，这里用一条通过三个交点的平滑曲线示意形状，
标注只标"落在 $-1$ 左侧才算穿越"，不冒充教材真实曲线。

结构不稳定：$G(s)H(s)=K/[s^2(Ts+1)]$，$\nu=2$ 使低频相角起步 $-180°$，
相频始终在 $-180°\\sim-270°$，曲线从第三象限冲向无穷远，$(-1,j0)$ 被围住，
增益无法挽救（画正频率支示意）。
"""
from __future__ import annotations

import os
from pathlib import Path

import control as ct
import numpy as np

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
    x = np.linspace(-3.0, 0.6, 800)
    y = 0.9 * np.sin(np.pi * (x - x[0]) / 1.2) * np.exp(0.55 * (x + 1.25))
    ax.plot(x, y, color=fs.MAG, lw=2.3, zorder=4)

    ax.axvline(-1, color=fs.SUB, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.annotate(r"$-1$", (-1, 1.45), color=fs.SUB, fontsize=11, ha="center",
                bbox=BOX, zorder=8)
    for i, xc in enumerate(crossings):
        colour = fs.PHA if xc < -1 else fs.INK
        ax.plot(xc, 0, "o", ms=6, color=colour, zorder=7)
        ax.annotate(rf"$\omega_{i + 1}$: {xc:g}", (xc, 0),
                    xytext=(0, 22 if i % 2 == 0 else -30),
                    textcoords="offset points", fontsize=10, color=colour,
                    ha="center", bbox=BOX, zorder=8)
    ax.plot(-1, 0, marker="x", color=fs.INK, ms=10, mew=1.8, zorder=9)
    ax.annotate(r"$(-1,\,j0)$", (-1, 0), xytext=(-4, -40),
                textcoords="offset points", fontsize=10, color=fs.INK,
                ha="center", bbox=BOX, zorder=9)
    ax.text(0.03, 0.06, r"$\mathrm{只有落在}-1\ \mathrm{左侧的交点才计入穿越; }$"
                        "\n"
                        r"$\mathrm{交点横坐标随}K\ \mathrm{线性缩放}$",
            transform=ax.transAxes, fontsize=10, color=fs.SUB, bbox=BOX,
            va="bottom", zorder=9)
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
    ax.annotate(r"$(-1,\,j0)$", (-1, 0), xytext=(-2, 20),
                textcoords="offset points", fontsize=10, color=fs.INK,
                ha="center", bbox=BOX, zorder=9)
    ax.annotate(r"$\omega\to0^+$" "\n" r"$\to\infty\angle-180^\circ$",
                (z.real[0], z.imag[0]), xytext=(-52, -6),
                textcoords="offset points", fontsize=10, color=fs.MAG,
                bbox=BOX, zorder=9)
    ax.annotate(r"$\omega\to\infty:\ 0\angle-270^\circ$", (0, 0),
                xytext=(8, -30), textcoords="offset points", fontsize=10,
                color=fs.PHA, bbox=BOX, zorder=9)
    ax.text(0.03, 0.05,
            r"$\mathrm{正频率支整条在第二象限 (相角}-180^\circ\sim-270^\circ\mathrm{)}$"
            "\n"
            r"$\mathrm{原点二重极点补}\ 180^\circ\ \mathrm{弧后闭合成环, 环必含}"
            r"(-1,j0)$" "\n"
            r"$\mathrm{调}K\ \mathrm{只改变环的大小, 包围关系不变}$"
            "\n"
            r"$\mathrm{(补弧半径}\infty\mathrm{, 此处不画; 规则见上表)}$",
            transform=ax.transAxes, fontsize=10, color=fs.SUB, bbox=BOX,
            va="bottom", zorder=9)
    finish(fig, OUT / "频域-奈氏-结构不稳定.png",
           "仅正频率支；低频端沿 -180° 方向伸向无穷远，"
           "与 180° 补弧闭合成环后必含 (-1, j0)。")


if __name__ == "__main__":
    fig_conditionally_stable()
    fig_structurally_unstable()
