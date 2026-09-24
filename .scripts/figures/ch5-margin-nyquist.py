# figure: 频域-稳定裕度-奈氏图.png
"""奈氏图上的稳定裕度：γ 量曲线与单位圆的交点，h 量曲线与负实轴的交点。

系统与 频域-稳定裕度.png（伯德图）相同：G(s) = 2/[s(s+1)(0.1s+1)]。
  * wc = 1.2437，|G(jwc)| = 1，∠G(jwc) = -148.29°  ->  gamma = 31.71°
  * wx = sqrt(10) = 3.1623（转折频率 1 与 10 的几何中点），|G(jwx)| = 0.1818
  * h = 1/0.1818 = 5.5（14.807 dB）
画法：
  * γ —— 单位圆上从 (-1, j0) 到 G(jwc) 的圆心角（两点同在单位圆上，角以原点为顶点）；
  * h —— 曲线交负实轴于 G(jwx)，该点到原点的距离为 1/h（尺寸线画在负实轴上）。
第三象限被曲线斜穿，文字标注一律走轴上方/右下方的空区，避免压线。

Build: ..\\build.ps1 -File .\\ch5-margin-nyquist.py
"""
from __future__ import annotations

import numpy as np

import control as ct
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import figures_style as fs
import _nyquist_style as ns

NUM, DEN = [2.0], [0.1, 1.1, 1.0, 0.0]
SYS = ct.tf(NUM, DEN)


def resp(w):
    w = np.atleast_1d(np.asarray(w, dtype=float))
    return np.polyval(NUM, 1j * w) / np.polyval(DEN, 1j * w)


def verify():
    gm, pm, wx, wc = ct.margin(SYS)
    assert abs(wc - 1.2437) < 1e-3, wc
    assert abs(pm - 31.71) < 0.01, pm
    assert abs(wx - np.sqrt(10.0)) < 1e-6, wx
    assert abs(gm - 5.5) < 1e-9, gm
    zc = complex(resp(wc)[0])
    assert abs(abs(zc) - 1.0) < 1e-9, abs(zc)          # 截止频率处落在单位圆上
    assert abs(180.0 + np.degrees(np.angle(zc)) - pm) < 1e-6
    zx = complex(resp(wx)[0])
    assert abs(zx.real + 1.0 / gm) < 1e-12, zx         # 穿越频率处落在负实轴上
    assert abs(zx.imag) < 1e-12, zx
    assert abs(-20.0 * np.log10(abs(zx)) - 14.807) < 0.01
    print(f"verified: wc={wc:.4f} gamma={pm:.2f}° |G(jwc)|={abs(zc):.6f} | "
          f"wx={wx:.4f} |G(jwx)|={abs(zx):.4f} h={gm:.4f} ({20 * np.log10(gm):.2f} dB)")
    return wc, pm, wx, gm, zc, zx


def draw(wc, gamma, wx, h, zc, zx):
    fig, ax = ns.canvas("奈氏图上的稳定裕度（与伯德图同一系统）",
                        r"$G(s)=\frac{2}{s(s+1)(0.1s+1)}$",
                        (-1.55, 1.0), (-1.55, 1.0), figsize=(7.0, 6.9))

    # 单位圆：曲线上 |G| = 1 的那个点就是 ωc
    th = np.linspace(0.0, 2.0 * np.pi, 721)
    ax.plot(np.cos(th), np.sin(th), color=fs.SUB, lw=1.0, ls=(0, (5, 4)),
            zorder=2)
    # 标注移到左上角外侧：原位置横跨 y 轴竖线，而虚线圈的弧又斜穿左上角，
    # 所以右端对齐到 x = −0.60（弧在 y≈0.95 处只到 x≈−0.31）
    ax.text(-0.60, 0.95, "单位圆  |G| = 1", color=fs.SUB, fontsize=11,
            ha="right", va="center", zorder=8)

    # 幅相曲线（正频率支）+ 临界点
    ns.curve(ax, SYS, np.geomspace(0.70, 40.0, 3000), arrows=(1.05, 2.4))
    ax.plot([-1.0], [0.0], marker="*", ms=16, color=fs.PHA, zorder=9)
    ax.annotate("(-1, j0)", (-1.0, 0.0), xytext=(-8, 11),
                textcoords="offset points", ha="right", fontsize=11,
                color=fs.PHA, bbox=ns.BOX, zorder=10)

    # --- γ：单位圆上从 (-1, j0) 量到 G(jωc) 的圆心角 ---
    ax.plot([0.0, zc.real], [0.0, zc.imag], color=fs.SUB, lw=0.9,
            ls=(0, (4, 3)), zorder=4)
    ax.add_patch(Arc((0.0, 0.0), 2.0, 2.0, theta1=180.0, theta2=180.0 + gamma,
                     color=fs.PHA, lw=3.2, zorder=6))
    mid = np.radians(180.0 + gamma / 2.0)
    ax.text(1.22 * np.cos(mid), 1.22 * np.sin(mid), f"γ = {gamma:.1f}°",
            color=fs.PHA, fontsize=12, ha="center", va="center",
            bbox=ns.BOX, zorder=10)

    # ωc：第三象限被曲线斜穿，标注挪到 A 点左下方空区，用细引线连回交点
    ax.annotate(f"ωc = {wc:.2f}", (zc.real, zc.imag), xytext=(-1.30, -0.62),
                textcoords="data", ha="center", va="center", fontsize=11,
                color=fs.PHA, bbox=ns.BOX, zorder=10,
                arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8,
                                shrinkA=0.0, shrinkB=3.0))

    # --- h：尺寸线画在负实轴上（O→交点 = 1/h，交点→临界点 = 补足到 1）---
    ax.plot([0.0, zx.real], [0.0, 0.0], color=fs.PHA, lw=3.2, zorder=7,
            solid_capstyle="butt")
    ax.plot([zx.real, -1.0], [0.0, 0.0], color=fs.PHA, lw=1.6,
            ls=(0, (4, 3)), zorder=7)
    ax.plot([zx.real, zx.real], [-0.06, 0.06], color=fs.PHA, lw=1.4, zorder=7)
    ax.plot([zx.real], [0.0], "o", ms=5.5, color=fs.PHA, zorder=8)

    # ωx、|G(jωx)|、h 三个数成块放在**第一象限**（曲线只走左半平面、ω>0 时 y>0 那侧全空），
    # 引线斜下连到负实轴上的交点；原先放右下 → 块角贴着单位圆弧（弧在 y=−0.66 处鼓到 x≈0.75）
    ax.annotate(f"ωx = {wx:.2f}\n|G(jωx)| = {abs(zx):.3f}\n"
                f"h = {h:.1f}（{20 * np.log10(h):.1f} dB）", (zx.real, -0.06),
                xytext=(0.06, 0.42), textcoords="data", ha="left", va="top",
                fontsize=11, color=fs.INK, bbox=ns.BOX, zorder=10,
                arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8,
                                shrinkA=2.0, shrinkB=2.0))

    ns.finish(fig, fs.ATTACH_DIR / "频域-稳定裕度-奈氏图.png",
              footer="曲线交单位圆于 ωc ⟹ γ = 180° + ∠G(jωc) = 31.7°；"
                     "交负实轴于 ωx ⟹ h = 1/∣G(jωx)∣ = 5.5（14.8 dB）。\n"
                     "只画正频率支（ω 由 0⁺ 增至 ∞）；单位圆与负实轴，就是两个裕度的量尺。",
              rect=(0.005, 0.085, 0.995, 0.935))


if __name__ == "__main__":
    draw(*verify())
