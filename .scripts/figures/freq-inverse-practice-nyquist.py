# figure: 频域-反求-综合题奈氏.png
# -*- coding: utf-8 -*-
"""补充算例（自编）的奈氏图：G(s)=2500/[(s^2+2.588s+25)(0.01s+1)]。

起点 (100,0) → 向右上凸起 → 穿负虚轴 → 第三象限 → 负实轴交点 (−9.39, 0)
→ 第二象限 → 沿 −270° 方向回到原点。等比例坐标。

构建：..\\build.ps1 -File .\\freq-inverse-practice-nyquist.py
"""
import numpy as np
import control as ct
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
sys = ct.tf([2500.0], np.polymul([1.0, 2.588, 25.0], [0.01, 1.0]))


def at(w):
    return complex(ct.frequency_response(sys, [w]).fresp[0, 0, 0])


W = np.logspace(-1.2, 3.0, 4000)
Z = np.asarray(ct.frequency_response(sys, W).fresp[0, 0, :])

fig, ax = plt.subplots(figsize=(7.0, 10.6))
ax.plot(Z.real, Z.imag, color=fs.MAG, lw=2.1)
ax.axhline(0, color=fs.SUB, lw=0.85)
ax.axvline(0, color=fs.SUB, lw=0.85)

BOX = dict(facecolor="white", edgecolor="none", alpha=0.95, pad=1.2)


def mark(z, text, dx=9, dy=9, color=fs.PHA):
    ax.plot([z.real], [z.imag], "o", ms=5.5, color=color, zorder=6)
    ax.annotate(text, (z.real, z.imag), xytext=(dx, dy), textcoords="offset points",
                fontsize=13, color=color, bbox=BOX, zorder=7)


mark(at(4.65), "A", dx=10, dy=-18)
mark(complex(0, at(4.9365).imag), "B", dx=-24, dy=-16)
mark(at(16.8469), "C", dx=-8, dy=-20)
mark(at(47.7266), "D", dx=12, dy=12)
ax.plot([at(0.05).real], [at(0.05).imag], "o", ms=5.5, color=fs.MAG, zorder=6)
ax.annotate("K=100", (at(0.05).real, at(0.05).imag), xytext=(6, 8),
            textcoords="offset points", fontsize=12, color=fs.MAG, bbox=BOX, zorder=7)

ax.set_xlim(-13, 132)
ax.set_ylim(-212, 22)
ax.set_aspect("equal", adjustable="box")
ax.grid(True, color=fs.GRID, lw=0.55, alpha=0.6)
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel(r"$\mathrm{Re}\,G(\mathrm{j}\omega)$")
ax.set_ylabel(r"$\mathrm{Im}\,G(\mathrm{j}\omega)$")

fig.suptitle(r"$G(s)=\frac{2500}{(s^2+2.588s+25)(0.01s+1)}$", fontsize=15.5, y=0.965)
fig.text(0.5, 0.012,
         "A 离原点最远（ωr=4.65，|G|=200） · B 穿负虚轴（ω=4.94）\n"
         "C 负实轴交点（ω=16.85，19.5 dB） · D 单位圆交点（ωc≈47.7）",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB, family=FAM, linespacing=1.6)

fig.subplots_adjust(left=0.16, right=0.96, top=0.92, bottom=0.135)
fs.save(fig, "频域-反求-综合题奈氏.png")
