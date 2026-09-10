# -*- coding: utf-8 -*-
"""第5章例题补图（二）：伯德/时域曲线 7 张。

  * 频域-例56-非最小相位渐近线.png   05-1-3 例5-6
  * 频域-例57-实测幅频辨识.png       05-3-2 例5-7
  * 频域-例513-相角裕度与阻尼比.png  05-3-b-2 例5-13
  * 频域-例514-增益与裕度.png        05-2-d 例5-14
  * 频域-例517-雕刻机.png            05-3-b-1 例5-17
  * 频域-例518-磁盘驱动.png          05-3-b-1 例5-18
  * 频域-算例-渐近线反求.png         05-3-2 反求例

图内文字不混用中文与 `$…$`；说明性文字放笔记题注，图内只留短标注。
脚本会把关键指标打印出来，便于与笔记里的数字核对。

构建：..\\build.ps1 -File .\\ch5-bode-examples.py
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


def bode_data(sys, w):
    """返回 (mag_dB, phase_deg)，用 frequency_response 取数据自己画。"""
    r = ct.frequency_response(sys, w)
    mag = 20 * np.log10(np.abs(r.fresp[0, 0, :]))
    pha = np.unwrap(np.angle(r.fresp[0, 0, :])) * 180 / np.pi
    return mag, pha


def style_bode(axm, axp, w, mag, pha, title, ylim_db=None):
    axm.set_xscale("log")
    axp.set_xscale("log")
    axm.plot(w, mag, color=fs.MAG, linewidth=2.0)
    axp.plot(w, pha, color=fs.PHA, linewidth=2.0)
    axm.set_ylabel("L / dB", color=fs.MAG)
    axp.set_ylabel("φ / °", color=fs.PHA)
    axp.set_xlabel("ω / (rad/s)")
    axm.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    axp.axhline(-180, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    for ax in (axm, axp):
        ax.grid(True, which="both", color=fs.GRID, linewidth=0.5, alpha=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    if ylim_db:
        axm.set_ylim(*ylim_db)
    axm.set_title(title, pad=8)


# ================================================================ 例5-6
sys56 = ct.tf([2000, -4000], np.polymul(np.polymul([1, 0, 0], [1, 1]), [1, 10, 400]))
w = np.logspace(-1.5, 2.6, 3000)
mag, pha = bode_data(sys56, w)
wa = np.array([1e-1, 1, 2, 20, 400.0])          # 渐近线折点
La = np.array([20 - 40 * np.log10(1e-1 / 1),    # ω=1 处 20 dB
               20,
               20 - 60 * np.log10(2 / 1),
               20 - 60 * np.log10(2) - 40 * np.log10(20 / 2),
               0])
La[4] = La[3] - 80 * np.log10(400 / 20)
fig, axs = plt.subplots(2, 1, figsize=(7.4, 6.0), sharex=True)
style_bode(axs[0], axs[1], w, mag, pha, "例5-6  非最小相位系统的对数幅频渐近线", (-90, 60))
axs[0].plot(wa, La, color=fs.PHA, linewidth=1.6, linestyle=(0, (6, 4)),
            label="渐近线")
for xv, lab in ((1, "1"), (2, "2"), (20, "20")):
    axs[0].axvline(xv, color=fs.SUB, linewidth=1.0, linestyle=(0, (4, 3)))
    axs[0].annotate(lab, xy=(xv, -84), color=fs.SUB, fontsize=11, ha="center")
axs[0].annotate("(1, 20 dB)", xy=(1, 20), xytext=(-0.55, 32), color=fs.INK, fontsize=11)
axs[0].legend(loc="upper right", fontsize=11)
save(fig, "频域-例56-非最小相位渐近线.png")
print("例5-6  L(1)=%.2f dB" % np.interp(np.log10(1), np.log10(w), mag))

# ================================================================ 例5-7
sys57 = ct.tf([1, 0], np.polymul([1 / 3.98, 1],
                                 [1 / 50.1 ** 2, 0.408 / 50.1, 1]))
w = np.logspace(-2, 3, 3000)
mag, pha = bode_data(sys57, w)
wa = np.array([1e-2, 3.98, 50.1, 1e3])
La = np.array([20 * np.log10(1e-2), 20 * np.log10(3.98), 20 * np.log10(3.98),
               20 * np.log10(3.98) - 40 * np.log10(1e3 / 50.1)])
fig, axs = plt.subplots(2, 1, figsize=(7.4, 6.0), sharex=True)
style_bode(axs[0], axs[1], w, mag, pha, "例5-7  实测对数幅频曲线与渐近线", (-70, 40))
axs[0].plot(wa, La, color=fs.PHA, linewidth=1.6, linestyle=(0, (6, 4)),
            label="渐近线（基线）")
for xv in (3.98, 50.1):
    axs[0].axvline(xv, color=fs.SUB, linewidth=1.0, linestyle=(0, (4, 3)))
axs[0].annotate("3.98", xy=(3.98, -66), color=fs.SUB, fontsize=11, ha="center")
axs[0].annotate("50.1", xy=(50.1, -66), color=fs.SUB, fontsize=11, ha="center")
wpk = 50.1 * np.sqrt(1 - 2 * 0.204 ** 2)
print("例5-7  峰频 %.2f、峰值 %.2f dB、基线 %.2f dB、Mr=%.3f"
      % (wpk, np.interp(np.log10(wpk), np.log10(w), mag),
         20 * np.log10(3.98), 10 ** ((np.interp(np.log10(wpk), np.log10(w), mag)
                                      - 20 * np.log10(3.98)) / 20)))
axs[0].plot([wpk], [np.interp(np.log10(wpk), np.log10(w), mag)], marker="o",
            color=fs.INK, markersize=6)
axs[0].annotate("谐振峰 ≈ 20 dB", xy=(wpk, np.interp(np.log10(wpk), np.log10(w), mag)),
                xytext=(6, 12), textcoords="offset points", color=fs.INK, fontsize=11)
axs[0].annotate("基线 12 dB", xy=(20, 20 * np.log10(3.98)), xytext=(26, 14),
                textcoords="offset points", color=fs.PHA, fontsize=11)
axs[0].legend(loc="lower left", fontsize=11)
save(fig, "频域-例57-实测幅频辨识.png")

# ================================================================ 例5-13
z = np.linspace(0.02, 1.0, 900)
gam = np.degrees(np.arctan(2 * z / np.sqrt(np.sqrt(4 * z ** 4 + 1) - 2 * z ** 2)))
fig, ax = plt.subplots(figsize=(6.8, 5.2))
ax.plot(z, gam, color=fs.MAG, linewidth=2.2)
ax.set_xlabel("阻尼比 ζ")
ax.set_ylabel("相角裕度 γ / °", color=fs.MAG)
ax.grid(True, color=fs.GRID, linewidth=0.6, alpha=0.85)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
zs = np.sqrt(3 / 8)
gs = np.degrees(np.arctan(2 * zs / np.sqrt(np.sqrt(4 * zs ** 4 + 1) - 2 * zs ** 2)))
ax.plot([zs], [gs], marker="o", color=fs.PHA, markersize=7)
ax.annotate("ζ = 0.612\nγ = 60.0°", xy=(zs, gs), xytext=(18, -26),
            textcoords="offset points", color=fs.PHA, fontsize=11.5)
ax.axhline(60, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
ax.set_title("例5-13  典型二阶系统的 γ—ζ 关系（$\\gamma$ 只与 ζ 有关）".replace("$\\gamma$", "γ"), pad=8)
print("例5-13  ζ=√(3/8)=%.4f 时 γ=%.2f°" % (zs, gs))
save(fig, "频域-例513-相角裕度与阻尼比.png")

# ================================================================ 例5-14
fig, axs = plt.subplots(2, 1, figsize=(7.4, 6.0), sharex=True)
w = np.logspace(-1, 2.5, 3000)
for K, color, lab in ((5, fs.MAG, "K = 5"), (20, fs.PHA, "K = 20")):
    sys = ct.tf([K], np.polymul([1, 0], np.polymul([1, 1], [0.1, 1])))
    mag, pha = bode_data(sys, w)
    axs[0].plot(w, mag, color=color, linewidth=2.0, label=lab)
    axs[1].plot(w, pha, color=color, linewidth=2.0, label=lab)
    gm, pm, wg, wc = ct.margin(sys)
    print("例5-14  K=%2d: ωc=%.3f  γ=%.1f°  ωg=%.3f  h=%.3f (%.2f dB)"
          % (K, wc, pm, wg, 1 / gm if gm else np.inf, 20 * np.log10(gm) if gm else 0))
axs[0].set_ylabel("L / dB")
axs[1].set_ylabel("φ / °")
axs[1].set_xlabel("ω / (rad/s)")
for ax in axs:
    ax.set_xscale("log")
    ax.grid(True, which="both", color=fs.GRID, linewidth=0.5, alpha=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="upper right", fontsize=11)
axs[0].axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axs[1].axhline(-180, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axs[0].axvline(2.1, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axs[0].axvline(4.23, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
axs[0].set_title("例5-14  增益对相角裕度与幅值裕度的影响", pad=8)
save(fig, "频域-例514-增益与裕度.png")


# ================================================================ 例题三联图（例5-17 / 例5-18）
def example_triptych(name, title, Gs, tmax, wlim, lab_c="闭环"):
    Phi = ct.feedback(Gs, 1)
    fig, axs = plt.subplots(2, 2, figsize=(9.2, 7.0))
    axm, axp, axc, axt = axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]
    w = np.logspace(*wlim, 3000)
    mag, pha = bode_data(Gs, w)
    style_bode(axm, axp, w, mag, pha, title)
    gm, pm, wg, wc = ct.margin(Gs)
    axm.axvline(wc, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    axp.axvline(wc, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    axm.annotate("ωc = %.4g" % wc, xy=(wc, max(mag) - 4), xytext=(6, 0),
                 textcoords="offset points", color=fs.INK, fontsize=11)
    axp.annotate("γ = %.1f°" % pm, xy=(wc, -180), xytext=(6, -22),
                 textcoords="offset points", color=fs.PHA, fontsize=11)
    if gm and np.isfinite(gm):
        axm.annotate("h = %.2f (%.1f dB)" % (gm, 20 * np.log10(gm)),
                     xy=(wg, -20 * np.log10(gm)), xytext=(-8, -26),
                     textcoords="offset points", color=fs.MAG, fontsize=11, ha="right")
        axp.axvline(wg, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
        axp.annotate("ωg = %.4g" % wg, xy=(wg, -180), xytext=(6, -40),
                     textcoords="offset points", color=fs.INK, fontsize=11)
    magc, phac = bode_data(Phi, w)
    axc.semilogx(w, magc, color=fs.MAG, linewidth=2.0)
    axc.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    axc.axhline(-3, color=fs.PHA, linewidth=0.9, linestyle=(0, (4, 3)))
    axc.set_ylabel("20lg|Φ| / dB", color=fs.MAG)
    axc.set_xlabel("ω / (rad/s)")
    axc.grid(True, which="both", color=fs.GRID, linewidth=0.5, alpha=0.8)
    for s in ("top", "right"):
        axc.spines[s].set_visible(False)
    wb = ct.bandwidth(Phi)
    ipk = int(np.argmax(magc))
    axc.plot([w[ipk]], [magc[ipk]], marker="o", color=fs.INK, markersize=6)
    axc.annotate("Mr = %.3f (%.2f dB)\nωr = %.4g" % (10 ** (magc[ipk] / 20), magc[ipk], w[ipk]),
                 xy=(w[ipk], magc[ipk]), xytext=(8, -30), textcoords="offset points",
                 color=fs.INK, fontsize=11)
    axc.annotate("ωb = %.4g" % wb, xy=(wb, -3), xytext=(8, 8),
                 textcoords="offset points", color=fs.PHA, fontsize=11)
    axc.set_title(lab_c + "幅频（含 Mr、ωb）", pad=8)
    t = np.linspace(0, tmax, 4000)
    tt, yy = ct.step_response(Phi, t)
    info = ct.step_info(Phi)                 # 默认 2% 误差带
    info5 = ct.step_info(Phi, SettlingTimeThreshold=0.05)
    axt.plot(tt, yy, color=fs.MAG, linewidth=2.0)
    axt.axhline(1, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    axt.axhspan(0.95, 1.05, color=fs.FILL, zorder=0)
    axt.set_xlabel("t / s")
    axt.set_ylabel("c(t)")
    axt.grid(True, color=fs.GRID, linewidth=0.5, alpha=0.8)
    for s in ("top", "right"):
        axt.spines[s].set_visible(False)
    osig = (max(yy) - 1) * 100
    axt.set_title("阶跃响应（σ%% = %.1f%%，ts(2%%) ≈ %.4g）" % (osig, info["SettlingTime"]), pad=8)
    fig.tight_layout()
    save(fig, name)
    print("  %s: ωc=%.4g γ=%.2f° h=%.2f(%.1fdB) Mr=%.3f ωr=%.4g ωb=%.4g σ%%=%.1f%% ts2%%=%.4g ts5%%=%.4g tp=%.4g"
          % (name, wc, pm, gm if gm else float("inf"),
             20 * np.log10(gm) if gm else 0, 10 ** (magc[ipk] / 20), w[ipk], wb,
             osig, info["SettlingTime"], info5["SettlingTime"], info["PeakTime"]))


sys17 = ct.tf([2], np.polymul([1, 0], np.polymul([1, 1], [1, 2])))
example_triptych("频域-例517-雕刻机.png",
                 "例5-17  雕刻机：开环 L 与 φ（K1 = 2）",
                 sys17, 25, (-2, 1.6))

num18 = [100, 100]
den18 = np.polymul(np.polymul([0.001, 1], [1 / 20, 1]),
                   np.polymul([1, 0], [(1 / 18850) ** 2, 2 * 0.3 / 18850, 1]))
sys18 = ct.tf(num18, den18)
example_triptych("频域-例518-磁盘驱动.png",
                 "例5-18  磁盘驱动：开环 L 与 φ（K = 100）",
                 sys18, 0.02, (2, 5.5))

# ================================================================ 渐近线反求算例
w = np.logspace(-0.3, 1.6, 300)
seg = [(np.array([0.5, 2]), np.array([20 + 20 * np.log10(0.5 / 1) + 20 * np.log10(1 / 0.5) - 20 * np.log10(1 / 0.5), 0])), ]
fig, ax = plt.subplots(figsize=(7.4, 4.6))
wa = np.array([0.5, 2, 10, 40.0])
La = np.array([20 + 20 * np.log10(1 / 0.5), 20 - 20 * np.log10(2), 0, 0])
La[0] = 20 - 20 * np.log10(0.5)          # ω=1 处 20 dB
La[1] = La[0] - 20 * np.log10(2 / 0.5)
La[2] = La[1] - 40 * np.log10(10 / 2)
La[3] = La[2] - 60 * np.log10(40 / 10)
ax.semilogx(wa, La, color=fs.MAG, linewidth=2.2)
ax.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
for xv, lab in ((0.5, "0.5"), (2, "2"), (10, "10")):
    ax.axvline(xv, color=fs.SUB, linewidth=1.0, linestyle=(0, (4, 3)))
ax.annotate("−20 dB/dec", xy=(1.0, 16), color=fs.MAG, fontsize=11.5)
ax.annotate("−40 dB/dec", xy=(4.4, 2), color=fs.MAG, fontsize=11.5)
ax.annotate("−60 dB/dec", xy=(20, -18), color=fs.MAG, fontsize=11.5)
ax.annotate("(1, 20 dB)", xy=(1, 20), xytext=(8, 10), textcoords="offset points",
            color=fs.INK, fontsize=11)
ax.annotate("(2, 14 dB)", xy=(2, 14), xytext=(10, 12), textcoords="offset points",
            color=fs.INK, fontsize=11)
ax.annotate("(10, −14 dB)", xy=(10, -14), xytext=(10, 12), textcoords="offset points",
            color=fs.INK, fontsize=11)
ax.set_xlabel("ω / (rad/s)")
ax.set_ylabel("L / dB", color=fs.MAG)
ax.grid(True, which="both", color=fs.GRID, linewidth=0.5, alpha=0.8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_title("渐近线反求算例：G = 10/[s(0.5s+1)(0.1s+1)]", pad=8)
save(fig, "频域-算例-渐近线反求.png")
