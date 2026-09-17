# figure: 频域-反求-综合题Bode.png
# -*- coding: utf-8 -*-
"""补充算例（自编）：G(s)=2500/[(s^2+2.588s+25)(0.01s+1)] 的伯德图。

A = 谐振峰 ωr=4.65（46 dB）；B = ωn=5（相角 −92.9°）；D = 截止频率（0 dB）。
构建：..\\build.ps1 -File .\\freq-inverse-practice-bode.py
"""
import numpy as np
import control as ct
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
sys = ct.tf([2500.0], np.polymul([1.0, 2.588, 25.0], [0.01, 1.0]))

W = np.logspace(-1.0, 2.9, 2400)
resp = ct.frequency_response(sys, W).fresp[0, 0, :]
L = 20 * np.log10(np.abs(resp))
PH = np.degrees(np.unwrap(np.angle(resp)))


def at(w):
    return complex(ct.frequency_response(sys, [w]).fresp[0, 0, 0])


lo, hi = 20.0, 200.0
for _ in range(120):
    mid = (lo + hi) / 2
    if abs(at(mid)) > 1.0:
        lo = mid
    else:
        hi = mid
WC = (lo + hi) / 2

WA = np.array([0.1, 5.0, 100.0, 800.0])
LA = np.array([40.0, 40.0, 40 - 40 * np.log10(100 / 5), 40 - 40 * np.log10(100 / 5) - 60 * np.log10(800 / 100)])

fig, (ax_m, ax_p) = fs.new_bode_axes(figsize=(7.8, 5.6))
BOX = dict(facecolor="white", edgecolor="none", alpha=0.95, pad=1.2)


def mark(ax, x, y, text, dx=9, dy=9, color=fs.PHA):
    ax.plot([x], [y], "o", ms=5.5, color=color, zorder=6)
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                fontsize=13, color=color, bbox=BOX, zorder=7)


ax_m.semilogx(W, L, color=fs.MAG, lw=2.0)
ax_p.semilogx(W, PH, color=fs.PHA, lw=2.0)
ax_m.semilogx(WA, LA, color=fs.SUB, lw=1.4, ls=(0, (5, 3)))

for ax in (ax_m, ax_p):
    fs.tidy(ax, turn_freqs=[5.0, 100.0, WC])
ax_m.axhline(0, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax_p.axhline(-180, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax_m.set_ylim(-70, 60)
ax_p.set_ylim(-285, 20)
ax_p.set_yticks([0, -90, -180, -270])
ax_m.set_title("对数幅频特性", loc="left", fontsize=13, color=fs.SUB, family=FAM)
ax_p.set_title("对数相频特性", loc="left", fontsize=13, color=fs.SUB, family=FAM)

mark(ax_m, 4.65, 20 * np.log10(abs(at(4.65))), "A", dx=-16, dy=8)
mark(ax_m, WC, 0.0, "D", dx=8, dy=-18)
mark(ax_p, 5.0, -90.0, "B", dx=9, dy=-16)

fig.suptitle(r"$G(s)=\frac{2500}{(s^2+2.588s+25)(0.01s+1)}$", fontsize=16, y=0.975)
fig.text(0.5, 0.015,
         "A 谐振峰 ωr=4.65（46 dB） · B ωn=5（−92.9°）\n"
         "D 截止频率 ωc（精确 47.7，渐近读数 50，虚线为渐近线）",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB, family=FAM, linespacing=1.6)

fig.subplots_adjust(left=0.105, right=0.97, top=0.87, bottom=0.225, hspace=0.30)
fs.save(fig, "频域-反求-综合题Bode.png")
