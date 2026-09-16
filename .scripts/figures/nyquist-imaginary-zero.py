# figure: 频域-奈氏-虚轴零点判稳.png
"""Nyquist plot for exercise 5-16: a conjugate pair of imaginary-axis zeros.

G(s) = k(s**2+1)/[s(s+5)].  The figure shows the positive-frequency branch for
k = 10; the closed-loop stability condition k > 0 is verified symbolically and
against the actual right-indented Nyquist contour.
"""
from __future__ import annotations

import os
from pathlib import Path

import control as ct
import numpy as np
import sympy as sp

import figures_style as fs
from _nyquist_style import canvas, curve, response, point, note, finish, BOX

s = ct.tf("s")


def model(k):
    return k * (s * s + 1) / (s * (s + 5))


def winding(system, eps=1e-3, radius=1e6, n=20000):
    """Winding of 1+G about the origin on the indented RHP Nyquist contour.

    Clockwise contour: -j*R -> up the negative imaginary axis -> small right
    semicircle around the origin -> on to +j -> small right semicircles around
    -j and +j (RHP side, so those open-loop zeros stay outside) -> +j*R ->
    large right arc back to -j*R.  Counted by signed crossings of the negative
    real axis, which is far more robust than unwrapping the phase.
    """
    up = lambda lo, hi: 1j * np.geomspace(lo, hi, n)          # noqa: E731
    dn = lambda lo, hi: -1j * np.geomspace(lo, hi, n)         # noqa: E731
    arc = lambda c, r: c + r * np.exp(                            # noqa: E731
        1j * np.linspace(-np.pi / 2, np.pi / 2, n))
    contour = np.concatenate([
        dn(radius, eps),
        arc(0, eps)[1:],
        up(eps, 1)[:-1],
        arc(1j, eps)[1:],
        up(1, radius)[1:],
        radius * np.exp(1j * np.linspace(np.pi / 2, -np.pi / 2, n))[1:],
    ])
    for centre, r in ((0, eps), (1j, eps), (-1j, eps)):
        # No pole or zero may sit on the path.  The discretised small arcs come
        # within about 0.35 r of their centre, so guard at 0.3 r.
        assert np.min(np.abs(contour - centre)) > 0.3 * r
    values = np.asarray(system(contour)).reshape(-1)
    x, y = values.real + 1.0, values.imag
    sign = np.sign(y)
    sign[sign == 0] = 1
    total = 0
    for i in np.where(np.diff(sign) != 0)[0]:
        t = -y[i] / (y[i + 1] - y[i])
        if x[i] + t * (x[i + 1] - x[i]) < 0:      # crossing left of the origin
            total += -1 if y[i] > 0 else 1        # CCW positive
    return total


def verify():
    w, k = sp.symbols("w k", positive=True)
    re_g = k * (w**2 - 1) / (w**2 + 25)
    im_g = 5 * k * (w**2 - 1) / (w * (w**2 + 25))
    g_jw = sp.simplify(sp.expand_complex(
        (k * (sp.I * w) ** 2 + k) / (sp.I * w * (sp.I * w + 5))))
    assert sp.simplify(sp.re(g_jw) - re_g) == 0
    assert sp.simplify(sp.im(g_jw) - im_g) == 0

    # |G| = k|1-w^2| / [w sqrt(w^2+25)].  SymPy will not merge the nested
    # radicals, so prove the squared identity exactly; the sign of 1-w^2 is then
    # carried by the absolute value and checked numerically below.
    mag = k * sp.Abs(1 - w**2) / (w * sp.sqrt(w**2 + 25))
    assert sp.simplify(sp.expand((1 - w**2) ** 2 + 25 * w**2)
                       - (1 + 23 * w**2 + w**4)) == 0
    assert sp.simplify((re_g**2 + im_g**2) * w**2 * (w**2 + 25)
                       / (k**2 * (1 - w**2) ** 2) - 1) == 0

    # Cross check the closed forms against the complex function itself.
    g_num = sp.lambdify(w, g_jw.subs(k, 1), "cmath")
    for wv in (0.2, 0.5, 0.9, 1.0, 1 / sp.sqrt(3), 1.1, 2.0, 3.0, 40.0):
        fv = float(wv)
        assert abs(g_num(fv).real - float(re_g.subs({w: fv, k: 1}))) < 1e-12, wv
        assert abs(g_num(fv).imag - float(im_g.subs({w: fv, k: 1}))) < 1e-12, wv
        assert abs(abs(g_num(fv)) - float(mag.subs({w: fv, k: 1}))) < 1e-12, wv

    # Key points and monotonicity.
    assert sp.simplify(re_g.subs(w, 1)) == 0 and sp.simplify(im_g.subs(w, 1)) == 0
    assert sp.simplify(im_g / re_g - 5 / w) == 0      # 过原点，方向 y = 5x
    assert sp.simplify(re_g.subs(w, 1 / sp.sqrt(3)) + k / 38) == 0
    assert sp.simplify(im_g.subs(w, 1 / sp.sqrt(3)) + 5 * sp.sqrt(3) * k / 38) == 0
    assert sp.simplify(mag.subs(w, 1 / sp.sqrt(3)) - sp.sqrt(19) * k / 19) == 0
    assert sp.simplify(sp.limit(re_g, w, sp.oo) - k) == 0
    assert sp.simplify(sp.limit(im_g, w, sp.oo)) == 0
    assert sp.simplify(sp.diff(re_g, w) - 52 * k * w / (w**2 + 25) ** 2) == 0
    # The tangent at the origin is y = 5x, so the crossing is not tangential.
    assert sp.simplify(sp.diff(im_g, w).subs(w, 1)
                       / sp.diff(re_g, w).subs(w, 1) - 5) == 0
    # The hint arctan 0.2 = 11.3 deg is arctan(1/5), i.e. the w = 1 value.
    assert abs(float(sp.atan(sp.Rational(1, 5))) * 180 / np.pi - 11.3099) < 1e-3
    # arctan(sqrt(3)/5) = 19.11 deg is arctan(w/5) at w = sqrt(3), not at w = 1.
    assert abs(float(sp.atan(sp.sqrt(3) / 5)) * 180 / np.pi - 19.1066) < 1e-3
    print("PASS: real/imag parts and |G| match the complex function at 9 frequencies; "
          "w=1 -> -101.31 deg via 11.31 deg; w=1/sqrt3 -> -96.59 deg")

    def poles(kv):
        return ct.poles(ct.feedback(model(kv), 1))

    def char_roots(kv):
        """Roots of the closed-loop characteristic polynomial (k+1)s^2+5s+k."""
        return np.roots([kv + 1, 5, kv])

    for kv in (0.01, 0.5, 1, 7.3, 100, 5000):
        r = poles(kv)
        assert np.all(r.real < -1e-9), (kv, r)
        # D(s) = (k+1)s^2 + 5s + k: product k/(k+1), sum -5/(k+1), both roots < 0.
        assert np.allclose(np.sort(r.real), np.sort(char_roots(kv).real)), kv
        assert np.allclose(np.prod(char_roots(kv)), kv / (kv + 1))
        assert np.allclose(np.sum(char_roots(kv)), -5 / (kv + 1))
    for kv in (-0.5, -1, -2, -100):
        r = poles(kv)
        if kv > -1:
            assert np.count_nonzero(r.real > 1e-9) == 1, (kv, r)   # product k/(k+1) < 0
        else:
            assert np.count_nonzero(r.real > 1e-9) >= 1, (kv, r)
    # k = 0: closed-loop characteristic polynomial 5s, so the loop sits on the
    # stability boundary (pole at the origin) rather than being asymptotically stable.
    assert np.allclose(np.roots([1, 5, 0]), [-5.0, 0.0])

    # The winding number of 1+G on the indented contour must equal Z.
    for kv in (0.05, 1, 7.3, 100, 5000, -0.5, -1.5, 10):
        wind = winding(model(kv))
        z_expected = np.count_nonzero(char_roots(kv).real > 0)
        assert wind == z_expected, (kv, wind, z_expected)

    # Shape of the plotted branch: origin at w = 1, Re increasing, and |Im| within
    # the local bound sqrt(5) k for w >= 1 (its global peak sits near w = 5.37).
    samples = response(model(10), np.geomspace(1e-5, 1e5, 4000))
    assert -10.0 < samples.real.min() and samples.real.max() < 10.0
    assert np.all(np.diff(samples.real) > 0)
    upper = response(model(10), np.geomspace(1.0, 1e5, 2000))
    assert np.max(np.abs(upper.imag)) < 5 ** 0.5 * 10
    print("PASS: 6 stable gains give both closed-loop poles in the left half-plane; "
          "k<0 gives an unstable pole; 8 indented-contour windings match Z=0/1/2")


def draw():
    # 图内只用数学式与拉丁标签：matplotlib 的字体回退对含 $...$ 的串不生效，
    # 一旦把汉字写进同一字符串就会渲染成方框；中文说明放在笔记的图注里。
    # 曲线在 ω→0+ 处趋向无穷远，只能取局部视野；出口用「branch to ∞」标出。
    # 图内文字压到最少，行为说明放页脚。
    k = 10.0
    system = model(k)
    w = np.unique(np.r_[np.geomspace(1e-3, 1e4, 24000),
                        0.5, 1 / np.sqrt(3), 1.0, np.sqrt(3), 2.0, 5.0])
    fig, ax = canvas("", r"$G(s)=k(s^2+1)/[s(s+5)],\quad k=10$",
                     (-2.4, 11.6), (-1.8, 2.6), figsize=(7.4, 3.0))
    curve(ax, system, w, (0.62, 1.7, 8.0))

    # 判据点 (-1, 0) 用 × 标出（含义写在图注里），曲线过原点 ω = 1。
    ax.plot(-1, 0, marker="x", color=fs.INK, markersize=8, zorder=8)
    point(ax, 0, r"$\omega=1$", (-52, 2), color=fs.PHA, size=5)
    ax.annotate("", xy=(0.42, -0.42), xytext=(1.15, -1.15),
                arrowprops=dict(arrowstyle="-|>", color=fs.PHA, lw=1.2), zorder=6)

    # 上边界的出口：ω→0+ 处竖直升出视野（局部视野，见页脚说明）。
    ax.annotate(r"to $\infty$ as $\omega\to0^+$", (-0.55, 2.28), fontsize=10,
                color=fs.SUB, bbox=BOX, zorder=9)

    out = Path(os.environ.get("FIGURE_OUT",
                              fs.ATTACH_DIR / "频域-奈氏-虚轴零点判稳.png"))
    finish(fig, out,
           r"positive-frequency branch, arrows along increasing $\omega$"
           r" (local view; it runs to $\infty$ at $\omega\to0^+$ and returns"
           r" to $(k,0)$ as $\omega\to\infty$)"
           "\n"
           r"$\angle G(\omega{=}1^-)=-101.3^\circ$, "
           r"$\angle G(\omega{=}1^+)=-281.3^\circ$;"
           r" $P=0$, no encirclement $\Rightarrow Z=0$ (stable for all $k>0$)",
           footer_size=9.5, rect=(0.005, 0.185, 0.995, 0.975))


if __name__ == "__main__":
    verify()
    draw()
