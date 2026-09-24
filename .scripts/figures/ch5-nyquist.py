# -*- coding: utf-8 -*-
"""第5章例题补图（一）：奈氏图 4 张。

  * 频域-奈氏-开环不稳定.png   —— 05-2-c 自编例一：K/[(s-1)(s+2)(s+3)]，K=8
  * 频域-奈氏-二型补弧.png     —— 05-2-c 自编例二：K/[s^2(s+1)]，K=1
  * 频域-奈氏-虚轴极点.png     —— 05-2-c 自编例三：(s+1)/(s^2+1)
  * 频域-奈氏-条件稳定.png     —— 已迁到 nyquist-05-2-c.py（同名的示意图由该脚本生成，
                                本脚本不再输出，避免两张脚本互相覆盖同一文件）

图内文字**不混用中文与 `$…$`**（mathtext 接管整串会让中文掉字形），
统一用「中文 + 纯文本数学」（ω、ν、∠、⁻ 等 Unicode 符号）。
补弧的真实半径是无穷大，图中按可视范围画成示意弧并在题注里说明。

构建：..\\build.ps1 -File .\\ch5-nyquist.py
"""
import os

import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()
OUT = os.path.join(fs.REPO_ROOT, "附件")


def axes(ax, lim, title, aspect=True, neg1_off=(7, 9)):
    if aspect:
        ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(*lim[0])
    ax.set_ylim(*lim[1])
    ax.axhline(0, color=fs.SUB, linewidth=0.8, zorder=1)
    ax.axvline(0, color=fs.SUB, linewidth=0.8, zorder=1)
    ax.grid(True, color=fs.GRID, linewidth=0.6, alpha=0.85)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel("实部")
    ax.set_ylabel("虚部")
    ax.set_title(title, pad=8)
    ax.plot([-1], [0], marker="*", color=fs.PHA, markersize=13, zorder=6)
    ax.annotate("(-1, j0)", xy=(-1, 0), xytext=neg1_off,
                textcoords="offset points", color=fs.PHA, fontsize=11)


def arrow(ax, x, y, dx, dy, color=fs.MAG):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6,
                                mutation_scale=14), zorder=5)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=fs.DPI)
    plt.close(fig)
    print("saved", path)


# ---------------------------------------------------------------- 例一
K = 8.0
w = np.logspace(-2, 2.2, 4000)
G = K / ((1j * w - 1) * (1j * w + 2) * (1j * w + 3))
fig, ax = plt.subplots(figsize=(6.8, 6.0))
axes(ax, ((-1.75, 0.35), (-0.55, 0.75)),
      "自编例一   G = K/[(s−1)(s+2)(s+3)]，K = 8")
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.0, label="正频率支", zorder=4)
ax.plot(G.real, -G.imag, color=fs.MAG, linewidth=1.2, linestyle=(0, (5, 3)),
        label="负频率支（共轭）", zorder=3)
ax.plot([-K / 6], [0], marker="o", color=fs.PHA, markersize=7, zorder=6)
ax.annotate("起点 G(0) = −K/6 = −1.33\n（向下离开实轴 → 正半次穿越）",
            xy=(-K / 6, 0), xytext=(-1.72, 0.30), color=fs.PHA, fontsize=11.5)
ax.plot([-K / 10], [0], marker="o", color=fs.PHA, markersize=7, zorder=6)
ax.annotate("ω = 1 处：−K/10 = −0.8\n（落在 −1 右侧，不计）",
            xy=(-K / 10, 0), xytext=(-0.55, -0.48), color=fs.PHA, fontsize=11.5)
arrow(ax, G[600].real, G[600].imag, 0.06, -0.09)
arrow(ax, G[2500].real, G[2500].imag, -0.05, 0.08)
ax.legend(loc="upper right", fontsize=11)
save(fig, "频域-奈氏-开环不稳定.png")

# ---------------------------------------------------------------- 例二
K = 1.0
R = 4.6                                   # 示意弧的终止半径（真实半径 ∞）
w = np.logspace(-0.75, 1.8, 2000)
G = K / ((1j * w) ** 2 * (1j * w + 1))
keep = np.abs(G) <= R                      # 只画落在示意弧以内的部分
fig, ax = plt.subplots(figsize=(6.8, 5.8))
axes(ax, ((-R - 0.6, R - 1.2), (-R + 1.8, R - 2.0)),
      "自编例二   G = K/[s²(s+1)]，K = 1（Ⅱ 型）", neg1_off=(7, -20))
ax.plot(G.real[keep], G.imag[keep], color=fs.MAG, linewidth=2.2,
        label="正频率支", zorder=4)
# 原点补弧：半径随角度增大，示意「趋向无穷远」
th = np.linspace(0, -np.pi, 400)
rr = 3.0 + (R - 3.0) * np.abs(th) / np.pi
ax.plot(rr * np.cos(th), rr * np.sin(th), color=fs.PHA, linewidth=1.8,
        linestyle=(0, (6, 4)), label="原点补弧（ν×90° = 180°，顺时针）", zorder=5)
arrow(ax, rr[150] * np.cos(th[150]), rr[150] * np.sin(th[150]),
      0.5 * np.cos(th[150] - 1.2), 0.5 * np.sin(th[150] - 1.2), color=fs.PHA)
# 正常支恒在第二象限、补弧恒在下半平面且下探到 y≈−3.8（被裁），
# 所以「上半部左右两侧」是两张标签的空区，补弧终点标签也抬到左上再用引线连回
ax.annotate("补弧终点", xy=(-R + 0.4, -0.2),
            xytext=(-R - 0.45, 2.25), color=fs.PHA, fontsize=11.5,
            arrowprops=dict(arrowstyle="-", linewidth=0.8, color=fs.SUB))
ax.annotate("正常支（恒在上半平面）", xy=(-2.6, 1.4), xytext=(0.30, 2.25),
            color=fs.MAG, fontsize=11.5,
            arrowprops=dict(arrowstyle="-", linewidth=0.8, color=fs.SUB))
arrow(ax, G[700].real, G[700].imag, 0.10, 0.16)
# 图例省去：线型含义写在笔记题注里
save(fig, "频域-奈氏-二型补弧.png")

# ---------------------------------------------------------------- 例三
R = 3.1                                   # 补弧半径；两条正常支都截到同一半径上，正好接弧
w1 = np.logspace(-1.2, -0.004, 3000)      # 0 < ω < 1
w2 = np.logspace(0.004, 1.2, 3000)        # ω > 1
G1 = (1j * w1 + 1) / (1 - w1 ** 2)
G2 = (1j * w2 + 1) / (1 - w2 ** 2)
k1 = np.abs(G1) <= R
k2 = np.abs(G2) <= R
fig, ax = plt.subplots(figsize=(6.8, 6.2))
axes(ax, ((-R - 0.5, R + 0.5), (-R - 0.5, R + 0.5)),
      "自编例三   G = (s+1)/(s²+1)（开环极点在 ±j）")
ax.plot(G1.real[k1], G1.imag[k1], color=fs.MAG, linewidth=2.2,
        label="正频率支（ω < 1）", zorder=4)
ax.plot(G2.real[k2], G2.imag[k2], color=fs.MAG, linewidth=2.2,
        label="正频率支（ω > 1）", zorder=4)
ax.plot([1], [0], marker="o", color=fs.MAG, markersize=6, zorder=6)
ax.annotate("ω = 0", xy=(1, 0), xytext=(1.15, -0.35),
            color=fs.MAG, fontsize=11.5)
ax.annotate("ω → 1⁻", xy=(2.3, 2.3), xytext=(2.45, 2.1),
            color=fs.MAG, fontsize=11.5)
ax.annotate("ω → 1⁺", xy=(-2.3, -2.3), xytext=(-3.35, -2.05),
            color=fs.MAG, fontsize=11.5)
th = np.linspace(np.deg2rad(45), np.deg2rad(-135), 400)
ax.plot(R * np.cos(th), R * np.sin(th), color=fs.PHA, linewidth=1.8,
        linestyle=(0, (6, 4)), label="绕 j 的补弧（顺时针 180°）", zorder=5)
arrow(ax, R * np.cos(0.1), R * np.sin(0.1), 0.45 * np.cos(-1.0), 0.45 * np.sin(-1.0),
      color=fs.PHA)
arrow(ax, G1[k1][-40].real, G1[k1][-40].imag, 0.10, 0.22)
arrow(ax, G2[k2][40].real, G2[k2][40].imag, 0.04, -0.07)
# 图例省去：线型含义写在笔记题注里
save(fig, "频域-奈氏-虚轴极点.png")
