# figure: 频域-幅相-零点组合-0型左右零点.png
"""Zero-combination Nyquist figures for 05-1-3-b-8.

Each figure isolates one row of the endpoint table: what a left/right real
zero, a complex-conjugate pair, and the out-of-table elements (all-pass,
unstable inertia) do to the shape and to the continuous end phase.
Every branch and crossing used in the captions is asserted below.

Build: .\\build.ps1 -File .\\zero-combination-nyquist.py
"""
from __future__ import annotations
import os
from pathlib import Path

import numpy as np
import control as ct
from scipy import signal

import figures_style as fs
from _nyquist_style import canvas, curve, response, point, note, finish, BOX

s = ct.tf("s")
W = np.geomspace(1e-4, 1e4, 20000)
OUT = Path(os.environ.get("FIGURE_OUT", fs.ATTACH_DIR / "unused.png")).parent

# --- 0 型：两惯性 + 一个实零点（τ = 0.5 < T₁ + T₂）------------------------
TAU, T1, T2 = 0.5, 1.0, 2.0
G0L = (1 + TAU * s) / ((1 + T1 * s) * (1 + T2 * s))
G0R = (1 - TAU * s) / ((1 + T1 * s) * (1 + T2 * s))

# --- Ⅰ 型：两惯性 + 一对共轭复零点（尾一标准形，常数项归一到 1）----------
ZT, ZT1, ZT2, ZETA = 4.0, 1.0, 2.0, 0.5
Q_L = (s / ZT) ** 2 + 2 * ZETA * (s / ZT) + 1
Q_R = (s / ZT) ** 2 - 2 * ZETA * (s / ZT) + 1
GIL = Q_L / (s * (1 + ZT1 * s) * (1 + ZT2 * s))
GIR = Q_R / (s * (1 + ZT1 * s) * (1 + ZT2 * s))
CROSS_WINDOW = (0.2, 2.0)          # 两对复零点各在此窗口内穿一次负实轴

# --- 表外元素 -------------------------------------------------------------
T_AP = 1.0
GAP = (1 - T_AP * s) / (1 + T_AP * s)
GUN = 1.0 / (1 - T_AP * s)


def value_at(system, omega):
    return complex(response(system, [omega])[0])


def crossings(system, part, lo=1e-3, hi=1e4):
    """正频率上 imag（穿实轴）或 real（穿虚轴）的全部变号点，二分后返回 (ω, 交点值)。"""
    def g(omega):
        v = response(system, [omega])[0]
        return v.imag if part == "imag" else v.real

    w = np.geomspace(lo, hi, 40000)
    vals = np.array([g(x) for x in w])
    idx = np.where(np.diff(np.sign(vals)) != 0)[0]
    out = []
    for i in idx:
        a, b = w[i], w[i + 1]
        for _ in range(200):
            m = np.sqrt(a * b)
            if np.sign(g(m)) == np.sign(g(a)):
                a = m
            else:
                b = m
        root = np.sqrt(a * b)
        out.append((root, value_at(system, root)))
    return out


# 两对复零点的穿轴点一次算好，供校验与绘图共用
ZL_CROSS = crossings(GIL, "imag", *CROSS_WINDOW)[0][1]
ZR_CROSS = crossings(GIR, "imag", *CROSS_WINDOW)[0][1]


def branch_phase(system, ref, at):
    """把数值相角整体平移，使 ω = at 处的相角等于 ref，得到连续分支。"""
    z = response(system, W)
    phase = np.degrees(np.unwrap(np.angle(z)))
    phase += 360 * np.round((ref - phase[int(np.argmin(np.abs(W - at)))]) / 360)
    return phase


def end_phase(system, lo):
    """从低频角 lo 起展开，返回 (起点角, 终点角)。"""
    phase = branch_phase(system, lo, W[0])
    return phase[0], phase[-1]


def check_phase(system, lo, hi):
    """端点角等于表格值；整段连续分支无 180° 以上的跳变。"""
    z = response(system, W)
    phase = branch_phase(system, lo, W[0])
    assert abs(phase[0] - lo) < 0.5, (phase[0], lo)
    assert abs(phase[-1] - hi) < 0.5, (phase[-1], hi)
    assert np.all(np.abs(np.diff(phase)) < 180), np.abs(np.diff(phase)).max()
    # 复平面上的实际转角必须与分支累计量一致（离散求和最多差一个整圈）
    total = np.sum(np.diff(np.angle(z))) * 180 / np.pi
    assert min(abs((total - (phase[-1] - phase[0])) % 360),
               abs((total - (phase[-1] - phase[0])) % 360 - 360)) < 1e-6, total


def verify():
    # 0 型：起点同为 (K, 0) = (1, 0)；连续终点角 0°→-90° 与 0°→-270°
    for system, lo, hi in [(G0L, 0, -90), (G0R, 0, -270)]:
        check_phase(system, lo, hi)
    for system in (G0L, G0R):
        np.testing.assert_allclose(value_at(system, 1e-6).real, 1.0, rtol=1e-11)
        assert abs(value_at(system, 1e-6) - 1) < 1e-5
    # 实部/虚部解析式（τ 项在实部同号、虚部反号），与 control 对照
    w = np.geomspace(1e-3, 1e3, 500)
    den = (1 + T1**2 * w**2) * (1 + T2**2 * w**2)
    np.testing.assert_allclose(
        response(G0L, w),
        (1 - T1 * T2 * w**2 + TAU * (T1 + T2) * w**2
         - 1j * w * (T1 + T2 - TAU * (1 - T1 * T2 * w**2))) / den,
        rtol=1e-9, atol=1e-13)
    np.testing.assert_allclose(
        response(G0R, w),
        (1 - T1 * T2 * w**2 - TAU * (T1 + T2) * w**2
         - 1j * w * (T1 + T2 + TAU * (1 - T1 * T2 * w**2))) / den,
        rtol=1e-9, atol=1e-13)
    # τ < T₁ + T₂ ⇒ 右零点曲线不在实部零点处穿负实轴，只从左下方绕行
    assert TAU < T1 + T2
    z = response(G0R, w)
    assert not np.any(np.abs(z.imag) < 1e-3 * np.abs(z.real))
    assert z.real.min() > -0.30 and z.imag.min() < -0.70
    # 关于实轴的镜像只是 O(ω) 意义下的：低频实部之差按 O(ω²) 趋零，虚部相反数不符
    for omega in (1e-4, 1e-3, 1e-2):
        a, b = value_at(G0L, omega), value_at(G0R, omega)
        assert abs(a.real - b.real) < 40 * omega**2
    assert abs(value_at(G0L, 1).imag + value_at(G0R, 1).imag) > 0.05

    # Ⅰ 型复零点对（n = 3）：左对 -270°→-90°，右对 -90°→-450°（复零点按二阶计）
    # 左对的低频端与右对的高频端在同一分支上，故用 branch_phase 指定参考点
    assert abs(branch_phase(GIL, -270, W[-1])[-1] + 90) < 0.5     # 左对高频端 -90°
    assert abs(branch_phase(GIR, -270, W[0])[0] + 90) < 0.5       # 右对低频端 -90°
    check_phase(GIR, -90, -450)
    # 两对零点在 ω_z 处相角恰为 ±90°，整体值可用解析式复算
    for system, sign in [(GIL, +1), (GIR, -1)]:
        num = (1j) ** 2 + sign * 2 * ZETA * 1j + 1
        den_z = (1j * ZT) * (1 + 1j * ZT) * (1 + 2j * ZT)
        np.testing.assert_allclose(value_at(system, ZT), num / den_z, rtol=1e-12)
    # 穿轴点：两对都在低频侧穿负实轴，交点在绘制前一次算好
    assert abs(ZL_CROSS.imag) < 1e-4 and ZL_CROSS.real < 0, ZL_CROSS
    assert abs(ZR_CROSS.imag) < 1e-4 and ZR_CROSS.real < 0, ZR_CROSS
    # 表外元素：一阶全通转半圈止于 (-1, 0)；右半极点惯性止于 +90°，P = 1
    check_phase(GAP, 0, -180)
    np.testing.assert_allclose(np.abs(response(GAP, W)), 1, rtol=1e-12)
    assert abs(value_at(GAP, 1) + 1j) < 1e-9           # (1-j)/(1+j) = -j
    check_phase(GUN, 0, 90)
    assert np.all(response(GUN, W).imag >= 0)
    assert abs(value_at(GUN, 1) - (0.5 + 0.5j)) < 1e-9  # 1/(1-j) = (1+j)/2

    # control 与 SciPy 独立复核（同 openloop-nyquist.py 的做法）
    grid = np.geomspace(1e-4, 1e4, 801)
    for model in (G0L, G0R, GIL, GIR, GAP, GUN):
        z_control = response(model, grid)
        _, z_scipy = signal.freqresp((model.num[0][0], model.den[0][0]), grid)
        err = np.max(np.abs(z_control - z_scipy) / (1 + np.abs(z_control)))
        assert err < 1e-12, err
    print("verified: endpoints, crossings, mirror order, unity gain; control/SciPy 6 x 801")


def draw_zero_pair():
    name = "频域-幅相-零点组合-0型左右零点.png"
    fig, ax = canvas("0 型双惯性：左零点与右零点（τ = 0.5，T₁ = 1，T₂ = 2）",
                     r"$G_L=\frac{1+0.5s}{(1+s)(1+2s)},\quad"
                     r"G_R=\frac{1-0.5s}{(1+s)(1+2s)}$",
                     (-0.88, 1.15), (-1.08, 0.34), figsize=(6.6, 6.0))
    curve(ax, G0L, W, (0.35, 1.1), fs.MAG, "左零点：φ 由 0° 到 -90°")
    curve(ax, G0R, W, (0.5, 1.3), fs.PHA, "右零点：φ 由 0° 到 -270°")
    point(ax, 1.0, r"$\omega=0$", (-58, 14), limit=True, color=fs.SUB)
    # ω=2 的点落在曲线自己身上，标签就近摆放必然压线：抬到右上空区再用细引线连回
    z2 = value_at(G0R, 2.0)
    ax.plot(z2.real, z2.imag, "o", ms=5, color=fs.PHA, zorder=7)
    ax.annotate(r"$\omega=2$", (z2.real, z2.imag), xytext=(0.62, 0.22),
                fontsize=11, color=fs.PHA, bbox=BOX, zorder=8, ha="center",
                va="center", arrowprops=dict(arrowstyle="-", linewidth=0.8,
                                             color=fs.SUB))
    point(ax, 0, r"$\omega\to\infty$", (8, 10), limit=True)
    note(ax, "起点同为 (1, 0)：\n多转半圈才到正虚轴", (0.035, 0.86))
    ax.legend(loc="lower left", fontsize=11, bbox_to_anchor=(0.02, 0.12))
    finish(fig, OUT / name, "两条曲线只在低频与高频渐近意义上互为镜像，实部并不处处相等。")


def draw_complex_pair():
    name = "频域-幅相-零点组合-Ⅰ型复零点对.png"
    fig, ax = canvas("Ⅰ型双惯性：一对共轭复零点（ω_z = 4，ζ = 0.5，T₁ = 1，T₂ = 2）",
                     r"$G_L=\frac{(s/4)^2+0.25s+1}{s(1+s)(1+2s)},\quad"
                     r"G_R=\frac{(s/4)^2-0.25s+1}{s(1+s)(1+2s)}$",
                     (-4.6, 1.1), (-5.6, 0.72), figsize=(7.0, 6.0))
    curve(ax, GIL, W, (0.35, 1.4), fs.MAG, "左复零点对：−270°→−90°")
    curve(ax, GIR, W, (0.35, 1.4), fs.PHA, "右复零点对：−90°→−450°")
    point(ax, ZL_CROSS, "跨负实轴", (-40, 26))
    point(ax, 0, r"$\omega\to\infty$", (8, 10), limit=True)
    # 两条曲线绕的圈几乎占满坐标轴，任何够宽的框都会压住低频竖渐近线或纵轴；
    # 而 set_aspect("equal") 又把坐标轴压到画布中间（左右各留约 1/4 空白），
    # 故放弃图例（改在图注里按颜色点名），说明块写到坐标轴右侧的那片画布留白里。
    fig.text(0.985, 0.50, "复零点对\n按二阶计\nΔm_eff = ±2", ha="right", va="center",
             fontsize=10.5, color=fs.SUB, bbox=BOX)
    finish(fig, OUT / name,
           "深蓝：左复零点对 −270°→−90°；赭红：右复零点对 −90°→−450°；"
           "低频竖渐近线同为 −K(T₁+T₂) = −3。")


def draw_out_of_table():
    name = "频域-幅相-零点组合-一阶全通.png"
    fig, ax = canvas("一阶全通（T = 1）", r"$G(s)=(1-s)/(1+s)$",
                     (-1.28, 1.28), (-1.30, 0.45), figsize=(6.6, 4.6))
    curve(ax, GAP, W, (0.35, 0.9, 2.3))
    point(ax, 1.0, r"$\omega=0$", (-40, 28), limit=True, color=fs.SUB)
    point(ax, -1j, r"$\omega=1/T$", (8, -20))
    point(ax, -1.0, r"$\omega\to\infty$", (8, -20), limit=True)
    note(ax, "幅值恒为 1：\n单位圆下半段", (0.035, 0.88))
    # 下半圆只在 y ≤ 0，且框整体右移到 x>0，绕开纵轴与圆的两个端点
    note(ax, "相位由 0° 降到 -180°", (0.55, 0.80))
    finish(fig, OUT / name, "幅值恒为 1 但相位有界：与纯延迟同落单位圆，一个转半圈、一个永远绕。")


def draw_unstable_inertia():
    name = "频域-幅相-零点组合-不稳定惯性.png"
    fig, ax = canvas("右半极点惯性（T = 1）", r"$G(s)=1/(1-s)$",
                     (-0.30, 1.30), (-0.30, 1.30), figsize=(6.6, 5.6))
    curve(ax, GUN, W, (0.35, 0.9, 2.3))
    point(ax, 1.0, r"$\omega=0$", (-58, 12), limit=True, color=fs.SUB)
    point(ax, 1j, r"$\omega=1/T$", (8, 6))
    point(ax, 0, r"$\omega\to\infty$", (8, 10), limit=True)
    # 上半圆只占 y ∈ [0, 0.5]，且两块说明都右移到 x>0，绕开贯穿全高的纵轴
    note(ax, "第一象限：圆心 (1/2, 0)、\n半径 1/2 的上半圆", (0.45, 0.04))
    note(ax, "相位由 0° 升到 +90°（P = 1）", (0.23, 0.92))
    finish(fig, OUT / name, "相频与惯性环节互反；开环右半极点数 P = 1，判稳须按完整奈氏计数。")


if __name__ == "__main__":
    verify()
    draw_zero_pair()
    draw_complex_pair()
    draw_out_of_table()
    draw_unstable_inertia()
