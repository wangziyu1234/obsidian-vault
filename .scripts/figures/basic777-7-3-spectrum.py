# figure: 777-7-3-ans-频谱图.png
"""Ideal impulse-sampled spectrum for basic exercise 7-3."""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import figures_style as fs


OUTPUT_NAME = Path(__file__).read_text(encoding="utf-8").splitlines()[0].split(":", 1)[1].strip()
T = 0.1
SAMPLE_RATE = 1.0 / T
SOURCE_FREQUENCIES = np.array([1.0, 2.0, 4.0])
SOURCE_AMPLITUDES = np.array([3.0, 1.5, 1.0])
IMPULSE_WEIGHTS = SAMPLE_RATE * SOURCE_AMPLITUDES / 2.0


def spectral_lines():
    """Return (replica index, frequency in Hz, Dirac impulse weight)."""
    return [
        (m, m * SAMPLE_RATE + sign * frequency, weight)
        for m in range(-1, 2)
        for frequency, weight in zip(SOURCE_FREQUENCIES, IMPULSE_WEIGHTS)
        for sign in (-1, 1)
    ]


def verify_spectrum(lines):
    """Check positions, scaling, symmetry and a sampled-signal DFT."""
    assert np.isclose(T * SAMPLE_RATE, 1.0)
    assert SOURCE_FREQUENCIES.max() < SAMPLE_RATE / 2.0
    np.testing.assert_allclose(IMPULSE_WEIGHTS, [15.0, 7.5, 5.0])
    positions = sorted(frequency for _, frequency, _ in lines)
    np.testing.assert_array_equal(
        positions,
        [-14, -12, -11, -9, -8, -6, -4, -2, -1,
         1, 2, 4, 6, 8, 9, 11, 12, 14],
    )
    assert len(set(positions)) == 18
    weights_by_frequency = {frequency: weight for _, frequency, weight in lines}
    for _, frequency, weight in lines:
        assert weights_by_frequency[-frequency] == weight
        if frequency + SAMPLE_RATE in weights_by_frequency:
            assert weights_by_frequency[frequency + SAMPLE_RATE] == weight

    # One second contains ten samples and complete periods of all three tones.
    sample_times = np.arange(10) * T
    samples = sum(
        amplitude * np.cos(2.0 * np.pi * frequency * sample_times)
        for frequency, amplitude in zip(SOURCE_FREQUENCIES, SOURCE_AMPLITUDES)
    )
    coefficients = np.fft.fft(samples) / len(samples)
    for frequency, weight in zip(SOURCE_FREQUENCIES, IMPULSE_WEIGHTS):
        for bin_index in (int(frequency), -int(frequency)):
            np.testing.assert_allclose(
                SAMPLE_RATE * coefficients[bin_index], weight, atol=1e-12
            )
    np.testing.assert_allclose(coefficients[[0, 3, 5, 7]], 0.0, atol=1e-12)


def main():
    lines = spectral_lines()
    verify_spectrum(lines)
    fs.use_style()
    fig, ax = plt.subplots(figsize=(8.8, 4.3))
    fig.subplots_adjust(left=0.09, right=0.975, bottom=0.30, top=0.755)

    fig.text(0.5, 0.95, "Spectrum of ideal impulse sampling", ha="center", fontsize=16)
    fig.text(
        0.5, 0.865,
        r"$P(f)=\int_{-\infty}^{\infty}p(t)e^{-j2\pi ft}\,dt$"
        r"     $T=0.1\,\mathrm{s},\quad f_s=10\,\mathrm{Hz}$",
        ha="center", fontsize=12,
    )

    ax.set_xlim(-15, 15)
    ax.set_ylim(0, 19.5)
    ax.set_xticks(np.arange(-15, 16, 5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.set_yticks([0, 5, 7.5, 15])
    ax.set_yticklabels(["0", "5", "7.5", "15"])
    ax.set_xlabel(r"Frequency $f$ / Hz", fontsize=12, labelpad=5)
    ax.set_ylabel("Impulse weight", fontsize=12, labelpad=8)
    ax.tick_params(axis="both", labelsize=11)
    ax.tick_params(axis="x", which="minor", length=2.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=fs.GRID, linewidth=0.6, linestyle=":", zorder=0)

    for m, frequency, weight in lines:
        color = fs.MAG if m == 0 else fs.PHA
        ax.plot([frequency, frequency], [0, weight], color=color, linewidth=1.35, zorder=3)
        ax.plot(frequency, weight, marker="^", markersize=5.5, color=color, zorder=4)

    for m in (-1, 0, 1):
        label = "central: " if m == 0 else "replica: "
        ax.text(
            m * SAMPLE_RATE, 17.4, label + rf"$m={m}$",
            color=fs.MAG if m == 0 else fs.PHA, fontsize=11,
            ha="center", va="center",
        )

    fig.text(
        0.5, 0.14,
        r"$f=10m\pm1,\ 10m\pm2,\ 10m\pm4\ \mathrm{Hz}$"
        r"; weights $15,\ 7.5,\ 5$; $m\in\mathbb{Z}$.",
        ha="center", fontsize=11,
    )
    fig.text(
        0.5, 0.065,
        "Copies continue indefinitely. Arrow heights show impulse weights, not ordinary amplitudes.",
        ha="center", fontsize=10.5, color=fs.SUB,
    )
    fs.save(fig, OUTPUT_NAME)
    plt.close(fig)
    print("PASS: 18 line positions, weights, symmetry, periodicity and DFT scaling.")


if __name__ == "__main__":
    main()
