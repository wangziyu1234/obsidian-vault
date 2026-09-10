# -*- coding: utf-8 -*-
"""05-1-2 §5.2.6 典型环节幅相（奈氏）曲线总览（教材图5-10）。

八个典型环节各一子图，标出起点、终点与关键点；箭头表示 ω 增大方向。
图内文字不混用中文与 `$…$`（mathtext 会接管整串、中文掉字形），公式一律纯文本。

构建：..\\build.ps1 -File .\\ch5-typical-links-nyquist.py
"""
import os

import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()
OUT = os.path.join(fs.REPO_ROOT, "附件")
W = np.logspace(-2, 2, 1200)


def style(ax, xlim, ylim, title):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axhline(0, color=fs.SUB, linewidth=0.7, zorder=1)
    ax.axvline(0, color=fs.SUB, linewidth=0.7, zorder=1)
    ax.grid(True, color=fs.GRID, linewidth=0.5, alpha=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=9)
    ax.set_title(title, fontsize=11.5, pad=5)


def arrow(ax, x, y, dx, dy):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=fs.MAG, lw=1.5,
                                mutation_scale=12), zorder=6)


def dot(ax, x, y, lab, off=(6, 6), color=fs.PHA):
    ax.plot([x], [y], marker="o", color=color, markersize=5.5, zorder=6)
    ax.annotate(lab, xy=(x, y), xytext=off, textcoords="offset points",
                color=color, fontsize=10)


fig, axs = plt.subplots(2, 4, figsize=(13.6, 6.6))

# (1) 比例 K = 2
ax = axs[0, 0]
style(ax, (-0.4, 3.0), (-1.2, 1.2), "比例  G = K（K = 2）")
dot(ax, 2, 0, "实轴上一点", off=(-10, 14))
ax.set_xlabel("实部", fontsize=10)

# (2) 积分 1/s
ax = axs[0, 1]
style(ax, (-1.2, 1.2), (-2.6, 0.6), "积分  G = 1/s")
G = 1 / (1j * W)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.0)
arrow(ax, 0, -1.6, 0, 0.35)
dot(ax, 0, 0, "ω→∞：原点", off=(8, 4))
ax.annotate("ω→0⁺：沿 −90° 到 −j∞", xy=(0, -2.5), xytext=(-1.15, -2.45),
            color=fs.INK, fontsize=10)

# (3) 微分 s
ax = axs[0, 2]
style(ax, (-1.2, 1.2), (-0.6, 2.6), "微分  G = s")
G = 1j * W
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.0)
arrow(ax, 0, 1.6, 0, 0.35)
dot(ax, 0, 0, "ω = 0：原点", off=(8, -2))
ax.annotate("ω→∞：沿 +90° 到 +j∞", xy=(0, 2.5), xytext=(-1.15, 2.2),
            color=fs.INK, fontsize=10)

# (4) 惯性 1/(Ts+1)，T = 1
ax = axs[0, 3]
style(ax, (-0.25, 1.25), (-0.75, 0.35), "惯性  G = 1/(Ts+1)（T = 1）")
G = 1 / (1 + 1j * W)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.0)
arrow(ax, 0.68, -0.36, -0.06, 0.06)
dot(ax, 1, 0, "起点 (1, j0)", off=(-14, 12))
dot(ax, 0, 0, "终点：原点 ∠−90°", off=(6, 2))
ax.annotate("第四象限半圆\n圆心 (0.5, 0)、半径 0.5", xy=(0.5, -0.5), xytext=(-0.22, -0.72),
            color=fs.SUB, fontsize=10)

# (5) 一阶微分 1+Ts，T = 1
ax = axs[1, 0]
style(ax, (-0.5, 2.4), (-0.5, 2.6), "一阶微分  G = 1+Ts（T = 1）")
G = 1 + 1j * W
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.0)
arrow(ax, 1, 1.6, 0, 0.35)
dot(ax, 1, 0, "起点 (1, j0)", off=(-16, -16))
ax.annotate("竖直射线 Re = 1\nω→∞：+j∞", xy=(1, 2.4), xytext=(-0.45, 2.15),
            color=fs.INK, fontsize=10)

# (6) 振荡环节，ζ = 0.5、ωn = 1
ax = axs[1, 1]
style(ax, (-0.6, 1.25), (-1.35, 0.4), "振荡  1/(s²+2ζs+1)，ζ = 0.5")
G = 1 / (1 - W ** 2 + 2j * 0.5 * W)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.0)
arrow(ax, -0.1, -0.9, 0.1, 0.12)
dot(ax, 1, 0, "起点 (1, j0)", off=(-16, 10))
dot(ax, 0, -1, "ωn 处 (0, −j/(2ζ))", off=(14, -16))
ax.annotate("ω→∞：原点 ∠−180°", xy=(0, 0), xytext=(6, 6), color=fs.INK, fontsize=10)

# (7) 二阶微分，ζ = 0.5、ωn = 1
ax = axs[1, 2]
style(ax, (-2.6, 1.25), (-0.4, 2.4), "二阶微分  s²+2ζs+1，ζ = 0.5")
G = 1 - W ** 2 + 2j * 0.5 * W
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.0)
arrow(ax, -1.6, 1.9, -0.35, 0.12)
dot(ax, 1, 0, "起点 (1, j0)", off=(4, -14))
dot(ax, 0, 1, "ωn 处 (0, j2ζ)", off=(6, 4))
ax.annotate("ω→∞：沿 180° 到 ∞", xy=(-2.5, 2.2), xytext=(-2.55, -0.35),
            color=fs.INK, fontsize=10)

# (8) 延迟 e^{-τs}，τ = 1
ax = axs[1, 3]
style(ax, (-1.35, 1.35), (-1.35, 1.35), "延迟  G = e^(−τs)（τ = 1）")
th = np.linspace(0, -2.2 * np.pi, 800)
ax.plot(np.cos(th), np.sin(th), color=fs.MAG, linewidth=2.0)
arrow(ax, np.cos(-1.4), np.sin(-1.4), 0.16 * np.cos(-1.4 - 1.57),
      0.16 * np.sin(-1.4 - 1.57))
ax.annotate("单位圆：|G| ≡ 1，相位 −ωτ\n顺时针无限绕转", xy=(0, 0),
            xytext=(-1.3, 0.95), color=fs.INK, fontsize=10)

fig.suptitle("典型环节幅相曲线（奈氏图）总览：起点、终点与形状", fontsize=13.5, y=0.99)
fig.tight_layout(rect=(0, 0, 1, 0.96))
out = os.path.join(OUT, "频域-典型环节-奈氏图总览.png")
fig.savefig(out, dpi=fs.DPI)
print("saved", out)
