# -*- coding: utf-8 -*-
"""把早期两张伯德图统一到「上下两层」风格（文件名不变，笔记无需改动）：

  伯德-例512.png  —— 05-2-b 例5-12：G = K/(s+1)³，K = 4 与 K = 10
  伯德-例515.png  —— 05-3-b-2 例5-15：G = 9/[s(Ts+1)]，T = 2/27，标出 γ = 60°

构建：..\\build.ps1 -File .\\ch5-legacy-bode.py
"""
import os

import numpy as np
import matplotlib.pyplot as plt
import control as ct

import figures_style as fs

fs.use_style()
OUT = os.path.join(fs.REPO_ROOT, "附件")


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=fs.DPI)
    plt.close(fig)
    print("saved", path)


def fdata(sys, w):
    r = ct.frequency_response(sys, w)
    mag = 20 * np.log10(np.abs(r.fresp[0, 0, :]))
    pha = np.unwrap(np.angle(r.fresp[0, 0, :])) * 180 / np.pi
    return mag, pha


# ---------------- 例5-12：K/(s+1)^3 ----------------
w = np.logspace(-1, 2, 3000)
fig, (axm, axp) = fs.new_bode_axes(figsize=(6.6, 6.4))
for ax in (axm, axp):
    ax.set_xscale("log")
    ax.set_xlim(w[0], w[-1])
    fs.tidy(ax)
for K, color, ls in ((4, fs.MAG, "-"), (10, fs.PHA, (0, (6, 4)))):
    sys = ct.tf([K], np.polymul([1, 1], np.polymul([1, 1], [1, 1])))
    mag, pha = fdata(sys, w)
    axm.plot(w, mag, color=color, linewidth=2.0, linestyle=ls, label="K = %d" % K)
    gm, pm, wg, wc = ct.margin(sys)
    print("例5-12  K=%2d: ωc=%.3f γ=%.1f° ωg=%.3f h=%.2f (%.2f dB)"
          % (K, wc, pm, wg, gm, 20 * np.log10(gm)))
    if K == 4:
        axp.plot(w, pha, color=fs.PHA, linewidth=2.0)
        axm.axvline(wc, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
        axp.axvline(wc, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
        axm.annotate("ωc = %.3f" % wc, xy=(wc, 16), xytext=(6, 0),
                     textcoords="offset points", color=fs.INK, fontsize=11)
        axp.annotate("γ = %.1f°" % pm, xy=(wc, -180), xytext=(8, -22),
                     textcoords="offset points", color=fs.PHA, fontsize=11)
axm.axvline(3.162, color=fs.SUB, linewidth=0.9, linestyle=(0, (2, 3)))
axp.axvline(3.162, color=fs.SUB, linewidth=0.9, linestyle=(0, (2, 3)))
axm.annotate("ωg = 1.732", xy=(1.732, 8), xytext=(-8, 0), textcoords="offset points",
             color=fs.SUB, fontsize=10.5, ha="right")
axp.annotate("两种 K 的相频相同", xy=(0.02, 0.06), xycoords="axes fraction",
             color=fs.SUB, fontsize=10.5)
axm.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axp.axhline(-180, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axm.set_ylim(-45, 25)
axp.set_ylim(-300, -60)
axp.set_yticks([-270, -180, -90])
axm.legend(loc="lower left", fontsize=11)
fig.suptitle("例5-12  G = K/(s+1)³：K = 4 与 K = 10", fontsize=13, y=0.97)
save(fig, "伯德-例512.png")

# ---------------- 例5-15：G = 9/[s(Ts+1)]，T = 2/27 ----------------
T = 2 / 27
sys = ct.tf([9], np.polymul([1, 0], [T, 1]))
w = np.logspace(-0.5, 2.2, 3000)
mag, pha = fdata(sys, w)
fig, (axm, axp) = fs.new_bode_axes(figsize=(6.6, 6.4))
for ax in (axm, axp):
    ax.set_xscale("log")
    ax.set_xlim(w[0], w[-1])
    fs.tidy(ax)
axm.plot(w, mag, color=fs.MAG, linewidth=2.2)
axp.plot(w, pha, color=fs.PHA, linewidth=2.2)
gm, pm, wg, wc = ct.margin(sys)
print("例5-15  T=2/27: ωc=%.4f γ=%.2f°（应为 7.79423、60°）" % (wc, pm))
axm.axvline(wc, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axp.axvline(wc, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axm.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axp.axhline(-180, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axp.axhline(-120, color=fs.PHA, linewidth=0.9, linestyle=(0, (2, 3)))
axm.annotate("ωc = %.4g rad/s（L = 0 dB）" % wc, xy=(wc, 14), xytext=(8, 0),
             textcoords="offset points", color=fs.INK, fontsize=11)
axp.annotate("γ = 180° + φ(ωc) = %.1f°" % pm, xy=(wc, -180), xytext=(-8, 34),
             textcoords="offset points", color=fs.PHA, fontsize=11, ha="right")
axm.set_ylim(-40, 40)
axp.set_ylim(-200, -80)
axp.set_yticks([-180, -150, -120, -90])
fig.suptitle("例5-15  G = 9/[s(Ts+1)]，T = 2/27，ωc = 7.794，γ = 60°", fontsize=12.5, y=0.97)
save(fig, "伯德-例515.png")
