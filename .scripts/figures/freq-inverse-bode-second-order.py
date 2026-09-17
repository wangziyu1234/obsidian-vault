# figure: 频域-反求-二阶Bode.png
# -*- coding: utf-8 -*-
"""例5.24：二阶振荡系统 G(s)=9000/(s^2+12.18s+900) 的伯德图（第一部分·伯德图用）。

上栏对数幅频（实线精确、虚线渐近、谐振峰），下栏对数相频。
A = 谐振频率 ωr（幅频峰）；B = ωn（相角 -90°）；C = -40dB/dec 下降段；D = 截止频率（0 dB）。

构建：..\\build.ps1 -File .\\freq-inverse-bode-second-order.py
"""
import numpy as np
import control as ct
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
K, XI, WN = 10.0, 0.203, 30.0
WR = 28.77                           # 谐振频率（题给读数）
WC_ASYM = WN * np.sqrt(10)           # 渐近线读数 94.87 rad/s
sys = ct.tf([K * WN ** 2], [1.0, 2 * XI * WN, WN ** 2])

W = np.logspace(-1.2, 3.4, 2400)
resp = ct.frequency_response(sys, W).fresp[0, 0, :]
L = 20 * np.log10(np.abs(resp))
PH = np.degrees(np.unwrap(np.angle(resp)))


def at(w):
    return complex(ct.frequency_response(sys, [w]).fresp[0, 0, 0])


lo, hi = 30.0, 400.0
for _ in range(120):
    mid = (lo + hi) / 2
    if abs(at(mid)) > 1.0:
        lo = mid
    else:
        hi = mid
WC = (lo + hi) / 2

fig, (ax_m, ax_p) = fs.new_bode_axes(figsize=(7.8, 5.6))

BOX = dict(facecolor="white", edgecolor="none", alpha=0.95, pad=1.2)


def mark(ax, x, y, text, dx=9, dy=9, color=fs.PHA):
    ax.plot([x], [y], "o", ms=5.5, color=color, zorder=6)
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                fontsize=13, color=color, bbox=BOX, zorder=7)


ax_m.semilogx(W, L, color=fs.MAG, lw=2.0)
ax_p.semilogx(W, PH, color=fs.PHA, lw=2.0)
wa = np.array([0.4, WN, 260.0])
ax_m.semilogx(wa, 20 - 40 * np.log10(np.maximum(wa, WN) / WN),
              color=fs.SUB, lw=1.3, ls=(0, (5, 3)))

for ax in (ax_m, ax_p):
    fs.tidy(ax, turn_freqs=[WR, WN, WC_ASYM])
ax_m.axhline(0, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax_m.set_ylim(-40, 40)
ax_p.set_ylim(-200, 12)
ax_p.set_yticks([0, -90, -180])
ax_m.set_title("对数幅频特性", loc="left", fontsize=13, color=fs.SUB, family=FAM)
ax_p.set_title("对数相频特性", loc="left", fontsize=13, color=fs.SUB, family=FAM)

mark(ax_m, WR, 20 * np.log10(abs(at(WR))), "A", dx=-16, dy=8)
mark(ax_m, 50.0, 20 * np.log10(abs(at(50.0))), "C", dx=8, dy=-18)
mark(ax_m, WC, 0.0, "D", dx=6, dy=-20)
mark(ax_p, WN, -90.0, "B", dx=9, dy=-16)

fig.suptitle(r"$G(s)=\frac{9000}{s^2+12.18s+900}$", fontsize=17, y=0.975)
fig.text(0.5, 0.015,
         "A 谐振频率 ωr=28.77（峰高 28 dB） · B ωn=30（−90°）\n"
         "C 下降段 ω=50 · D 截止频率 ωc（精确 99.1，渐近读数 94.9）",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB, family=FAM, linespacing=1.6)

fig.subplots_adjust(left=0.105, right=0.97, top=0.87, bottom=0.225, hspace=0.30)
fs.save(fig, "频域-反求-二阶Bode.png")
