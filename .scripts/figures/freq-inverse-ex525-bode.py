# figure: 频域-反求-例525Bode.png
# -*- coding: utf-8 -*-
"""例5.25：G(s)=40(s+0.5)/[s(s+0.2)(s^2+s+1)] 的伯德图（渐近线 + 精确曲线）。

点划线 = 低频延长线（过基准点 (ω=1, 40 dB)）；虚线 = 逐段折出的渐近线。
构建：..\\build.ps1 -File .\\freq-inverse-ex525-bode.py
"""
import numpy as np
import control as ct
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
num = np.array([40.0, 20.0])                                   # 40(s+0.5)
den = np.polymul(np.polymul([1.0, 0.0], [1.0, 0.2]), [1.0, 1.0, 1.0])
sys = ct.tf(num, den)

W = np.logspace(-1.7, 2.3, 2400)
resp = ct.frequency_response(sys, W).fresp[0, 0, :]
L = 20 * np.log10(np.abs(resp))
PH = np.degrees(np.unwrap(np.angle(resp)))


def asym(w):
    """低频延长线 L=20lgK-20lgw，在 0.2 / 0.5 / 1 处依次叠加斜率增量"""
    v = 40 - 20 * np.log10(w)
    l02 = 40 - 20 * np.log10(0.2)
    l05 = l02 - 40 * np.log10(0.5 / 0.2)
    l1 = l05 - 20 * np.log10(1.0 / 0.5)
    out = []
    for x in np.atleast_1d(w):
        y = 40 - 20 * np.log10(x)
        if x > 0.2:
            y = l02 + (-40) * np.log10(x / 0.2)
        if x > 0.5:
            y = l05 + (-20) * np.log10(x / 0.5)
        if x > 1.0:
            y = l1 + (-60) * np.log10(x / 1.0)
        out.append(y)
    return np.array(out) if len(out) > 1 else out[0]


WA = np.logspace(-1.7, 2.3, 600)
LA = asym(WA)
WLF = np.logspace(-1.7, 0.6, 200)                              # 低频延长线（只画到 ω≈4）
LLF = 40 - 20 * np.log10(WLF)

fig, (ax_m, ax_p) = fs.new_bode_axes(figsize=(7.8, 5.6))
ax_m.semilogx(W, L, color=fs.MAG, lw=2.0)
ax_p.semilogx(W, PH, color=fs.PHA, lw=2.0)
ax_m.semilogx(WA, LA, color=fs.SUB, lw=1.4, ls=(0, (5, 3)))
ax_m.semilogx(WLF, LLF, color=fs.SUB, lw=1.1, ls=(0, (2, 2)))

for ax in (ax_m, ax_p):
    fs.tidy(ax, turn_freqs=[0.2, 0.5, 1.0])
ax_m.axhline(0, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax_p.axhline(-180, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax_m.set_ylim(-95, 82)
ax_p.set_ylim(-285, -70)
ax_p.set_yticks([-90, -180, -270])
ax_m.set_title("对数幅频特性", loc="left", fontsize=13, color=fs.SUB, family=FAM)
ax_p.set_title("对数相频特性", loc="left", fontsize=13, color=fs.SUB, family=FAM)

ax_m.plot([1.0], [40.0], "o", ms=6, color=fs.MAG, zorder=6)
ax_m.annotate("基准点 (1, 40 dB)", (1.0, 40.0), xytext=(10, 8),
              textcoords="offset points", fontsize=12, color=fs.MAG,
              bbox=dict(facecolor="white", edgecolor="none", alpha=0.95, pad=1.2), zorder=7)

# 斜率标签一律沉到各段渐近线的下方约 15 dB：本图坐标轴只有 157px 高，
# 一个 20px 的文字框折算下来有 18 dB 高，贴着渐近线放必然同时压住渐近线、低频延长线和精确曲线。
for x, y, txt in [(0.06, 72, "-20"), (0.33, 21, "-40"), (0.72, 11, "-20"), (2.2, -24, "-60")]:
    ax_m.text(x, y, txt, fontsize=11, color=fs.SUB, ha="center", family=FAM,
              bbox=dict(facecolor="white", edgecolor="none", alpha=0.9, pad=0.8))

fig.suptitle(r"$G(s)=\frac{40(s+0.5)}{s(s+0.2)(s^2+s+1)}$", fontsize=16, y=0.975)
fig.text(0.5, 0.012,
         "虚线 = 渐近线（转折 0.2 / 0.5 / 1，斜率 −20 → −40 → −20 → −60）\n"
         "点划线 = 低频延长线，过基准点 (ω=1, 40 dB)",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB, family=FAM, linespacing=1.6)

fig.subplots_adjust(left=0.105, right=0.97, top=0.87, bottom=0.225, hspace=0.30)
fs.save(fig, "频域-反求-例525Bode.png")
