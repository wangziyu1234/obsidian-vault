# figure: 频域-一阶低通Bode.png
# -*- coding: utf-8 -*-
"""一阶低通 G(s)=1/(Ts+1) 的伯德图（自控 05-1-2 惯性环节示例）。

构建：..\\build.ps1 -File .\\bode-first-order.py
说明：曲线数据全部由 control 库算，改 T 即可换转折频率；
      网格/配色/字体由 figures_style 统一，不要在脚本里另设。
"""
import numpy as np
import control as ct

import figures_style as fs

fs.use_style()

T = 0.5                                  # 时间常数，转折频率 1/T = 2 rad/s
sys = ct.tf([1], [T, 1])

fig, (ax_mag, ax_pha) = fs.new_bode_axes()

# 由库算幅值/相位，自己画线，便于完全控制线型与图例
w = np.logspace(-1, 2, 800)
resp = ct.frequency_response(sys, w)
mag_db = 20 * np.log10(np.abs(resp.fresp[0, 0, :]))
phase_deg = np.degrees(np.unwrap(np.angle(resp.fresp[0, 0, :])))

ax_mag.semilogx(w, mag_db, color=fs.MAG, linewidth=1.9, label=r"$L(\omega)$")
ax_pha.semilogx(w, phase_deg, color=fs.PHA, linewidth=1.9, label=r"$\varphi(\omega)$")

for ax in (ax_mag, ax_pha):
    fs.tidy(ax, turn_freqs=[1 / T])

# 转折频率处 -3 dB / -45° 的标注
ax_mag.plot([1 / T], [-3], "o", color=fs.MAG, markersize=5)
ax_mag.annotate(r"$-3$ dB @ $\omega=1/T$", xy=(1 / T, -3),
                xytext=(0.16, 0.22), textcoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color=fs.SUB, linewidth=1.0),
                color=fs.SUB, fontsize=12)
ax_pha.plot([1 / T], [-45], "o", color=fs.PHA, markersize=5)

ax_mag.legend(loc="lower left")
ax_pha.legend(loc="lower left")

fig.tight_layout()
fs.save(fig, "频域-一阶低通Bode.png")
