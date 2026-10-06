# figure: 777-基础8-11-分区相轨迹.png
"""Exercise 8-11: saturation feedback and exact local eigendirections."""
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import figures_style as fs


def dynamics(t, state):
    e, v = state
    return [v, -2*v-5*np.clip(e+v, -1, 1)]


def main():
    fs.use_style()
    fig, ax = plt.subplots(figsize=(7.4, 5.8))
    fig.subplots_adjust(left=0.12, right=0.96, bottom=0.27, top=0.77)
    e = np.linspace(-4, 4, 500)
    ax.plot(e, 1-e, '--', color=fs.SUB, lw=1.1)
    ax.plot(e, -1-e, '--', color=fs.SUB, lw=1.1)
    # Zero-acceleration rays belong only to their respective saturation regions.
    reference_color = '#438174'
    for side in (-1, 1):
        reference_e = side*np.linspace(3.5, 4, 80)
        reference_v = np.full_like(reference_e, -side*2.5)
        np.testing.assert_allclose(
            -2*reference_v-5*np.clip(reference_e+reference_v, -1, 1), 0,
            atol=1e-12,
        )
        ax.plot(reference_e, reference_v, color=reference_color, lw=1.4, zorder=3)
    ee, vv = np.meshgrid(np.linspace(-3.8, 3.8, 19), np.linspace(-3.2, 3.2, 17))
    de, dv = vv, -2*vv-5*np.clip(ee+vv, -1, 1)
    norm = np.hypot(de, dv)
    ax.quiver(ee, vv, de/np.maximum(norm, 1e-12), dv/np.maximum(norm, 1e-12),
              color=fs.GRID, scale=34, width=0.0025, zorder=1)
    for initial in ([3.5, 0], [-3.5, 0], [1.5, 2], [-1.5, -2], [0, 3], [0, -3]):
        sol = solve_ivp(dynamics, (0, 22), initial, rtol=1e-9, atol=1e-11,
                        max_step=0.025)
        assert sol.success and np.linalg.norm(sol.y[:, -1]) < 0.0001
        ax.plot(sol.y[0], sol.y[1], color=fs.MAG, lw=1.4, zorder=3)
        for target in (0.35, 1.1):
            i = np.searchsorted(sol.t, target)
            ax.annotate('', xy=sol.y[:, i+5], xytext=sol.y[:, i],
                        arrowprops=dict(arrowstyle='->', color=fs.MAG, lw=1.15))
    for lam in ((-7+np.sqrt(29))/2, (-7-np.sqrt(29))/2):
        assert np.isclose(lam*lam+7*lam+5, 0)
        loc = np.linspace(-0.8, 0.8, 400)
        keep = np.abs((1+lam)*loc) <= 0.9
        ax.plot(loc[keep], lam*loc[keep], ':', color=fs.PHA, lw=1.5, zorder=4)
    ax.scatter([0], [0], color=fs.PHA, s=22, zorder=5)
    ax.axhline(0, color=fs.INK, lw=0.6)
    ax.axvline(0, color=fs.INK, lw=0.6)
    ax.set(xlim=(-4, 4), ylim=(-3.4, 3.4), xlabel=r'$e$', ylabel=r'$v=\dot e$')
    ax.spines[['top', 'right']].set_visible(False)
    fig.text(0.5, 0.94, '8-11: piecewise phase trajectories', ha='center', fontsize=16)
    fig.text(0.5, 0.865, r'$\dot e=v,\quad\dot v=-2v-5\,\mathrm{sat}(e+v)$',
             ha='center', fontsize=14)
    fig.text(0.5, 0.16, r'Green: zero acceleration at $v=\pm5/2$ in the outer regions.',
             ha='center', fontsize=10.5, color=reference_color)
    fig.text(0.5, 0.105, r'Dashed switching lines: $e+v=\pm1$.', ha='center', fontsize=11)
    fig.text(0.5, 0.04, r'Dotted local directions: $v=\lambda_{\pm}e$, '
             r'$\lambda_{\pm}=(-7\pm\sqrt{29})/2$; stable node at $(0,0)$.',
             ha='center', fontsize=11)
    name = Path(__file__).read_text(encoding='utf-8').splitlines()[0].split(':', 1)[1].strip()
    fs.save(fig, name)
    plt.close(fig)
    print('PASS: piecewise dynamics, local eigenvalues and converging trajectories')


if __name__ == '__main__':
    main()
