# figure: 频域-例527-稳态输出.png
"""例5.27（课件例7）：振荡环节的正弦稳态输出，输出幅值是输入的 3 倍、相位滞后 90°。

只有频率特性能一眼读出这两个数：幅值比 = |G(jω)|、相位差 = φ(ω)。
"""
import numpy as np

import figures_style as fs

fs.use_style()
import matplotlib.pyplot as plt

W = 10.0                  # 输入频率 ω = 2πf = 10 rad/s
GAIN = 3.0                # 稳态输出幅值 / 输入幅值
T = 2 * np.pi / W         # 周期
t = np.linspace(0, 2 * T, 2000)

r = np.sin(W * t)
c = GAIN * np.sin(W * t - np.pi / 2)

fig, ax = plt.subplots(figsize=(7.4, 3.6))

ax.plot(t, c, color=fs.PHA, linewidth=1.8, label=r"$\mathrm{稳态输出}\ c_s(t)$")
ax.plot(t, r, color=fs.MAG, linewidth=1.6, linestyle=(0, (5, 3)),
        label=r"$\mathrm{输入}\ r(t)$")
ax.axhline(0, color=fs.SUB, linewidth=0.8)

# 两个峰值之间正好差 T/4 —— 这就是“滞后 90°”
t_r = np.pi / (2 * W)
t_c = np.pi / (2 * W) + T / 4
ax.annotate(
    "", xy=(t_c, -1.9), xytext=(t_r, -1.9),
    arrowprops=dict(arrowstyle="<->", color=fs.INK, linewidth=1.0),
)
ax.text(
    (t_r + t_c) / 2, -2.5, r"$\Delta t=T/4\mathrm{，即滞后}\ 90^\circ$",
    ha="center", va="top", fontsize=11.5,
)
for x, y in ((t_r, 1.0), (t_c, 3.0)):
    ax.plot([x], [y], marker="o", markersize=4, color=fs.INK)
ax.vlines([t_r, t_c], 0, [1.0, 3.0], color=fs.INK, linewidth=0.7,
          linestyle=(0, (2, 2)))

ax.set_xlabel(r"$t$ / s")
ax.set_ylabel(r"$r,\ c_s$")
ax.set_ylim(-3.6, 3.9)
ax.set_yticks([-3, -1.5, 0, 1.5, 3])
ax.set_xlim(0, t[-1])
ax.grid(True, color=fs.GRID, linewidth=0.6, alpha=0.9)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.legend(loc="upper left", ncol=2, fontsize=11.5)

fig.tight_layout()
fs.save(fig, "频域-例527-稳态输出.png")
