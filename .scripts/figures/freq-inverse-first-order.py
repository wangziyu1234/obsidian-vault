# figure: 频域-反求-一阶伯德奈氏对应.png
# -*- coding: utf-8 -*-
"""例5.23：一阶系统 G(s)=31.6/(0.5s+1) 的伯德图与奈氏图点对点对应。

左栏：对数幅频（实线精确、虚线渐近）与对数相频。
右栏：奈氏图正频率支（第四象限半圆，圆心 K/2、半径 K/2）。
标点：A = 转折频率（相角 -45°）；B = -20dB/dec 段的读数校验点；C = 截止频率（单位圆交点）。

构建：..\\build.ps1 -File .\\freq-inverse-first-order.py
"""
import numpy as np
import control as ct
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
K = 10 ** 1.5                        # 20 lg K = 30 dB
T = 0.5                              # 转折频率 1/T = 2 rad/s
WC = 2 * 10 ** 1.5                   # 渐近法截止频率 = 63.2 rad/s
WB = 10.0                            # 幅频读数校验点
sys = ct.tf([K], [T, 1])

W = np.logspace(-1.25, 2.35, 1400)
resp = ct.frequency_response(sys, W).fresp[0, 0, :]
L = 20 * np.log10(np.abs(resp))
PH = np.degrees(np.unwrap(np.angle(resp)))


def at(w):
    return complex(ct.frequency_response(sys, [w]).fresp[0, 0, 0])


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
wa = np.array([0.055, 2.0, 45.0])
ax_m.semilogx(wa, 30 - 20 * np.log10(np.maximum(wa, 2.0) / 2.0),
              color=fs.SUB, lw=1.3, ls=(0, (5, 3)), label="asymptote")

for ax in (ax_m, ax_p):
    fs.tidy(ax, turn_freqs=[2.0, WC])
ax_m.axhline(0, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax_m.set_ylabel(r"$L(\omega)$ / dB")
ax_p.set_ylabel(r"$\varphi(\omega)$ / $^\circ$")
ax_p.set_xlabel(r"$\omega$ / (rad/s)")
ax_m.set_ylim(-28, 36)
ax_p.set_ylim(-104, 8)
ax_p.set_yticks([0, -45, -90])
ax_m.set_title("对数幅频特性", loc="left", fontsize=12.5, color=fs.SUB, family=FAM)
ax_p.set_title("对数相频特性", loc="left", fontsize=12.5, color=fs.SUB, family=FAM)

mark(ax_m, WB, 20 * np.log10(abs(at(WB))), "B")
mark(ax_m, WC, 20 * np.log10(abs(at(WC))), "C")
mark(ax_p, 2.0, -45.0, "A")

# ---------------- 右：奈氏图 ----------------
WN = np.logspace(-1.6, 3.6, 2400)
zn = np.asarray(ct.frequency_response(sys, WN).fresp[0, 0, :])
ax_n.plot(zn.real, zn.imag, color=fs.MAG, lw=2.2)
th = np.linspace(0, 2 * np.pi, 500)
ax_n.plot(np.cos(th), np.sin(th), color=fs.SUB, lw=1.1, ls=(0, (4, 3)))
ax_n.plot([0, 26.0], [0, -26.0], color=fs.SUB, lw=1.0, ls=(0, (2, 2)))
ax_n.plot([K], [0], "o", ms=5.0, color=fs.MAG, zorder=6)
ax_n.annotate("$K=31.6$", (K, 0), xytext=(-58, 4), textcoords="offset points",
              fontsize=12, color=fs.MAG, bbox=BOX, zorder=7)
ax_n.annotate("-45°", (12.0, -12.0), xytext=(10, -14), textcoords="offset points",
              fontsize=11.5, color=fs.SUB, bbox=BOX, zorder=7)
ax_n.annotate("unit circle", (0.55, -0.72), xytext=(14, -2), textcoords="offset points",
              fontsize=11, color=fs.SUB, bbox=BOX, zorder=7, family=FAM)

for w, key, dx, dy in [(2.0, "A", 10, -22), (WB, "B", 10, -20), (WC, "C", 10, -20)]:
    z = at(w)
    mark(ax_n, z.real, z.imag, key, dx=dx, dy=dy)

ax_n.set_xlim(-5, 36)
ax_n.set_ylim(-19.5, 6.5)
ax_n.set_xticks([0, 10, 20, 30])
ax_n.set_yticks([-15, -10, -5, 0, 5])
ax_n.set_aspect("equal", adjustable="box")
ax_n.axhline(0, color=fs.SUB, lw=0.9)
ax_n.axvline(0, color=fs.SUB, lw=0.9)
ax_n.grid(True, color=fs.GRID, lw=0.55, alpha=0.6)
ax_n.spines[["top", "right"]].set_visible(False)
ax_n.set_xlabel(r"$\mathrm{Re}\,G(\mathrm{j}\omega)$")
ax_n.set_ylabel(r"$\mathrm{Im}\,G(\mathrm{j}\omega)$")
ax_n.set_title("奈氏图（正频率支）", loc="left", fontsize=12.5, color=fs.SUB, family=FAM)

fig.suptitle(r"$G(s)=\frac{31.6}{0.5s+1}$", fontsize=15.5, y=0.975)
fig.text(0.5, 0.022,
         "A 转折频率 ω=2（相角 −45°）  ·  B 渐近线读数校验点 ω=10  ·  C 截止频率 ωc=63.2（单位圆交点）",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB, family=FAM)

fig.subplots_adjust(left=0.075, right=0.985, top=0.88, bottom=0.20)
fs.save(fig, "频域-反求-一阶伯德奈氏对应.png")
