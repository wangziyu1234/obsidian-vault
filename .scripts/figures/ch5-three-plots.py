# -*- coding: utf-8 -*-
"""三种图示法：3 张单图（05-1-1 §5.1.4）。

同一个 RC 一阶低通 G(s) = 1/(0.5s+1)（教材图5-3/5-7/5-8）分别画成
  频域-图示法-幅相曲线.png      幅相曲线（奈氏图）
  频域-图示法-伯德图.png        对数频率特性（伯德图，单轴左右双刻度）
  频域-图示法-尼科尔斯图.png    对数幅相曲线（尼科尔斯图）

构建：..\\build.ps1 -File .\\ch5-three-plots.py
"""
import os

import numpy as np
import matplotlib.pyplot as plt
import control as ct

import figures_style as fs

fs.use_style()
OUT = os.path.join(fs.REPO_ROOT, "附件")
sys = ct.tf([1], [0.5, 1])
w = np.logspace(-2, 2, 3000)
r = ct.frequency_response(sys, w)
G = r.fresp[0, 0, :]
mag = 20 * np.log10(np.abs(G))
pha = np.unwrap(np.angle(G)) * 180 / np.pi


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=fs.DPI)
    plt.close(fig)
    print("saved", path)


# ---------------- (a) 幅相曲线 ----------------
fig, ax = plt.subplots(figsize=(5.8, 4.8))
ax.plot(G.real, G.imag, color=fs.MAG, linewidth=2.4)
th = np.linspace(-np.pi, 0, 300)
ax.plot(0.5 + 0.5 * np.cos(th), 0.5 * np.sin(th), color=fs.SUB,
        linewidth=0.9, linestyle=(0, (2, 3)))
ax.plot([0.5], [0], marker="x", color=fs.SUB, markersize=6)
ax.annotate("ω = 0", xy=(1, 0), xytext=(1.06, -0.07), color=fs.INK, fontsize=11)
ax.annotate("ω → ∞", xy=(0, 0), xytext=(-0.30, -0.07), color=fs.INK, fontsize=11)
# 说明块放正下方空带：半圆最低只到 −0.5，且整块右移到 x>0.1 之外，避免压住 x=0 纵轴
ax.annotate("圆心 (0.5, 0)、半径 0.5 的半圆", xy=(0.5, -0.5), xytext=(0.45, -0.82),
            color=fs.SUB, fontsize=10.5, ha="center")
ax.annotate("", xy=(0.5, -0.52), xytext=(0.45, -0.74),
            arrowprops=dict(arrowstyle="-|>", color=fs.MAG, lw=1.7, mutation_scale=14))
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-0.3, 1.2)
ax.set_ylim(-0.9, 0.4)
ax.axhline(0, color=fs.SUB, linewidth=0.8)
ax.axvline(0, color=fs.SUB, linewidth=0.8)
ax.grid(True, color=fs.GRID, linewidth=0.6, alpha=0.85)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xlabel("实部")
ax.set_ylabel("虚部")
ax.set_title("幅相曲线（奈氏图）\n横轴实部、纵轴虚部，ω 为参变量", pad=8)
save(fig, "频域-图示法-幅相曲线.png")

# ---------------- (b) 伯德图（上下两层） ----------------
fig, (ax, ax2) = fs.new_bode_axes(figsize=(6.6, 6.2))
for a in (ax, ax2):
    a.set_xscale("log")
    a.set_xlim(w[0], w[-1])
    fs.tidy(a)
ax.plot(w, mag, color=fs.MAG, linewidth=2.2)
ax2.plot(w, pha, color=fs.PHA, linewidth=2.2)
ax.set_ylim(-60, 10)
ax2.set_ylim(-100, 10)
ax2.set_yticks([0, -45, -90])
ax.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
ax.axvline(2, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
ax2.axvline(2, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
# 标注一律走曲线够不到的空区：幅频曲线在 ω>10 已降到 −15 dB 以下，
# 于是「右上（y 高）」和「右下（y 低）」各有一整条空带可用，再用细引线连回目标点。
ax.annotate("转折频率 1/T = 2", xy=(2, 5), xytext=(1.15, 5.5),
            color=fs.SUB, fontsize=10.5, ha="right")
ax.annotate("ω = 2 处 L = −3 dB", xy=(2, -3), xytext=(14, -5),
            color=fs.INK, fontsize=10.5, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", linewidth=0.8, color=fs.SUB))
ax.annotate("−20 dB/dec", xy=(40, -26.0), xytext=(40, -46),
            color=fs.MAG, fontsize=11, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", linewidth=0.8, color=fs.SUB))
ax2.annotate("ω = 2 处 φ = −45°", xy=(2, -45), xytext=(11, -10),
             color=fs.PHA, fontsize=10.5, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", linewidth=0.8, color=fs.SUB))
fig.suptitle("对数频率特性（伯德图）：上幅频、下相频，共用横轴 lgω", fontsize=13, y=0.97)
save(fig, "频域-图示法-伯德图.png")

# ---------------- (c) 尼科尔斯图 ----------------
fig, ax = plt.subplots(figsize=(5.8, 4.8))
ax.plot(pha, mag, color=fs.MAG, linewidth=2.2)
i2 = int(np.argmin(np.abs(w - 2)))
ax.plot([pha[i2]], [mag[i2]], marker="o", color=fs.PHA, markersize=6)
ax.annotate("ω = 2：(−45°, −3 dB)", xy=(pha[i2], mag[i2]), xytext=(12, 14),
            textcoords="offset points", color=fs.PHA, fontsize=10.5)
ax.annotate("ω = 0：(0°, 0 dB)", xy=(0, 0), xytext=(8, -36),
            textcoords="offset points", color=fs.INK, fontsize=10.5)
ax.annotate("ω → ∞：(−90°, −∞)", xy=(-90, -60), xytext=(-18, 10),
            textcoords="offset points", color=fs.INK, fontsize=10.5)
ax.set_xlim(-100, 10)
ax.set_ylim(-70, 12)
ax.set_xlabel("φ / °")
ax.set_ylabel("L / dB", color=fs.MAG)
ax.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
ax.axvline(-180, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
ax.grid(True, color=fs.GRID, linewidth=0.6, alpha=0.85)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_title("对数幅相曲线（尼科尔斯图）\n横轴 φ、纵轴 L，均为线性分度", pad=8)
save(fig, "频域-图示法-尼科尔斯图.png")

print("ω=2 处 mag=%.2f dB, phase=%.2f°" % (mag[i2], pha[i2]))
