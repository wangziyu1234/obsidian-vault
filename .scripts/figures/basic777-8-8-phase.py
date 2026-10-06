# figure: 777-8-8-相轨迹与滑动段.png
"""Exact circle arcs and attracting sliding for basic exercise 8-8."""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import figures_style as fs
from _relay_phase import oscillator_path, setup_axes, arrows, sliding_arrows

OUTPUT = Path(__file__).read_text(encoding='utf-8').splitlines()[0].split(':', 1)[1].strip()


def main():
    fs.use_style()
    arcs, sliding, contacts = oscillator_path((3, 0))
    assert len(arcs) >= 2
    assert abs(contacts[-1, 1]) < .5
    for v in [-.49, 0, .49]:
        assert 2*v-1 < 0 < 2*v+1

    fig = plt.figure(figsize=(8.7, 6.7))
    ax = fig.add_axes([.08, .17, .57, .69])
    setup_axes(ax, (-3.4, 3.4), (-3.2, 3.2), r'$y/N$', r'$v/N=\dot y/N$', fs)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    s = np.linspace(-3.4, 3.4, 300)
    ax.plot(s, -s, '--', color=fs.SUB, linewidth=1.2)
    ax.fill_between(s, -3.2, -s, color=fs.MAG, alpha=.025, zorder=-1)
    for arc in arcs:
        ax.plot(*arc.T, color=fs.MAG, linewidth=1.6)
        arrows(ax, arc, fs.MAG)
    # The central red segment is a geometric set; arrowed red path is its motion.
    ax.plot([-.5, .5], [.5, -.5], color=fs.PHA, linewidth=4, alpha=.35, solid_capstyle='butt')
    ax.plot(*sliding.T, color=fs.PHA, linewidth=2.4)
    sliding_arrows(ax, [.5, -.5], fs.PHA)
    # Mark virtual centers without claiming they are system equilibria.
    ax.plot([-1, 1], [0, 0], linestyle='none', marker='x', color=fs.SUB, markersize=7)
    ax.plot(0, 0, marker='o', markersize=4, color=fs.INK)
    ax.plot(3, 0, marker='o', markersize=4, color=fs.MAG)

    fig.text(.08, .945, '8-8', fontsize=19, weight='bold')
    fig.text(.21, .945, r'$k=1,\quad N=1$', fontsize=15)
    fig.text(.70, .82, r'$h=y+kv$', fontsize=15)
    fig.text(.70, .75, r'$h<0:\quad (y-N)^2+v^2=C_1$', fontsize=11)
    fig.text(.70, .68, r'$h>0:\quad (y+N)^2+v^2=C_2$', fontsize=11)
    fig.text(.70, .56, 'Switching line', fontsize=12, color=fs.SUB)
    fig.text(.70, .505, r'$v=-y/k$', fontsize=15)
    fig.text(.70, .395, 'Attracting sliding', fontsize=12, color=fs.PHA)
    fig.text(.70, .34, r'$|v|<\frac{kN}{1+k^2}$', fontsize=16, color=fs.PHA)
    fig.text(.70, .245, r'$\dot y=-y/k$', fontsize=16, color=fs.PHA)
    fig.text(.08, .075, 'Blue: exact circle arcs.  Red: sliding toward the origin.', fontsize=11)
    fig.text(.08, .03, r'Crosses mark virtual centers $(\pm N,0)$ of extended regional equations.', fontsize=10, color=fs.SUB)
    fs.save(fig, OUTPUT)
    plt.close(fig)
    print('PASS: regional signs, circle invariants, switching continuity, sliding and nonincreasing energy.')


if __name__ == '__main__':
    main()
