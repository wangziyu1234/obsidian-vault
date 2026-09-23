# figure: 自控-频域-例529-裕度.png
"""例5.29（课件 §5.5 例5）：真实曲线与手绘渐近线同图对照。

G = 6(s/2.5+1)/[s(s/2+1)(s/5+1)(s/12.5+1)]，转折频率 2、2.5、5、12.5，
斜率 -20 → -40 → -20 → -40 → -60。
  * 渐近折线（手绘）：2.5<w<5 段 L_a = 20lg(4.8/w) 过 0 dB -> wc = 4.8，gamma = 20.3°
  * 真实频响（精确）：wc = 3.8473，gamma = 29.77°，wx = 7.3814，h = 3.1249 (9.90 dB)
wc = 4.8 紧挨转折频率 5，渐近误差在该处最大，故 gamma 被低估近 9°。
图内所有标注值都由断言逐点核对。

Build: .\\build.ps1 -File .\\ch5-margin-example5.py
"""
from __future__ import annotations

import numpy as np
import control as ct

import figures_style as fs
import matplotlib.pyplot as plt

NUM = [2.4, 6.0]                      # 6(0.4s+1)
DEN = [0.008, 0.156, 0.78, 1.0, 0.0]  # s(0.5s+1)(0.2s+1)(0.08s+1)
CORNERS = (2.0, 2.5, 5.0, 12.5)


def mag_db_exact(w: np.ndarray) -> np.ndarray:
    return 20 * np.log10(np.abs(np.polyval(NUM, 1j * w) / np.polyval(DEN, 1j * w)))


def mag_db_asymp(w: np.ndarray) -> np.ndarray:
    """手绘渐近折线：积分 -20，极点 2/5/12.5 各 -20，零点 2.5 回升 +20。"""
    w = np.asarray(w, dtype=float)
    la = 20 * np.log10(6.0 / w)
    la = la - 20 * np.log10(np.maximum(1.0, w / 2.0))
    la = la + 20 * np.log10(np.maximum(1.0, w / 2.5))
    la = la - 20 * np.log10(np.maximum(1.0, w / 5.0))
    la = la - 20 * np.log10(np.maximum(1.0, w / 12.5))
    return la


def phase_deg(w: np.ndarray) -> np.ndarray:
    return (np.degrees(np.arctan(w / 2.5)) - 90.0
            - np.degrees(np.arctan(w / 2.0))
            - np.degrees(np.arctan(w / 5.0))
            - np.degrees(np.arctan(w / 12.5)))


def verify() -> tuple[float, float, float, float, float, float]:
    # 精确：control 给 wc / gamma / wx / h
    gm, pm, wx, wc = ct.margin(ct.tf(NUM, DEN))
    assert abs(wc - 3.8473) < 1e-3, wc
    assert abs(pm - 29.767) < 0.01, pm
    assert abs(wx - 7.3814) < 1e-3, wx
    assert abs(gm - 3.1249) < 1e-3, gm
    assert abs(20 * np.log10(gm) - 9.899) < 0.01
    # 渐近：2.5<w<5 段 L_a = 20lg(4.8/w)，0 dB 交越在 4.8
    wa = 4.8
    assert abs(mag_db_asymp(np.array([wa]))[0]) < 1e-6, mag_db_asymp(np.array([wa]))[0]
    assert abs(180.0 + phase_deg(np.array([wa]))[0] - 20.26) < 0.02
    # wx 的四次方程：u^2 - 48.75u - 312.5 = 0，u = w^2（课件印 49.75 系笔误）
    u = np.roots([1.0, -48.75, -312.5])
    u = [float(r.real) for r in u if abs(r.imag) < 1e-9 and r.real > 0][0]
    assert abs(np.sqrt(u) - wx) < 1e-3, (u, wx)
    assert abs(phase_deg(np.array([wx]))[0] + 180.0) < 1e-6
    # 渐近 wc > 精确 wc：gamma 被低估
    assert wa > wc and (180.0 + phase_deg(np.array([wa]))[0]) < pm
    print(f"verified: 精确 wc={wc:.4f} gamma={pm:.2f}° wx={wx:.4f} h={gm:.4f} | "
          f"渐近 wc={wa} gamma={180 + phase_deg(np.array([wa]))[0]:.2f}°")
    return wc, wa, pm, 180.0 + phase_deg(np.array([wa]))[0], wx, gm


def draw(wc, wa, g_ex, g_as, wx, h) -> None:
    fs.use_style()
    w = np.geomspace(0.4, 60, 3000)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True)
    fig.suptitle("例5.29：真实频响与手绘渐近线 G = 6(0.4s+1)/[s(0.5s+1)(0.2s+1)(0.08s+1)]",
                 fontsize=13, y=0.98)

    # --- 幅频：真实 + 手绘渐近线 ---
    ax1.semilogx(w, mag_db_exact(w), color=fs.MAG, lw=2.2, zorder=3, label="真实 L(ω)")
    ax1.semilogx(w, mag_db_asymp(w), color=fs.SUB, lw=1.4, ls=(0, (5, 3)), zorder=2,
                 label="手绘渐近线")
    ax1.axhline(0, color=fs.INK, lw=0.9, zorder=1)
    for x, txt, dy in ((wc, "精确 ωc = 3.85", 22), (wa, "渐近 ωc = 4.8", -40)):
        ax1.axvline(x, color=fs.PHA if x == wc else fs.SUB, lw=1.1, ls=(0, (4, 3)), zorder=1)
        ax1.annotate(txt, xy=(x, 0), xytext=(4, dy), textcoords="offset points",
                     fontsize=11, color=fs.PHA if x == wc else fs.SUB)
    fs.tidy(ax1, turn_freqs=CORNERS)
    ax1.set_ylim(-40, 40)
    ax1.legend(loc="upper right", fontsize=11)

    # --- 相频：两个 wc 处的 gamma + wx ---
    ph = phase_deg(w)
    ax2.semilogx(w, ph, color=fs.PHA, lw=2.2, zorder=3)
    ax2.axhline(-180, color=fs.INK, lw=0.9, ls=(0, (5, 3)), zorder=2)
    for x, g, lab in ((wc, g_ex, "γ = 29.8°"), (wa, g_as, "γ = 20.3°")):
        y = -180.0 + g
        ax2.plot([x], [y], "o", ms=6, color=fs.INK, zorder=5)
        ax2.annotate(lab, xy=(x, y), xytext=(10, 16 if x == wc else -38),
                     textcoords="offset points", fontsize=11, color=fs.INK,
                     arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8))
    ax2.plot([wx], [-180.0], "o", ms=7, color=fs.INK, zorder=5)
    ax2.axvline(wx, color=fs.SUB, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax2.annotate("ωx = 7.38，h = 3.12", xy=(wx, -180.0), xytext=(14, 26),
                 textcoords="offset points", fontsize=11, color=fs.INK,
                 arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8))
    fs.tidy(ax2, turn_freqs=CORNERS)
    ax2.set_ylim(-250, -60)
    ax2.set_yticks([-90, -135, -180, -225])
    ax2.set_xlabel("ω / (rad/s)")

    fig.tight_layout(rect=(0, 0, 1, 0.955))
    fs.save(fig, "自控-频域-例529-裕度.png")


if __name__ == "__main__":
    draw(*verify())
