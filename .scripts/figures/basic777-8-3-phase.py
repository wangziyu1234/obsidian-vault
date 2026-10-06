# figure: 777-基础8-3-精确相轨迹.png
"""Exact first-integral levels for basic exercise 8-3 (Jiangnan 2017).

Source: question volume PDF p149, 2*x'' + x'^2 + x = 0.
The level curves are computed from exp(x)*(v*v+x-1) = C.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import figures_style as fs


def level_value(x, v):
    return np.exp(x) * (v * v + x - 1)


def rhs_squared(x, constant):
    return 1 - x + constant * np.exp(-x)


def level_curve(constant, left, right, count=1600):
    # Cosine spacing resolves the turning points without jagged square roots.
    theta = np.linspace(0, np.pi, count)
    x = left + (right-left) * (1-np.cos(theta)) / 2
    v = np.sqrt(np.maximum(rhs_squared(x, constant), 0))
    assert np.allclose(level_value(x, v), constant, atol=5e-12)
    # Gradient of the invariant is orthogonal to the original vector field.
    dx = v
    dv = -(v*v+x) / 2
    derivative = np.exp(x) * ((v*v+x)*dx + 2*v*dv)
    assert np.max(np.abs(derivative)) < 1e-10
    return x, v


def motion_arrow(ax, x, y, idx, reverse, color):
    a, b = (idx+25, idx-25) if reverse else (idx-25, idx+25)
    ax.annotate('', xy=(x[b], y[b]), xytext=(x[a], y[a]),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=1.5,
                                mutation_scale=15, shrinkA=0, shrinkB=0))


def main():
    fs.use_style()
    fig, ax = plt.subplots(figsize=(7.5, 8.4))
    fig.subplots_adjust(left=.12, right=.96, bottom=.18, top=.81)
    ax.set_xlim(-4.6, 1.7)
    ax.set_ylim(-3.35, 3.35)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$v=\dot{x}$')
    ax.set_xticks([-4, -3, -2, -1, 0, 1])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.grid(color=fs.GRID, alpha=.38, linewidth=.6)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

    blue = fs.MAG
    boundary = '#B23020'
    exterior = '#438174'
    for constant in (-.8, -.4, -.12):
        left = brentq(lambda x: np.exp(x)*(x-1)-constant, -30, 0)
        right = brentq(lambda x: np.exp(x)*(x-1)-constant, 0, 1)
        assert left < 0 < right < 1
        x, v = level_curve(constant, left, right)
        assert np.isclose(v[0], 0, atol=1e-6)
        assert np.isclose(v[-1], 0, atol=1e-6)
        ax.plot(x, v, color=blue, lw=1.7)
        ax.plot(x, -v, color=blue, lw=1.7)
        motion_arrow(ax, x, v, 1000, False, blue)
        motion_arrow(ax, x, -v, 850, True, blue)

    # C=0 is a nonclosed parabola, not an ellipse or a periodic orbit.
    x, v = level_curve(0, -4.6, 1)
    ax.plot(x, v, color=boundary, lw=1.9, linestyle='--')
    ax.plot(x, -v, color=boundary, lw=1.9, linestyle='--')
    motion_arrow(ax, x, v, 530, False, boundary)
    motion_arrow(ax, x, -v, 530, True, boundary)
    # Motion enters at the upper left edge and exits at the lower left edge.
    for sign, reverse in ((1, False), (-1, True)):
        xx=np.linspace(-4.59, -4.27, 100)
        yy=sign*np.sqrt(1-xx)
        motion_arrow(ax, xx, yy, 50, reverse, boundary)

    constant = .12
    right = brentq(lambda x: np.exp(x)*(x-1)-constant, 1, 2)
    left = brentq(lambda x: rhs_squared(x, constant)-3.35**2, -10, 0)
    x, v = level_curve(constant, left, right)
    assert right > 1
    ax.plot(x, v, color=exterior, lw=1.8)
    ax.plot(x, -v, color=exterior, lw=1.8)
    motion_arrow(ax, x, v, 620, False, exterior)
    motion_arrow(ax, x, -v, 620, True, exterior)
    # The two ends continue past the displayed top/bottom borders to x=-infinity.
    motion_arrow(ax, x, v, 110, False, exterior)
    motion_arrow(ax, x, -v, 110, True, exterior)

    ax.plot(0, 0, 'o', color=fs.INK, markersize=4.5, zorder=5)
    legend = [
        Line2D([], [], color=blue, lw=1.8,
               label=r'$-1<C<0$  $\mathrm{\u95ed\u8f68}$'),
        Line2D([], [], color=boundary, lw=1.8, linestyle='--',
               label=r'$C=0$  $\mathrm{\u8fb9\u754c}$'),
        Line2D([], [], color=exterior, lw=1.8,
               label=r'$C>0$  $\mathrm{\u975e\u95ed\u8f68}$'),
        Line2D([], [], color=fs.INK, marker='o', linestyle='None', markersize=4,
               label=r'$C=-1$  $\mathrm{\u4e2d\u5fc3\u70b9}$'),
    ]
    # Decode CJK escapes after the raw math strings have been constructed.
    for handle in legend:
        label=handle.get_label()
        for code in ('95ed','8f68','8fb9','754c','975e','4e2d','5fc3','70b9'):
            label=label.replace('\\u'+code, chr(int(code,16)))
        handle.set_label(label)
    ax.legend(handles=legend, loc='upper right', frameon=True,
              facecolor='white', edgecolor='none', framealpha=1, fontsize=11.5)
    fig.text(.5, .965, '\u57fa\u7840 8-3\uff1a\u7cbe\u786e\u76f8\u8f68\u8ff9',
             ha='center', fontsize=17)
    fig.text(.5, .912, r'$\mathrm{e}^{x}(v^2+x-1)=C$',
             ha='center', fontsize=17)
    fig.text(.5, .865, 'C \u4e3a\u7b2c\u4e00\u79ef\u5206\u5e38\u6570',
             ha='center', fontsize=11.5, color=fs.SUB)
    fig.text(.5, .070, '\u7bad\u5934\u8868\u793a\u8fd0\u52a8\u65b9\u5411\uff1a\u4e0a\u534a\u5e73\u9762\u5411\u53f3\uff0c\u4e0b\u534a\u5e73\u9762\u5411\u5de6\u3002',
             ha='center', fontsize=11.5)
    fig.text(.5, .035, '\u8fb9\u754c\u4e0e\u975e\u95ed\u8f68\u5747\u5411\u5de6\u65e0\u754c\u5ef6\u4f38\uff0c\u56fe\u4e2d\u4ec5\u663e\u793a\u6709\u9650\u8303\u56f4\u3002',
             ha='center', fontsize=11.5, color=fs.SUB)
    fs.save(fig, '777-\u57fa\u78408-3-\u7cbe\u786e\u76f8\u8f68\u8ff9.png')
    print('Verified 5 level curves, first-integral conservation, and turning points.')


if __name__ == '__main__':
    main()
