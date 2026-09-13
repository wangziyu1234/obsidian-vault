# Shared Nyquist plotting helpers; no standalone output.
"""Real frequency-response samples and direction arrows for note figures."""
from __future__ import annotations

import numpy as np
import control as ct
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path
from matplotlib.ticker import MaxNLocator
import figures_style as fs
import matplotlib.pyplot as plt

BOX = dict(facecolor="white", edgecolor="none", alpha=0.96, pad=1.5)


def response(system, omega):
    omega = np.atleast_1d(np.asarray(omega, dtype=float))
    return np.asarray(ct.frequency_response(system, omega).frdata).reshape(-1)


def canvas(title, formula, xlim, ylim, figsize=(6.6, 6.0)):
    fs.use_style()
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=14, y=0.98)
    ax.set_title(formula, fontsize=15, pad=12)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color=fs.SUB, lw=0.85, zorder=1)
    ax.axvline(0, color=fs.SUB, lw=0.85, zorder=1)
    ax.grid(True, color=fs.GRID, lw=0.55, alpha=0.55)
    ax.set_xlabel(r"$\mathrm{Re}\,G(j\omega)$")
    ax.set_ylabel(r"$\mathrm{Im}\,G(j\omega)$")
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=11)
    return fig, ax


def curve(ax, system, omega, arrows=(), color=fs.MAG, label=None):
    z = response(system, omega)
    ax.plot(z.real, z.imag, color=color, lw=2.3, label=label, zorder=3)
    # The entire arrow path consists of actual response samples, in increasing w.
    for at in arrows:
        q = response(system, np.geomspace(at / 1.13, at * 1.13, 40))
        verts = np.column_stack((q.real, q.imag))
        patch = FancyArrowPatch(path=Path(verts), arrowstyle="-|>",
                                mutation_scale=15, color=color, lw=1.7, zorder=5)
        ax.add_patch(patch)
    return z


def point(ax, z, label, offset=(7, 10), color=fs.PHA, limit=False, size=5):
    z = complex(z)
    ax.plot(z.real, z.imag, "o", ms=size, color=color,
            markerfacecolor="white" if limit else color, zorder=7)
    if label:
        ax.annotate(label, (z.real, z.imag), xytext=offset,
                    textcoords="offset points", fontsize=11, color=color,
                    bbox=BOX, zorder=8)


def note(ax, text, xy=(0.025, 0.03), color=fs.SUB, **kwargs):
    return ax.text(*xy, text, transform=ax.transAxes, fontsize=11,
                   color=color, bbox=BOX, zorder=8, **kwargs)


def finish(fig, path, footer="仅正频率支；箭头表示频率增大，空心点表示极限。"):
    fig.text(0.5, 0.025, footer, ha="center", va="bottom", fontsize=10, color=fs.SUB)
    fig.tight_layout(rect=(0.005, 0.055, 0.995, 0.94))
    fig.savefig(path, dpi=fs.DPI)
    plt.close(fig)
    print("saved", path)
