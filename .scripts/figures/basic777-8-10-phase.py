# figure: 777-基础8-10-分区相轨迹.png
"""Exact phase-curve family for a dead-zone relay and double integrator."""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs


OUTPUT_NAME = Path(__file__).read_text(encoding="utf-8").splitlines()[0].split(":", 1)[1].strip()
A = 0.7
B = 1.7
DEAD_ZONE_SPEEDS = (1.0, 1.5)


def phase_curve(speed):
    """Join straight dead-zone segments to exact parabolic outer arcs."""
    horizontal = np.linspace(-A, A, 201)
    descending = np.linspace(speed, -speed, 601)
    ascending = descending[::-1]
    top = np.column_stack((horizontal, np.full_like(horizontal, speed)))
    right = np.column_stack((A + (speed**2 - descending**2) / (2 * B), descending))
    bottom = np.column_stack((horizontal[::-1], np.full_like(horizontal, -speed)))
    left = np.column_stack((-A - (speed**2 - ascending**2) / (2 * B), ascending))
    return np.concatenate((top, right[1:], bottom[1:], left[1:]))


def verify_orbit(points, speed):
    error, velocity = points.T
    energy = velocity**2 / 2 + B * np.maximum(np.abs(error) - A, 0)
    np.testing.assert_allclose(energy, speed**2 / 2, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(points[0], points[-1])
    np.testing.assert_allclose(max(error), A + speed**2 / (2 * B))
    np.testing.assert_allclose(min(error), -A - speed**2 / (2 * B))

    # The polygon is clockwise, and every step follows the vector field.
    signed_twice_area = np.sum(error[:-1] * velocity[1:] - error[1:] * velocity[:-1])
    assert signed_twice_area < 0
    midpoint = (points[1:] + points[:-1]) / 2
    delta = np.diff(points, axis=0)
    acceleration = np.where(
        midpoint[:, 0] > A, -B,
        np.where(midpoint[:, 0] < -A, B, 0.0),
    )
    field = np.column_stack((midpoint[:, 1], acceleration))
    assert np.all(np.sum(delta * field, axis=1) > 0)
    np.testing.assert_allclose(
        delta[:, 0] * field[:, 1] - delta[:, 1] * field[:, 0], 0, atol=1e-12
    )
    assert np.all(np.abs(velocity[np.abs(error) < A]) == speed)


def arrow_between(ax, start, end, color):
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3, mutation_scale=11),
        zorder=5,
    )


def main():
    fs.use_style()
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    fig.subplots_adjust(left=0.13, right=0.965, bottom=0.225, top=0.745)
    fig.text(0.5, 0.945, "Dead-zone relay: phase trajectories", ha="center", fontsize=15)
    fig.text(0.5, 0.875, r"$a=0.7,\quad b=1.7,\quad v=\dot e$", ha="center", fontsize=13)
    fig.text(0.32, 0.808, r"$|v|=1$ in the dead zone", ha="center", color=fs.MAG, fontsize=10.5)
    fig.text(0.73, 0.808, r"$|v|=1.5$ in the dead zone", ha="center", color=fs.PHA, fontsize=10.5)

    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.85, 2.08)
    ax.axvspan(-A, A, facecolor=fs.FILL, alpha=0.4, zorder=0)
    ax.axvline(-A, color=fs.SUB, lw=0.85, ls=(0, (4, 3)), zorder=1)
    ax.axvline(A, color=fs.SUB, lw=0.85, ls=(0, (4, 3)), zorder=1)
    ax.axhline(0, color=fs.GRID, lw=0.65, zorder=0)
    ax.plot([-A, A], [0, 0], color=fs.INK, lw=3.3, solid_capstyle="butt", zorder=4)

    for speed, color in zip(DEAD_ZONE_SPEEDS, (fs.MAG, fs.PHA)):
        points = phase_curve(speed)
        verify_orbit(points, speed)
        ax.plot(points[:, 0], points[:, 1], color=color, lw=1.65, zorder=3)
        arrow_between(ax, (-0.22, speed), (0.08, speed), color)
        arrow_between(ax, (0.22, -speed), (-0.08, -speed), color)
        for side in (-1, 1):
            start_v, end_v = (0.55 * speed, 0.32 * speed) if side == 1 else (-0.55 * speed, -0.32 * speed)
            start_e = side * (A + (speed**2 - start_v**2) / (2 * B))
            end_e = side * (A + (speed**2 - end_v**2) / (2 * B))
            arrow_between(ax, (start_e, start_v), (end_e, end_v), color)

    ax.set_xticks([-A, 0, A])
    ax.set_xticklabels([r"$-a$", "0", r"$a$"])
    ax.set_yticks([-1.5, -1, 0, 1, 1.5])
    ax.set_yticklabels(["-1.5", "-1", "0", "1", "1.5"])
    ax.tick_params(labelsize=10.5)
    ax.set_xlabel(r"$e$", fontsize=13)
    ax.set_ylabel(r"$v=\dot e$", fontsize=13)
    ax.spines[["top", "right"]].set_visible(False)

    for position, label in (
        (-1.2, r"$\dot v=+b$"), (0, r"$\dot v=0$"), (1.2, r"$\dot v=-b$"),
    ):
        ax.text(position, 1.86, label, ha="center", fontsize=11)
    ax.annotate(
        r"$v=0,\ |e|\leq a$", xy=(0.28, 0), xytext=(0, 0.43),
        fontsize=10.5, ha="center", va="center",
        arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.SUB),
    )
    ax.text(0, -0.45, "Equilibrium set", ha="center", color=fs.SUB, fontsize=10.5)

    fig.text(
        0.5, 0.075, r"$H=\frac{1}{2}v^2+b\,\max(|e|-a,0)$ is constant on each orbit.",
        ha="center", fontsize=11,
    )
    fig.text(
        0.5, 0.022, "The origin is not isolated. The closed orbits form a family, not isolated limit cycles.",
        ha="center", fontsize=9, color=fs.SUB,
    )
    fs.save(fig, OUTPUT_NAME)
    plt.close(fig)
    print("PASS: exact energy, closed curves, turning points and clockwise vector-field direction.")


if __name__ == "__main__":
    main()
