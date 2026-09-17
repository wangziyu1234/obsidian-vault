# figure: 频域-反求-一阶Bode.png
# -*- coding: utf-8 -*-
"""例5.23：一阶系统 G(s)=31.6/(0.5s+1) 的伯德图（第一部分·伯德图用）。

上栏对数幅频（实线精确、虚线渐近），下栏对数相频。
A = 转折频率（相角 -45°）；B = -20dB/dec 段读数校验点；C = 截止频率（0 dB）。

构建：..\\build.ps1 -File .\\freq-inverse-bode-first-order.py
"""
import numpy as np
import control as ct
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
K = 10 ** 1.5                        # 20 lg K = 30 dB
T = 0.5                              # 转折频率 1/T = 2 rad/s
WC = 2 * 10 ** 1.5                   # 渐近法截止频率 63.2 rad/s
WB = 10.0                            # 读数校验点
sys = ct.tf([K], [T, 1])

W = np.logspace(-1.25, 2.35, 1400)
resp = ct.frequency_response(sys, W).fresp[0, 0, :]
L = 20 * np.log10(np.abs(resp))
PH = np.degrees(np.unwrap(np.angle(resp)))


def at(w):
    return complex(ct.frequency_response(sys, [w]).fresp[0, 0, 0])


fig, (ax_m, ax_p) = fs.new_bode_axes(figsize=(7.8, 5.6))

BOX = dict(facecolor="white", edgecolor="none", alpha=0.95, pad=1.2)


def mark(ax, x, y, text, dx=9, dy=9, color=fs.PHA):
    ax.plot([x], [y], "o", ms=5.5, color=color, zorder=6)
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                fontsize=13, color=color, bbox=BOX, zorder=7)


ax_m.semilogx(W, L, color=fs.MAG, lw=2.0)
ax_p.semilogx(W, PH, color=fs.PHA, lw=2.0)
wa = np.array([0.055, 2.0, 45.0])
ax_m.semilogx(wa, 30 - 20 * np.log10(np.maximum(wa, 2.0) / 2.0),
              color=fs.SUB, lw=1.3, ls=(0, (5, 3)))

for ax in (ax_m, ax_p):
    fs.tidy(ax, turn_freqs=[2.0, WC])
ax_m.axhline(0, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax_m.set_ylim(-28, 36)
ax_p.set_ylim(-104, 8)
ax_p.set_yticks([0, -45, -90])
ax_m.set_title("对数幅频特性", loc="left", fontsize=13, color=fs.SUB, family=FAM)
ax_p.set_title("对数相频特性", loc="left", fontsize=13, color=fs.SUB, family=FAM)

mark(ax_m, WB, 20 * np.log10(abs(at(WB))), "B")
mark(ax_m, WC, 20 * np.log10(abs(at(WC))), "C")
mark(ax_p, 2.0, -45.0, "A")

fig.suptitle(r"$G(s)=\frac{31.6}{0.5s+1}$", fontsize=17, y=0.975)
fig.text(0.5, 0.018,
         "A 转折频率 ω=2（相角 −45°）  ·  B 渐近线读数校验点 ω=10  ·  C 截止频率 ωc=63.2（0 dB）",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB, family=FAM)

fig.subplots_adjust(left=0.105, right=0.97, top=0.87, bottom=0.19, hspace=0.30)
fs.save(fig, "频域-反求-一阶Bode.png")
