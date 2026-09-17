# figure: 频域-反求-二阶伯德奈氏对应.png
# -*- coding: utf-8 -*-
"""例5.24：二阶振荡系统 G(s)=9000/(s^2+12.18s+900) 的伯德图与奈氏图点对点对应。

左栏：对数幅频（实线精确、虚线渐近、谐振峰）与对数相频。
右栏：奈氏图正频率支（0 型，起点 (K,0)、终点原点）。
标点：A = 谐振频率 ωr（幅频峰 / 奈氏图距原点最远点）；
      B = ωn（相角 -90° / 奈氏图与负虚轴交点）；
      C = -40dB/dec 下降段样本点；D = 截止频率 ωc（0 dB / 单位圆交点）。

构建：..\\build.ps1 -File .\\freq-inverse-second-order.py
"""
import numpy as np
import control as ct
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
K, XI, WN = 10.0, 0.203, 30.0
WR = 28.77                     # 谐振频率（题给读数）
sys = ct.tf([K * WN ** 2], [1.0, 2 * XI * WN, WN ** 2])
WC_ASYM = WN * np.sqrt(10)     # 渐近线读数 94.87 rad/s

W = np.logspace(-1.2, 3.4, 2400)
resp = ct.frequency_response(sys, W).fresp[0, 0, :]
L = 20 * np.log10(np.abs(resp))
PH = np.degrees(np.unwrap(np.angle(resp)))


def at(w):
    return complex(ct.frequency_response(sys, [w]).fresp[0, 0, 0])


# 精确 0 dB 穿越（二分）
lo, hi = 30.0, 400.0
for _ in range(120):
    mid = (lo + hi) / 2
    if abs(at(mid)) > 1.0:
        lo = mid
    else:
        hi = mid
WC = (lo + hi) / 2

fig = plt.figure(figsize=(12.6, 5.3))
gs = fig.add_gridspec(2, 2, width_ratios=[1.32, 1.0], wspace=0.26, hspace=0.34)
ax_m = fig.add_subplot(gs[0, 0])
ax_p = fig.add_subplot(gs[1, 0], sharex=ax_m)
ax_n = fig.add_subplot(gs[:, 1])

BOX = dict(facecolor="white", edgecolor="none", alpha=0.95, pad=1.2)


def mark(ax, x, y, text, dx=9, dy=9, color=fs.PHA):
    ax.plot([x], [y], "o", ms=5.5, color=color, zorder=6)
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                fontsize=13, color=color, bbox=BOX, zorder=7)


# ---------------- 左：伯德图 ----------------
ax_m.semilogx(W, L, color=fs.MAG, lw=2.0, label=r"$L(\omega)$")
ax_p.semilogx(W, PH, color=fs.PHA, lw=2.0, label=r"$\varphi(\omega)$")
wa = np.array([0.4, WN, 260.0])
ax_m.semilogx(wa, 20 - 40 * np.log10(np.maximum(wa, WN) / WN),
              color=fs.SUB, lw=1.3, ls=(0, (5, 3)), label="asymptote")

for ax in (ax_m, ax_p):
    fs.tidy(ax, turn_freqs=[WR, WN, WC_ASYM])
ax_m.axhline(0, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax_m.set_ylabel(r"$L(\omega)$ / dB")
ax_p.set_ylabel(r"$\varphi(\omega)$ / $^\circ$")
ax_p.set_xlabel(r"$\omega$ / (rad/s)")
ax_m.set_ylim(-40, 40)
ax_p.set_ylim(-200, 12)
ax_p.set_yticks([0, -90, -180])
ax_m.set_title("对数幅频特性", loc="left", fontsize=12.5, color=fs.SUB, family=FAM)
ax_p.set_title("对数相频特性", loc="left", fontsize=12.5, color=fs.SUB, family=FAM)

mark(ax_m, WR, 20 * np.log10(abs(at(WR))), "A", dx=-16, dy=8)
mark(ax_m, 50.0, 20 * np.log10(abs(at(50.0))), "C", dx=8, dy=-18)
mark(ax_m, WC, 0.0, "D", dx=6, dy=-20)
mark(ax_p, WN, -90.0, "B", dx=9, dy=-16)

# ---------------- 右：奈氏图 ----------------
WN_GRID = np.logspace(-1.4, 4.2, 3000)
zn = np.asarray(ct.frequency_response(sys, WN_GRID).fresp[0, 0, :])
ax_n.plot(zn.real, zn.imag, color=fs.MAG, lw=2.2)
th = np.linspace(0, 2 * np.pi, 600)
ax_n.plot(np.cos(th), np.sin(th), color=fs.SUB, lw=1.1, ls=(0, (4, 3)))
ax_n.plot([K], [0], "o", ms=5.0, color=fs.MAG, zorder=6)
ax_n.annotate(r"$K=10$", (K, 0), xytext=(7, 6), textcoords="offset points",
              fontsize=12, color=fs.MAG, bbox=BOX, zorder=7)
ax_n.annotate("unit circle", (0.62, 0.78), xytext=(6, 4), textcoords="offset points",
              fontsize=11, color=fs.SUB, bbox=BOX, zorder=7, family=FAM)

for w, key, dx, dy in [(WR, "A", 8, -20), (WN, "B", -20, -20), (50.0, "C", -22, 6), (WC, "D", -22, 6)]:
    z = at(w)
    mark(ax_n, z.real, z.imag, key, dx=dx, dy=dy)

ax_n.set_xlim(-11, 17)
ax_n.set_ylim(-28, 4)
ax_n.set_xticks([-10, -5, 0, 5, 10, 15])
ax_n.set_yticks([-25, -20, -15, -10, -5, 0])
ax_n.set_aspect("equal", adjustable="box")
ax_n.axhline(0, color=fs.SUB, lw=0.9)
ax_n.axvline(0, color=fs.SUB, lw=0.9)
ax_n.grid(True, color=fs.GRID, lw=0.55, alpha=0.6)
ax_n.spines[["top", "right"]].set_visible(False)
ax_n.set_xlabel(r"$\mathrm{Re}\,G(\mathrm{j}\omega)$")
ax_n.set_ylabel(r"$\mathrm{Im}\,G(\mathrm{j}\omega)$")
ax_n.set_title("奈氏图（正频率支）", loc="left", fontsize=12.5, color=fs.SUB, family=FAM)

fig.suptitle(r"$G(s)=\frac{9000}{s^2+12.18s+900}$", fontsize=15.5, y=0.975)
fig.text(0.5, 0.022,
         "A 谐振频率 ωr=28.77（幅频峰）  ·  B ωn=30（相角 −90°）  ·  C 下降段 ω=50  ·  "
         "D 截止频率 ωc（精确 99.1，渐近线读数 94.9）",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB, family=FAM)

fig.subplots_adjust(left=0.075, right=0.985, top=0.88, bottom=0.20)
fs.save(fig, "频域-反求-二阶伯德奈氏对应.png")
