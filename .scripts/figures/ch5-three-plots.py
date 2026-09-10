# -*- coding: utf-8 -*-
"""第5章补图：三种图示法对照（05-1-1 §5.1.5）。

同一个 RC 一阶低通 G(s) = 1/(0.5s+1)（教材图5-3/5-7/5-8）画成
  (a) 幅相曲线（奈氏图）  (b) 对数频率特性（伯德图）  (c) 对数幅相曲线（尼科尔斯图）

构建：..\\build.ps1 -File .\\ch5-three-plots.py
"""
import os

import numpy as np
import matplotlib.pyplot as plt
import control as ct

import figures_style as fs

fs.use_style()
sys = ct.tf([1], [0.5, 1])
w = np.logspace(-2, 2, 3000)
r = ct.frequency_response(sys, w)
G = r.fresp[0, 0, :]
mag = 20 * np.log10(np.abs(G))
pha = np.unwrap(np.angle(G)) * 180 / np.pi

fig = plt.figure(figsize=(13.2, 4.4))

# ---------------- (a) 幅相曲线 ----------------
ax1 = fig.add_subplot(1, 3, 1)
ax1.plot(G.real, G.imag, color=fs.MAG, linewidth=2.2)
ax1.plot([0.5], [0], marker="x", color=fs.SUB, markersize=6)
th = np.linspace(-np.pi, 0, 300)
ax1.plot(0.5 + 0.5 * np.cos(th), 0.5 * np.sin(th), color=fs.SUB,
         linewidth=0.9, linestyle=(0, (2, 3)))
ax1.annotate("ω = 0", xy=(1, 0), xytext=(1.06, -0.06), color=fs.INK, fontsize=11)
ax1.annotate("ω → ∞", xy=(0, 0), xytext=(-0.22, -0.06), color=fs.INK, fontsize=11)
ax1.annotate("圆心 (0.5, 0)、半径 0.5 的半圆", xy=(0.5, -0.5), xytext=(-0.06, -0.74),
             color=fs.SUB, fontsize=10.5)
ax1.annotate("", xy=(0.35, -0.28), xytext=(0.45, -0.20),
             arrowprops=dict(arrowstyle="-|>", color=fs.MAG, lw=1.6, mutation_scale=14))
ax1.set_aspect("equal", adjustable="box")
ax1.set_xlim(-0.25, 1.15)
ax1.set_ylim(-0.85, 0.45)
ax1.set_xlabel("实部")
ax1.set_ylabel("虚部")
ax1.set_title("(a) 幅相曲线（奈氏图）\n横轴实部、纵轴虚部，ω 为参变量", pad=8)

# ---------------- (b) 伯德图 ----------------
ax2 = fig.add_subplot(1, 3, 2)
ax2.semilogx(w, mag, color=fs.MAG, linewidth=2.2)
ax2.set_ylabel("L / dB", color=fs.MAG)
ax2.set_xlabel("ω / (rad/s)")
ax2.set_ylim(-60, 10)
ax3 = ax2.twinx()
ax3.semilogx(w, pha, color=fs.PHA, linewidth=2.2)
ax3.set_ylabel("φ / °", color=fs.PHA)
ax3.set_ylim(-100, 10)
ax3.set_yticks([0, -45, -90])
ax2.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
ax2.axvline(2, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
ax2.annotate("转折频率 1/T = 2", xy=(2, 8), xytext=(-4, 0),
             textcoords="offset points", color=fs.SUB, fontsize=10.5)
ax2.annotate("−20 dB/dec", xy=(20, -30), color=fs.MAG, fontsize=11)
ax2.annotate("ω = 2 处：−3 dB、−45°", xy=(2, -3), xytext=(14, -46),
             textcoords="offset points", color=fs.INK, fontsize=10.5)
for ax in (ax2,):
    ax.grid(True, which="both", color=fs.GRID, linewidth=0.5, alpha=0.8)
    for s in ("top",):
        ax.spines[s].set_visible(False)
ax2.set_title("(b) 对数频率特性（伯德图）\n横轴 lgω 分度，幅频、相频分画", pad=8)

# ---------------- (c) 尼科尔斯图 ----------------
ax4 = fig.add_subplot(1, 3, 3)
ax4.plot(pha, mag, color=fs.MAG, linewidth=2.2)
ax4.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
ax4.axvline(-180, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
i2 = int(np.argmin(np.abs(w - 2)))
ax4.plot([pha[i2]], [mag[i2]], marker="o", color=fs.PHA, markersize=6)
ax4.annotate("ω = 2：(−45°, −3 dB)", xy=(pha[i2], mag[i2]), xytext=(10, 12),
             textcoords="offset points", color=fs.PHA, fontsize=10.5)
ax4.annotate("ω = 0：\n(0°, 0 dB)", xy=(0, 0), xytext=(6, -34),
             textcoords="offset points", color=fs.INK, fontsize=10.5)
ax4.annotate("−90°\n(ω → ∞)", xy=(-90, -60), xytext=(-16, 8),
             textcoords="offset points", color=fs.INK, fontsize=10.5)
ax4.set_xlim(-100, 10)
ax4.set_ylim(-70, 12)
ax4.set_xlabel("φ / °")
ax4.set_ylabel("L / dB", color=fs.MAG)
ax4.grid(True, color=fs.GRID, linewidth=0.5, alpha=0.8)
for s in ("top", "right"):
    ax4.spines[s].set_visible(False)
ax4.set_title("(c) 对数幅相曲线（尼科尔斯图）\n横轴 φ、纵轴 L，均为线性分度", pad=8)

fig.tight_layout()
out = os.path.join(fs.REPO_ROOT, "附件", "频域-三种图示法对照.png")
fig.savefig(out, dpi=fs.DPI)
print("saved", out)
print("ω=2 处 mag=%.2f dB, phase=%.2f°" % (mag[i2], pha[i2]))
print("圆心 (0.5,0) 半径 0.5；|G(0)|=%.3f" % abs(G[0]))
