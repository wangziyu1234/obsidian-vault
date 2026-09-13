# figure: 频域-奈氏-0型单惯性.png
"""Nine open-loop shapes and five lecture-example figures.

Build with build.ps1 -File openloop-nyquist.py.  All figures use control's
frequency_response; analytic values are independently asserted below.
FIGURE_ONLY may select one or more output names, separated by semicolons.
FIGURE_OUT supplies the output directory, as in the shared build tool.
"""
from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import control as ct
from scipy import signal
import figures_style as fs
from _nyquist_style import canvas, curve, response, point, note, finish

s = ct.tf("s")
W = np.geomspace(1e-4, 1e4, 18000)
OUT = Path(os.environ.get("FIGURE_OUT", fs.ATTACH_DIR / "unused.png")).parent
ONLY = set(filter(None, os.environ.get("FIGURE_ONLY", "").split(";")))
G1 = 1 / (1 + s)
G02 = 1 / ((1 + s) * (1 + 2*s))
G03 = 1 / ((1 + s) * (1 + 2*s) * (1 + 0.5*s))
GI1 = G1 / s
GI2 = G02 / s
GIZ = (1 + 4*s) * G02 / s
GII1 = G1 / s**2
GII2 = G02 / s**2
GOSC = 1 / (s**2 + s + 1)
GEX1 = 5 * GI2
GEX2 = (1 + 6*s) * G03 / s**2
GEX3 = s**3 / ((s + 0.2) * (s + 1) * (s + 5))


def selected(name):
    return not ONLY or name in ONLY


def verify():
    w = np.geomspace(1e-3, 1e3, 600)
    d = (1+w*w) * (1+4*w*w)
    expected = -15/d - 1j*5*(1-2*w*w)/(w*d)
    np.testing.assert_allclose(response(GEX1, w), expected, rtol=2e-13, atol=2e-13)
    np.testing.assert_allclose(response(GEX1, [1/np.sqrt(2)]), [-10/3], atol=1e-12)
    np.testing.assert_allclose(response(GII2, w),
        -(1-2*w*w)/(w*w*d) + 1j*3/(w*d), rtol=2e-13, atol=1e-10)
    np.testing.assert_allclose(response(GEX2, [1/(2*np.sqrt(2))]), [-128/9], atol=1e-12)
    assert response(GII2, [1e-4])[0].imag > 0
    assert response(GEX2, [1e-4])[0].imag < 0
    assert response(GII2, [1e3])[0].real > 0
    assert response(GEX2, [1e3])[0].imag > 0
    a = 6.2
    d3 = (1+25*w*w)*(1+w*w)*(1+0.04*w*w)
    expected3 = -w**4*(a-w*w)/d3 - 1j*w**3*(1-a*w*w)/d3
    np.testing.assert_allclose(response(GEX3, w), expected3, rtol=3e-13, atol=1e-13)
    np.testing.assert_allclose(response(GEX3, [1/np.sqrt(a)]), [-25/936], atol=1e-13)
    np.testing.assert_allclose(response(GEX3, [np.sqrt(a)]),
        [1j*31*np.sqrt(155)/936], atol=1e-13)
    mag = np.abs(response(GEX3, w))
    assert np.all(mag < 1) and np.all(np.diff(mag) > 0)
    np.testing.assert_allclose(response(G02, [1/np.sqrt(2)]).real, [0], atol=1e-14)
    np.testing.assert_allclose(response(G03, [np.sqrt(3.5)]), [-4/45], atol=1e-13)
    np.testing.assert_allclose(response(GOSC, [1]), [-1j], atol=1e-13)
    for system, lo, hi in [(G1,0,-90),(G02,0,-180),(G03,0,-270),
                            (GI1,-90,-180),(GI2,-90,-270),(GIZ,-90,-180),
                            (GII1,-180,-270),(GII2,-180,-360),(GOSC,0,-180),
                            (GEX2,-180,-360),(GEX3,270,0)]:
        z = response(system, W)
        phase = np.degrees(np.unwrap(np.angle(z)))
        phase += 360 * np.round((lo-phase[0])/360)
        assert abs(phase[0]-lo) < 0.08, (lo,phase[0])
        assert abs(phase[-1]-hi) < 0.08, (hi,phase[-1])
    # Cross-check the numerical evaluator with SciPy on an independent grid.
    grid = np.geomspace(1e-4, 1e4, 801)
    models = (G1,G02,G03,GI1,GI2,GIZ,GII1,GII2,GOSC,GEX1,GEX2,GEX3,
              1/(1-s),1/(s*s-s+1))
    for model in models:
        z_control = response(model, grid)
        _, z_scipy = signal.freqresp((model.num[0][0],model.den[0][0]),grid)
        err = np.max(np.abs(z_control-z_scipy)/(1+np.abs(z_control)))
        assert err < 1e-12, err
    print("verified: analytic crossings, quadrants, phases; control/SciPy 14 x 801 samples")


def shape(name, title, formula, system, limits, arrows, phase, start=None,
          crossing=None, asymptote=None, note_text=None):
    if not selected(name):
        return
    fig, ax = canvas(title, formula, *limits)
    curve(ax, system, W, arrows)
    if asymptote is not None:
        ax.axvline(asymptote, color=fs.SUB, lw=1.1, ls=(0,(4,3)), zorder=2)
        note(ax, rf"$\mathrm{{Re}}\,G\to {asymptote:g}$", (0.025,0.9))
    if start is not None:
        point(ax, start, r"$\omega=0$", (-42,12))
    point(ax, 0, r"$\omega\to\infty$", (9,12), limit=True)
    if crossing is not None:
        value, label, offset = crossing
        point(ax, value, label, offset)
    note(ax, phase)
    if note_text:
        note(ax, note_text, (0.025,0.8))
    finish(fig, OUT/name)


def draw_shapes():
    shape("频域-奈氏-0型单惯性.png", "0 型：单惯性（K = 1，T = 1）",
          r"$G(s)=1/(1+s)$", G1, ((-0.2,1.2),(-0.78,0.22)), (0.65,2.0),
          r"$\varphi:0^\circ\to-90^\circ$", start=1)
    shape("频域-奈氏-0型双惯性.png", "0 型：双惯性（T₁ = 1，T₂ = 2）",
          r"$G(s)=1/[(1+s)(1+2s)]$", G02, ((-0.28,1.18),(-0.84,0.24)), (0.22,0.8),
          r"$\varphi:0^\circ\to-180^\circ$", start=1)
    shape("频域-奈氏-0型三惯性.png", "0 型：三惯性（T₁ = 1，T₂ = 2，T₃ = 0.5）",
          r"$G(s)=1/[(1+s)(1+2s)(1+0.5s)]$", G03,
          ((-0.36,1.18),(-0.86,0.30)), (0.23,0.9),
          r"$\varphi:0^\circ\to-270^\circ$", start=1,
          crossing=(-4/45,r"$-4/45$",(-40,20)))
    shape("频域-奈氏-Ⅰ型单惯性.png", "Ⅰ型：单惯性（K = 1，T = 1）",
          r"$G(s)=1/[s(1+s)]$", GI1, ((-1.55,0.7),(-2.9,0.4)), (0.4,1.1),
          r"$\varphi:-90^\circ\to-180^\circ$", asymptote=-1)
    shape("频域-奈氏-Ⅰ型双惯性.png", "Ⅰ型：双惯性（K = 1，T₁ = 1，T₂ = 2）",
          r"$G(s)=1/[s(1+s)(1+2s)]$", GI2, ((-3.45,0.6),(-3.3,0.65)), (0.21,0.55),
          r"$\varphi:-90^\circ\to-270^\circ$", asymptote=-3,
          crossing=(-2/3,r"$-2/3$",(-25,19)))
    shape("频域-奈氏-Ⅰ型带零点.png", "Ⅰ型：带零点（τ = 4，T₁ = 1，T₂ = 2）",
          r"$G(s)=(1+4s)/[s(1+s)(1+2s)]$", GIZ,
          ((-1.65,1.65),(-3.65,0.5)), (0.35,1.4),
          r"$\varphi:-90^\circ\to-180^\circ$", asymptote=1)
    shape("频域-奈氏-Ⅱ型单惯性.png", "Ⅱ型：单惯性（K = 1，T = 1）",
          r"$G(s)=1/[s^2(1+s)]$", GII1, ((-4.1,0.7),(-0.65,2.4)), (0.52,1.05),
          r"$\varphi:-180^\circ\to-270^\circ$",
          note_text="低频端在第二象限，延伸至图外")
    shape("频域-奈氏-Ⅱ型双惯性.png", "Ⅱ型：双惯性（K = 1，T₁ = 1，T₂ = 2）",
          r"$G(s)=1/[s^2(1+s)(1+2s)]$", GII2,
          ((-4.8,1.6),(-0.9,5.1)), (0.38,0.8),
          r"$\varphi:-180^\circ\to-360^\circ$",
          crossing=(2j*np.sqrt(2)/3,r"$\omega=1/\sqrt{2}$",(13,10)))
    shape("频域-奈氏-0型振荡.png", "0 型：振荡环节（K = 1，ωₙ = 1，ζ = 0.5）",
          r"$G(s)=1/(s^2+s+1)$", GOSC,
          ((-0.6,1.4),(-1.4,0.45)), (0.5,1.45),
          r"$\varphi:0^\circ\to-180^\circ$", start=1,
          crossing=(-1j,r"$\omega_n=1$",(10,-20)))


def draw_type1_example():
    name = "频域-幅相例题-Ⅰ型双惯性.png"
    if not selected(name): return
    fig, ax = canvas("例题：Ⅰ型双惯性系统", r"$G(s)=5/[s(s+1)(2s+1)]$",
                     (-17.2,3.0),(-16.0,3.8))
    curve(ax, GEX1, W, (0.18,0.46,1.1))
    ax.axvline(-15, color=fs.SUB, lw=1.2, ls=(0,(4,3)))
    note(ax, r"$\mathrm{Re}\,G\to-15$", (0.025,0.88))
    point(ax, -10/3, r"$(-10/3,\,0)$", (-80,18))
    point(ax, 0, r"$\omega\to\infty$", (7,14), limit=True)
    note(ax, r"$\omega_x=1/\sqrt{2}$", (0.48,0.19))
    note(ax, r"$\varphi:-90^\circ\to-270^\circ$", (0.48,0.08))
    finish(fig, OUT/name, "第三象限 → 负实轴 → 第二象限；低频无穷远部分已裁去。")


def draw_type2_example():
    name = "频域-幅相例题-Ⅱ型零点对比.png"
    if not selected(name): return
    fig, ax = canvas("Ⅱ型系统对比：一组明确参数的示例",
        r"$G_1=\frac{1}{s^2(1+s)(1+2s)},\quad G_2=\frac{1+6s}{s^2(1+s)(1+2s)(1+0.5s)}$",
        (-27,4),(-12,15), figsize=(7.4,6.7))
    curve(ax, GII2, W, (0.21,0.36), fs.MAG, r"$G_1$")
    curve(ax, GEX2, W, (0.24,0.52), fs.PHA, r"$G_2$")
    point(ax, -128/9, r"$(-128/9,\,0)$", (-47,-28))
    point(ax, 0, r"$\omega\to\infty$", (6,13), limit=True)
    note(ax, "G₁ 低频：第二象限", (0.035,0.89), color=fs.MAG)
    note(ax, "G₂ 低频：第三象限", (0.035,0.14), color=fs.PHA)
    note(ax, r"$\tau=6>1+2+0.5$", (0.035,0.055))
    ax.legend(loc="upper right", fontsize=11)
    finish(fig, OUT/name, "两条曲线均从第一象限趋于原点；无穷远段已裁去。")



def draw_type2_endpoint_zoom():
    name = "频域-幅相例题-Ⅱ型原点放大.png"
    if not selected(name): return
    fig, ax = canvas("Ⅱ型对比：趋近原点的高频段放大",
        r"$G_1=\frac{1}{s^2(1+s)(1+2s)},\quad G_2=\frac{1+6s}{s^2(1+s)(1+2s)(1+0.5s)}$",
        (-0.025,0.15),(-0.025,0.19),figsize=(7.4,6.6))
    curve(ax, GII2, W, (1.6,2.5), fs.MAG, r"$G_1$")
    curve(ax, GEX2, W, (2.5,3.6), fs.PHA, r"$G_2$")
    point(ax, 0, r"$\omega\to\infty$", (8,-18), limit=True)
    note(ax, r"$\varphi\to-360^\circ$", (0.62,0.50))
    note(ax, "均在第一象限", (0.62,0.38))
    ax.legend(loc="upper right",fontsize=11)
    finish(fig, OUT/name, "与全图使用相同参数；箭头沿真实曲线趋于原点，无延长支。")


def draw_origin_zero_example():
    a = 6.2
    name = "频域-幅相例题-三重微分.png"
    if selected(name):
        fig, ax = canvas("例题：三个原点零点，终点不在原点",
            r"$G(s)=s^3/[(s+0.2)(s+1)(s+5)]$",
            (-0.15,1.16),(-0.13,0.93))
        theta = np.linspace(0,np.pi,1200)
        ax.plot(np.cos(theta),np.sin(theta),ls=(0,(4,3)),lw=1,color=fs.SUB,zorder=1)
        curve(ax, GEX3, W, (0.8,2.5,7))
        point(ax, 0, r"$\omega=0$", (5,-21), limit=True)
        point(ax, -25/936, "A", (-19,9))
        point(ax, 1j*31*np.sqrt(155)/936, "B", (-18,7))
        point(ax, 1, r"$\omega\to\infty$", (-66,-22), limit=True)
        note(ax, r"$|G|=1$", (0.64,0.82))
        note(ax, r"$\varphi:270^\circ\to0^\circ$", (0.38,0.10))
        finish(fig, OUT/name, "虚线为单位圆辅助线；原点附近的第三象限细节另见放大图。")
    name = "频域-幅相例题-三重微分原点放大.png"
    if selected(name):
        fig, ax = canvas("三重微分例题：原点附近放大",
            r"$G(s)=s^3/[(s+0.2)(s+1)(s+5)]$",
            (-0.045,0.022),(-0.018,0.048))
        curve(ax, GEX3, W, (0.12,0.30,0.48))
        point(ax, 0, r"$\omega=0$", (6,-15), limit=True)
        point(ax, -25/936, r"$A=(-25/936,\,0)$", (-13,14))
        note(ax, "先进入第三象限，再向上穿过负实轴", (0.025,0.9))
        finish(fig, OUT/name, "仅截取起始段；箭头表示频率增大。")


if __name__ == "__main__":
    verify()
    draw_shapes()
    draw_type1_example()
    draw_type2_example()
    draw_type2_endpoint_zoom()
    draw_origin_zero_example()
