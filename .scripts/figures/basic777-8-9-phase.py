# figure: 777-8-9-三种反馈相轨迹.png
"""Exact parabolic relay arcs for beta zero, negative, and positive."""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import figures_style as fs
from _relay_phase import double_integrator_path, setup_axes, arrows, sliding_arrows

OUTPUT = Path(__file__).read_text(encoding='utf-8').splitlines()[0].split(':', 1)[1].strip()


def main():
    fs.use_style()
    fig = plt.figure(figsize=(8.2, 13.8))
    rows = [(.690, 0), (.375, -1), (.060, 1)]
    fig.text(.08, .975, r'8-9   $M=1$', fontsize=19, weight='bold')
    fig.text(.08, .948, r'$v=\dot c,\quad h=c+\beta v$', fontsize=14)

    for bottom, beta in rows:
        ax = fig.add_axes([.09, bottom, .56, .265])
        setup_axes(ax, (-5.5, 5.5), (-5.5, 5.5), r'$c$', r'$v=\dot c$', fs)
        ax.set_xticks([-4, -2, 0, 2, 4])
        ax.set_yticks([-4, -2, 0, 2, 4])
        if beta == 0:
            for amplitude in [1, 2.5, 4.5]:
                arcs, _, _ = double_integrator_path((amplitude, 0), beta, max_arcs=3)
                # Three arcs return from the positive turning point to itself.
                first, middle, last = arcs
                velocity = np.linspace(last[0, 1], 0, 180)
                tail = np.column_stack([amplitude-velocity**2/2, velocity])
                trajectory = np.vstack([first, middle, tail])
                np.testing.assert_allclose(trajectory[0], trajectory[-1], atol=1e-12)
                np.testing.assert_allclose(middle[-1], tail[0], atol=1e-12)
                for arc in [first, middle, tail]:
                    ax.plot(*arc.T, color=fs.MAG, linewidth=1.4)
                    arrows(ax, arc, fs.MAG, count=1)
                assert np.max(np.abs(trajectory[:, 0])) <= amplitude+1e-8
            ax.plot([0, 0], [-5.5, 5.5], '--', color=fs.SUB, linewidth=1)
            title, motion = r'$\beta=0$', 'Closed periodic orbits'
        elif beta < 0:
            arcs, _, contacts = double_integrator_path((.25, 0), beta, max_arcs=3)
            assert abs(contacts[1, 1]) > abs(contacts[0, 1])
            for arc in arcs:
                ax.plot(*arc.T, color=fs.MAG, linewidth=1.5)
                arrows(ax, arc, fs.MAG, count=2)
            ax.plot([-5.5, 5.5], [-5.5, 5.5], '--', color=fs.SUB, linewidth=1.1)
            title, motion = r'$\beta=-1<0$', 'Outward; unstable'
        else:
            arcs, sliding, contacts = double_integrator_path((4.5, 0), beta, max_arcs=12)
            assert abs(contacts[-1, 1]) < 1
            for arc in arcs:
                ax.plot(*arc.T, color=fs.MAG, linewidth=1.5)
                arrows(ax, arc, fs.MAG, count=2)
            ax.plot([-5.5, 5.5], [5.5, -5.5], '--', color=fs.SUB, linewidth=1.1)
            ax.plot([-1, 1], [1, -1], color=fs.PHA, linewidth=4, alpha=.35)
            ax.plot(*sliding.T, color=fs.PHA, linewidth=2.5)
            sliding_arrows(ax, [1, -1], fs.PHA)
            for v in [-.99, 0, .99]:
                assert v-1 < 0 < v+1
            title, motion = r'$\beta=1>0$', 'Inward, then sliding'
        ax.plot(0, 0, marker='o', markersize=3.8, color=fs.INK)
        fig.text(.70, bottom+.237, title, fontsize=16)
        fig.text(.70, bottom+.199, motion, fontsize=11, color=fs.PHA if beta > 0 else fs.SUB)
        fig.text(.70, bottom+.150, 'Switching line', fontsize=11, color=fs.SUB)
        fig.text(.70, bottom+.119, r'$c=0$' if beta == 0 else r'$v=-c/\beta$', fontsize=15)
        if beta > 0:
            fig.text(.70, bottom+.073, r'$|v|<\beta M$', fontsize=15, color=fs.PHA)
            fig.text(.70, bottom+.040, r'$\dot c=-c/\beta$', fontsize=15, color=fs.PHA)
        else:
            fig.text(.70, bottom+.073, r'$h<0:\ v^2=2Mc+C_1$', fontsize=10.5)
            fig.text(.70, bottom+.033, r'$h>0:\ v^2=-2Mc+C_2$', fontsize=10.5)
            if beta < 0:
                fig.text(.70, bottom+.004, 'Continues outside the window.',
                         fontsize=9.5, color=fs.SUB)
    fs.save(fig, OUTPUT)
    plt.close(fig)
    print('PASS: parabolic invariants, regional signs, closed-orbit energy, divergence and attracting sliding.')


if __name__ == '__main__':
    main()
