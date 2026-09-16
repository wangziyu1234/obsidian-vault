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
from matplotlib.ticker import MaxNLocator

import matplotlib.pyplot as plt

from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MplPath

import figures_style as fs
from _nyquist_style import canvas, curve, response, note, finish, BOX

s = ct.tf("s")


def model(k):
    return k * (s * s + 1) / (s * (s + 5))


def winding(system, w0=complex(-1, 0), eps=1e-3, radius=1e5, n=200000):
    """CCW winding of G about w0 on the RHP boundary, indented right at s = 0.

    The imaginary-axis zeros at +-j are regular points of G (its numerator is a
    polynomial), so the contour may pass through them; only the pole at the
    origin needs a small right semicircle.  Counted by signed crossings of the
    leftward ray from w0, which is numerically robust.
    """
    up = lambda lo, hi: 1j * np.geomspace(lo, hi, n)          # noqa: E731
    dn = lambda lo, hi: -1j * np.geomspace(lo, hi, n)         # noqa: E731
    arc = radius * np.exp(1j * np.linspace(np.pi / 2, 3 * np.pi / 2, n))
    indent = eps * np.exp(1j * np.linspace(-np.pi / 2, np.pi / 2, n))
    contour = np.concatenate([dn(radius, eps), indent[1:], up(eps, radius)[1:],
                              arc[1:]])
    values = np.asarray(system(contour)).reshape(-1) - w0
    sign = np.sign(values.imag)
    sign[sign == 0] = 1
    total = 0
    for i in np.where(np.diff(sign) != 0)[0]:
        t = -values.imag[i] / (values.imag[i + 1] - values.imag[i])
        xc = values.real[i] + t * (values.real[i + 1] - values.real[i])
        if xc < 0:
            total += 1 if values.imag[i] < 0 else -1    # upward = CCW positive
    return total


def verify():
    w, k = sp.symbols("w k", positive=True)
    # Re/Im are built from fully expanded polynomials: SymPy's re/im leave the
    # unexpanded I*w form untouched and then silently return garbage.
    jw = sp.I * w
    numerator = sp.expand(k * (jw**2 + 1))
    denominator = sp.expand(jw * (jw + 5))
    g_jw = sp.simplify(numerator / denominator)
    conjugate = sp.expand(denominator.subs(sp.I, -sp.I))
    product = sp.expand(numerator * conjugate)
    modulus2 = sp.expand(denominator * conjugate)
    assert sp.simplify(modulus2 - w**2 * (w**2 + 25)) == 0
    re_g = sp.simplify(sp.re(product) / modulus2)
    im_g = sp.simplify(sp.im(product) / modulus2)
    assert sp.simplify(re_g - k * (w**2 - 1) / (w**2 + 25)) == 0
    assert sp.simplify(im_g - 5 * k * (w**2 - 1) / (w * (w**2 + 25))) == 0
    mag = sp.simplify(sp.sqrt(re_g**2 + im_g**2))
    assert sp.simplify(mag - k * sp.Abs(w**2 - 1)
                       / (w * sp.sqrt(w**2 + 25))) == 0

    # Cross check the closed forms against the complex function itself.
    g_num = sp.lambdify(w, g_jw.subs(k, 1), "cmath")
    for wv in (0.05, 0.2, 0.5, 1.0, 1.5, 2.0, np.sqrt(5), 5.0, 40.0, 200.0):
        fv = float(wv)
        assert abs(g_num(fv).real - float(re_g.subs({w: fv, k: 1}))) < 1e-12, wv
        assert abs(g_num(fv).imag - float(im_g.subs({w: fv, k: 1}))) < 1e-12, wv
        assert abs(abs(g_num(fv)) - float(mag.subs({w: fv, k: 1}))) < 1e-12, wv

    # Key points of the branch.
    assert sp.simplify(re_g.subs(w, 1)) == 0 and sp.simplify(im_g.subs(w, 1)) == 0
    assert sp.simplify(im_g / re_g - 5 / w) == 0                # 过原点，方向 y = 5x
    assert sp.simplify(sp.limit(re_g, w, 0, "+") + k / 25) == 0  # Re 下界 -k/25
    assert sp.limit(im_g, w, 0, "+") == -sp.oo                  # 起点 -j∞
    assert sp.simplify(sp.diff(re_g, w) - 52 * k * w / (w**2 + 25) ** 2) == 0
    assert sp.simplify(sp.limit(re_g, w, sp.oo) - k) == 0
    assert sp.simplify(sp.limit(im_g, w, sp.oo)) == 0
    # Im has a single positive maximum on w > 0.
    extrema = [r for r in sp.solve(sp.diff(im_g, w), w) if r.is_real and r > 0]
    assert len(extrema) == 1, extrema
    assert abs(float(im_g.subs({w: extrema[0], k: 1})) - 0.4814338) < 1e-6
    # The branch stays in the strip -k/25 < Re G < k; Im G changes sign at w = 1.
    for wv in (0.05, 0.3, 1.0, 1.5, 2.24, 5.0, 20.0, 200.0):
        assert -1 / 25 < float(re_g.subs({w: wv, k: 1})) < 1.0, wv
    for wv in (0.05, 0.3, 0.8):
        assert float(im_g.subs({w: wv, k: 1})) < 0, wv
    for wv in (1.2, 2.24, 5.0, 200.0):
        assert float(im_g.subs({w: wv, k: 1})) > 0, wv
    # Re G changes sign exactly at w = 1.
    for wv in (0.2, 0.9):
        assert float(re_g.subs({w: wv, k: 1})) < 0
    for wv in (1.2, 5.0, 60.0):
        assert float(re_g.subs({w: wv, k: 1})) > 0
    # The hint arctan 0.2 = 11.3 deg is arctan(1/5), the w = 1 value.
    assert abs(float(sp.atan(sp.Rational(1, 5))) * 180 / np.pi - 11.3099) < 1e-3
    print("PASS: Re G = k(w^2-1)/(w^2+25), Im G = 5k(w^2-1)/[w(w^2+25)]; G(j1)=0, "
          "-k/25 < Re G < k, Im G < 0, Im peak 0.4814k near w = 5.37")

    def poles(kv):
        return ct.poles(ct.feedback(model(kv), 1))

    def char_roots(kv):
        """Roots of the closed-loop characteristic polynomial (k+1)s^2+5s+k."""
        return np.roots([kv + 1, 5, kv])

    for kv in (0.01, 0.5, 1, 7.3, 100, 5000):
        r = poles(kv)
        assert np.all(r.real < -1e-9), (kv, r)
        assert np.allclose(np.sort(r.real), np.sort(char_roots(kv).real)), kv
        assert np.allclose(np.prod(char_roots(kv)), kv / (kv + 1))
        assert np.allclose(np.sum(char_roots(kv)), -5 / (kv + 1))
    for kv in (-0.5, -1, -2, -100):
        assert np.count_nonzero(poles(kv).real > 1e-9) >= 1, kv
    # k = 0: closed-loop characteristic polynomial 5s, so the loop sits on the
    # stability boundary (pole at the origin) rather than being asymptotically stable.
    assert np.allclose(np.roots([1, 5, 0]), [-5.0, 0.0])

    # Two independent Nyquist checks.
    # (a) The branch obeys -k/25 < Re G < k; for k < 25 that is already right of
    #     -1, and for larger k the curve stays below the real axis, so in both
    #     cases (-1, 0) is never encircled.
    for kv in (0.05, 0.5, 1, 2, 10, 100, 1000):
        assert np.count_nonzero(char_roots(kv).real > 0) == 0, kv
        samples = response(model(kv), np.geomspace(1e-4, 1e4, 6000))
        assert samples.real.min() > -kv / 25 - 1e-9, (kv, samples.real.min())
        # (b) The clockwise-contour winding counter returns 0 as well.
        assert winding(model(kv)) == 0, kv
    print("PASS: 6 positive gains give two left-half-plane poles; -k/25 < Re G < k "
          "for 7 gains from k=0.05 to k=1000, so (-1,0) is never encircled")


def draw():
    # 图内只用数学式与拉丁标签：matplotlib 的字体回退对含 $...$ 的串不生效，
    # 一旦把汉字写进同一字符串就会渲染成方框；中文说明放在笔记的图注里。
    # 曲线纵向跨度极大（Im 从 ω→0+ 的 -∞ 回到 ω→∞ 的 0），用 symlog 纵轴
    # 一栏画全；频率采样取到两端极限，让两支在两端自然贴轴、闭合成环。
    k = 10.0
    system = model(k)
    fs.use_style()
    fig, ax = plt.subplots(figsize=(7.4, 4.6))

    w = np.unique(np.r_[np.geomspace(1e-4, 1e6, 30000),
                        np.sqrt(5), 1.0 - 1e-12, 1.0 + 1e-12])
    w = w[w != 1.0]
    samples = response(system, w)
    order = np.argsort(w)
    pos = samples[order]
    ax.plot(pos.real, pos.imag, color=fs.MAG, lw=2.2, zorder=4,
            label=r"positive branch: $\omega:0^+\to\infty$")
    ax.plot(pos.real, -pos.imag, color=fs.PHA, lw=1.4, ls=(0, (6, 3)), zorder=3,
            label="negative branch (mirror image)")
    for at in (0.45, 1.6, 5.0):
        q = response(system, np.geomspace(at / 1.25, at * 1.25, 40))
        ax.add_patch(FancyArrowPatch(path=MplPath(np.column_stack((q.real, q.imag))),
                                     arrowstyle="-|>", mutation_scale=13,
                                     color=fs.MAG, lw=1.5, zorder=6))

    ax.set_yscale("symlog", linthresh=1e-2)
    ax.set_ylim(-2.5e4, 2.5e4)
    ax.set_xlim(-3.2, 12.4)
    ax.axhline(0, color=fs.SUB, lw=0.9, zorder=1)
    ax.axvline(0, color=fs.SUB, lw=0.9, zorder=1)
    ax.grid(True, color=fs.GRID, lw=0.55, alpha=0.55)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=10)
    ax.set_xlabel(r"$Re G$", fontsize=11)
    ax.set_ylabel(r"$Im G$   (symlog scale)", fontsize=11)

    ax.plot(-1, 0, marker="x", color=fs.INK, markersize=9, zorder=8,
            label=r"critical point $(-1,\,0)$")
    ax.annotate(r"$\omega=1:\ G=0$", (0, 0), xytext=(16, -34),
                textcoords="offset points", fontsize=10, color=fs.PHA, bbox=BOX)
    ax.annotate(r"$\omega\to\infty:\ G\to(k,\,0)$", (k, 0), xytext=(-118, 30),
                textcoords="offset points", fontsize=10, color=fs.SUB, bbox=BOX,
                arrowprops=dict(arrowstyle="-|>", color=fs.SUB, lw=1.0))
    ax.legend(loc="upper left", fontsize=9.5, framealpha=0.95,
              facecolor="white", edgecolor=fs.GRID)

    out = Path(os.environ.get("FIGURE_OUT",
                              fs.ATTACH_DIR / "频域-奈氏-虚轴零点判稳.png"))
    fig.tight_layout(rect=(0.005, 0.02, 0.995, 0.99))
    fig.savefig(str(out), dpi=fs.DPI)
    plt.close(fig)
    print("saved", out)


if __name__ == "__main__":
    verify()
    draw()
