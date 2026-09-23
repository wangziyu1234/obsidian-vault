# figure: 自控-频域-虚轴极点对判稳.png
"""虚轴极点对的对数判稳：相角在 w=5 处下跳 180°，补线带来一次负穿越。

以课件 §5.4.3 例2 的 G = 1000/[s(s^2+25)(0.2s+1)] 为例：
  * 开环极点 0、±j5、-5：P = 0，nu=1 补 90°，等幅振荡环节一对补 180°；
  * phi(5^-) = -135°，phi(5^+) = -315°：25-w^2 变号使相角下跳 180°，
    这条补线在 L(w)>0 段内自上而下穿过 -180°，是一次负穿越；
  * N = 0 - 1 = -1，Z = P - 2N = 2，闭环不稳定；
  * 劳斯/特征根复核 0.2s^4+s^3+5s^2+25s+1000=0 恰有 2 个右半平面根。

Build: .\\build.ps1 -File .\\ch5-imaginary-pole-pair.py
"""
from __future__ import annotations

import numpy as np
import control as ct

import figures_style as fs
import matplotlib.pyplot as plt

NUM = [1000.0]
DEN = [0.2, 1.0, 5.0, 25.0, 0.0]  # 0.2 s^4 + s^3 + 5 s^2 + 25 s
W_N = 5.0


def mag_db(w: np.ndarray) -> np.ndarray:
    """|G| 的 dB 值；w=5 处为 +inf（谐振尖峰）。"""
    w = np.asarray(w, dtype=float)
    a = np.abs(np.polyval(NUM, 1j * w) / np.polyval(DEN, 1j * w))
    return 20 * np.log10(np.where(a > 0, a, np.nan))


def phase_deg(w: np.ndarray) -> np.ndarray:
    """连续相角分支：w<5 为 -90-arctan(0.2w)，w>5 再减 180°。"""
    w = np.asarray(w, dtype=float)
    return np.where(w < W_N, -90.0 - np.degrees(np.arctan(0.2 * w)),
                    -270.0 - np.degrees(np.arctan(0.2 * w)))


def mag_db_asymp(w: np.ndarray) -> np.ndarray:
    """手绘渐近折线：K=40 低频 -20，转折都在 w=5（振荡对 -40 + 惯性 -20），此后 -80。"""
    w = np.asarray(w, dtype=float)
    la = 20 * np.log10(40.0 / w)
    return la - 60 * np.log10(np.maximum(1.0, w / W_N))


def verify() -> float:
    # 特征根复核：闭环 1+G=0 恰有 2 个右半平面根
    cl = np.roots([0.2, 1.0, 5.0, 25.0, 1000.0])
    n_rhp = int(np.sum(cl.real > 1e-9))
    assert n_rhp == 2, cl
    # 相角关键读数
    for w, val in ((W_N - 1e-6, -135.0), (W_N + 1e-6, -315.0), (1e6, -360.0)):
        got = phase_deg(np.array([w]))[0]
        assert abs(got - val) < 1e-3, (w, got, val)
    # 截止频率（w>5 段 |G|=1）
    wc = ct.margin(ct.tf(NUM, DEN))[3]
    assert abs(wc - 8.9287) < 1e-3, wc
    a_wc = abs(np.polyval(NUM, 1j * wc) / np.polyval(DEN, 1j * wc))
    assert abs(a_wc - 1.0) < 1e-6, a_wc
    # w=5 在 L>0 计数段内（|G(5-)| -> inf）
    assert mag_db(np.array([4.999]))[0] > 20
    # 渐近折线在 w=5 处的高度：20lg(40/5)=20lg8
    assert abs(mag_db_asymp(np.array([W_N]))[0] - 20 * np.log10(8.0)) < 1e-9
    print(f"verified: phi: -135/-315/-360, wc={wc:.4f}, 闭环右半平面根 {n_rhp} 个, Z=2")
    return wc


def draw(wc: float) -> None:
    fs.use_style()
    w_lo, w_hi = 0.1, 100.0
    w = np.geomspace(w_lo, w_hi, 4000)
    wn = np.array([W_N])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True)
    fig.suptitle("虚轴极点对判稳：G = 1000/[s(s²+25)(0.2s+1)]", fontsize=14, y=0.98)

    # --- 幅频：L>0 段着色 + 谐振尖峰 ---
    ax1.axvspan(w_lo, wc, color=fs.FILL, alpha=0.85, zorder=0)
    ax1.axhline(0, color=fs.INK, lw=0.9, zorder=2)
    ax1.semilogx(w, mag_db(w), color=fs.MAG, lw=2.2, zorder=3, label="真实 L(ω)")
    ax1.semilogx(w, mag_db_asymp(w), color=fs.SUB, lw=1.4, ls=(0, (5, 3)), zorder=2,
                 label="手绘渐近线")
    ax1.axvline(wc, color=fs.SUB, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax1.annotate("L > 0 段（计数有效）", xy=(0.11, 0.86), xycoords="axes fraction",
                 fontsize=11, color=fs.INK)
    ax1.annotate("ωc = 8.93", xy=(wc, 0), xytext=(14, -26),
                 textcoords="offset points", fontsize=11, color=fs.SUB)
    fs.tidy(ax1, turn_freqs=(W_N,))
    ax1.set_ylim(-40, 90)
    ax1.legend(loc="upper right", fontsize=11)

    # --- 相频：w=5 处下跳 180°（补线），穿过 -180° 一次 ---
    ax2.axvspan(w_lo, wc, color=fs.FILL, alpha=0.85, zorder=0)
    ax2.semilogx(w, phase_deg(w), color=fs.PHA, lw=2.2, zorder=3)
    # 补线：w=5 处 -135° -> -315° 的垂直虚线
    ax2.plot([W_N, W_N], [-135.0, -315.0], color=fs.INK, lw=1.6, ls=(0, (4, 3)), zorder=4)
    ax2.plot([W_N], [-180.0], "o", ms=7, color=fs.INK, zorder=6)
    ax2.annotate("补线下跳 180°\n自上而下穿 −180°：负穿越", xy=(W_N, -180.0),
                 xytext=(22, 46), textcoords="offset points", fontsize=11,
                 color=fs.INK, arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8))
    ax2.axhline(-180, color=fs.INK, lw=0.9, ls=(0, (5, 3)), zorder=2)
    for x, y, lab in ((1.4, -116, "−135°"), (7.2, -296, "−315°")):
        ax2.annotate(lab, xy=(x, y), fontsize=10, color=fs.SUB)
    fs.tidy(ax2, turn_freqs=(W_N,))
    ax2.set_ylim(-390, -60)
    ax2.set_yticks([-90, -180, -270, -360])
    ax2.set_xlabel(r"$\omega$ / (rad/s)")

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fs.save(fig, "自控-频域-虚轴极点对判稳.png")


if __name__ == "__main__":
    draw(verify())
