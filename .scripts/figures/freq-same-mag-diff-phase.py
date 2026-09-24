# figure: 频域-幅频相同相频不同.png
"""课件 §5.3.4 的四行表：同一张 L(ω)，四条不同的 φ(ω)。

Ⅰ 型、一个零点、一个极点，零点与极点各自可以落在左半平面（首一形 (s/ω+1)）
或右半平面（(s/ω-1)）。四种组合的 |G| 完全相同，只差 K_v 的一个符号，
而符号只进相频——所以由 L(ω) 不能唯一确定 G(s)。
"""
import numpy as np

import figures_style as fs

fs.use_style()
import matplotlib.pyplot as plt

K = 1.0
WZ, WP = 2.0, 5.0          # 零点、极点转折频率
w = np.logspace(-1.5, 2.2, 2000)

# 图内中文与 $…$ 不能混在一条字符串里（mathtext 会接管整串、中文掉字形），
# 所以汉字一律包进 \mathrm{}。第 4 行按课件口径把 +90°→+270° 写成 −270°→−90°；
# 起止值直接标理论极限（采样区间够宽，误差 <1°）。
CASES = [
    (r"$\mathrm{零点}\,+\mathrm{、极点}\,+$",  1.0,  1.0, fs.MAG, 0.0,
     r"-90^\circ\to-90^\circ"),
    (r"$\mathrm{零点}\,-\mathrm{、极点}\,+$", -1.0,  1.0, fs.PHA, 0.0,
     r"+90^\circ\to-90^\circ"),
    (r"$\mathrm{零点}\,-\mathrm{、极点}\,-$", -1.0, -1.0, "#1F7A5A", 0.0,
     r"-90^\circ\to-90^\circ"),
    (r"$\mathrm{零点}\,+\mathrm{、极点}\,-$",  1.0, -1.0, "#8A5A1F", -360.0,
     r"-270^\circ\to-90^\circ"),
]


def response(sz, sp):
    num = K * (1j * w / WZ + sz)
    den = (1j * w) * (1j * w / WP + sp)
    return num / den


fig, (ax_mag, ax_ph) = fs.new_bode_axes(figsize=(7.4, 5.6))

ref = None
for label, sz, sp, color, offset, span in CASES:
    G = response(sz, sp)
    mag = 20 * np.log10(np.abs(G))
    if ref is None:
        ref = mag
        ax_mag.plot(w, mag, color=fs.MAG, linewidth=1.6)
    else:
        assert np.allclose(ref, mag, atol=1e-6), label
    phi = np.unwrap(np.angle(G)) * 180.0 / np.pi + offset
    ax_ph.plot(w, phi, color=color, linewidth=1.5, label=label + rf"$\ \ {span}$")

ax_mag.set_xscale("log")
ax_ph.set_xscale("log")
ax_mag.set_yticks([-40, -20, 0, 20])
ax_ph.set_yticks([90, 0, -90, -180, -270])
# 纵轴下界特意放宽到 -430：图例是 2 行、横跨全图，必须整个沉到最低那条
# 曲线（-270°）之下，否则图例框会把曲线咬掉一大段（上一版咬掉 618 个采样点）。
ax_ph.set_ylim(-430, 130)
ax_mag.set_xlim(w[0], w[-1])

ax_mag.text(
    0.03, 0.12, r"$\mathrm{四种情形的}\ L(\omega)\ \mathrm{完全重合}$",
    transform=ax_mag.transAxes, fontsize=12, color=fs.SUB,
)
fs.tidy(ax_mag, turn_freqs=(WZ, WP))
fs.tidy(ax_ph)                       # 相频图自己画转折线
for xf in (WZ, WP):                  # 竖线只画到曲线区（y≥-280），
    ax_ph.plot([xf, xf], [-280, 130],  # 不往下伸进图例带，否则图例框会压住它
               color=fs.SUB, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax_mag.set_xlabel("")
ax_ph.legend(loc="lower left", ncol=2, fontsize=9, handlelength=1.5,
             borderaxespad=0.4, labelspacing=0.35)

fs.save(fig, "频域-幅频相同相频不同.png")
