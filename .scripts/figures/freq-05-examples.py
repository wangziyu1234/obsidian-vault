# figure: 奈氏-例512.png
"""Frequency-domain figures reproduced from the transfer functions in the notes.

K/(s+1)^3 for example 5-12; 9/[s(1+Ts)] with T = 2/27 for example 5-15;
10(1+0.456s)/[s(1+0.114s)(1+s)] for the lead-compensation example 6-4.
Chinese labels sit inside $\\mathrm{...}$ (see figures_style.use_style).
"""
from __future__ import annotations

import os
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
    """Whole Nyquist loci and a separate critical-point enlargement."""
    from _nyquist_style import response, curve
    s = ct.tf("s")
    fs.use_style()
    fig, axes = plt.subplots(1,2,figsize=(10.6,5.2))
    w = np.geomspace(1e-5,1e5,10000)
    for ax in axes:
        ax.axhline(0,color=fs.SUB,lw=.8)
        ax.axvline(0,color=fs.SUB,lw=.8)
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(True,color=fs.GRID,lw=.5,alpha=.6)
        ax.set_xlabel(r"$\mathrm{Re}\,G(j\omega)$",fontsize=12)
        ax.set_ylabel(r"$\mathrm{Im}\,G(j\omega)$",fontsize=12)
        ax.plot(-1,0,"x",color=fs.INK,ms=8,zorder=7)
    for k,colour in [(4,fs.MAG),(10,fs.PHA)]:
        model=k/(s+1)**3
        z=response(model,w)
        assert abs(response(model,[np.sqrt(3)])[0]+k/8)<1e-12
        assert np.count_nonzero(ct.poles(ct.feedback(model)).real>0)==(0 if k==4 else 2)
        assert max(abs(z.imag)) < 8
        for i,ax in enumerate(axes):
            curve(ax,model,w,((.3,) if i==0 else (1.25,2.3)),color=colour)
            ax.plot(np.r_[k,z.real,0],np.r_[0,-z.imag,0],color=colour,lw=1.2,ls=":")
            ax.plot(-k/8,0,"o",color=colour,ms=5,zorder=7)
        axes[0].plot(k,0,"o",color=colour,ms=5)
    axes[0].set_xlim(-3,11)
    axes[0].set_ylim(-8,8)
    axes[0].set_aspect("equal",adjustable="box")
    axes[0].set_title("完整轨迹：实线正频率，点线负频率",fontsize=11)
    axes[1].set_xlim(-1.65,.3)
    axes[1].set_ylim(-.7,.55)
    axes[1].set_title("放大判据点附近",fontsize=12)
    box=dict(facecolor="white",edgecolor="none",pad=1.5)
    for x,text,colour,pos in [(-.5,r"$-1/2$",fs.MAG,(-.30,.36)),
                              (-1.25,r"$-5/4$",fs.PHA,(-1.56,.36))]:
        axes[1].annotate(text,(x,0),xytext=pos,color=colour,fontsize=12,
                         bbox=box,arrowprops=dict(arrowstyle="-",color=colour,lw=.7))
    axes[1].annotate(r"$(-1,0)$",(-1,0),xytext=(.035,-.59),
                     fontsize=11,bbox=box,
                     arrowprops=dict(arrowstyle="-",color=fs.SUB,lw=.6))
    fig.suptitle(r"$G(s)=K/(s+1)^3$",fontsize=15,y=.98)
    fig.text(.5,.05,"蓝：K = 4，闭环稳定；红：K = 10，闭环有两个右半平面极点。",
             ha="center",fontsize=11,color=fs.SUB)
    fig.subplots_adjust(left=.07,right=.98,top=.82,bottom=.19,wspace=.30)
    fig.savefig(str(fs.ATTACH_DIR/"奈氏-例512.png"),dpi=fs.DPI)
    plt.close(fig)


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
    compensated_gc = (1 + 0.456 * s) / (1 + 0.114 * s)
    corrected = compensated_gc * g0
    _, exact_gamma, _, exact_wc = ct.margin(corrected)
    assert 4.42 < exact_wc < 4.44 and 49.5 < exact_gamma < 49.7
    assert abs(ct.dcgain(compensated_gc) - 1) < 1e-12
    fig, (axm, axp) = bode_axes()
    add_bode(axm, axp, g0, fs.MAG, r"$\mathrm{校正前}\ L_0$")
    add_bode(axm, axp, corrected, fs.PHA, r"$\mathrm{校正后}\ L_0\cdot 4G_c$",
             linestyle=(0, (6, 3)))
    _, gam0, _, wc0 = ct.margin(g0)
    wc1, gam1 = exact_wc, exact_gamma
    for wc, gamma, colour, label_y in (
            (wc0, gam0, fs.MAG, -191),
            (wc1, gam1, fs.PHA, -207)):
        axp.plot(wc, gamma - 180, "o", color=colour, ms=6, zorder=7)
        for ax in (axm, axp):
            ax.axvline(wc, color=colour, lw=0.9, ls=(0, (4, 4)), alpha=0.8)
        axp.text(0.025, label_y,
                 rf"$\omega_c={wc:.2f}$, $\gamma={gamma:.1f}^\circ$",
                 fontsize=10, color=colour,
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    axm.axhline(0, color=fs.SUB, lw=0.8)
    axp.axhline(-180, color=fs.SUB, lw=0.8, ls=(0, (4, 4)))
    axm.legend(loc="lower left", fontsize=10, framealpha=0.95,
               facecolor="white", edgecolor=fs.GRID)
    axm.set_xlim(0.01, 100)
    axm.set_ylim(-70, 70)
    axp.set_ylim(-215, -80)
    axm.tick_params(labelbottom=False)
    fig.suptitle(r"$\mathrm{例6-4}\ \ \mathrm{串联超前校正前后}$",
                 fontsize=13, y=0.97)
    fig.subplots_adjust(left=0.12, right=0.97, top=0.90, bottom=0.11, hspace=0.14)
    fig.savefig(str(fs.ATTACH_DIR / "校正-例64超前.png"), dpi=fs.DPI)
    plt.close(fig)
    print(f"  校正前: wc={wc0:.2f}, gamma={gam0:.1f} deg")
    print(f"  校正后: wc={wc1:.2f}, gamma={gam1:.1f} deg")


if __name__ == "__main__":
    if os.environ.get("FIGURE_ONLY") == "512":
        fig_nyquist_512()
    elif os.environ.get("FIGURE_ONLY") == "64":
        fig_bode_64()
    else:
        fig_nyquist_512()
        fig_bode_512()
        fig_bode_515()
        fig_bode_64()
