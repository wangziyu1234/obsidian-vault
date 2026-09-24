# -*- coding: utf-8 -*-
"""第5章例题补图（二）：全部单图，伯德类统一「单轴 + 左右双刻度」。

  频域-例56-非最小相位渐近线.png   05-1-3 例5-6（折线渐近线 + 精确曲线）
  频域-例57-实测幅频辨识.png       05-3-2 例5-7
  频域-例513-相角裕度与阻尼比.png  05-3-b-2 例5-13（单图）
  频域-例514-增益与裕度.png        05-2-d 例5-14（K=5 与 K=20 对照）
  频域-例517-开环Bode.png / -闭环幅频.png / -阶跃响应.png     05-3-b-1 例5-17
  频域-例518-开环Bode.png / -闭环幅频.png / -阶跃响应.png     05-3-b-1 例5-18
  频域-算例-渐近线反求.png         05-3-2 反求例（单图）

图内文字不混用中文与 `$…$`；说明放笔记题注，图内只留短标注。
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


def fdata(sys, w):
    r = ct.frequency_response(sys, w)
    mag = 20 * np.log10(np.abs(r.fresp[0, 0, :]))
    pha = np.unwrap(np.angle(r.fresp[0, 0, :])) * 180 / np.pi
    return mag, pha


def bode_axes(w, ylim_db, ylim_ph, yticks_ph=(-180, -90, 0, 90)):
    """上下两层：上幅频 L/dB、下相频 φ/°，共用横轴（与典型环节伯德图一致）。"""
    fig, (axm, axp) = fs.new_bode_axes(figsize=(6.6, 6.4))
    for ax in (axm, axp):
        ax.set_xscale("log")
        ax.set_xlim(w[0], w[-1])
        fs.tidy(ax)
    axm.set_ylim(*ylim_db)
    axp.set_ylim(*ylim_ph)
    axp.set_yticks(list(yticks_ph))
    axm.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    axp.axhline(-180, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    return fig, axm, axp


def single(title, xlabel, ylabel, figsize=(6.0, 4.6)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(True, color=fs.GRID, linewidth=0.6, alpha=0.85)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=8)
    # 默认底边距会把 xlabel 的下沿挤出画布（自检报 [越界] 2~5px），留宽一点
    fig.subplots_adjust(bottom=0.135, top=0.90)
    return fig, ax


# ================================================================ 例5-6
sys56 = ct.tf([2000, -4000], np.polymul(np.polymul([1, 0, 0], [1, 1]), [1, 10, 400]))
w = np.logspace(-1.5, 2.6, 3000)
mag, pha = fdata(sys56, w)
fig, ax, ax2 = bode_axes(w, (-90, 60), (-380, 40), (-360, -270, -180, -90, 0))
ax.plot(w, mag, color=fs.MAG, linewidth=2.0)
ax2.plot(w, pha, color=fs.PHA, linewidth=2.0)
wa = np.array([1e-1, 1, 2, 20, 400.0])
La = np.zeros(5)
La[0] = 20 - 40 * np.log10(1e-1)
La[1] = 20
La[2] = 20 - 60 * np.log10(2)
La[3] = La[2] - 40 * np.log10(20 / 2)
La[4] = La[3] - 80 * np.log10(400 / 20)
ax.plot(wa, La, color=fs.INK, linewidth=1.4, linestyle=(0, (6, 4)))
for xv, lab in ((1, "1"), (2, "2"), (20, "20")):
    ax.axvline(xv, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    # 转折频率标签摆竖线**右侧**（ha="left"），别骑在线上把线咬断
    ax.annotate(lab, xy=(xv, -85), xytext=(5, 0), textcoords="offset points",
                color=fs.SUB, fontsize=10.5, ha="left", va="center")
ax.annotate("渐近线过 (1, 20 dB)", xy=(1, 20), xytext=(-0.5, 34), color=fs.INK, fontsize=11)
# 斜率串拆两行并整体左移到 ω=0.045：写成一行会横跨到 ω=1 以外，正好压住竖虚线
ax.annotate("−40 → −60 →" "\n" "−40 → −80 dB/dec", xy=(0.045, -58),
            color=fs.INK, fontsize=11, va="top")
ax.set_title("例5-6  非最小相位系统的对数幅频渐近线（实线精确、点线渐近）", pad=8)
save(fig, "频域-例56-非最小相位渐近线.png")
print("例5-6  L(1)=%.2f dB" % np.interp(np.log10(1), np.log10(w), mag))

# ================================================================ 例5-7
sys57 = ct.tf([1, 0], np.polymul([1 / 3.98, 1],
                                 [1 / 50.1 ** 2, 0.408 / 50.1, 1]))
w = np.logspace(-2, 3, 3000)
mag, pha = fdata(sys57, w)
fig, ax, ax2 = bode_axes(w, (-70, 40), (-200, 20), (-180, -90, 0))
ax.plot(w, mag, color=fs.MAG, linewidth=2.0)
ax2.plot(w, pha, color=fs.PHA, linewidth=2.0)
wa = np.array([1e-2, 3.98, 50.1, 1e3])
La = np.array([20 * np.log10(1e-2), 20 * np.log10(3.98), 20 * np.log10(3.98),
               20 * np.log10(3.98) - 40 * np.log10(1e3 / 50.1)])
ax.plot(wa, La, color=fs.INK, linewidth=1.4, linestyle=(0, (6, 4)))
for xv, lab in ((3.98, "3.98"), (50.1, "50.1")):
    ax.axvline(xv, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    # 同样摆竖线右侧，不骑线
    ax.annotate(lab, xy=(xv, -66), xytext=(5, 0), textcoords="offset points",
                color=fs.SUB, fontsize=10.5, ha="left", va="center")
wpk = 50.1 * np.sqrt(1 - 2 * 0.204 ** 2)
mpk = np.interp(np.log10(wpk), np.log10(w), mag)
ax.plot([wpk], [mpk], marker="o", color=fs.INK, markersize=6)
ax.annotate("谐振峰 ≈ 20 dB", xy=(wpk, mpk), xytext=(8, 10),
            textcoords="offset points", color=fs.INK, fontsize=11)
# "基线 12 dB"贴着水平段放会压住实线与渐近线；沉到段下方再用细引线连回，
# 并整体落在两条转折竖线（3.98 / 50.1）之间，免得压住竖线
ax.annotate("基线 12 dB", xy=(6, 12), xytext=(0, -62), textcoords="offset points",
            color=fs.SUB, fontsize=11,
            arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.SUB))
ax.set_title("例5-7  实测对数幅频曲线（实线）与渐近线/基线（点线）", pad=8)
save(fig, "频域-例57-实测幅频辨识.png")
print("例5-7  峰频 %.2f、峰值 %.2f dB、基线 12.00 dB" % (wpk, mpk))

# ================================================================ 例5-13（单图）
z = np.linspace(0.02, 1.0, 900)
gam = np.degrees(np.arctan(2 * z / np.sqrt(np.sqrt(4 * z ** 4 + 1) - 2 * z ** 2)))
fig, ax = single("例5-13  典型二阶系统的 γ—ζ 关系", "阻尼比 ζ", "相角裕度 γ / °",
                 (6.2, 4.4))
ax.plot(z, gam, color=fs.MAG, linewidth=2.2)
zs = np.sqrt(3 / 8)
gs = np.degrees(np.arctan(2 * zs / np.sqrt(np.sqrt(4 * zs ** 4 + 1) - 2 * zs ** 2)))
ax.plot([zs], [gs], marker="o", color=fs.PHA, markersize=7)
ax.annotate("ζ = 0.612\nγ = 60.0°", xy=(zs, gs), xytext=(18, -30),
            textcoords="offset points", color=fs.PHA, fontsize=11.5)
ax.axhline(60, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
save(fig, "频域-例513-相角裕度与阻尼比.png")
print("例5-13  ζ=√(3/8)=%.4f 时 γ=%.2f°" % (zs, gs))

# ================================================================ 例5-14
w = np.logspace(-1, 2.5, 3000)
fig, ax, ax2 = bode_axes(w, (-50, 40), (-280, -60), (-270, -180, -90))
for K, ls, lab in ((5, "-", "K = 5"), (20, (0, (6, 4)), "K = 20")):
    sys = ct.tf([K], np.polymul([1, 0], np.polymul([1, 1], [0.1, 1])))
    mag, pha = fdata(sys, w)
    ax.plot(w, mag, color=fs.MAG, linewidth=2.0, linestyle=ls, label=lab)
    ax2.plot(w, pha, color=fs.PHA, linewidth=2.0, linestyle=ls, label=lab)
    gm, pm, wg, wc = ct.margin(sys)
    print("例5-14  K=%2d: ωc=%.3f γ=%.1f° ωg=%.3f h=%.2f (%.2f dB)"
          % (K, wc, pm, wg, gm, 20 * np.log10(gm)))
ax.axvline(2.1, color=fs.SUB, linewidth=0.9, linestyle=(0, (2, 3)))
ax.axvline(3.162, color=fs.SUB, linewidth=0.9, linestyle=(0, (2, 3)))
# 幅频：右上角被图例占了，曲线又斜穿全图，安全空区只剩左下角 → ωc 标注放左下。
# 相频：左下角被图例占了 → ωg 标注放右上角，两者都用细引线连回目标点。
ax.annotate("ωc = 2.10（K = 5）", xy=(2.1, 0), xytext=(0.03, 0.34),
            textcoords="axes fraction", color=fs.INK, fontsize=10.5,
            ha="left", va="top",
            arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.INK))
ax.annotate("ωc = 4.23（K = 20）", xy=(4.23, 0), xytext=(0.03, 0.18),
            textcoords="axes fraction", color=fs.INK, fontsize=10.5,
            ha="left", va="top",
            arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.INK))
ax2.annotate("ωg = 3.16（两种增益相同）", xy=(3.162, -180), xytext=(0.97, 0.90),
             textcoords="axes fraction", color=fs.SUB, fontsize=10.5,
             ha="right", va="top",
             arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.SUB))
ax.legend(loc="upper right", fontsize=11)
ax2.legend(loc="lower left", fontsize=11)
ax.set_title("例5-14  增益对裕度的影响（蓝 L、红 φ；实线 K = 5，虚线 K = 20）", pad=8)
save(fig, "频域-例514-增益与裕度.png")


# ================================================================ 例题三张单图
def example_three(prefix, title, Gs, tmax, wlim, ylim_db, ylim_ph):
    Phi = ct.feedback(Gs, 1)
    w = np.logspace(*wlim, 3000)
    mag, pha = fdata(Gs, w)
    fig, ax, ax2 = bode_axes(w, ylim_db, ylim_ph)
    ax.plot(w, mag, color=fs.MAG, linewidth=2.0)
    ax2.plot(w, pha, color=fs.PHA, linewidth=2.0)
    gm, pm, wg, wc = ct.margin(Gs)
    ax.axvline(wc, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    ax2.axvline(wg, color=fs.SUB, linewidth=0.9, linestyle=(0, (2, 3)))
    ax.annotate("ωc = %.4g" % wc, xy=(wc, ylim_db[1] - 6), xytext=(6, 0),
                textcoords="offset points", color=fs.INK, fontsize=11)
    # γ 标注放 -180° 线下方、且留在 wc 左侧（wc 右边有 ωg 竖线，框跨过去会压线）
    ax2.annotate("γ = %.1f°" % pm, xy=(wc, -180), xytext=(-8, -22),
                 textcoords="offset points", color=fs.PHA, fontsize=11,
                 ha="right")
    if gm and np.isfinite(gm):
        # 幅频曲线斜穿全图，"贴着交点放"必然压住下降段（例5-17/5-18 各咬掉
        # 150 个采样点）。安全空区只有左下角（低频高幅值、此处无曲线），
        # 故标注统一沉到左下，再用细引线连回 (ωg, -20lg h)。
        ax.annotate("h = %.2f（%.1f dB）" % (gm, 20 * np.log10(gm)),
                    xy=(wg, -20 * np.log10(gm)), xytext=(0.03, 0.06),
                    textcoords="axes fraction", color=fs.MAG, fontsize=11,
                    ha="left", va="bottom",
                    arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.MAG))
        ax2.annotate("ωg = %.4g" % wg, xy=(wg, -180), xytext=(8, -42),
                     textcoords="offset points", color=fs.SUB, fontsize=10.5)
    ax.set_title(title + "  开环对数频率特性", pad=8)
    save(fig, "频域-%s-开环Bode.png" % prefix)

    magc, _ = fdata(Phi, w)
    fig, ax = single(title + "  闭环幅频", "ω / (rad/s)", "20lg|Φ| / dB", (6.2, 4.6))
    ax.set_xscale("log")
    ax.plot(w, magc, color=fs.MAG, linewidth=2.2)
    # 顶部留出 20 dB 空白专门放 Mr 标注（两行框约 36px 高，留少了会顶出轴外撞标题）
    ax.set_ylim(top=float(magc.max()) + 28.0)
    ax.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    ax.axhline(-3, color=fs.PHA, linewidth=0.9, linestyle=(0, (4, 3)))
    wb = ct.bandwidth(Phi)
    ipk = int(np.argmax(magc))
    ax.plot([w[ipk]], [magc[ipk]], marker="o", color=fs.INK, markersize=6)
    ax.plot([wb], [-3], marker="o", color=fs.PHA, markersize=6)
    # Mr 标注抬到谐振峰**上方**：峰值是整条曲线的最高点，上方必然是空的；
    # 原来放右下，正好压在高频下降段上（例5-18 咬掉 315 个采样点）。
    ax.annotate("Mr = %.3f（%.2f dB）\nωr = %.4g" % (10 ** (magc[ipk] / 20), magc[ipk], w[ipk]),
                xy=(w[ipk], magc[ipk]), xytext=(8, 14), textcoords="offset points",
                color=fs.INK, fontsize=11, va="bottom")
    ax.annotate("ωb = %.4g（−3 dB）" % wb, xy=(wb, -3), xytext=(10, 10),
                textcoords="offset points", color=fs.PHA, fontsize=11)
    save(fig, "频域-%s-闭环幅频.png" % prefix)

    t = np.linspace(0, tmax, 4000)
    tt, yy = ct.step_response(Phi, t)
    info = ct.step_info(Phi)
    info5 = ct.step_info(Phi, SettlingTimeThreshold=0.05)
    fig, ax = single(title + "  单位阶跃响应", "t / s", "c(t)", (6.2, 4.6))
    ax.plot(tt, yy, color=fs.MAG, linewidth=2.2)
    ax.axhline(1, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
    ax.axhspan(0.95, 1.05, color=fs.FILL, zorder=0)
    osig = (max(yy) - 1) * 100
    # 峰值附近曲线密集，贴着放必然压住上升/下降沿；改放右下角空区 + 细引线
    ax.annotate("σ%% = %.1f%%\ntp = %.3g s" % (osig, info["PeakTime"]),
                xy=(info["PeakTime"], max(yy)), xytext=(0.60, 0.10),
                textcoords="axes fraction", color=fs.PHA, fontsize=11,
                ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-", lw=0.8, color=fs.PHA))
    ax.annotate("ts(5%%) = %.3g s" % info5["SettlingTime"], xy=(info5["SettlingTime"], 1.05),
                xytext=(10, 14), textcoords="offset points", color=fs.INK, fontsize=11)
    save(fig, "频域-%s-阶跃响应.png" % prefix)
    print("  %s: ωc=%.4g γ=%.2f° h=%.2f(%.1fdB) Mr=%.3f ωr=%.4g ωb=%.4g "
          "σ%%=%.1f%% ts2%%=%.4g ts5%%=%.4g tp=%.4g"
          % (prefix, wc, pm, gm if gm else float("inf"),
             20 * np.log10(gm) if gm else 0, 10 ** (magc[ipk] / 20), w[ipk], wb,
             osig, info["SettlingTime"], info5["SettlingTime"], info["PeakTime"]))


sys17 = ct.tf([2], np.polymul([1, 0], np.polymul([1, 1], [1, 2])))
example_three("例517", "例5-17 雕刻机（K1 = 2）", sys17, 25, (-2, 1.6), (-95, 35), (-280, -60))

num18 = [100, 100]
den18 = np.polymul(np.polymul([0.001, 1], [1 / 20, 1]),
                   np.polymul([1, 0], [(1 / 18850) ** 2, 2 * 0.3 / 18850, 1]))
sys18 = ct.tf(num18, den18)
example_three("例518", "例5-18 磁盘驱动（K = 100）", sys18, 0.02, (2, 5.5), (-80, 40), (-360, -60))

# ================================================================ 渐近线反求算例（单图）
fig, ax = single("渐近线反求算例：G = 10/[s(0.5s+1)(0.1s+1)]", "ω / (rad/s)", "L / dB",
                 (6.6, 4.4))
ax.set_xscale("log")
wa = np.array([0.5, 2, 10, 40.0])
La = np.zeros(4)
La[0] = 20 - 20 * np.log10(0.5)
La[1] = La[0] - 20 * np.log10(2 / 0.5)
La[2] = La[1] - 40 * np.log10(10 / 2)
La[3] = La[2] - 60 * np.log10(40 / 10)
ax.plot(wa, La, color=fs.MAG, linewidth=2.2)
ax.axhline(0, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
for xv in (0.5, 2, 10):
    ax.axvline(xv, color=fs.SUB, linewidth=0.9, linestyle=(0, (4, 3)))
# 斜率标签放到折线**外侧**的空档（后两段折线很陡，放"下方"仍会被折线穿过，
# 改放"上方"）：判据是框顶/框底必须越过折线在框右端的取值。
ax.annotate("−20 dB/dec", xy=(0.6, 9), color=fs.MAG, fontsize=11.5, va="bottom")
ax.annotate("−40 dB/dec", xy=(4.4, 6), color=fs.MAG, fontsize=11.5, va="bottom")
ax.annotate("−60 dB/dec", xy=(20, -20), color=fs.MAG, fontsize=11.5, va="bottom")
for xy, lab in (((1, 20), "(1, 20 dB)"), ((2, 14), "(2, 14 dB)"), ((10, -14), "(10, −14 dB)")):
    # 抬到折线之上，且起点留在折点右侧，避免压住 ω=0.5 的竖虚线
    ax.annotate(lab, xy=xy, xytext=(6, 6), textcoords="offset points",
                color=fs.INK, fontsize=11, va="bottom")
save(fig, "频域-算例-渐近线反求.png")
