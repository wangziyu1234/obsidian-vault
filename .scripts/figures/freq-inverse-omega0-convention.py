# figure: 频域-反求-低频延长线与ω0.png
# -*- coding: utf-8 -*-
"""由伯德图反求：三种型别的低频渐近线都过 (ω=1, L=20lg K)，与 0 dB 线的交点 ω0 = K^(1/ν)。

教材 §5-2.4 式(5-55)—(5-57) 的几何读法：
    方法一 任取 ω0 算高度   La(ω) = 20lg K - 20ν·lg ω
    方法二 取 ω = 1         La(1) = 20lg K           ⇒ 三条延长线共过 (1, 20lg K)
    方法三 取 La(ω0) = 0    ω0 = K^(1/ν)             ⇒ 与 0 dB 线的交点
取 K = 10（20lg K = 20 dB），ν = 0, 1, 2 三条低频段的延长线画在一起。
注意：ν = 0 的水平线一般不与 0 dB 相交，ω0 这个口径只对 ν ≥ 1 有意义。

图内文字规则（figures_style 里记过的坑）：含 $…$ 的字符串不能混中文，
所以本图的中文标注一律写成纯文本（希腊字母用 Unicode 字符）。

构建：..\build.ps1 -File .\freq-inverse-omega0-convention.py
"""
import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

FAM = ["Microsoft YaHei", "SimHei"]
K = 10.0
L1 = 20 * np.log10(K)          # 20 dB

COL = {0: fs.MAG, 1: "#1D9E75", 2: fs.PHA}
LBL = {0: "ν = 0（0 型，水平线）",
       1: "ν = 1（Ⅰ 型，-20 dB/dec）",
       2: "ν = 2（Ⅱ 型，-40 dB/dec）"}

fig, ax = plt.subplots(figsize=(7.8, 4.7))

w = np.array([0.12, 26.0])
for nu in (0, 1, 2):
    ax.semilogx(w, L1 - 20 * nu * np.log10(w), color=COL[nu], lw=2.0, label=LBL[nu])

ax.axhline(0, color=fs.SUB, lw=0.9, ls=(0, (2, 2)))
ax.vlines(1.0, -70, L1, color=fs.SUB, lw=1.0, ls=(0, (4, 3)))

ax.plot([1.0], [L1], "o", ms=6.5, color=fs.INK, zorder=6)
ax.annotate("ω = 1 处 L = 20lg K（方法二）", (1.0, L1),
            xytext=(14, 18), textcoords="offset points",
            fontsize=12, color=fs.INK, family=FAM)

for nu in (1, 2):
    w0 = K ** (1.0 / nu)
    ax.plot([w0], [0], "o", ms=6.5, color=COL[nu], zorder=6)
    if nu == 1:
        off, ha, va = (10, -22), "left", "top"
    else:
        off, ha, va = (-10, -10), "right", "top"
    ax.annotate(r"$\omega_0=K^{1/\nu}=%.3g$" % w0, (w0, 0),
                xytext=off, textcoords="offset points",
                ha=ha, va=va, fontsize=12.5, color=COL[nu])

ax.set_xlim(0.12, 26)
ax.set_ylim(-70, 45)
ax.set_ylabel(r"$L_a(\omega)$ / dB")
ax.set_xlabel(r"$\omega$ / (rad/s)")
ax.set_xticks([0.1, 1, K ** 0.5, K, 100])
ax.set_xticklabels([r"$0.1$", r"$1$", r"$3.16$", r"$10$", r"$100$"])
ax.set_yticks([0, L1])
ax.set_yticklabels([r"$0$", r"$20\lg K$"])
ax.minorticks_off()
fs.tidy(ax)
ax.legend(loc="lower left", fontsize=11.5, handlelength=2.4)
ax.set_title("低频渐近线的延长线共过 (1, 20lg K)，与 0 dB 线的交点 ω0 = K^(1/ν)\n"
             "Ⅰ 型 ω0 = K，Ⅱ 型 ω0 = √K（此图取 K = 10，即 20 dB）",
             fontsize=12.5, color=fs.INK, pad=10, family=FAM)

fig.text(0.5, 0.015,
         "方法一 任取 ω 算高度 La = 20lg K - 20ν·lg ω  ·  方法二 取 ω = 1 读 20lg K  ·  "
         "方法三 令 La = 0 反解 ω0 = K^(1/ν)\n"
         "低频频段（ω < ωmin，即所有交接频率之前）才有这条唯一的直线段，"
         "过了第一个交接频率斜率就要折",
         ha="center", va="bottom", fontsize=10.5, color=fs.SUB,
         family=FAM, linespacing=1.7)

fig.subplots_adjust(left=0.10, right=0.975, top=0.855, bottom=0.245)
fs.save(fig, "频域-反求-低频延长线与ω0.png")
