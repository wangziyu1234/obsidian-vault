# figure: 频域-奈氏-条件稳定.png
# figure: 频域-奈氏-结构不稳定.png
"""Schematic crossing order and a true positive-frequency Nyquist branch."""
from __future__ import annotations

import os
from pathlib import Path
import control as ct
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MplPath
import figures_style as fs
from _nyquist_style import response, BOX

OUT = Path(os.environ.get("FIGURE_OUT", fs.ATTACH_DIR / "unused.png")).parent


def canvas(title, xlim, ylim):
    fs.use_style()
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    fig.subplots_adjust(left=.12, right=.97, bottom=.22, top=.86)
    fig.suptitle(title, fontsize=14, y=.97)
    ax.set(xlim=xlim, ylim=ylim, xlabel=r"$\mathrm{Re}$", ylabel=r"$\mathrm{Im}$")
    ax.axhline(0, color=fs.SUB, lw=.8)
    ax.axvline(0, color=fs.SUB, lw=.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=.2)
    ax.tick_params(labelsize=10)
    return fig, ax


def arrow(ax, x, y, start, stop):
    path = MplPath(np.column_stack((x[start:stop], y[start:stop])))
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>",
                 mutation_scale=14, lw=1.8, color=fs.MAG, zorder=6))


def label(ax, text, xy, xytext, color=fs.INK):
    ax.annotate(text, xy, xytext=xytext, ha="center", va="center",
                fontsize=11, color=color, bbox=BOX, zorder=8,
                arrowprops=dict(arrowstyle="-", color=color, lw=.7))


def save(fig, name, lines):
    for y, line in zip((.092, .038), lines):
        fig.text(.5, y, line, ha="center", fontsize=11, color=fs.SUB)
    fig.savefig(OUT / name, dpi=fs.DPI)
    plt.close(fig)


def fig_conditionally_stable():
    fig, ax = canvas("条件稳定：交点位置随增益变化", (-2.9, .55), (-1.7, 1.25))
    knots_x = [0.1, -1.55, -2, -2.5, -1.5, -1.05, -.5, -.1, 0]
    knots_y = [-2.3, -1.05, 0, .72, 0, -.62, 0, .38, 0]
    t = np.linspace(0, 1, 9)
    tt = np.sort(np.r_[np.linspace(0, 1, 1500), t])
    sx, sy = CubicSpline(t, knots_x), CubicSpline(t, knots_y)
    x, y = sx(tt), sy(tt)
    for ti, xi, sign in zip(t[[2, 4, 6]], [-2, -1.5, -.5], [1, -1, 1]):
        assert abs(sx(ti) - xi) < 1e-10 and abs(sy(ti)) < 1e-10
        assert np.sign(sy(ti, 1)) == sign
    signs = np.sign(y[np.abs(y) > .01])
    assert np.count_nonzero(signs[1:] != signs[:-1]) == 3
    assert y[0] < ax.get_ylim()[0] and x[-1] == y[-1] == 0
    ax.axvspan(-2.9, -1, color=fs.PHA, alpha=.045, zorder=0)
    ax.plot(x, y, lw=2.4, color=fs.MAG)
    ax.plot([-1, -1], [-.85, .88], ls="--", lw=.8, color=fs.SUB)
    for at in [.17, .42, .67, .90]:
        i = np.searchsorted(tt, at)
        arrow(ax, x, y, i, i + 30)
    for xi, tx, tag, color in [(-2, -2.38, r"$\omega_1:\ -2\quad\uparrow$", fs.PHA),
                               (-1.5, -1.48, r"$\omega_2:\ -1.5\quad\downarrow$", fs.PHA),
                               (-.5, -.30, r"$\omega_3:\ -0.5\quad\uparrow$", fs.SUB)]:
        ax.plot(xi, 0, "o", color=color, ms=5)
        label(ax, tag, (xi, 0), (tx, 1.05), color)
    ax.plot(-1, 0, "x", color=fs.INK, ms=9, mew=2)
    label(ax, r"$(-1,0)$", (-1, 0), (-.52, -.93))
    ax.text(-2.72, -1.40, "阴影区：仅计 −1 左侧穿越", fontsize=11, color=fs.PHA)
    label(ax, r"$\omega\to0^+$" + "\n" + r"$\downarrow\ \infty$",
          (sx(.07), sy(.07)), (.18, -1.14))
    ax.set_xticks([-2.5, -2, -1.5, -1, -.5, 0])
    save(fig, "频域-奈氏-条件稳定.png", [
        "K = 10；形状示意，箭头为频率增大方向",
        r"$\mathrm{稳定区间:}\quad 0<K<5\quad\mathrm{或}\quad 20/3<K<20$",
    ])


def fig_structurally_unstable():
    s = ct.tf("s")
    system = 1 / (s*s*(s+1))
    w = np.geomspace(.006, 100, 15000)
    z = response(system, w)
    assert np.all(z.real < 0) and np.all(z.imag > 0)
    assert abs(np.angle(z[0]) - np.pi) < .01 and abs(z[-1]) < 1e-5
    assert abs(np.angle(z[-1]) - np.pi/2) < .011
    assert np.allclose(response(system, [1]), [-.5+.5j])
    for k in [.001, 1, 1000]:
        poles = ct.poles(ct.feedback(k*system))
        assert np.count_nonzero(poles.real > 0) == 2
    fig, ax = canvas("结构不稳定：正频率支与判稳", (-6, .9), (-.65, 3.1))
    ax.plot(z.real, z.imag, color=fs.MAG, lw=2.4)
    for at in [.5, .85, 1.7]:
        i = np.searchsorted(w, at)
        arrow(ax, z.real, z.imag, i, i + 120)
    ax.plot(-1, 0, "x", color=fs.INK, ms=9, mew=2)
    ax.plot(-.5, .5, "o", color=fs.PHA, ms=5)
    label(ax, r"$\omega=1:\ (-1/2,\ 1/2)$", (-.5, .5), (-2.3, 1.8), fs.PHA)
    label(ax, r"$(-1,0)$", (-1, 0), (-2, -.43))
    ax.text(-5.65, .40, r"$G(s)H(s)=\frac{K}{s^2(Ts+1)}$",
            fontsize=13, color=fs.INK)
    ax.text(-5.65, -.35, r"$K=T=1$", fontsize=12, color=fs.SUB)
    i = np.searchsorted(z.real, -5.85)
    label(ax, r"$\omega\to0^+:\quad\infty\angle-180^\circ$",
          (z.real[i], z.imag[i]), (-3.8, 2.7), fs.SUB)
    label(ax, r"$\omega\to\infty$" + "\n" + r"$0\angle-270^\circ$", (0, 0), (-.65, 2.0))
    save(fig, "频域-奈氏-结构不稳定.png", [
        "仅画正频率支；负频率支及虚轴极点补弧未画",
        r"$T=1:\quad\mathrm{Routh}\ \mathrm{首列}\ 1,1,-K,K\quad\Rightarrow\quad 2\ \mathrm{个右半平面根}\ (K>0)$",
    ])


if __name__ == "__main__":
    fig_conditionally_stable()
    fig_structurally_unstable()
