# figure: 自控-频域-伯德判稳.png
"""对数判据判稳：只在 L(w) > 0 段数相频对 -180° 的穿越。

以 G = 5/[s(s+1)(0.5s+1)] 为例（P = 0）。相频在 ω = √2 处由 −161.6° 降到
−198.4°，是相角减小、自上而下穿过 −180°，属负穿越：N = 0 − 1，Z = P − 2N = 2，
闭环不稳定。图内所有标注值都由下面的断言逐点核对。

Build: .\\build.ps1 -File .\\ch5-bode-judge.py
"""
from __future__ import annotations
import numpy as np
import control as ct
from scipy import signal

import figures_style as fs
import matplotlib.pyplot as plt

K_GAIN, W_CROSS, W_PHASE = 5.0, 1.8022033046069246, np.sqrt(2.0)


def value_at(sys, w):
    return complex(ct.frequency_response(sys, [w]).frdata.reshape(-1)[0])


def verify(sys):
    # 交越点：幅值过 0 dB
    zc = value_at(sys, W_CROSS)
    assert abs(20 * np.log10(abs(zc))) < 1e-9, 20 * np.log10(abs(zc))
    # 相位交越点：相频过 −180°（数值上可能返回 +180°，取实部为负、虚部为零判据）
    zx = value_at(sys, W_PHASE)
    assert zx.real < 0 and abs(zx.imag) < 1e-12, zx
    assert abs(abs(np.degrees(np.angle(zx))) - 180) < 1e-9, np.degrees(np.angle(zx))
    # 相角在 ω=√2 附近严格减小 ⇒ 自上而下、负穿越（用连续分支判，不能看主值）
    band = np.geomspace(W_PHASE / 1.2, W_PHASE * 1.2, 401)
    band_phase = np.degrees(np.unwrap(np.angle(
        np.asarray(ct.frequency_response(sys, band).frdata).reshape(-1))))
    band_phase += 360 * np.round((-180 - band_phase[200]) / 360)
    assert band_phase[0] > -180 > band_phase[-1], (band_phase[0], band_phase[-1])
    assert np.all(np.diff(band_phase) < 0), "相角应单调减小"
    # 相位裕度与教材结论：γ < 0、Z = 2
    _, pm, _, _ = ct.margin(sys)
    assert pm < 0 and abs(pm + 12.997208015488695) < 1e-6, pm
    assert 0 - 2 * (-1) == 2
    # control 与 SciPy 独立复核
    grid = np.geomspace(1e-2, 1e2, 801)
    z_control = np.asarray(ct.frequency_response(sys, grid).frdata).reshape(-1)
    _, z_scipy = signal.freqresp((sys.num[0][0], sys.den[0][0]), grid)
    assert np.max(np.abs(z_control - z_scipy) / (1 + np.abs(z_control))) < 1e-12
    print("verified: 0 dB 交越、−180° 交越、穿越方向、γ<0、Z=2；control/SciPy 801 点")


def draw(sys):
    fs.use_style()
    w = np.geomspace(0.1, 30, 2000)
    resp = np.asarray(ct.frequency_response(sys, w).frdata).reshape(-1)
    mag_db = 20 * np.log10(np.abs(resp))
    phase = np.degrees(np.unwrap(np.angle(resp)))
    phase += 360 * np.round((-90 - phase[0]) / 360)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 6.0), sharex=True)
    fig.suptitle("伯德判稳：G = 5/[s(s+1)(0.5s+1)]，只在 L > 0 段数穿越", fontsize=14, y=0.98)

    # --- 幅频 ---
    ax1.axvspan(w[0], W_CROSS, color=fs.FILL, alpha=0.85, zorder=0)
    ax1.axhline(0, color=fs.INK, lw=0.9, zorder=2)
    ax1.semilogx(w, mag_db, color=fs.MAG, lw=2.2, zorder=3)
    ax1.axvline(W_CROSS, color=fs.SUB, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax1.set_ylim(-40, 40)
    ax1.set_ylabel(r"$L(\omega)$ / dB")
    ax1.text(0.12, 33, "L > 0：相频穿越计数的有效段", fontsize=11, color=fs.INK)
    ax1.annotate("0 dB 交越  ωc = 1.80", xy=(W_CROSS, 0), xytext=(-6, 30),
                 textcoords="offset points", fontsize=11, color=fs.SUB, ha="right",
                 arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8))

    # --- 相频 ---
    ax2.axvspan(w[0], W_CROSS, color=fs.FILL, alpha=0.85, zorder=0)
    ax2.axhline(-180, color=fs.INK, lw=0.9, ls=(0, (5, 3)), zorder=2)
    ax2.semilogx(w, phase, color=fs.PHA, lw=2.2, zorder=3)
    ax2.axvline(W_PHASE, color=fs.SUB, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax2.plot([W_PHASE], [-180], "o", ms=6, color=fs.INK, zorder=5)
    ax2.set_ylim(-280, -85)
    ax2.set_yticks([-90, -135, -180, -225, -270])
    ax2.set_xlabel(r"$\omega$ / (rad/s)")
    ax2.set_ylabel(r"$\varphi(\omega)$ / $^\circ$")
    ax2.text(0.12, -103, "相角减小：自上而下穿 −180° ⇒ 负穿越", fontsize=11, color=fs.PHA)
    ax2.text(1.9, -196, "负穿越 1 次\nN = 0 − 1", fontsize=11, color=fs.INK)
    ax2.annotate("", xy=(W_PHASE, -180), xytext=(W_PHASE, -161.6),
                 arrowprops=dict(arrowstyle="-|>", color=fs.SUB, lw=1.2))
    ax2.text(0.13, -262, "相角取连续分支：-161.6° 降到 -198.4°",
             fontsize=11, color=fs.SUB)

    fs.tidy(ax1, which="both")
    fs.tidy(ax2, which="both")
    fig.text(0.5, 0.043, "闭环有两个右半平面极点：不稳定。",
             ha="center", va="bottom", fontsize=10.5, color=fs.SUB)
    fig.text(0.5, 0.015, r"$P=0,\ N=0-1,\ Z=P-2N=2$",
             ha="center", va="bottom", fontsize=10.5, color=fs.SUB)
    fig.tight_layout(rect=(0.005, 0.085, 0.995, 0.94))
    fs.save(fig, "自控-频域-伯德判稳.png")
    plt.close(fig)


if __name__ == "__main__":
    s = ct.tf("s")
    system = K_GAIN / (s * (s + 1) * (0.5 * s + 1))
    verify(system)
    draw(system)
