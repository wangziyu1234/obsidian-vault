# figure: 频域-幅相-四种型别对照.png
# -*- coding: utf-8 -*-
"""例5.4：同一副两惯性极点、只改型别 ν 时的四条幅相曲线（0/Ⅰ/Ⅱ/Ⅲ 型）。

取 T1 = 1、T2 = 0.2、K = 1，ω 从 1e-3 扫到 1e3。
四条曲线的尺度差别来自 s^ν（|G| ~ 1/ω^ν），所以这幅图只看三件事：
**从哪个象限进来、沿什么方向进来、往哪儿收**——位置角的数值对照见正文表格。

点线 = 起点方向 ∞∠(−ν×90°)；箭头 = 频率增大的方向。

图内文字规则：含 $…$ 的字符串不混中文，中文标注一律纯文本。

构建：..\build.ps1 -File .\type-family-compare.py
"""
import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
T1, T2, K = 1.0, 0.2, 1.0
W = np.logspace(-3, 3, 4001)

COL = {0: fs.MAG, 1: "#1D9E75", 2: fs.PHA, 3: "#8A4B08"}
LBL = {0: "ν = 0（0 型）", 1: "ν = 1（Ⅰ 型）",
       2: "ν = 2（Ⅱ 型）", 3: "ν = 3（Ⅲ 型）"}
START = {1: r"$\infty\angle-90^\circ$", 2: r"$\infty\angle-180^\circ$",
         3: r"$\infty\angle-270^\circ$"}

LIM = 1.8
fig, ax = plt.subplots(figsize=(7.2, 7.0))

for nu in (0, 1, 2, 3):
    s = 1j * W
    G = K / ((s ** nu) * (1 + T1 * s) * (1 + T2 * s))
    ax.plot(G.real, G.imag, color=COL[nu], lw=2.0, label=LBL[nu])

# 起点方向（低频射线）
for nu, ang in ((1, -90.0), (2, -180.0), (3, -270.0)):
    a = np.deg2rad(ang)
    r = np.array([0.5, LIM - 0.05])
    ax.plot(r * np.cos(a), r * np.sin(a), color=COL[nu], lw=1.0, ls=(0, (2, 3)))
    tx, ty = LIM - 0.08, LIM - 0.08
    if nu == 1:
        ax.annotate(START[nu], (0.07, -(LIM - 0.72)), xytext=(0, 0),
                    textcoords="offset points", fontsize=12.5, color=COL[nu],
                    ha="left", va="center")
    elif nu == 2:
        ax.annotate(START[nu], (-(LIM - 0.02), 0.45), xytext=(0, 0),
                    textcoords="offset points", fontsize=12.5, color=COL[nu],
                    ha="left", va="top")
    else:
        ax.annotate(START[nu], (0, LIM - 0.3), xytext=(12, 6),
                    textcoords="offset points", fontsize=12.5, color=COL[nu])

# 频率增大方向的箭头
for nu, wm in ((0, 3.0), (1, 0.60), (2, 0.45), (3, 0.32)):
    s = 1j * W
    G = K / ((s ** nu) * (1 + T1 * s) * (1 + T2 * s))
    i = int(np.argmin(np.abs(W - wm)))
    j = min(i + 80, len(W) - 1)
    ax.annotate("", xy=(G.real[j], G.imag[j]), xytext=(G.real[i], G.imag[i]),
                arrowprops=dict(arrowstyle="-|>", color=COL[nu], lw=1.5,
                                shrinkA=0, shrinkB=0))

ax.plot([0], [0], "o", ms=5.5, color=fs.INK, zorder=6)
ax.axhline(0, color=fs.SUB, lw=0.8)
ax.axvline(0, color=fs.SUB, lw=0.8)

ax.set_xlim(-LIM, LIM)
ax.set_ylim(-LIM, LIM)
ax.set_aspect("equal")
ax.grid(True, color=fs.GRID, lw=0.6, alpha=0.9)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.set_xlabel(r"$\mathrm{Re}$", fontsize=14, labelpad=6)
ax.set_ylabel(r"$\mathrm{Im}$", fontsize=14, labelpad=14)
ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
ax.legend(loc="lower left", fontsize=11.5, handlelength=2.4)
ax.set_title("同一副两惯性极点、只改型别 ν 的四条幅相曲线\n"
             "T1 = 1，T2 = 0.2，K = 1；ν 越大越贴原点，只看进来的方向与收尾的象限",
             fontsize=12, color=fs.INK, pad=10, family=FAM)

fig.text(0.5, 0.012,
         "起点：0 型在实轴上 (K, 0)；Ⅰ/Ⅱ/Ⅲ 型沿 ∞∠−90°/−180°/−270° 进来（细点线即三条起动射线）\n"
         "终点连续相角 −180°/−270°/−360°/−450°：0 型沿 −Re 收、Ⅰ 型沿 +Im 收、\n"
         "Ⅱ 型沿 +Re 收、Ⅲ 型沿 −Im 收",
         ha="center", va="bottom", fontsize=10, color=fs.SUB,
         family=FAM, linespacing=1.7)

fig.subplots_adjust(left=0.115, right=0.975, top=0.90, bottom=0.225)
fs.save(fig, "频域-幅相-四种型别对照.png")
