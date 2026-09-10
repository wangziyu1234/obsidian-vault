# -*- coding: utf-8 -*-
"""典型环节伯德图（自控 05-1-2 §5.2）。

一次生成 8 张附件图，统一「单轴 + 左右双刻度」风格（与笔记 5.2 表格内
2×4 缩略图一致：左轴 L(ω)/dB 蓝、右轴 φ(ω)/° 赭红、灰网格、转折频率竖线）。

构建：..\\build.ps1 -File .\\bode-typical-links.py
注意：本脚本一次写多张图，因此不靠 FIGURE_OUT（那是单张通道），
      直接写 附件\\；文件名必须与 05-1-2 笔记里的 ![[...]] 完全一致。
"""
import os

import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

OUT = os.path.join(fs.REPO_ROOT, "附件")
W_MIN, W_MAX = 1e-2, 1e2          # 默认频率范围
W1, W2 = 1e-1, 1e1                # 带转折频率的环节用窄范围，转折点居中


def bode_dual(ax, w, mag_db, pha_deg, ylim_db, title):
    """按笔记既有风格画一张：左轴幅频（蓝）、右轴相频（赭红）。

    title 用两行："中文名\\n$公式$"。**不要写成同一条字符串**——字符串里同时
    有 CJK 和 `$...$` 时，mathtext 会接管整串并套 CM 字体集，
    中文因缺字形变成方框（纯中文、纯公式、中文+西文都没问题）。
    """
    ax.set_xscale("log")
    ax.set_xlim(w[0], w[-1])
    ax.set_ylim(*ylim_db)

    ax.plot(w, mag_db, color=fs.MAG, linewidth=2.0, zorder=3)
    ax.set_ylabel(r"$L(\omega)$/dB", color=fs.MAG)
    ax.tick_params(axis="y", colors=fs.MAG)
    ax.spines["left"].set_color(fs.MAG)

    ax.grid(True, which="major", color=fs.GRID, linewidth=0.7, alpha=0.9)
    ax.grid(True, which="minor", color=fs.GRID, linewidth=0.4, alpha=0.5)
    ax.set_xlabel(r"$\omega$ / (rad/s)")

    ax2 = ax.twinx()
    ax2.plot(w, pha_deg, color=fs.PHA, linewidth=2.0, zorder=3)
    ax2.set_ylim(-180, 180)
    ax2.set_yticks([180, 90, 0, -90, -180])
    ax2.set_ylabel(r"$\varphi(\omega)$ / $^\circ$", color=fs.PHA)
    ax2.tick_params(axis="y", colors=fs.PHA)
    ax2.spines["right"].set_color(fs.PHA)
    ax2.spines["left"].set_visible(False)

    ax.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)), zorder=1)
    ax.set_title(title, pad=8)
    return ax2


def note(ax, text, xy=(0.95, 0.07)):
    ax.text(*xy, text, transform=ax.transAxes, ha="right", va="bottom",
            color=fs.SUB, fontsize=12)


# ---------- 数据 ----------
w = np.logspace(np.log10(W_MIN), np.log10(W_MAX), 800)
wc = np.logspace(np.log10(W1), np.log10(W2), 800)

# 1 比例 K=1：幅值 0 dB 水平线，相角恒 0°
fig, ax = plt.subplots(figsize=(7.65, 4.5))
bode_dual(ax, w, np.zeros_like(w), np.zeros_like(w), (-45, 45), "比例环节\n$K$")
note(ax, "0 dB")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "频域-典型环节-比例Bode.png"), dpi=200); plt.close(fig)

# 2 积分 1/s：-20 dB/dec，相角恒 -90°
fig, ax = plt.subplots(figsize=(7.65, 4.5))
bode_dual(ax, w, -20 * np.log10(w), np.full_like(w, -90.0), (-45, 45), "积分环节\n$1/s$")
# 渐近线（与曲线重合，画出斜率示意）
ax.plot(w, -20 * np.log10(w), color=fs.SUB, linewidth=1.0, linestyle=(0, (5, 3)), zorder=2)
note(ax, r"$-20$ dB/dec")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "频域-典型环节-积分Bode.png"), dpi=200); plt.close(fig)

# 3 微分 s：+20 dB/dec，相角恒 +90°
fig, ax = plt.subplots(figsize=(7.65, 4.5))
bode_dual(ax, w, 20 * np.log10(w), np.full_like(w, 90.0), (-45, 45), "微分环节\n$s$")
ax.plot(w, 20 * np.log10(w), color=fs.SUB, linewidth=1.0, linestyle=(0, (5, 3)), zorder=2)
note(ax, r"$+20$ dB/dec")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "频域-典型环节-微分Bode.png"), dpi=200); plt.close(fig)

# 4 惯性 1/(Ts+1)，T=1：转折 ω=1
T = 1.0
mag = -10 * np.log10(1 + (wc * T) ** 2)
pha = -np.degrees(np.arctan(wc * T))
fig, ax = plt.subplots(figsize=(7.65, 4.5))
bode_dual(ax, wc, mag, pha, (-45, 45), "惯性环节\n$1/(Ts+1)$")
ax.axvline(1 / T, color="#8A94A3", linewidth=1.4, linestyle=":", zorder=2)
ax.text(1 / T, 38, r"$\omega_c$", ha="center", va="bottom", color=fs.SUB, fontsize=12)
# 渐近线：0 dB 段 + -20 dB/dec 段
ax.plot([wc[0], 1 / T], [0, 0], color=fs.SUB, linewidth=1.1, linestyle=(0, (5, 3)), zorder=2)
ax.plot([1 / T, wc[-1]], [0, -20 * np.log10(wc[-1] / T)], color=fs.SUB,
        linewidth=1.1, linestyle=(0, (5, 3)), zorder=2)
note(ax, r"$-20$ dB/dec")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "频域-典型环节-惯性Bode.png"), dpi=200); plt.close(fig)

# 5 一阶微分 Ts+1，T=1（与惯性关于 0 dB 对称）
fig, ax = plt.subplots(figsize=(7.65, 4.5))
bode_dual(ax, wc, -mag, -pha, (-45, 45), "一阶微分环节\n$Ts+1$")
ax.axvline(1 / T, color="#8A94A3", linewidth=1.4, linestyle=":", zorder=2)
ax.text(1 / T, 38, r"$\omega_c$", ha="center", va="bottom", color=fs.SUB, fontsize=12)
ax.plot([wc[0], 1 / T], [0, 0], color=fs.SUB, linewidth=1.1, linestyle=(0, (5, 3)), zorder=2)
ax.plot([1 / T, wc[-1]], [0, 20 * np.log10(wc[-1] / T)], color=fs.SUB,
        linewidth=1.1, linestyle=(0, (5, 3)), zorder=2)
note(ax, r"$+20$ dB/dec")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "频域-典型环节-一阶微分Bode.png"), dpi=200); plt.close(fig)

# 6 振荡环节 ωn²/(s²+2ζωn s+ωn²)，ζ<1：谐振峰、-40 dB/dec
fig, ax = plt.subplots(figsize=(7.65, 4.5))
ax.set_xscale("log")
ax.set_xlim(W1, W2)
ax.set_ylim(-45, 45)
ax.grid(True, which="major", color=fs.GRID, linewidth=0.7, alpha=0.9)
ax.grid(True, which="minor", color=fs.GRID, linewidth=0.4, alpha=0.5)
ax.set_xlabel(r"$\omega/\omega_n$")
ax.set_ylabel(r"$L(\omega)$/dB", color=fs.MAG)
ax.tick_params(axis="y", colors=fs.MAG)
ax.spines["left"].set_color(fs.MAG)
ax.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)), zorder=1)

ax2 = ax.twinx()
ax2.set_ylim(-180, 180)
ax2.set_yticks([180, 90, 0, -90, -180])
ax2.set_ylabel(r"$\varphi(\omega)$ / $^\circ$", color=fs.PHA)
ax2.tick_params(axis="y", colors=fs.PHA)
ax2.spines["right"].set_color(fs.PHA)
ax2.spines["left"].set_visible(False)
ax.set_title("振荡环节\n" + r"$\omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2)$", pad=8)

u = wc  # 以 ω/ωn 为横轴
ZETAS = [(0.1, "#7FA6CC"), (0.3, "#4C7BA6"), (0.5, "#2A5C8A"), (0.707, "#1F3D7A")]
for zeta, col in ZETAS:
    m = -10 * np.log10((1 - u ** 2) ** 2 + (2 * zeta * u) ** 2)
    p = -np.degrees(np.arctan2(2 * zeta * u, 1 - u ** 2))
    ax.plot(u, m, color=col, linewidth=1.6)
    ax2.plot(u, p, color=col, linewidth=1.6)

# ζ 标注统一收在左上角竖排：贴着曲线放会被后画的相频曲线盖住
for i, (zeta, col) in enumerate(ZETAS):
    ax.text(0.885, 0.86 - 0.075 * i, rf"$\zeta={zeta}$", transform=ax.transAxes,
            color=col, fontsize=11, va="top", ha="left")

# -40 dB/dec 渐近线示意
ax.plot([1, W2], [0, -40 * np.log10(W2)], color=fs.SUB, linewidth=1.1,
        linestyle=(0, (5, 3)), zorder=2)
ax.text(0.03, 0.85, r"$-40$ dB/dec", transform=ax.transAxes, ha="left", va="center",
        color="#8A94A3", fontsize=12)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "频域-典型环节-振荡Bode.png"), dpi=200); plt.close(fig)

# 7 二阶微分（与振荡关于 0 dB 对称、相频反号）
fig, ax = plt.subplots(figsize=(7.65, 4.5))
ax.set_xscale("log")
ax.set_xlim(W1, W2)
ax.set_ylim(-45, 45)
ax.grid(True, which="major", color=fs.GRID, linewidth=0.7, alpha=0.9)
ax.grid(True, which="minor", color=fs.GRID, linewidth=0.4, alpha=0.5)
ax.set_xlabel(r"$\omega/\omega_n$")
ax.set_ylabel(r"$L(\omega)$/dB", color=fs.MAG)
ax.tick_params(axis="y", colors=fs.MAG)
ax.spines["left"].set_color(fs.MAG)
ax.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)), zorder=1)

ax2 = ax.twinx()
ax2.set_ylim(-180, 180)
ax2.set_yticks([180, 90, 0, -90, -180])
ax2.set_ylabel(r"$\varphi(\omega)$ / $^\circ$", color=fs.PHA)
ax2.tick_params(axis="y", colors=fs.PHA)
ax2.spines["right"].set_color(fs.PHA)
ax2.spines["left"].set_visible(False)
ax.set_title("二阶微分环节\n" + r"$1-\frac{\omega^2}{\omega_n^2}+\mathrm{j}\frac{2\zeta\omega}{\omega_n}$", pad=8)

for zeta, col in ZETAS:
    m = 10 * np.log10((1 - u ** 2) ** 2 + (2 * zeta * u) ** 2)
    p = np.degrees(np.arctan2(2 * zeta * u, 1 - u ** 2))
    ax.plot(u, m, color=col, linewidth=1.6)
    ax2.plot(u, p, color=col, linewidth=1.6)

for i, (zeta, col) in enumerate(ZETAS):
    ax.text(0.03, 0.14 - 0.075 * i, rf"$\zeta={zeta}$", transform=ax.transAxes,
            color=col, fontsize=11, va="top", ha="left")

ax.plot([1, W2], [0, 40 * np.log10(W2)], color=fs.SUB, linewidth=1.1,
        linestyle=(0, (5, 3)), zorder=2)
ax.text(0.97, 0.06, r"$+40$ dB/dec", transform=ax.transAxes, ha="right", va="bottom",
        color="#8A94A3", fontsize=12)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "频域-典型环节-二阶微分Bode.png"), dpi=200); plt.close(fig)

# 8 延迟 e^{-τs}，τ=0.1：幅值恒 0 dB，相角线性下降
tau = 0.1
fig, ax = plt.subplots(figsize=(7.65, 4.5))
bode_dual(ax, w, np.zeros_like(w), -np.degrees(w * tau), (-45, 45),
          "延迟环节\n" + r"$e^{-\tau s}$")
note(ax, "0 dB")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "频域-典型环节-延迟Bode.png"), dpi=200); plt.close(fig)

print("saved 8 typical-link Bode figures to", OUT)
