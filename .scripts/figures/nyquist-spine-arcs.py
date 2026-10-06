# figure: 频域-奈氏-虚轴奇点补弧.png
"""Local s-plane detours; the positive imaginary-axis contour runs upward."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import figures_style as fs

NAME = "频域-奈氏-虚轴奇点补弧.png"
CN = ["Microsoft YaHei", "SimHei"]
RADIUS, CENTER = 0.30, 0.75


def arrow(ax, start, end, color, lw=1.6):
    ax.annotate("", xy=end, xytext=start, zorder=1 if color == fs.GRID else 4,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=12))


def setup(ax, title):
    ax.set_xlim(-0.72, 3.15)
    ax.set_ylim(-0.28, 1.52)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")
    arrow(ax, (-0.42, 0), (0.92, 0), fs.GRID, 1)
    arrow(ax, (0, -0.10), (0, 1.40), fs.GRID, 1)
    ax.text(0.14, 1.34, r"$\operatorname{Im}s$", fontsize=11, color=fs.SUB)
    ax.text(0.62, -0.23, r"$\operatorname{Re}s$", fontsize=11, color=fs.SUB)
    ax.set_title(title, fontfamily=CN, fontsize=14, loc="left", pad=4)


def arc(ax, center, start, end):
    theta = np.linspace(start, end, 161)
    z = 1j * center + RADIUS * np.exp(1j * theta)
    ax.plot(z.real, z.imag, color=fs.PHA, lw=2.5)
    arrow(ax, (z[74].real, z[74].imag),
          (z[90].real, z[90].imag), fs.PHA, 2.0)
    assert np.all(z.real >= -1e-12)
    assert np.all(np.diff(np.unwrap(np.angle(z - 1j * center))) > 0)
    return z


def words(ax, first, formula, last, color=fs.PHA):
    ax.text(1.17, 1.03, first, fontfamily=CN, fontsize=13)
    ax.text(1.17, 0.68, formula, fontsize=13, color=color)
    ax.text(1.17, 0.31, last, fontfamily=CN, fontsize=12, color=color)


def fig_spine_arcs():
    fs.use_style()
    fig, axes = plt.subplots(3, 1, figsize=(6.2, 8.5))
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.025, top=0.95, hspace=0.30)
    ax = axes[0]
    setup(ax, "① 原点 ν 重极点：绕四分之一圈")
    z = arc(ax, 0, 0, np.pi / 2)
    assert np.allclose([z[0], z[-1]], [RADIUS, 1j * RADIUS])
    for nu in (1, 2, 3):
        phase = np.unwrap(np.angle(1 / z**nu))
        assert np.isclose(phase[-1] - phase[0], -nu * np.pi / 2)
    ax.plot([0, 0], [RADIUS, 1.18], color=fs.MAG, lw=2.3)
    arrow(ax, (0, 0.87), (0, 1.13), fs.MAG)
    ax.plot(0, 0, "x", color=fs.PHA, ms=8, mew=2)
    ax.text(-0.16, -0.17, "0", fontsize=12)
    ax.text(0.37, 0.06, r"$\varepsilon$", fontsize=12)
    words(ax, "小弧逆时针走", r"$\theta: 0\to\pi/2$", "映射为顺时针无穷大弧")
    ax.text(1.17, -0.04, r"$\Delta\arg G=-\nu\pi/2$", fontsize=13, color=fs.PHA)

    ax = axes[1]
    setup(ax, "② 非零虚轴 q 重极点：绕半圈")
    z = arc(ax, CENTER, -np.pi / 2, np.pi / 2)
    assert np.allclose([z[0], z[-1]],
                       [1j * (CENTER - RADIUS), 1j * (CENTER + RADIUS)])
    for q in (1, 2, 3):
        phase = np.unwrap(np.angle(1 / (z - 1j * CENTER)**q))
        assert np.isclose(phase[-1] - phase[0], -q * np.pi)
    ax.plot([0, 0], [0, CENTER - RADIUS], color=fs.MAG, lw=2.3)
    ax.plot([0, 0], [CENTER + RADIUS, 1.22], color=fs.MAG, lw=2.3)
    arrow(ax, (0, 0.15), (0, 0.35), fs.MAG)
    arrow(ax, (0, 1.08), (0, 1.23), fs.MAG)
    ax.plot(0, CENTER, "x", color=fs.PHA, ms=8, mew=2)
    ax.text(-0.16, CENTER, r"$j\omega_0$", ha="right", va="center", fontsize=12)
    ax.text(-0.16, -0.17, "0", fontsize=12)
    words(ax, "以极点为圆心向右绕", r"$\theta:-\pi/2\to\pi/2$", "映射为顺时针无穷大弧")
    ax.text(1.17, -0.04, r"$\Delta\arg G=-q\pi$", fontsize=13, color=fs.PHA)

    ax = axes[2]
    setup(ax, "③ 虚轴零点：直接通过")
    ax.plot([0, 0], [0, 1.23], color=fs.MAG, lw=2.3)
    arrow(ax, (0, 0.25), (0, 0.48), fs.MAG)
    arrow(ax, (0, 0.97), (0, 1.20), fs.MAG)
    ax.plot(0, CENTER, "o", color=fs.MAG, ms=8, mfc="white", mew=2)
    ax.text(-0.16, CENTER, r"$j\omega_0$", ha="right", va="center", fontsize=12)
    ax.text(-0.16, -0.17, "0", fontsize=12)
    words(ax, "零点处解析，无需绕行", r"$G(j\omega_0)=0$", "映射连续经过原点", color=fs.MAG)
    fs.save(fig, NAME)
    plt.close(fig)


if __name__ == "__main__":
    fig_spine_arcs()
