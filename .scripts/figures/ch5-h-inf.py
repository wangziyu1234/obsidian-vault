# figure: 自控-频域-h无穷的判据.png
"""05-4-3 §5.4.7 配图：相频够不到 −180° ⟺ 无 ωx ⟺ h = ∞。

(a) 三种「够不到」的相频（都是最小相位、相角单调的标准形式）：
      一阶   G = 5/(0.5s+1)        φ: 0° → −90°
      I 型二阶 G = 5/[s(0.5s+1)]    φ: −90° → −180°（只在 ω→∞ 处逼近）
      0 型二阶 G = 5/(s²+0.6s+1)    φ: 0° → −180°（只在 ω→∞ 处逼近）
    三条都**没有有限交点**，$h=\\infty$。

(b) 两个反例（相角被零点或延迟破坏单调性）：
      最小相位带零点 G = (s+1)²/[s(s+0.01)²]（ν=1、n−m=1，比二阶还"轻"）
          —— 极点靠低频、零点靠高频，相角被凹到 −247°，两个交点
      含延迟         G = e^{−0.5s}/[s(s+1)]              —— 相角无下界，交点无穷多个
    有交点 ⟹ h 有限。

注意 (b) 里极点必须写成 (s+0.01)²，写成 (0.01s+1)² 就变成 ω=100 的极点了。

断言部分会自己复核：前三者 0 < ω < ∞ 上无 −180° 交点，后两者有。

图内文字一律「纯文本 + Unicode 数学」，不与 $…$ 混排（mathtext 接管整串会掉汉字字形）。

**标注位置**（2026-09-24 重排）：三条曲线在中频段（ω≈0.5~3）挤在一起，原来贴着曲线放的
三块白底标注全被曲线穿过（用户指出「遮挡还挺厉害的」）。现在改成：
  * (a) 三条曲线的说明收进**左下角图例**——那片区域（y < −190）没有任何曲线；
  * (b) 两块说明上移到 **φ > −90° 的空带**——两条曲线都从 −90° 往下走，永远不会进这条带；
  * 「−180° 线」标签放 (a) 栏左端线上方，(a) 栏左端只剩它，与图例上下错开。
改标注位置后务必跑 `_check_fig_layout.py`（已能查 [压线]）。

Build: ..\\build.ps1 -File .\\ch5-h-inf.py
"""
from __future__ import annotations

import numpy as np

import matplotlib.pyplot as plt
import control as ct

import figures_style as fs

GREEN = "#2F6B3A"
ORANGE = "#B4651A"
W = np.logspace(-3.2, 2.4, 4000)
LEVEL = -180.0


def phase_of(sys):
    _, ph, om = ct.frequency_response(sys, W)
    return om, np.degrees(np.unwrap(np.squeeze(np.asarray(ph))))


def delay_phase(om, tau=0.5):
    """e^{−τs}/[s(s+1)] 的精确相角（不用 Pade 近似）：−90° − arctan ω − τω(rad)。"""
    return -90.0 - np.degrees(np.arctan(om)) - np.degrees(tau * om)


def crosses(om, ph):
    d = ph - LEVEL
    return [float(om[i] * (om[i + 1] / om[i]) ** (-d[i] / (d[i + 1] - d[i])))
            for i in np.where(d[:-1] * d[1:] < 0)[0]]


def verify():
    s = ct.tf("s")
    flat = [("一阶", 5 / (0.5 * s + 1)),
            ("I 型二阶", 5 / (s * (0.5 * s + 1))),
            ("0 型二阶", 5 / (s ** 2 + 0.6 * s + 1))]
    for name, sys in flat:
        om, ph = phase_of(sys)
        assert not crosses(om, ph), (name, crosses(om, ph))
        assert ph.min() > LEVEL - 1e-6, (name, ph.min())
    om0, ph0 = phase_of((s + 1) ** 2 / (s * (s + 0.01) ** 2))
    assert ph0.min() < LEVEL - 30.0, ph0.min()
    x0 = crosses(om0, ph0)
    assert len(x0) >= 2, x0
    xd = crosses(W, delay_phase(W))
    assert xd, xd
    print("h-inf check ok: 一阶/I型二阶/0型二阶 相角最低 %.2f° < 阈值外（无交点）；"
          "带零点凹到 %.1f°、交点 %s；延迟首过 %.3f rad/s"
          % (max(phase_of(v)[1].min() for _, v in flat), ph0.min(),
             [round(v, 4) for v in x0], xd[0]))


def draw():
    fs.use_style()
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.2, 7.4), sharex=True,
                                  gridspec_kw=dict(hspace=0.13))
    fig.subplots_adjust(left=0.105, right=0.982, top=0.882, bottom=0.155)
    s = ct.tf("s")

    for a in (ax, ax2):
        a.set_xscale("log")
        a.set_ylim(-305.0, 25.0)
        a.set_yticks([0, -60, -120, -180, -240, -300])
        a.axhline(LEVEL, color=fs.INK, lw=1.5, ls=(0, (6, 3)), zorder=3)
        a.grid(True, which="major", color=fs.GRID, lw=0.6, alpha=0.9)
        a.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(W[0], W[-1])
    ax2.set_xlabel("ω / (rad/s)")
    for a in (ax, ax2):
        a.set_ylabel("相角 φ / °")

    # ---------- (a) 够不到 −180° ----------
    # 三条曲线在中频段挤成一团，标注不能贴曲线放：统一收进左下角图例（y < −190 无曲线）
    items = [("一阶  G = 5/(0.5s+1)：只到 −90°", 5 / (0.5 * s + 1), fs.MAG),
             ("I 型二阶  G = 5/[s(0.5s+1)]：只逼近 −180°", 5 / (s * (0.5 * s + 1)), fs.PHA),
             ("0 型二阶  G = 5/(s²+0.6s+1)：只逼近 −180°", 5 / (s ** 2 + 0.6 * s + 1), GREEN)]
    for lb, sys, col in items:
        om, ph = phase_of(sys)
        ax.plot(om, ph, color=col, lw=2.3, zorder=5, label=lb)
    ax.legend(loc="lower left", bbox_to_anchor=(0.012, 0.010), fontsize=10.5,
              handlelength=1.5, borderpad=0.6, labelspacing=0.55, borderaxespad=0.35,
              frameon=True, facecolor="white", edgecolor="none", framealpha=0.95)
    ax.set_title("(a) 相角够不到 −180°：无 ωx，h = ∞（一阶、二阶最小相位系统都是这样）",
                 fontsize=12.5, pad=7)
    ax.text(0.00075, -170, "−180° 线", color=fs.INK, fontsize=10.5, ha="left",
            va="bottom", zorder=9,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.4))

    # ---------- (b) 反例：零点 / 延迟 ----------
    om0, ph0 = phase_of((s + 1) ** 2 / (s * (s + 0.01) ** 2))
    ax2.plot(om0, ph0, color=ORANGE, lw=2.3, zorder=5)
    ax2.plot(W, delay_phase(W), color=fs.PHA, lw=2.3, zorder=5)
    for xc in crosses(om0, ph0):
        ax2.plot([xc], [LEVEL], "o", ms=6.5, color=ORANGE, zorder=8, clip_on=False)
    xd = crosses(W, delay_phase(W))
    ax2.plot([xd[0]], [LEVEL], "o", ms=6.5, color=fs.PHA, zorder=8, clip_on=False)

    # 两条曲线都从 −90° 往下走 ⟹ φ > −90° 的带子里没有曲线，标注放这里最稳
    ax2.text(0.00075, -30, "含延迟  G = e^(−0.5s)/[s(s+1)]：相角无下界，交点无穷多个",
             color=fs.PHA, fontsize=10.5, ha="left", va="center", zorder=9,
             bbox=dict(facecolor="white", edgecolor="none", pad=1.4))
    ax2.text(0.00075, -66,
             "最小相位带零点  G = (s+1)²/[s(s+0.01)²]：相角被凹到 −247°，出现两个交点",
             color=ORANGE, fontsize=10.5, ha="left", va="center", zorder=9,
             bbox=dict(facecolor="white", edgecolor="none", pad=1.4))
    ax2.annotate("首次穿过 −180°", (xd[0], LEVEL), xytext=(2.6, -215.0),
                 textcoords="data", ha="left", va="center", fontsize=10.5,
                 color=fs.INK, zorder=9,
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.4),
                 arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8,
                                 shrinkA=3.0, shrinkB=3.0))
    ax2.set_title("(b) 反例：带零点或延迟后相角不再单调 —— 穿过 −180°，h 变有限",
                  fontsize=12.5, pad=7)

    fig.suptitle("相频够不到 −180° ⟺ 无穿越频率 ⟺ h = ∞", fontsize=14, y=0.972)
    fig.text(0.5, 0.030, "判据只对「积分＋一阶惯性」这类相角单调的形式成立；"
                         "带零点、带延迟时老实画相频（§5.4.7）",
             ha="center", va="bottom", fontsize=10.5, color=fs.SUB)
    fs.save(fig, "自控-频域-h无穷的判据.png")


if __name__ == "__main__":
    verify()
    draw()
