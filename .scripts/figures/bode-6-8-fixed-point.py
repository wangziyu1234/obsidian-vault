# figure: 频域-例68定点法对照.png
r"""6-8 定点图解：为什么 wC = wc0^2/wA 在这道题不能用。

上栏：L0 与两组校正后曲线（原答案 aT=0.5 / 精确式 aT=0.716），标出各自 0dB 穿越。
下栏：把公式口径的 -40dB/dec 假设（过 (wc0,0) 的虚线）画在真实 L0 上，
      直观看出 wA=5 处公式只认 -7.96dB、真实是 -11.14dB，缺 3.18dB。

排版注意（实测，本脚本已按此写）：
  * 图内中文一律写成 `$\mathrm{汉字}$`，**整串以 `$` 开头**（先数学后中文）；
    图例的旧写法 `r"$L_0$ 被校对象"` 会让整串走 mathtext 的默认字体，汉字变方框。
  * 标点（：，）留在 `$\mathrm{}$` 段外，段内写全角标点会报 no glyph for U+FF1A/U+FF0C。
  * 带白底 bbox 的标注不许压曲线：落点先跑 `_probe_layout.py` 量数据坐标，
    不够放就挪到曲线够不到的空区再拉引线（arrowstyle="-"）。
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs

fs.use_style()

MAG = fs.MAG
PHA = fs.PHA
SUB = fs.SUB
INK = fs.INK
GRN = "#1B7F4B"
GLD = "#8A6508"

wc0 = np.sqrt(10.0)


def L0(w):
    """被校对象 10/[s(s+1)(0.2s+1)]，dB。"""
    return 20 * np.log10(10.0 / (w * np.sqrt(1 + w ** 2) * np.sqrt(1 + (0.2 * w) ** 2)))


def L1(w, aT, T):
    """校正后开环，dB。"""
    return L0(w) + 20 * np.log10(np.sqrt(1 + (aT * w) ** 2) / np.sqrt(1 + (T * w) ** 2))


w = np.logspace(np.log10(0.1), np.log10(100), 3000)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 7.6), sharex=True)

# ---------------- 上栏 ----------------
ax1.axhline(0, color=INK, linewidth=1.0)
ax1.plot(w, L0(w), color=MAG, linewidth=2.2, label=r"$\mathrm{被校对象}\ L_0$")
ax1.plot(w, L1(w, 0.5, 0.1), color=PHA, linewidth=1.9, linestyle=(0, (5, 3)),
         label=r"$\mathrm{原答案}\ aT=0.5$")
ax1.plot(w, L1(w, 0.716, 0.05), color=GRN, linewidth=2.1,
         label=r"$\mathrm{精确式}\ aT=0.716$")

for xb in (1.0,):
    ax1.axvline(xb, color=SUB, linewidth=0.8, linestyle=(0, (2, 4)))
ax1.axvline(3.96, color=PHA, linewidth=1.2, linestyle=(0, (5, 3)))
ax1.axvline(5.0, color=GRN, linewidth=1.2)

# 两条穿越说明放左上空白区（并排两行），曲线在 y>20 的区域够不到；
# 读数靠对应颜色的竖线，不再拉引线（避免标注框被引线穿进）。
ax1.text(0.115, 31.0, r"$\mathrm{原答案实际穿越}\ \omega_{\mathrm{c}}=3.96$",
         fontsize=11.5, color=PHA, va="center")
ax1.text(0.115, 24.0, r"$\mathrm{精确式穿越}\ \omega_{\mathrm{c}}=5.00$",
         fontsize=11.5, color=GRN, va="center")
ax1.text(0.115, 17.0, r"$\mathrm{虚线竖线}=1$", fontsize=11.5, color=SUB, va="center")

ax1.set_ylabel(r"$L(\omega)$ / dB")
ax1.set_ylim(-40, 40)
ax1.set_yticks([-40, -20, 0, 20, 40])
fs.tidy(ax1, turn_freqs=())
ax1.legend(loc="lower left", fontsize=10.5, frameon=True, facecolor="white",
           edgecolor=SUB, framealpha=1.0)
# ω_c0 的竖线本身就是网格刻度，直接写在刻度旁，不拉引线
ax1.text(wc0 * 1.12, 1.2, r"$\omega_{\mathrm{c0}}=\sqrt{10}$", fontsize=11.5,
         color=SUB, ha="left", va="bottom")

# ---------------- 下栏 ----------------
ax2.axhline(0, color=INK, linewidth=1.0)
ax2.plot(w, L0(w), color=MAG, linewidth=2.2)

# 公式假设的 -40dB/dec 段：过 (wc0,0)，到 wA=5 高度 -7.96dB
wa = np.logspace(np.log10(wc0), np.log10(5.0), 50)
ax2.plot(wa, -40 * np.log10(wa / wc0), color=GLD, linewidth=2.0, linestyle=(0, (4, 3)))
ax2.annotate(r"$\mathrm{公式假设的}\ -40\,\mathrm{dB/dec}\ \mathrm{段}$", xy=(3.1, 0.1),
             xytext=(0.115, 26.0), fontsize=11.5, color=GLD, va="center",
             arrowprops=dict(arrowstyle="-", color=GLD, linewidth=0.9))
ax2.annotate(r"$\mathrm{真实}\ L_0\ \mathrm{在}\ 3.16\sim5\ \mathrm{只走}\ -20\,\mathrm{dB/dec}$",
             xy=(4.0, -11.5), xytext=(0.115, -31.0), fontsize=11.5, color=MAG, va="center",
             arrowprops=dict(arrowstyle="-", color=MAG, linewidth=0.9))

ax2.plot([5, 5], [L0(5.0), -40 * np.log10(5.0 / wc0)], color=INK, linewidth=1.4)
ax2.plot([5], [L0(5.0)], marker="o", markersize=5.5, color=INK)
ax2.plot([5], [-40 * np.log10(5.0 / wc0)], marker="o", markersize=5.5, color=GLD)
ax2.annotate(r"$\mathrm{公式认的深度}\ -7.96\ \mathrm{dB}$", xy=(5.25, -7.96),
             xytext=(0.115, 6.0), fontsize=11.5, color=GLD, va="center",
             arrowprops=dict(arrowstyle="-", color=GLD, linewidth=0.9))
ax2.annotate(r"$\mathrm{真实深度}\ -11.14\ \mathrm{dB}$", xy=(5.25, -11.14),
             xytext=(0.115, -20.5), fontsize=11.5, color=INK, va="center",
             arrowprops=dict(arrowstyle="-", color=INK, linewidth=0.9))
ax2.annotate(r"$\mathrm{差}\ 3.18\ \mathrm{dB}$", xy=(5.45, -12.0), xytext=(6.6, -18.8),
             fontsize=11.5, color=INK, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=INK, linewidth=0.9))

ax2.set_ylabel(r"$L(\omega)$ / dB")
ax2.set_xlabel(r"$\omega$ / (rad/s)")
ax2.set_ylim(-40, 40)
ax2.set_yticks([-40, -20, 0, 20, 40])
fs.tidy(ax2, turn_freqs=(1.0, 5.0))

for ax in (ax1, ax2):
    ax.set_xscale("log")
    ax.set_xlim(0.1, 100)
    ax.set_xticks([0.1, 0.5, 1, 2, 5, 10, 20, 50, 100])
    ax.set_xticklabels(["0.1", "0.5", "1", "2", "5", "10", "20", "50", "100"])
    ax.minorticks_off()

fig.subplots_adjust(left=0.10, right=0.975, top=0.975, bottom=0.085, hspace=0.10)
fs.save(fig, "频域-例68定点法对照.png")
