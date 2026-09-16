# 批量出图：教材例4.2 / 例4.4 / 例4.6，以及 MATLAB 绘制一节的两张根轨迹。
# 每张图的 figure: 声明见各自的 build 函数；本脚本一次生成四张附件 PNG。
"""Root-locus figures reproduced from the system data recorded in the notes.

All curves come from control.root_locus_map; nothing is sampled by hand.
Chinese labels must sit inside $\\mathrm{...}$ (see figures_style.use_style).
"""
from __future__ import annotations

from pathlib import Path

import control as ct
import numpy as np

import matplotlib.pyplot as plt

import figures_style as fs

CLIP = 6.0          # viewing radius: far branches run off frame and are clipped


def locus_branches(system, gains):
    """Return one array of complex roots per branch.

    control.root_locus_map returns a PoleZeroData object whose .loci array is
    indexed [gain, root]; the old root_locus() tuple order is (roots, gains).
    """
    data = ct.root_locus_map(system, gains)
    loci = np.atleast_2d(np.asarray(data.loci))
    return [loci[:, j] for j in range(loci.shape[1])]


def canvas(figsize=(6.6, 5.4)):
    fs.use_style()
    fig, ax = plt.subplots(figsize=figsize)
    ax.axhline(0, color=fs.SUB, lw=0.9, zorder=1)
    ax.axvline(0, color=fs.SUB, lw=0.9, zorder=1)
    ax.grid(True, color=fs.GRID, lw=0.55, alpha=0.55)
    ax.set_aspect("equal", adjustable="box")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=10)
    ax.set_xlabel(r"$Re$", fontsize=11.5)
    ax.set_ylabel(r"$Im$", fontsize=11.5)
    return fig, ax


def add_arrows(ax, system, gains, colour):
    for at in gains:
        for branch in locus_branches(system, np.linspace(at * 0.92, at * 1.08, 40)):
            if branch.size < 6 or np.any(np.abs(branch) > CLIP):
                continue
            ax.annotate("", xy=(branch.real[-1], branch.imag[-1]),
                        xytext=(branch.real[-4], branch.imag[-4]),
                        arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.4),
                        zorder=6)


def add_locus(ax, system, gains, colour=fs.MAG, arrows=(), label=None):
    first = True
    for branch in locus_branches(system, gains):
        keep = np.abs(branch) < CLIP
        ax.plot(branch.real[keep], branch.imag[keep], color=colour, lw=2.0,
                zorder=3, label=label if first else None)
        first = False
    if arrows:
        add_arrows(ax, system, arrows, colour)


def add_poles_zeros(ax, system, show_zeros=True, colour_x=fs.INK):
    p = system.poles()
    p = p[np.abs(p) < CLIP]
    ax.plot(p.real, p.imag, "x", color=colour_x, ms=9, mew=1.8, zorder=7,
            label=r"$\mathrm{开环极点}$")
    if show_zeros and system.zeros().size:
        z = system.zeros()
        z = z[np.abs(z) < CLIP]
        ax.plot(z.real, z.imag, "o", color=fs.PHA, ms=8, mfc="white", mew=1.8,
                zorder=7, label=r"$\mathrm{开环零点}$")


def save(fig, ax, name, xlim, ylim, title):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=13, pad=10)
    ax.legend(loc="upper left", fontsize=9.5, framealpha=0.95,
              facecolor="white", edgecolor=fs.GRID)
    out = fs.ATTACH_DIR / name
    fig.tight_layout(rect=(0.005, 0.02, 0.995, 0.98))
    fig.savefig(str(out), dpi=fs.DPI)
    plt.close(fig)
    print("saved", out)


def fig_04_1_ex42():
    """例4.2：G(s)=K(0.5s+1)/(0.5s^2+s+1)，复数部分为圆，圆心在零点 -2。"""
    s = ct.tf("s")
    system = (0.5 * s + 1) / (0.5 * s * s + s + 1)
    fig, ax = canvas()
    add_locus(ax, system, np.linspace(0, 60, 8000),
              label=r"$\mathrm{根轨迹}\ (K:0\to\infty)$", arrows=(1.0, 3.0))
    add_poles_zeros(ax, system)
    theta = np.linspace(0, 2 * np.pi, 500)
    ax.plot(-2 + np.sqrt(2) * np.cos(theta), np.sqrt(2) * np.sin(theta),
            color=fs.SUB, lw=1.1, ls=(0, (5, 4)), zorder=2,
            label=r"$\mathrm{理论圆}\ |s+2|=\sqrt{2}$")
    save(fig, ax, "根轨迹-041-例42b.png", (-6.5, 2.5), (-4.2, 4.2),
         r"$\mathrm{例4.2}\ \ G(s)=K(0.5s+1)/(0.5s^2+s+1)$")


def fig_04_2_2_ex44():
    """例4.4：GH=K*/[s(s+3)(s^2+2s+2)]，虚轴交点 s=±j√2、K*=6。"""
    s = ct.tf("s")
    system = 1 / (s * (s + 3) * (s * s + 2 * s + 2))
    fig, ax = canvas()
    add_locus(ax, system, np.linspace(0, 40, 8000),
              label=r"$\mathrm{根轨迹}\ (K^*:0\to\infty)$", arrows=(1.5, 8.0))
    add_poles_zeros(ax, system, show_zeros=False)
    ax.plot([0, 0], [-np.sqrt(2), np.sqrt(2)], "s", color=fs.PHA, ms=7, zorder=7,
            label=r"$\mathrm{虚轴交点}\ s=\pm j\sqrt{2}\ (K^*=6)$")
    ax.axvline(0, color=fs.INK, lw=1.0, alpha=0.35, zorder=1)
    save(fig, ax, "根轨迹-042-例44.png", (-5.2, 2.2), (-3.6, 3.6),
         r"$\mathrm{例4.4}\ \ G(s)H(s)=K^*/[s(s+3)(s^2+2s+2)]$")


def fig_04_2_2_ex46():
    """教材例4-6：正反馈 GH=K*(s+2)/[(s+3)(s^2+2s+2)]，零度根轨迹。"""
    s = ct.tf("s")
    system = (s + 2) / ((s + 3) * (s * s + 2 * s + 2))
    fig, ax = canvas()
    add_locus(ax, system, np.linspace(0, 40, 8000),
              label=r"$\mathrm{零度根轨迹}\ (K^*:0\to\infty)$", arrows=(2.0, 9.0))
    add_poles_zeros(ax, system)
    # 出射角 -71.6°（教材例4-6）：画一小段方向示意
    p1 = -1 + 1j
    ang = np.deg2rad(-71.6)
    ax.annotate("", xy=(p1.real + 0.85 * np.cos(ang), p1.imag + 0.85 * np.sin(ang)),
                xytext=(p1.real, p1.imag),
                arrowprops=dict(arrowstyle="-|>", color=fs.PHA, lw=1.6), zorder=8)
    ax.annotate(r"$\theta_{p_1}=-71.6^\circ$", (p1.real + 0.9 * np.cos(ang),
                                               p1.imag + 0.9 * np.sin(ang)),
                xytext=(10, -16), textcoords="offset points", fontsize=10,
                color=fs.PHA, zorder=9)
    save(fig, ax, "根轨迹-042-例46.png", (-5.2, 2.6), (-3.2, 3.2),
         r"$\mathrm{例4.6（正反馈）}\ \ G(s)H(s)=K^*(s+2)/[(s+3)(s^2+2s+2)]$")


def fig_04_4_s012():
    """04-4 例2：纯三阶 G=K*/[s(s+1)(s+2)]，虚轴交点 s=±j√2、K*=6。"""
    s = ct.tf("s")
    system = 1 / (s * (s + 1) * (s + 2))
    fig, ax = canvas()
    add_locus(ax, system, np.linspace(0, 20, 8000),
              label=r"$\mathrm{根轨迹}\ (K^*:0\to\infty)$", arrows=(0.8, 5.0))
    add_poles_zeros(ax, system, show_zeros=False)
    ax.plot([0, 0], [-np.sqrt(2), np.sqrt(2)], "s", color=fs.PHA, ms=7, zorder=7,
            label=r"$\mathrm{虚轴交点}\ s=\pm j\sqrt{2}\ (K^*=6)$")
    save(fig, ax, "根轨迹-044-s012.png", (-4.2, 1.8), (-3.2, 3.2),
         r"$\mathrm{三阶系统}\ \ G(s)=K^*/[s(s+1)(s+2)]$")


def fig_04_4_s2s1():
    """04-4 例3：G=K*(s+2)/[s(s+1)]，复数部分为圆弧。"""
    s = ct.tf("s")
    system = (s + 2) / (s * (s + 1))
    fig, ax = canvas()
    add_locus(ax, system, np.linspace(0, 60, 8000),
              label=r"$\mathrm{根轨迹}\ (K^*:0\to\infty)$", arrows=(1.0, 4.0))
    add_poles_zeros(ax, system)
    theta = np.linspace(0, 2 * np.pi, 500)
    ax.plot(-1 + np.sqrt(2) * np.cos(theta), np.sqrt(2) * np.sin(theta),
            color=fs.SUB, lw=1.1, ls=(0, (5, 4)), zorder=2,
            label=r"$\mathrm{圆弧}\ |s+1|=\sqrt{2}$")
    save(fig, ax, "根轨迹-044-s2s1.png", (-4.6, 1.6), (-2.6, 2.6),
         r"$\mathrm{含零点系统}\ \ G(s)=K^*(s+2)/[s(s+1)]$")


if __name__ == "__main__":
    fig_04_1_ex42()
    fig_04_2_2_ex44()
    fig_04_2_2_ex46()
    fig_04_4_s012()
    fig_04_4_s2s1()
