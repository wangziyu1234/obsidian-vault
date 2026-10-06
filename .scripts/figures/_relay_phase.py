"""Exact relay phase arcs, with Filippov sliding after the first contact."""

import numpy as np
from scipy.optimize import brentq
from matplotlib.patches import FancyArrowPatch


def oscillator_path(initial, k=1.0, level=1.0, max_arcs=30):
    state = np.asarray(initial, dtype=float)
    side = 1 if state[0] + k * state[1] > 0 else -1
    arcs, contacts = [], []
    limit = k * level / (1 + k*k)
    for _ in range(max_arcs):
        center = -side * level
        x0, v0 = state

        def point(t):
            return np.array([center + (x0-center)*np.cos(t) + v0*np.sin(t),
                             -(x0-center)*np.sin(t) + v0*np.cos(t)])

        times = np.linspace(1e-7, 2*np.pi, 5000)
        h = np.array([point(t)[0] + k*point(t)[1] for t in times])
        j = np.flatnonzero(side*h <= 0)[0]
        assert j > 0, 'The new arc must enter its assigned region.'
        end = brentq(lambda t: point(t)[0] + k*point(t)[1], times[j-1], times[j], xtol=1e-13)
        arc = point(np.linspace(0, end, max(100, int(end*220)))).T
        np.testing.assert_allclose((arc[:, 0]-center)**2 + arc[:, 1]**2,
                                   (x0-center)**2 + v0*v0, atol=1e-10)
        assert np.min(side*(arc[:, 0] + k*arc[:, 1])) > -1e-9
        assert np.min(np.diff(arc[:, 0]) * (arc[:-1, 1] + arc[1:, 1])) > -1e-12
        np.testing.assert_allclose(arc[0], state, atol=1e-12)
        arcs.append(arc)
        state = arc[-1]
        contacts.append(state.copy())
        if abs(state[1]) < limit + 1e-9:
            sliding = state[None, :] * np.exp(-np.linspace(0, 10*k, 400)[:, None]/k)
            np.testing.assert_allclose(sliding[:, 0] + k*sliding[:, 1], 0, atol=1e-9)
            all_points = np.vstack(arcs+[sliding])
            energy = .5*all_points[:, 1]**2 + .5*all_points[:, 0]**2 + level*abs(all_points[:, 0])
            assert np.max(np.diff(energy)) < 1e-8
            assert np.linalg.norm(sliding[-1]) < 1e-4
            return arcs, sliding, np.array(contacts)
        side *= -1
    raise AssertionError('Expected to reach the attracting sliding segment.')


def double_integrator_path(initial, beta, level=1.0, max_arcs=5):
    state = np.asarray(initial, dtype=float)
    side = 1 if state[0] + beta * state[1] > 0 else -1
    arcs, contacts = [], []
    for _ in range(max_arcs):
        x0, v0 = state
        acc = -side*level
        roots = np.roots([acc/2, v0+beta*acc, x0+beta*v0])
        times = sorted(float(t.real) for t in roots if abs(t.imag) < 1e-10 and t.real > 1e-7)
        assert times
        end = times[0]
        t = np.linspace(0, end, max(140, int(end*180)))
        arc = np.column_stack([x0+v0*t+acc*t*t/2, v0+acc*t])
        assert np.min(side*(arc[:, 0]+beta*arc[:, 1])) > -1e-8
        assert np.min(np.diff(arc[:, 0]) * (arc[:-1, 1] + arc[1:, 1])) > -1e-12
        np.testing.assert_allclose(arc[:, 1]**2 - 2*acc*arc[:, 0],
                                   v0*v0 - 2*acc*x0, atol=1e-8)
        np.testing.assert_allclose(arc[0], state, atol=1e-12)
        arcs.append(arc)
        state = arc[-1]
        contacts.append(state.copy())
        if beta > 0 and abs(state[1]) < beta*level + 1e-9:
            sliding = state[None, :] * np.exp(-np.linspace(0, 10*beta, 400)[:, None]/beta)
            np.testing.assert_allclose(sliding[:, 0]+beta*sliding[:, 1], 0, atol=1e-9)
            points = np.vstack(arcs+[sliding])
            energy = points[:, 1]**2/2 + level*abs(points[:, 0])
            assert np.max(np.diff(energy)) < 1e-8
            assert np.linalg.norm(sliding[-1]) < 1e-4
            return arcs, sliding, np.array(contacts)
        side *= -1
    points = np.vstack(arcs)
    energy = points[:, 1]**2/2 + level*abs(points[:, 0])
    if beta == 0:
        assert np.ptp(energy) < 1e-8
    elif beta < 0:
        assert np.min(np.diff(energy)) > -1e-8
        assert np.min(np.diff(abs(np.array(contacts)[:, 1]))) > 0
    return arcs, None, np.array(contacts)


def arrows(ax, points, color, count=2, size=13):
    """Draw arrows only on fully visible interior portions of an arc."""
    lo, hi = ax.get_xlim(), ax.get_ylim()
    good = ((points[:, 0] > lo[0]+.15) & (points[:, 0] < lo[1]-.15)
            & (points[:, 1] > hi[0]+.15) & (points[:, 1] < hi[1]-.15))
    candidates = np.flatnonzero(good)
    if len(candidates) < 15:
        return
    for frac in np.linspace(.30, .70, count):
        idx = candidates[int(frac*(len(candidates)-1))]
        step = max(4, len(points)//35)
        j = min(idx+step, len(points)-1)
        if not good[j] or np.linalg.norm(points[j]-points[idx]) < .025:
            continue
        ax.add_patch(FancyArrowPatch(points[idx], points[j], arrowstyle='-|>',
                                    mutation_scale=size, color=color, linewidth=1.2, zorder=5))


def sliding_arrows(ax, endpoint, color):
    """Show motion on both halves of an attracting sliding segment."""
    endpoint = np.asarray(endpoint, dtype=float)
    for sign in [-1, 1]:
        start, end = sign * .88 * endpoint, sign * .32 * endpoint
        assert np.dot(end-start, start) < 0
        assert (end[0]-start[0])*start[1] > 0
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>',
                                    mutation_scale=12, color=color, linewidth=1.2, zorder=6))


def setup_axes(ax, xlim, ylim, xlabel, ylabel, fs):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal', adjustable='box')
    ax.axhline(0, color=fs.SUB, linewidth=.7, zorder=0)
    ax.axvline(0, color=fs.SUB, linewidth=.7, zorder=0)
    ax.set_xlabel(xlabel, labelpad=4)
    ax.set_ylabel(ylabel, labelpad=3)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=10)
