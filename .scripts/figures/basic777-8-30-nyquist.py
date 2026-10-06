# figure: 777-基础8-30-奈氏与负倒描述函数.png
"""Normalized frequency traces and inverse describing function for 8-30."""

from pathlib import Path

import control as ct
import numpy as np
import matplotlib.pyplot as plt

import figures_style as fs


OUTPUT_NAME = Path(__file__).read_text(encoding="utf-8").splitlines()[0].split(":", 1)[1].strip()
S = ct.tf("s")
SYSTEM = 1 / (S * (S + 1) * (2 * S + 1))
OMEGA_CROSS = 1 / np.sqrt(2.0)


def response(omega):
    frequencies = np.atleast_1d(omega)
    order = np.argsort(frequencies)
    values = np.asarray(ct.frequency_response(SYSTEM, frequencies[order]).frdata).reshape(-1)
    return values[np.argsort(order)]


def direction_arrow(ax, start_omega, end_omega, conjugate=False, color=fs.MAG):
    points = response([start_omega, end_omega])
    if conjugate:
        points = points.conjugate()
    ax.annotate(
        "", xy=(points[1].real, points[1].imag),
        xytext=(points[0].real, points[0].imag),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.15, mutation_scale=10),
        zorder=5,
    )


def verify_curve(omega, values):
    expected_real = -3 / ((1 + omega**2) * (1 + 4 * omega**2))
    expected_imag = -(1 - 2 * omega**2) / (omega * (1 + omega**2) * (1 + 4 * omega**2))
    np.testing.assert_allclose(values.real, expected_real, rtol=1e-10, atol=1e-12)
    np.testing.assert_allclose(values.imag, expected_imag, rtol=1e-10, atol=1e-12)
    np.testing.assert_allclose(response(OMEGA_CROSS), [-2 / 3 + 0j], atol=1e-12)
    assert np.all(values.real < 0)
    assert np.all(values.imag[omega < OMEGA_CROSS * 0.999] < 0)
    assert np.all(values.imag[omega > OMEGA_CROSS * 1.001] > 0)
    assert abs(values[0].real + 3) < 1e-5
    assert values[0].imag < -1e4
    assert abs(values[-1]) < 1e-10 and values[-1].imag > 0
    assert np.count_nonzero(np.diff(np.signbit(values.imag))) == 1
    # At balance, -1/(K*N(A)) = -pi*A/(6*K) = -2/3.
    for gain in (0.5, 1.0, 4.0):
        amplitude = 4 * gain / np.pi
        np.testing.assert_allclose(-np.pi * amplitude / (6 * gain), -2 / 3)


def main():
    omega = np.logspace(-5, 5, 24000)
    values = response(omega)
    verify_curve(omega, values)
    fs.use_style()
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.2))
    fig.subplots_adjust(left=0.078, right=0.98, bottom=0.21, top=0.765, wspace=0.25)

    fig.text(0.5, 0.95, "Nyquist traces and inverse describing function", ha="center", fontsize=16)
    fig.text(
        0.5, 0.882, r"$G(s)/K=1/[s(s+1)(2s+1)],\quad K>0$",
        ha="center", fontsize=13,
    )
    fig.text(0.20, 0.825, r"$\omega>0$: solid blue", color=fs.MAG, ha="center", fontsize=11)
    fig.text(0.50, 0.825, r"$\omega<0$: dashed red", color=fs.PHA, ha="center", fontsize=11)
    fig.text(0.80, 0.825, "Arrows: increasing frequency", color=fs.SUB, ha="center", fontsize=11)

    for ax in axes:
        ax.plot(values.real, values.imag, color=fs.MAG, lw=1.55, zorder=3)
        ax.plot(values.real, -values.imag, color=fs.PHA, lw=1.3, ls=(0, (4, 2)), zorder=2)
        ax.axhline(0, color=fs.GRID, lw=0.7, zorder=0)
        ax.axvline(0, color=fs.GRID, lw=0.7, zorder=0)
        ax.plot([-3.48, 0], [0, 0], color=fs.INK, lw=1.35, zorder=1)
        ax.plot(-2 / 3, 0, "o", color=fs.INK, ms=4.5, zorder=6)
        ax.set_xlabel(r"$\mathrm{Re}\,[G(\mathrm{j}\omega)/K]$", fontsize=12)
        ax.set_ylabel(r"$\mathrm{Im}\,[G(\mathrm{j}\omega)/K]$", fontsize=12)
        ax.tick_params(labelsize=10)
        ax.spines[["top", "right"]].set_visible(False)

    global_ax, detail_ax = axes
    global_ax.set_xlim(-3.5, 0.2)
    global_ax.set_ylim(-1000, 1000)
    global_ax.set_yscale("symlog", linthresh=0.1)
    global_ax.set_yticks([-1000, -10, -0.1, 0, 0.1, 10, 1000])
    global_ax.set_yticklabels(["-1000", "-10", "-0.1", "0", "0.1", "10", "1000"])
    global_ax.set_xticks([-3, -2, -1, 0])
    global_ax.axvline(-3, color=fs.GRID, lw=0.8, ls=":", zorder=0)
    global_ax.text(-2.55, 190, r"$\omega\to0^-:\ \mathrm{Im}\to+\infty$", fontsize=10.5)
    global_ax.text(-2.55, -220, r"$\omega\to0^+:\ \mathrm{Im}\to-\infty$", fontsize=10.5)
    global_ax.text(-2.55, 24, r"$\mathrm{Re}\to-3$", fontsize=10.5, color=fs.SUB)
    global_ax.text(-2.36, 0.35, r"$-1/[K N(A)]$", fontsize=11, ha="center")
    global_ax.annotate(
        "", xy=(-2.78, 0), xytext=(-1.75, 0),
        arrowprops=dict(arrowstyle="-|>", lw=1.2, color=fs.INK, mutation_scale=11),
        zorder=5,
    )
    global_ax.text(-2.3, -0.12, r"$A$ increases", fontsize=10, ha="center")
    direction_arrow(global_ax, 0.20, 0.25)
    direction_arrow(global_ax, 0.25, 0.20, conjugate=True, color=fs.PHA)

    detail_ax.set_xlim(-0.95, 0.065)
    detail_ax.set_ylim(-0.20, 0.20)
    detail_ax.set_xticks([-0.8, -0.6, -0.4, -0.2, 0])
    detail_ax.set_yticks([-0.2, -0.1, 0, 0.1, 0.2])
    detail_ax.text(-0.88, 0.158, "Detail near the crossing", fontsize=11)
    detail_ax.annotate(
        r"$(-2/3,0)$" + "\n" + r"$\omega=1/\sqrt{2}\ \mathrm{rad/s}$",
        xy=(-2 / 3, 0), xytext=(-0.63, -0.17),
        fontsize=10.5, ha="left", va="center",
        arrowprops=dict(arrowstyle="-", color=fs.SUB, lw=0.8),
    )
    direction_arrow(detail_ax, 0.88, 1.06)
    direction_arrow(detail_ax, 1.06, 0.88, conjugate=True, color=fs.PHA)
    direction_arrow(detail_ax, 1.6, 2.0)
    direction_arrow(detail_ax, 2.0, 1.6, conjugate=True, color=fs.PHA)

    fig.text(
        0.5, 0.10,
        r"$-1/[K N(A)]=-\pi A/(6K)$; balance at $A=4K/\pi$.",
        ha="center", fontsize=12,
    )
    fig.text(
        0.5, 0.035,
        "Left: symmetric log scale on Im. Frequency traces shown; the pole at s = 0 requires contour indentation.",
        ha="center", fontsize=10, color=fs.SUB,
    )
    fs.save(fig, OUTPUT_NAME)
    plt.close(fig)
    print("PASS: control response, exact formulas, one negative-real crossing, endpoints and gain scaling.")


if __name__ == "__main__":
    main()
