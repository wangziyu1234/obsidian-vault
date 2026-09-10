# -*- coding: utf-8 -*-
"""典型环节幅相曲线：8 张单图（05-1-2 §5.2.6）。

与 `bode-typical-links.py` 的 8 张伯德图一一对应：
  频域-典型环节-比例Nyquist.png / 积分 / 微分 / 惯性 / 一阶微分 / 振荡 / 二阶微分 / 延迟

图内文字不混用中文与 `$…$`；公式一律纯文本。
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
    ax.axhline(0, color=fs.SUB, linewidth=0.8, zorder=1)
    ax.axvline(0, color=fs.SUB, linewidth=0.8, zorder=1)
    ax.grid(True, color=fs.GRID, linewidth=0.6, alpha=0.85)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel("实部")
    ax.set_ylabel("虚部")
    ax.set_title(title, pad=8)


def arrow(ax, x, y, dx, dy):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=fs.MAG, lw=1.7,
                                mutation_scale=14), zorder=6)


def dot(ax, x, y, lab, off=(7, 7), color=fs.PHA):
    ax.plot([x], [y], marker="o", color=color, markersize=6, zorder=6)
    ax.annotate(lab, xy=(x, y), xytext=off, textcoords="offset points",
                color=color, fontsize=11)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=fs.DPI)
    plt.close(fig)
    print("saved", path)


def newfig():
    return plt.subplots(figsize=(5.6, 4.6))


# 1 比例
fig, ax = newfig()
style(ax, (-0.4, 3.0), (-1.0, 1.0), "比例环节  G = K（K = 2）")
dot(ax, 2, 0, "实轴上一点，不随 ω 变", off=(-150, 18))
save(fig, "频域-典型环节-比例Nyquist.png")

# 2 积分
fig, ax = newfig()
style(ax, (-1.1, 1.1), (-2.6, 0.7), "积分环节  G = 1/s")
G = 1 / (1j * W)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
arrow(ax, 0, -1.6, 0, 0.35)
dot(ax, 0, 0, "ω→∞：原点", off=(10, 6))
ax.annotate("ω→0⁺：沿 −90° 到 −j∞", xy=(0, -2.5), xytext=(-1.05, -2.45),
            color=fs.INK, fontsize=11)
save(fig, "频域-典型环节-积分Nyquist.png")

# 3 微分
fig, ax = newfig()
style(ax, (-1.1, 1.1), (-0.7, 2.6), "微分环节  G = s")
G = 1j * W
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
arrow(ax, 0, 1.6, 0, 0.35)
dot(ax, 0, 0, "ω = 0：原点", off=(10, -4))
ax.annotate("ω→∞：沿 +90° 到 +j∞", xy=(0, 2.5), xytext=(-1.05, 2.2),
            color=fs.INK, fontsize=11)
save(fig, "频域-典型环节-微分Nyquist.png")

# 4 惯性
fig, ax = newfig()
style(ax, (-0.25, 1.3), (-0.8, 0.35), "惯性环节  G = 1/(Ts+1)（T = 1）")
G = 1 / (1 + 1j * W)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
arrow(ax, 0.68, -0.37, -0.05, 0.06)
dot(ax, 1, 0, "起点 (1, j0)（ω = 0）", off=(-145, 16))
dot(ax, 0, 0, "终点：原点 ∠−90°", off=(8, 4))
ax.annotate("第四象限半圆：圆心 (0.5, 0)、半径 0.5", xy=(0.5, -0.55),
            xytext=(-0.2, -0.74), color=fs.SUB, fontsize=10.5)
save(fig, "频域-典型环节-惯性Nyquist.png")

# 5 一阶微分
fig, ax = newfig()
style(ax, (-0.5, 2.4), (-0.6, 2.6), "一阶微分环节  G = 1+Ts（T = 1）")
G = 1 + 1j * W
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
arrow(ax, 1, 1.6, 0, 0.35)
dot(ax, 1, 0, "起点 (1, j0)（ω = 0）", off=(-150, -20))
ax.annotate("竖直射线 Re = 1，ω→∞：+j∞", xy=(1, 2.45), xytext=(-0.45, 2.2),
            color=fs.INK, fontsize=11)
save(fig, "频域-典型环节-一阶微分Nyquist.png")

# 6 振荡
fig, ax = newfig()
style(ax, (-0.65, 1.3), (-1.45, 0.4), "振荡环节  1/(s²+2ζs+1)，ζ = 0.5")
G = 1 / (1 - W ** 2 + 2j * 0.5 * W)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
arrow(ax, -0.12, -0.9, 0.1, 0.12)
dot(ax, 1, 0, "起点 (1, j0)（ω = 0）", off=(-150, 12))
dot(ax, 0, -1, "ωn 处 (0, −j/(2ζ))", off=(12, -18))
ax.annotate("ω→∞：原点 ∠−180°", xy=(0, 0), xytext=(10, 10), color=fs.INK, fontsize=11)
save(fig, "频域-典型环节-振荡Nyquist.png")

# 7 二阶微分
fig, ax = newfig()
style(ax, (-2.7, 1.3), (-0.5, 2.5), "二阶微分环节  s²+2ζs+1，ζ = 0.5")
G = 1 - W ** 2 + 2j * 0.5 * W
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
arrow(ax, -1.6, 1.9, -0.35, 0.12)
dot(ax, 1, 0, "起点 (1, j0)（ω = 0）", off=(4, -20))
dot(ax, 0, 1, "ωn 处 (0, j2ζ)", off=(8, 6))
ax.annotate("恒在上半平面，ω→∞：沿 180° 到 ∞", xy=(-2.6, 2.3),
            xytext=(-2.65, -0.4), color=fs.INK, fontsize=11)
save(fig, "频域-典型环节-二阶微分Nyquist.png")

# 8 延迟
fig, ax = newfig()
style(ax, (-1.4, 1.4), (-1.4, 1.4), "延迟环节  G = e^(−τs)（τ = 1）")
th = np.linspace(0, -2.2 * np.pi, 800)
ax.plot(np.cos(th), np.sin(th), color=fs.MAG, linewidth=2.2)
arrow(ax, np.cos(-1.4), np.sin(-1.4), 0.16 * np.cos(-2.97), 0.16 * np.sin(-2.97))
ax.annotate("单位圆：|G| ≡ 1，相位 −ωτ\n顺时针无限绕转", xy=(0, 0),
            xytext=(-1.35, 1.0), color=fs.INK, fontsize=11)
save(fig, "频域-典型环节-延迟Nyquist.png")

# 9 不稳定惯性（非最小相位）：第一象限半圆（惯性半圆关于实轴的镜像）
fig, ax = newfig()
style(ax, (-0.25, 1.3), (-0.35, 0.8), "不稳定惯性环节  1/(1−Ts)（T = 1）")
G = 1 / (1 - 1j * W)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
arrow(ax, 0.68, 0.37, -0.05, -0.06)
dot(ax, 1, 0, "起点 (1, j0)（ω = 0）", off=(-150, -20))
dot(ax, 0, 0, "终点：原点 ∠+90°", off=(8, -4))
ax.annotate("第一象限半圆：圆心 (0.5, 0)、半径 0.5\n（与惯性环节关于实轴对称）",
            xy=(0.5, 0.55), xytext=(-0.2, 0.7), color=fs.SUB, fontsize=10.5)
save(fig, "频域-典型环节-不稳定惯性Nyquist.png")

# 10 不稳定振荡（非最小相位）：上半平面（振荡曲线关于实轴的镜像）
fig, ax = newfig()
style(ax, (-0.65, 1.3), (-0.4, 1.45), "不稳定振荡环节  1/(s²−2ζs+1)，ζ = 0.5")
G = 1 / (1 - W ** 2 - 2j * 0.5 * W)
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
arrow(ax, -0.12, 0.9, 0.1, -0.12)
dot(ax, 1, 0, "起点 (1, j0)（ω = 0）", off=(-150, -16))
dot(ax, 0, 1, "ωn 处 (0, j/(2ζ))", off=(10, 4))
ax.annotate("ω→∞：原点 ∠+180°", xy=(0, 0), xytext=(10, -14), color=fs.INK, fontsize=11)
save(fig, "频域-典型环节-不稳定振荡Nyquist.png")
