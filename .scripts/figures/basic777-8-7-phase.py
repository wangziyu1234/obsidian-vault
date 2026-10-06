# figure: 777-基础8-7-等倾线与相轨迹.png
"""Exercise 8-7: exact LTI trajectories and isoclines."""
from pathlib import Path
import numpy as np
import control as ct
import matplotlib.pyplot as plt
import figures_style as fs


def main():
    fs.use_style()
    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    fig.subplots_adjust(left=0.12, right=0.96, bottom=0.24, top=0.78)
    x = np.linspace(-0.6, 2.6, 250)
    ax.plot([1, 1], [-1.8, 1.8], '--', color=fs.SUB, lw=0.85)
    ax.plot(x, 1-x, '--', color=fs.SUB, lw=0.85)
    ax.plot(x, (1-x)/2, '--', color=fs.SUB, lw=0.85)
    xx, vv = np.meshgrid(np.linspace(-0.5, 2.5, 17), np.linspace(-1.7, 1.7, 17))
    dx, dv = vv, 1-xx-vv
    norm = np.hypot(dx, dv)
    ax.quiver(xx, vv, dx/np.maximum(norm, 1e-12), dv/np.maximum(norm, 1e-12),
              color=fs.GRID, scale=31, width=0.0025, zorder=1)
    system = ct.ss([[0, 1], [-1, -1]], np.zeros((2, 1)), np.eye(2), np.zeros((2, 1)))
    time = np.linspace(0, 14, 1200)
    for initial in ([1.4, 0], [-1.4, 0], [0, 1.6], [0, -1.6]):
        result = ct.initial_response(system, time, X0=initial)
        states = np.asarray(result.states)
        assert np.linalg.norm(states[:, -1]) < 0.003
        px, pv = states[0]+1, states[1]
        ax.plot(px, pv, color=fs.MAG, lw=1.5, zorder=3)
        for i in (50, 165):
            ax.annotate('', xy=(px[i+10], pv[i+10]), xytext=(px[i], pv[i]),
                        arrowprops=dict(arrowstyle='->', color=fs.MAG, lw=1.2))
    ax.scatter([1], [0], color=fs.PHA, s=24, zorder=4)
    ax.axhline(0, color=fs.INK, lw=0.6)
    ax.axvline(0, color=fs.INK, lw=0.6)
    ax.set(xlim=(-0.6, 2.6), ylim=(-1.8, 1.8), xlabel=r'$x$', ylabel=r'$v=\dot x$')
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    fig.text(0.5, 0.94, '8-7: isoclines and phase trajectories', ha='center', fontsize=16)
    fig.text(0.5, 0.865, r'$\dot x=v,\quad\dot v=1-x-v$', ha='center', fontsize=14)
    fig.text(0.5, 0.08, r'Dashed: $x=1$, $v=1-x$, $v=(1-x)/2$; stable focus $(1,0)$.',
             ha='center', fontsize=11)
    assert np.allclose(np.linalg.eigvals(system.A).real, -0.5)
    name = Path(__file__).read_text(encoding='utf-8').splitlines()[0].split(':', 1)[1].strip()
    fs.save(fig, name)
    plt.close(fig)
    print('PASS: equilibrium, eigenvalues and converging exact LTI trajectories')


if __name__ == '__main__':
    main()
