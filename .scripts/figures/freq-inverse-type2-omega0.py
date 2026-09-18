# figure: 频域-反求-Ⅱ型Bode.png
# -*- coding: utf-8 -*-
"""例5.26：Ⅱ 型系统由对数幅频渐近线定 K（第一部分·伯德图用）。

示意用频率：ω1 = 1、ω0 = √10、ωc = 10、ω2 = 60（只定形状，不代表具体题给数据）。
折点 ω1 处高度 H = 40lg(ω0/ω1) = 20lg(ωc/ω1) = 20 dB。
虚线 = 低频 −40 dB/dec 渐近线的延长线，与 0 dB 线交于 ω0 ⇒ K = ω0²；
实线在 −20 dB/dec 段与 0 dB 线交于 ωc ⇒ K = ω1ωc。

构建：..\\build.ps1 -File .\\freq-inverse-type2-omega0.py
"""
import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]

W1, W0, WC, W2 = 1.0, np.sqrt(10.0), 10.0, 60.0
H = 40 * np.log10(W0 / W1)                       # = 20 dB
L2 = H - 20 * np.log10(W2 / W1)                  # ω2 处高度 ≈ −15.6 dB

fig, ax = plt.subplots(figsize=(7.8, 4.9))

# 渐近线三段：−40 → −20 → −60 dB/dec
wA = np.array([0.30, W1])
wB = np.array([W1, W2])
wC = np.array([W2, 170.0])
ax.semilogx(wA, H - 40 * np.log10(wA / W1), color=fs.MAG, lw=2.0)
ax.semilogx(wB, H - 20 * np.log10(wB / W1), color=fs.MAG, lw=2.0)
ax.semilogx(wC, L2 - 60 * np.log10(wC / W2), color=fs.MAG, lw=2.0)

# 低频 −40 段的延长线（虚线）
wD = np.array([W1, 4.6])
ax.semilogx(wD, H - 40 * np.log10(wD / W1), color=fs.PHA, lw=1.5,
            ls=(0, (5, 3)))

# 0 dB 参考线、H 水平虚线、ω1 竖虚线
ax.axhline(0, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax.hlines(H, 0.30, W1, color=fs.SUB, lw=1.0, ls=(0, (4, 3)))
ax.vlines(W1, 0, H, color=fs.SUB, lw=1.0, ls=(0, (4, 3)))

# 折点与 0 dB 交点
ax.plot([W1, W2], [H, L2], "o", ms=5.5, color=fs.MAG, zorder=6)
ax.plot([W1], [H], "o", ms=5.5, color=fs.PHA, zorder=6)
ax.plot([W0, WC], [0, 0], "o", ms=5.5, color=fs.PHA, zorder=6)

# 斜率标注
ax.annotate(r"$-40$ dB/dec", (0.85, H - 40 * np.log10(0.85 / W1)),
            xytext=(-26, 14), textcoords="offset points",
            fontsize=12, color=fs.MAG)
ax.annotate(r"$-20$ dB/dec", (1.7, H - 20 * np.log10(1.7 / W1)),
            xytext=(4, 14), textcoords="offset points",
            fontsize=12, color=fs.MAG)
ax.annotate(r"$-60$ dB/dec", (72.0, L2 - 60 * np.log10(72.0 / W2)),
            xytext=(8, -4), textcoords="offset points",
            fontsize=12, color=fs.MAG)

ax.set_xlim(0.30, 220)
ax.set_ylim(-45, 50)
ax.set_ylabel(r"$L(\omega)$ / dB")
ax.set_xlabel(r"$\omega$ / (rad/s)")
ax.set_xticks([W1, W0, WC, W2])
ax.set_xticklabels([r"$\omega_1$", r"$\omega_0$", r"$\omega_c$", r"$\omega_2$"])
for lbl, c in zip(ax.get_xticklabels(), [fs.INK, fs.PHA, fs.PHA, fs.INK]):
    lbl.set_color(c)
    lbl.set_fontsize(14)
ax.set_yticks([0, H])
ax.set_yticklabels([r"$0$", r"$H$"])
ax.minorticks_off()
fs.tidy(ax)
ax.set_title(
    r"$G(s)=\frac{K\left(s/\omega_1+1\right)}{s^2\left(s^2/\omega_2^2"
    r"+2\xi s/\omega_2+1\right)}$",
    fontsize=16, color=fs.INK, pad=10)

fig.text(0.5, 0.018,
         "实线 渐近线折线（−40 → −20 → −60 dB/dec） · 虚线 低频 −40 dB/dec 段的延长线\n"
         "折点 ω1 处高 H：H = 40lg(ω0/ω1) = 20lg(ωc/ω1)，于是 K = ω0² = ω1ωc",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB,
         family=FAM, linespacing=1.6)

fig.subplots_adjust(left=0.095, right=0.975, top=0.855, bottom=0.235)
fs.save(fig, "频域-反求-Ⅱ型Bode.png")
