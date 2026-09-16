# 批量出图：教材例5-12（奈氏图 + 伯德图）、例5-15（伯德图）、例6-4（校正前后伯德图）。
"""Frequency-domain figures reproduced from the transfer functions in the notes.

K/(s+1)^3 for example 5-12; 9/[s(1+Ts)] with T = 2/27 for example 5-15;
10(1+0.456s)/[s(1+0.114s)(1+s)] for the lead-compensation example 6-4.
Chinese labels sit inside $\\mathrm{...}$ (see figures_style.use_style).
"""
from __future__ import annotations

import control as ct
import numpy as np

import matplotlib.pyplot as plt

import figures_style as fs

W = np.geomspace(1e-3, 1e3, 4000)


def gain_phase(system, w=W):
    resp = ct.frequency_response(system, w)
    mag = np.abs(resp.fresp[0, 0]).squeeze()
    phase = np.unwrap(np.angle(resp.fresp[0, 0].squeeze())) * 180 / np.pi
    return mag, phase


def crossover(mag, phase, w=W):
    """Return (omega_c where |G| = 1, gamma = 180 + phase there)."""
    idx = int(np.argmin(np.abs(mag - 1.0)))
    return w[idx], 180.0 + phase[idx]


def bode_axes(figsize=(7.6, 5.6)):
    fs.use_style()
    fig, (axm, axp) = plt.subplots(2, 1, sharex=True, figsize=figsize,
                                   gridspec_kw=dict(hspace=0.12))
    for ax in (axm, axp):
        ax.set_xscale("log")
        ax.grid(True, which="both", color=fs.GRID, lw=0.55, alpha=0.55)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=10)
    axm.set_ylabel(r"$L(\omega)$ / dB", fontsize=11.5)
    axp.set_ylabel(r"$\varphi$ / $^\circ$", fontsize=11.5)
    axp.set_xlabel(r"$\omega$ / (rad/s)", fontsize=11.5)
    return fig, (axm, axp)


def add_bode(axm, axp, system, colour, label, linestyle="-", lw=2.0):
    mag, phase = gain_phase(system)
    axm.semilogx(W, 20 * np.log10(mag), color=colour, lw=lw, ls=linestyle,
                 label=label)
    axp.semilogx(W, phase, color=colour, lw=lw, ls=linestyle)
    return mag, phase


def mark_gamma(axm, axp, system, colour, note_xy=(-96, -34)):
    mag, phase = gain_phase(system)
    wc, gamma = crossover(mag, phase)
    axp.plot(wc, phase[int(np.argmin(np.abs(W - wc)))], "o", color=colour, ms=7,
             zorder=7)
    axm.axvline(wc, color=colour, lw=0.9, ls=(0, (4, 4)), alpha=0.8)
    axp.axvline(wc, color=colour, lw=0.9, ls=(0, (4, 4)), alpha=0.8)
    axp.annotate(rf"$\omega_c={wc:.2f}$, $\gamma={gamma:.1f}^\circ$", (wc, -180),
                 xytext=note_xy, textcoords="offset points", fontsize=10,
                 color=colour, bbox=dict(facecolor="white", edgecolor="none",
                                         alpha=0.95, pad=1.5), zorder=8)
    return wc, gamma


def save(fig, name, title=None):
    if title:
        fig.suptitle(title, fontsize=13, y=0.97)
    fig.tight_layout(rect=(0.005, 0.02, 0.995, 0.95 if title else 0.99))
    out = fs.ATTACH_DIR / name
    fig.savefig(str(out), dpi=fs.DPI)
    plt.close(fig)
    print("saved", out)


# ---------------------------------------------------------------- 例5-12
def fig_nyquist_512():
    """K/(s+1)^3，K=4（稳定）与 K=10（不稳定）。"""
    s = ct.tf("s")
    fs.use_style()
    fig, ax = plt.subplots(figsize=(6.4, 5.8))
    ax.axhline(0, color=fs.SUB, lw=0.9, zorder=1)
    ax.axvline(0, color=fs.SUB, lw=0.9, zorder=1)
    ax.grid(True, color=fs.GRID, lw=0.55, alpha=0.55)
    ax.set_aspect("equal", adjustable="box")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel(r"$Re\,G(j\omega)$", fontsize=11.5)
    ax.set_ylabel(r"$Im\,G(j\omega)$", fontsize=11.5)
    for k, colour, style, label in (
            (4.0, fs.MAG, "-",
             r"$K=4$$:\ \mathrm{不包围}\ (-1,j0)$$\mathrm{, 稳定}$"),
            (10.0, fs.PHA, (0, (6, 3)),
             r"$K=10$$:\ \mathrm{包围}\ (-1,j0)$$\mathrm{, 不稳定}$")):
        resp = ct.frequency_response(k / (s + 1) ** 3, np.geomspace(1e-2, 1e2, 3000))
        z = resp.fresp[0, 0].squeeze()
        keep = (z.real > -4.0) & (z.real < 1.6) & (np.abs(z.imag) < 3.0)
        ax.plot(z.real[keep], z.imag[keep], color=colour, lw=2.0, ls=style,
                zorder=4, label=label)
    ax.plot(-1, 0, marker="x", color=fs.INK, ms=10, mew=1.8, zorder=8,
            label=r"$\mathrm{判据点}\ (-1,\,0)$")
    ax.set_xlim(-3.4, 1.4)
    ax.set_ylim(-2.4, 1.4)
    ax.legend(loc="lower left", fontsize=9.5, framealpha=0.95,
              facecolor="white", edgecolor=fs.GRID)
    save(fig, "奈氏-例512.png",
         r"$\mathrm{例5-12}\ \ G(s)=K/(s+1)^3$")


def fig_bode_512():
    """同一系统的伯德图：读数应与奈氏判稳一致。"""
    s = ct.tf("s")
    fig, (axm, axp) = bode_axes()
    add_bode(axm, axp, 4 / (s + 1) ** 3, fs.MAG, r"$K=4$")
    add_bode(axm, axp, 10 / (s + 1) ** 3, fs.PHA, r"$K=10$", linestyle=(0, (6, 3)))
    mark_gamma(axm, axp, 4 / (s + 1) ** 3, fs.MAG, note_xy=(-104, 16))
    mark_gamma(axm, axp, 10 / (s + 1) ** 3, fs.PHA, note_xy=(-104, -18))
    axm.axhline(0, color=fs.SUB, lw=0.8)
    axp.axhline(-180, color=fs.SUB, lw=0.8, ls=(0, (4, 4)))
    axm.legend(loc="lower left", fontsize=10, framealpha=0.95,
               facecolor="white", edgecolor=fs.GRID)
    save(fig, "伯德-例512.png",
         r"$\mathrm{例5-12}\ \ G(s)=K/(s+1)^3$")


# ---------------------------------------------------------------- 例5-15
def fig_bode_515():
    """9/[s(1+Ts)]，T=2/27 由 gamma=60° 反求。"""
    s = ct.tf("s")
    T = 2.0 / 27.0
    system = 9 / (s * (1 + T * s))
    fig, (axm, axp) = bode_axes()
    add_bode(axm, axp, system, fs.MAG, r"$G(s)=9/[s(1+Ts)]$")
    mark_gamma(axm, axp, system, fs.PHA, note_xy=(-118, 14))
    axm.axhline(0, color=fs.SUB, lw=0.8)
    axp.axhline(-180, color=fs.SUB, lw=0.8, ls=(0, (4, 4)))
    axm.legend(loc="lower left", fontsize=10, framealpha=0.95,
               facecolor="white", edgecolor=fs.GRID)
    save(fig, "伯德-例515.png",
         r"$\mathrm{例5-15}\ \ T=2/27,\ \omega_c=9\sqrt{3}/2,\ \gamma=60^\circ$")


# ---------------------------------------------------------------- 例6-4
def fig_bode_64():
    """串联超前校正前后：L0 与 L0*(4Gc)。"""
    s = ct.tf("s")
    g0 = 10 / (s * (s + 1))
    gc = (1 + 0.456 * s) / (1 + 0.114 * s)
    fig, (axm, axp) = bode_axes()
    add_bode(axm, axp, g0, fs.MAG, r"$\mathrm{校正前}\ L_0$")
    add_bode(axm, axp, 4 * gc * g0, fs.PHA, r"$\mathrm{校正后}\ L_0\cdot 4G_c$",
             linestyle=(0, (6, 3)))
    wc0, gam0 = mark_gamma(axm, axp, g0, fs.MAG, note_xy=(-96, 12))
    wc1, gam1 = mark_gamma(axm, axp, 4 * gc * g0, fs.PHA, note_xy=(-108, -20))
    axm.axhline(0, color=fs.SUB, lw=0.8)
    axp.axhline(-180, color=fs.SUB, lw=0.8, ls=(0, (4, 4)))
    axm.legend(loc="lower left", fontsize=10, framealpha=0.95,
               facecolor="white", edgecolor=fs.GRID)
    save(fig, "校正-例64超前.png",
         r"$\mathrm{例6-4}\ \ \mathrm{串联超前校正前后}$")
    print(f"  校正前: wc={wc0:.2f}, gamma={gam0:.1f} deg")
    print(f"  校正后: wc={wc1:.2f}, gamma={gam1:.1f} deg")


if __name__ == "__main__":
    fig_nyquist_512()
    fig_bode_512()
    fig_bode_515()
    fig_bode_64()
