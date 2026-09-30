# -*- coding: utf-8 -*-
# figure: 高数-三角不等式曲线比较.png
"""高数《附录 三角与代数补充》——三角不等式配图（曲线版）。

左：y=sin x、y=cos x、y=x、y=tan x 四条常用曲线同框，阴影标出不等式
    sin x < x < tan x 成立的区间 (0, π/2)，红点处画一条读数竖线；
右：商形式的夹逼 cos x < sin x/x < 1（0<x<π）。

构建：..\build.ps1 -File .\trig-inequality-curves.py
"""
import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

PI = np.pi


def main() -> None:
    fs.use_style()
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.6, 4.2))
    # 双面板不用 tight_layout（会静默拒绝执行），显式排版
    fig.subplots_adjust(left=0.062, right=0.985, top=0.885, bottom=0.125, wspace=0.19)

    # ================= 左：sin x / cos x / x / tan x =================
    x = np.linspace(-PI / 2 + 1e-4, PI / 2 - 1e-4, 4001)
    # 不等式成立的区间（画在底层当背景）
    axL.axvspan(0, PI / 2, color=fs.FILL, zorder=0)
    # 渐近线
    for xa in (-PI / 2, PI / 2):
        axL.axvline(xa, color=fs.SUB, linewidth=1.0, linestyle=(0, (4, 3)), zorder=1)

    # 绘制顺序 = 图例顺序：sin / cos / x / tan（zorder 各自显式给出，不受顺序影响）
    axL.plot(x, np.sin(x), color=fs.MAG, linewidth=1.9, zorder=3, label=r"$y=\sin x$")
    axL.plot(x, np.cos(x), color=fs.SUB, linewidth=1.5, zorder=2, label=r"$y=\cos x$")
    axL.plot(x, x, color=fs.INK, linewidth=1.8, zorder=4, label=r"$y=x$")
    axL.plot(x, np.tan(x), color=fs.PHA, linewidth=1.9, zorder=3, label=r"$y=\tan x$")

    # 读数竖线：x=1.2 处四条曲线的上下次序 cos < sin < x < tan
    x0 = 1.2
    y_dots = [np.cos(x0), np.sin(x0), x0, np.tan(x0)]
    axL.plot([x0, x0], [y_dots[0], y_dots[-1]], color=fs.SUB, linewidth=0.8,
             linestyle=":", zorder=5)
    axL.plot([x0] * 4, y_dots, linestyle="none", marker="o", markersize=5.0,
             markeredgecolor="white", markeredgewidth=0.8,
             color=fs.PHA, zorder=6)

    axL.set_xlim(-1.72, 1.72)
    axL.set_ylim(-3.0, 3.1)
    axL.set_xticks([-PI / 2, 0, PI / 2])
    axL.set_xticklabels([r"$-\frac{\pi}{2}$", r"$0$", r"$\frac{\pi}{2}$"])
    axL.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    axL.set_title("三角函数与 y=x 同框")
    # 图例右移，让开 x=-π/2 那条虚线；说明文字右端收到 1.42，避开 x=π/2 虚线
    axL.legend(loc="upper left", bbox_to_anchor=(0.09, 1.0), borderaxespad=0.0,
               handlelength=1.6, labelspacing=0.35)
    # 中文标点必须包进 \mathrm{}（mathtext.rm 指向 Microsoft YaHei），且整串先数学后中文：
    # 写成 "$…$：$…$" 时冒号落在 mathtext 之外，会退化成 dummy symbol（实测）
    axL.text(1.42, -2.45, r"$0<x<\frac{\pi}{2}\mathrm{：}\sin x<x<\tan x$",
             ha="right", va="center", color=fs.INK,
             bbox=dict(facecolor="white", edgecolor="none", pad=2.5), zorder=7)
    fs.tidy(axL)

    # ================= 右：cos x < sin x / x < 1 =================
    xr = np.linspace(1e-3, PI, 3001)
    sinc = np.sin(xr) / xr
    axR.fill_between(xr, np.cos(xr), 1.0, where=xr <= PI / 2,
                     color=fs.FILL, zorder=0)
    axR.axvline(PI / 2, color=fs.SUB, linewidth=1.0, linestyle=(0, (4, 3)), zorder=1)
    axR.axhline(1.0, color=fs.SUB, linewidth=1.0, linestyle=(0, (4, 3)), zorder=1,
                label=r"$1$")
    axR.plot(xr, np.cos(xr), color=fs.PHA, linewidth=1.9, zorder=3,
             label=r"$\cos x$")
    axR.plot(xr, sinc, color=fs.MAG, linewidth=1.9, zorder=3,
             label=r"$\dfrac{\sin x}{x}$")

    axR.set_xlim(0, 3.35)
    axR.set_ylim(-1.15, 1.35)
    axR.set_xticks([0, PI / 2, PI])
    axR.set_xticklabels([r"$0$", r"$\frac{\pi}{2}$", r"$\pi$"])
    axR.set_yticks([-1, -0.5, 0, 0.5, 1])
    axR.set_title("商形式的夹逼")
    axR.legend(loc="lower left", handlelength=1.6, labelspacing=0.35, borderaxespad=0.3)
    axR.text(3.28, 0.60, r"$\cos x<\dfrac{\sin x}{x}<1$",
             ha="right", va="center", color=fs.INK,
             bbox=dict(facecolor="white", edgecolor="none", pad=2.5), zorder=7)
    fs.tidy(axR)

    fs.save(fig, "高数-三角不等式曲线比较.png")


if __name__ == "__main__":
    main()
