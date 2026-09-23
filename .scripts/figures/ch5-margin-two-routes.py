# figure: 自控-频域-裕度两法对照.png
"""稳定裕度两条算法路线对照：精确幅值方程 vs 渐近线读数。

以课件 §5.5 例4 的 G = 100/[s(s+2)(s+10)] 为例（例5.17 同型）：
  * 精确解  A(w)=1  ->  u^3+104u^2+400u-10000=0, u=w^2 -> wc = 2.7992, gamma = 19.91°
  * 渐近线  2<w<10 段 L_a = 20lg(200/w^2) 过 0 dB -> wc = sqrt(10) = 3.1623, gamma = 14.79°
渐近线把 wc 高估、gamma 低估约 5°。图内所有标注值都由断言逐点核对。

Build: .\\build.ps1 -File .\\ch5-margin-two-routes.py
"""
from __future__ import annotations

import numpy as np
import control as ct

import figures_style as fs
import matplotlib.pyplot as plt

NUM, DEN = [100.0], [1.0, 12.0, 20.0, 0.0]
W_TURN1, W_TURN2 = 2.0, 10.0


def exact_wc() -> float:
    """解 u^3+104u^2+400u-10000=0 的正实根，u=w^2。"""
    roots = np.roots([1.0, 104.0, 400.0, -10000.0])
    real_pos = [r.real for r in roots if abs(r.imag) < 1e-9 and r.real > 0]
    assert len(real_pos) == 1, real_pos
    return float(np.sqrt(real_pos[0]))


def mag_db_exact(w: np.ndarray) -> np.ndarray:
    return 20 * np.log10(np.abs(np.polyval(NUM, 1j * w) / np.polyval(DEN, 1j * w)))


def mag_db_asymp(w: np.ndarray) -> np.ndarray:
    """渐近折线（Bode 形式 K=5）：<=2 段 -20，2~10 段 -40，>=10 段 -60。"""
    w = np.asarray(w, dtype=float)
    la = 20 * np.log10(5.0 / w)
    la = np.where(w > W_TURN1, la - 20 * np.log10(w / W_TURN1), la)
    la = np.where(w > W_TURN2, la - 20 * np.log10(w / W_TURN2), la)
    return la


def phase_deg(w: np.ndarray) -> np.ndarray:
    return -90.0 - np.degrees(np.arctan(w / 2.0)) - np.degrees(np.arctan(w / 10.0))


def verify() -> tuple[float, float, float, float]:
    wc = exact_wc()
    assert abs(wc - 2.7992) < 1e-3, wc
    a_wc = abs(np.polyval(NUM, 1j * wc) / np.polyval(DEN, 1j * wc))
    assert abs(a_wc - 1.0) < 1e-6, a_wc
    # 渐近线 0 dB 交越：2<w<10 段 L_a=20lg(10/w^2)=0 -> w=sqrt(10)
    wa = np.sqrt(10.0)
    assert abs(20 * np.log10(10.0 / wa**2)) < 1e-9
    assert abs(mag_db_asymp(np.array([wa]))[0]) < 1e-9
    # 相角裕度两条
    g_exact = 180.0 + phase_deg(np.array([wc]))[0]
    g_asymp = 180.0 + phase_deg(np.array([wa]))[0]
    assert abs(g_exact - 19.908) < 0.01, g_exact
    assert abs(g_asymp - 14.763) < 0.01, g_asymp
    # control 独立复核：wc、gamma、wx、h
    gm, pm, wx, wc2 = ct.margin(ct.tf(NUM, DEN))
    assert abs(wc2 - wc) < 1e-3 and abs(pm - g_exact) < 1e-2, (wc2, pm)
    assert abs(wx - np.sqrt(20.0)) < 1e-3 and abs(gm - 2.4) < 1e-3, (wx, gm)
    print(f"verified: wc={wc:.4f} gamma={g_exact:.2f}° | 渐近 wc={wa:.4f} "
          f"gamma={g_asymp:.2f}° | wx={wx:.4f} h={gm:.4f}")
    return wc, wa, g_exact, g_asymp


def draw(wc: float, wa: float, g_exact: float, g_asymp: float) -> None:
    fs.use_style()
    w = np.geomspace(0.5, 40, 2000)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True)
    fig.suptitle("裕度两法对照：G = 100/[s(s+2)(s+10)]，精确 vs 渐近线", fontsize=14, y=0.98)

    # --- 幅频 ---
    ax1.semilogx(w, mag_db_exact(w), color=fs.MAG, lw=2.2, zorder=3,
                 label="精确 L(ω)")
    ax1.semilogx(w, mag_db_asymp(w), color=fs.SUB, lw=1.4, ls=(0, (5, 3)), zorder=2,
                 label="渐近折线")
    ax1.axhline(0, color=fs.INK, lw=0.9, zorder=1)
    for x, txt, dy in ((wc, "精确 ωc = 2.80", 26), (wa, "渐近 ωc = √10 ≈ 3.16", -52)):
        ax1.axvline(x, color=fs.PHA if x == wc else fs.SUB, lw=1.1,
                    ls=(0, (4, 3)), zorder=1)
        ax1.annotate(txt, xy=(x, 0), xytext=(4, dy), textcoords="offset points",
                     fontsize=11, color=fs.PHA if x == wc else fs.SUB)
    fs.tidy(ax1, turn_freqs=(W_TURN1, W_TURN2))
    ax1.set_ylim(-45, 45)
    ax1.legend(loc="upper right", fontsize=11)

    # --- 相频 ---
    ph = phase_deg(w)
    ax2.semilogx(w, ph, color=fs.PHA, lw=2.2, zorder=3)
    ax2.axhline(-180, color=fs.INK, lw=0.9, ls=(0, (5, 3)), zorder=2)
    for x, g, lab in ((wc, g_exact, "γ = 19.9°"), (wa, g_asymp, "γ = 14.8°")):
        y = -180.0 + g
        ax2.plot([x], [y], "o", ms=6, color=fs.INK, zorder=5)
        ax2.annotate(lab, xy=(x, y), xytext=(10, 16 if x == wc else -38),
                     textcoords="offset points", fontsize=11, color=fs.INK,
                     arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8))
    fs.tidy(ax2, turn_freqs=(W_TURN1, W_TURN2))
    ax2.set_ylim(-262, -85)
    ax2.set_yticks([-90, -135, -180, -225])

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fs.save(fig, "自控-频域-裕度两法对照.png")


if __name__ == "__main__":
    draw(*verify())
