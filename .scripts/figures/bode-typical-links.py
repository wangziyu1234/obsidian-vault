# -*- coding: utf-8 -*-
"""典型环节伯德图（自控 05-1-2 §5.2）：8 张单图，**统一上下两层**
（上：对数幅频 L/dB，下：对数相频 φ/°，共用横轴）。

产物（与 8 张 `频域-典型环节-*Nyquist.png` 成对）：
  频域-典型环节-比例Bode.png / 积分 / 微分 / 惯性 / 一阶微分 / 振荡 / 二阶微分 / 延迟

图内文字不混用中文与 `$…$`（同串会让中文掉字形），标题写成两行：中文名 + 公式。
构建：..\\build.ps1 -File .\\bode-typical-links.py
"""
import os

import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()
OUT = os.path.join(fs.REPO_ROOT, "附件")

W = np.logspace(-2, 2, 1500)
W1 = np.logspace(-1, 1, 1500)          # 带转折频率的环节用窄范围


def emit(name, title, w, mag, pha, ylim_db, ylim_ph, turn=(), asymptote=None,
         note=None):
    """一张典型环节伯德图：上幅频、下相频，共用横轴。"""
    fig, (axm, axp) = fs.new_bode_axes(figsize=(6.4, 6.2))
    for ax in (axm, axp):
        ax.set_xscale("log")
        ax.set_xlim(w[0], w[-1])
        fs.tidy(ax, turn)
    axm.plot(w, mag, color=fs.MAG, linewidth=2.2)
    axp.plot(w, pha, color=fs.PHA, linewidth=2.2)
    axm.set_ylim(*ylim_db)
    axp.set_ylim(*ylim_ph)
    axm.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    axp.axhline(0, color=fs.SUB, linewidth=0.7, linestyle=(0, (1, 4)))
    axp.axhline(-180, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    if asymptote is not None:
        wa, La = asymptote
        axm.plot(wa, La, color=fs.INK, linewidth=1.3, linestyle=(0, (6, 4)))
    if note:
        axm.annotate(note, xy=(0.02, 0.06), xycoords="axes fraction",
                     color=fs.INK, fontsize=11)
    fig.suptitle(title, fontsize=13, y=0.97)
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=fs.DPI)
    plt.close(fig)
    print("saved", path)


# 1 比例 K = 1
emit("频域-典型环节-比例Bode.png", "比例环节\nK", W,
     np.full_like(W, 0.0), np.zeros_like(W), (-40, 40), (-180, 180),
     note="L ≡ 20lgK = 0 dB，φ ≡ 0°")

# 2 积分
emit("频域-典型环节-积分Bode.png", "积分环节\n1/s", W,
     -20 * np.log10(W), np.full_like(W, -90.0), (-60, 60), (-180, 180),
     note="过 (1, 0) 点、斜率 −20 dB/dec；φ ≡ −90°")

# 3 微分
emit("频域-典型环节-微分Bode.png", "微分环节\ns", W,
     20 * np.log10(W), np.full_like(W, 90.0), (-60, 60), (-180, 180),
     note="过 (1, 0) 点、斜率 +20 dB/dec；φ ≡ +90°")

# 4 惯性 T = 1
mag = -10 * np.log10(1 + W1 ** 2)
pha = -np.degrees(np.arctan(W1))
emit("频域-典型环节-惯性Bode.png", "惯性环节\n1/(Ts+1)", W1, mag, pha,
     (-40, 10), (-100, 10), turn=(1,),
     asymptote=([W1[0], 1, W1[-1]], [0, 0, -20]),
     note="转折频率 1/T = 1：φ = −45°、L ≈ −3 dB")

# 5 一阶微分 T = 1
emit("频域-典型环节-一阶微分Bode.png", "一阶微分环节\nTs+1", W1,
     -mag, -pha, (-10, 40), (-10, 100), turn=(1,),
     asymptote=([W1[0], 1, W1[-1]], [0, 0, 20]),
     note="转折频率 1/T = 1：φ = +45°、L ≈ +3 dB")

# 6 振荡 ζ = 0.5
z = 0.5
u = W1 ** 2
mag_osc = -10 * np.log10((1 - u) ** 2 + (2 * z * np.sqrt(u)) ** 2)
pha_osc = -np.degrees(np.arctan2(2 * z * np.sqrt(u), 1 - u))
emit("频域-典型环节-振荡Bode.png", "振荡环节\nωn²/(s²+2ζωn s+ωn²)", W1,
     mag_osc, pha_osc, (-60, 25), (-200, 20), turn=(1,),
     asymptote=([W1[0], 1, W1[-1]], [0, 0, -40]),
     note="转折频率 ωn = 1：φ = −90°、L = −20lg(2ζ)；本例 ζ = 0.5")

# 7 二阶微分 ζ = 0.5
emit("频域-典型环节-二阶微分Bode.png", "二阶微分环节\ns²/ωn²+2ζs/ωn+1", W1,
     -mag_osc, -pha_osc, (-25, 60), (-20, 200), turn=(1,),
     asymptote=([W1[0], 1, W1[-1]], [0, 0, 40]),
     note="转折频率 ωn = 1：φ = +90°、L = 20lg(2ζ)；本例 ζ = 0.5")

# 8 延迟 τ = 1
emit("频域-典型环节-延迟Bode.png", "延迟环节\ne^(−τs)", W,
     np.zeros_like(W), -np.degrees(W), (-40, 40), (-300, 60),
     note="L ≡ 0 dB；φ = −ωτ(rad) = −57.3°·ωτ，无相角限位")
