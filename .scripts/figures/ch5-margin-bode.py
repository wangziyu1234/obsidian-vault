# figure: 频域-稳定裕度.png
"""伯德图上的稳定裕度（重绘）。

标注口径与笔记正文一致：穿越频率写 ωx（课本口径，不写 ω_g），
参考线写 0 dB（不写 L = 0）；系统与 频域-稳定裕度-奈氏图.png 相同。
  * wc = 1.2437（幅频过 0 dB）      -> gamma = 180° + φ(wc) = 31.71°
  * wx = √10 = 3.1623（相频交 -180°）-> h(dB) = -20lg|G(jwx)| = 14.807 dB
两种图上四个量完全相同，只是读的位置不同。图内标注值全部断言核对。

Build: ..\\build.ps1 -File .\\ch5-margin-bode.py
"""
from __future__ import annotations

import numpy as np

import control as ct
import matplotlib.pyplot as plt

import figures_style as fs

NUM, DEN = [2.0], [0.1, 1.1, 1.0, 0.0]
SYS = ct.tf(NUM, DEN)


def mag_db(w) -> np.ndarray:
    w = np.atleast_1d(np.asarray(w, dtype=float))
    return 20 * np.log10(np.abs(np.polyval(NUM, 1j * w) / np.polyval(DEN, 1j * w)))


def phase_deg(w) -> np.ndarray:
    w = np.atleast_1d(np.asarray(w, dtype=float))
    return -90.0 - np.degrees(np.arctan(w)) - np.degrees(np.arctan(0.1 * w))


def verify():
    gm, pm, wx, wc = ct.margin(SYS)
    assert abs(wc - 1.2437) < 1e-3 and abs(pm - 31.71) < 0.01, (wc, pm)
    assert abs(wx - np.sqrt(10.0)) < 1e-6, wx
    h_db = 20.0 * np.log10(gm)
    assert abs(h_db - 14.807) < 0.01, h_db
    assert abs(mag_db(wc)[0]) < 1e-9, mag_db(wc)[0]           # ωc 处幅值过 0 dB
    assert abs(phase_deg(wx)[0] + 180.0) < 1e-9                # ωx 处相角为 -180°
    assert abs(180.0 + phase_deg(wc)[0] - pm) < 1e-6
    assert abs(mag_db(wx)[0] + h_db) < 1e-9
    print(f"verified: wc={wc:.4f} γ={pm:.2f}° | wx={wx:.4f} "
          f"L(wx)={mag_db(wx)[0]:.3f} dB -> h(dB)={h_db:.3f} dB")
    return wc, pm, wx, h_db


def draw(wc, gamma, wx, h_db):
    fs.use_style()
    w = np.geomspace(0.08, 120.0, 4000)

    fig, (ax1, ax2) = fs.new_bode_axes(figsize=(7.4, 6.4))
    fig.suptitle("伯德图上的稳定裕度（与奈氏图同一系统）", fontsize=14, y=0.975)
    ax1.set_title(r"$G(s)=\frac{2}{s(s+1)(0.1s+1)}$", fontsize=14, pad=8)

    # --- 幅频：ωc 过 0 dB，h(dB) 是 ωx 处到 0 dB 线的距离 ---
    ax1.semilogx(w, mag_db(w), color=fs.MAG, lw=2.2, zorder=3)
    ax1.axhline(0.0, color=fs.INK, lw=0.9, zorder=1)
    for x, lab, col in ((wc, f"ωc = {wc:.2f}", fs.PHA),
                        (wx, f"ωx = {wx:.2f}", fs.SUB)):
        ax1.axvline(x, color=col, lw=1.1, ls=(0, (4, 3)), zorder=1)
        ax1.annotate(lab, xy=(x, 0.0), xytext=(6, 14), textcoords="offset points",
                     fontsize=11, color=col, zorder=6)
    ax1.annotate("", xy=(wx, 0.0), xytext=(wx, -h_db),
                 arrowprops=dict(arrowstyle="<->", color=fs.PHA, lw=1.6))
    ax1.annotate(f"h(dB) = {h_db:.1f} dB", xy=(wx, -0.5 * h_db), xytext=(10, -4),
                 textcoords="offset points", fontsize=11, color=fs.PHA, zorder=6)
    ax1.annotate("0 dB", xy=(0.015, 0.0), xycoords=("axes fraction", "data"),
                 xytext=(0, 5), textcoords="offset points", fontsize=11,
                 color=fs.INK, zorder=6)
    fs.tidy(ax1)
    ax1.set_ylim(-62.0, 42.0)
    ax1.set_yticks([-60, -40, -20, 0, 20, 40])

    # --- 相频：ωx 交 -180°，γ 是 ωc 处到 -180° 线的距离 ---
    ax2.semilogx(w, phase_deg(w), color=fs.PHA, lw=2.2, zorder=3)
    ax2.axhline(-180.0, color=fs.INK, lw=0.9, ls=(0, (5, 3)), zorder=2)
    for x, col in ((wc, fs.PHA), (wx, fs.SUB)):
        ax2.axvline(x, color=col, lw=1.1, ls=(0, (4, 3)), zorder=1)
    ax2.plot([wc], [-180.0 + gamma], "o", ms=6.0, color=fs.INK, zorder=5)
    ax2.plot([wx], [-180.0], "o", ms=6.0, color=fs.INK, zorder=5)
    ax2.annotate("", xy=(wc, -180.0), xytext=(wc, -180.0 + gamma),
                 arrowprops=dict(arrowstyle="<->", color=fs.PHA, lw=1.6, zorder=6))
    ax2.annotate(f"γ = {gamma:.1f}°", xy=(wc, -180.0 + 0.5 * gamma),
                 xytext=(-14, -4), textcoords="offset points", ha="right",
                 fontsize=11, color=fs.PHA, zorder=6)
    ax2.annotate("φ = −180°（临界相位）", xy=(0.015, -180.0),
                 xycoords=("axes fraction", "data"), xytext=(0, -18),
                 textcoords="offset points", fontsize=11, color=fs.INK, zorder=6)
    fs.tidy(ax2)
    ax2.set_ylim(-268.0, -86.0)
    ax2.set_yticks([-90, -135, -180, -225])

    fig.text(0.5, 0.018,
             "γ 在幅频过 0 dB 处量（相频到 −180° 的余量）；"
             "h 在相频交 −180° 处量（幅频到 0 dB 的余量）。",
             ha="center", va="bottom", fontsize=10, color=fs.SUB)
    fig.tight_layout(rect=(0.005, 0.055, 0.995, 0.945))
    fs.save(fig, "频域-稳定裕度.png")


if __name__ == "__main__":
    draw(*verify())
