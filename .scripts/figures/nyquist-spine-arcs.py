# figure: 频域-奈氏-虚轴奇点补弧.png
"""虚轴奇点的围线绕法：三种情形在 s 平面上的小半圆（示意）。

三格对照（横轴 Re s，纵轴 Im s）：
  (a) 原点 ν 重极点：只需绕 1/4 圈的小右半圆，θ:0→90°；
  (b) 非零 jω₀ 处 q 重极点：绕完整小右半圆，θ:-90°→90°；
  (c) jω₀ 处零点：G 在该点解析，不必绕，围线直接穿过。

映射到 G 平面后分别是 ν×90° 逆时针、q×180° 顺时针的无穷大弧，以及"收于原点、
图像连续"——这三条写在正文表里，本图只交代 s 平面那一半。
图内中文一律写进 $\\mathrm{…}$，`$…$` 段内不用全角标点。

**为什么要竖排**（2026-09-24 改）：原来 1×3 横排、整图 11.4 英寸宽，笔记里按
|520 显示时每张子图只剩 ~170px，字全糊了。改成 3×1 竖排后每张子图占满整幅宽度，
同样 |520 显示下每张约 520px，能看清绕法与箭头。
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt

import figures_style as fs
from _nyquist_style import BOX

OUT = Path(os.environ.get("FIGURE_OUT", fs.ATTACH_DIR / "unused.png")).parent


def setup(ax):
    ax.set_xlim(-1.25, 1.55)
    ax.set_ylim(-1.15, 1.15)
    ax.axhline(0, color=fs.SUB, lw=0.9, zorder=1)
    ax.axvline(0, color=fs.SUB, lw=0.9, zorder=1)
    ax.grid(True, color=fs.GRID, lw=0.5, alpha=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=9)
    ax.set_xlabel(r"$Re\,s$", fontsize=10.5)
    ax.set_ylabel(r"$Im\,s$", fontsize=10.5)
    ax.set_aspect("equal", adjustable="box")


def arrow_arc(ax, r, a0, a1, colour, lw=2.2):
    t = np.linspace(np.deg2rad(a0), np.deg2rad(a1), 200)
    ax.plot(r * np.cos(t), r * np.sin(t), color=colour, lw=lw, zorder=4)
    k = -6 if a1 > a0 else 6
    ax.annotate("", xy=(r * np.cos(t[k]), r * np.sin(t[k])),
                xytext=(r * np.cos(t[k - 1]), r * np.sin(t[k - 1])),
                arrowprops=dict(arrowstyle="-|>", color=colour, lw=lw), zorder=6)


def fig_spine_arcs():
    fs.use_style()
    # 3×1 竖排：横排时每张子图在笔记里只有 ~170px 宽，字全糊了
    fig, axes = plt.subplots(3, 1, figsize=(5.4, 11.6))

    # (a) 原点 ν 重极点：只绕 1/4 圈
    ax = axes[0]
    setup(ax)
    ax.plot([0, 0], [-1.05, 1.05], color=fs.INK, lw=1.8, zorder=3)
    arrow_arc(ax, 0.45, 0, 90, fs.PHA)
    # 标签摆虚轴**左侧**（ha="right"）：原来从 x=-0.06 往右写，正好骑在虚轴上
    ax.text(-0.06, 1.06, r"$\mathrm{虚轴: }\sigma=0,\ \omega\in\mathbb{R}$",
            fontsize=10, color=fs.INK, bbox=BOX, ha="right", zorder=8)
    ax.text(0.52, 0.60,
            r"$\mathrm{小右半圆: }\theta:0\to90^\circ$" "\n"
            r"$\mathrm{(只需绕到正虚轴)}$" "\n"
            r"$\mathrm{映射: 逆时针}\ \nu\times90^\circ$",
            fontsize=10, color=fs.PHA, bbox=BOX, ha="left", zorder=8)
    ax.set_title(r"$\mathrm{(a) 原点}\ \nu\ \mathrm{重极点}$", fontsize=11.5)

    # (b) 非零 jω₀ 处 q 重极点：绕完整小右半圆
    ax = axes[1]
    setup(ax)
    ax.plot([-1.05, 1.05], [0, 0], color=fs.INK, lw=1.8, zorder=3)
    ax.plot([-1.05, 1.05], [0, 0], color=fs.INK, lw=0)
    ax.plot([-1.05, 1.05], [0.55, 0.55], color=fs.INK, lw=1.8, zorder=3)
    ax.plot(0, 0.55, "x", color=fs.PHA, ms=10, mew=2.2, zorder=5)
    arrow_arc(ax, 0.45, 90, -90, fs.PHA)
    ax.shift = 0.55
    ax.text(-1.08, 0.62, r"$s=j\omega_0$", fontsize=10, color=fs.PHA,
            bbox=BOX, ha="left", zorder=8)
    ax.text(0.52, 0.10,
            r"$\mathrm{完整小右半圆: }\theta:-90^\circ\to90^\circ$" "\n"
            r"$\mathrm{(完整半圈, 不是}\ 1/4\ \mathrm{圈)}$" "\n"
            r"$\mathrm{映射: 顺时针}\ q\times180^\circ$",
            fontsize=10, color=fs.PHA, bbox=BOX, ha="left", zorder=8)
    ax.set_title(r"$\mathrm{(b)}\ j\omega_0\ \mathrm{处}\ q\ \mathrm{重极点}$",
                 fontsize=11.5)

    # (c) jω₀ 处零点：不必绕
    ax = axes[2]
    setup(ax)
    ax.plot([-1.05, 1.05], [0, 0], color=fs.INK, lw=1.8, zorder=3)
    ax.plot([-1.05, 1.05], [0.55, 0.55], color=fs.INK, lw=1.8, zorder=3)
    ax.plot(0, 0.55, "o", color=fs.PHA, ms=10, mfc="white", mew=2.2, zorder=5)
    ax.text(-1.08, 0.62, r"$s=j\omega_0$", fontsize=10, color=fs.PHA,
            bbox=BOX, ha="left", zorder=8)
    ax.text(0.10, 0.10,
            r"$\mathrm{零点: }G\ \mathrm{在此解析}$" "\n"
            r"$\mathrm{围线直接穿过, 不绕}$" "\n"
            r"$\mathrm{映射: 两端收于原点, 连续}$",
            fontsize=10, color=fs.MAG, bbox=BOX, ha="left", zorder=8)
    ax.set_title(r"$\mathrm{(c)}\ j\omega_0\ \mathrm{处零点}$", fontsize=11.5)

    # (b)(c) 的围线画在 Im s = 0.55，标注一下
    for ax in axes[1:]:
        ax.annotate("", xy=(1.02, 0.55), xytext=(0.62, 0.55),
                    arrowprops=dict(arrowstyle="-|>", color=fs.MAG, lw=1.6),
                    zorder=6)

    fig.tight_layout(rect=(0.005, 0.02, 0.995, 0.99))
    out = OUT / "频域-奈氏-虚轴奇点补弧.png"
    fig.savefig(str(out), dpi=fs.DPI)
    plt.close(fig)
    print("saved", out)


if __name__ == "__main__":
    fig_spine_arcs()
