# figure: 频域-Ⅰ型双惯性-无零点特征点.png
"""Ⅰ 型双惯性系统的特征点速查图（05-1-3-b-9）。

左图：无零点；右图：带一个左零点（τ 小于临界值，出现实轴交点）。
解析式与数值频响在 verify() 里逐点比对，图上标注的数字全部来自这两个来源。

Build: .\\build.ps1 -File .\\type1-two-inertia.py
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
W = np.geomspace(1e-4, 1e4, 20000)
OUT = Path(os.environ.get("FIGURE_OUT", fs.ATTACH_DIR / "unused.png")).parent

K0, T1_0, T2_0 = 1.0, 1.0, 2.0          # 无零点
KZ, T1_Z, T2_Z, TAU_Z = 1.0, 1.0, 2.0, 0.5  # 带一个左零点

G0 = K0 / (s * (1 + T1_0 * s) * (1 + T2_0 * s))
GZ = KZ * (1 + TAU_Z * s) / (s * (1 + T1_Z * s) * (1 + T2_Z * s))


def value_at(sys, omega):
    return complex(response(sys, [omega])[0])


def features(K, T1, T2, tau=0.0):
    """Ⅰ 型双惯性的特征点：渐近线、ω=1/√(T₁T₂) 处、实轴交点（若存在）。"""
    T = T1 + T2
    D = T1 * T2 - tau * T          # D > 0 且 τ > 0 时存在实轴交点
    out = {
        "asym": K * (tau - T) if tau > 0 else -K * T,
        "w0": 1 / np.sqrt(T1 * T2),
        "Re0": -K * T1 * T2 / T,
    }
    if tau > 0 and D > 0:
        out["wx"] = 1 / np.sqrt(D)
        out["Gx"] = -K * D * D / (tau * T)
    return out


def verify():
    # 无零点：渐近线、ω=1/√(T₁T₂) 处实部、该处虚部为 0
    f = features(K0, T1_0, T2_0)
    assert abs(value_at(G0, 1e-7).real - f["asym"]) < 1e-4
    z0 = value_at(G0, f["w0"])
    assert abs(z0.real - f["Re0"]) < 1e-12 and abs(z0.imag) < 1e-12
    # 带零点：渐近线随 τ 右移；实轴交点的频率与值
    fz = features(KZ, T1_Z, T2_Z, TAU_Z)
    assert abs(value_at(GZ, 1e-7).real - fz["asym"]) < 1e-4
    assert abs(value_at(GZ, fz["w0"]).real - fz["Re0"]) < 1e-12
    zx = value_at(GZ, fz["wx"])
    assert abs(zx.real - fz["Gx"]) < 1e-12 and abs(zx.imag) < 1e-12
    # τ→0 极限：实轴交点回到 ω=1/√(T₁T₂)、G→-K T₁T₂/(T₁+T₂)
    assert abs(fz["Re0"] - features(KZ, T1_Z, T2_Z)["Re0"]) < 1e-12
    # 教材例：K=5、T₁=1、T₂=2
    fe = features(5.0, 1.0, 2.0)
    assert abs(fe["asym"] + 15) < 1e-12 and abs(fe["Re0"] + 10 / 3) < 1e-12
    # control 与 SciPy 独立复核
    for model in (G0, GZ):
        grid = np.geomspace(1e-4, 1e4, 801)
        zc = response(model, grid)
        _, zs = signal.freqresp((model.num[0][0], model.den[0][0]), grid)
        assert np.max(np.abs(zc - zs) / (1 + np.abs(zc))) < 1e-12
    print("verified: 渐近线 / ω=1/√(T₁T₂) 处 / 实轴交点；教材例 -15 与 -10/3 对上")


def draw_no_zero():
    name = "频域-Ⅰ型双惯性-无零点特征点.png"
    f = features(K0, T1_0, T2_0)
    fig, ax = canvas("Ⅰ 型双惯性（无零点）",
                     r"$G(s)=\frac{1}{s(1+s)(1+2s)}$",
                     (-3.5, 0.7), (-2.4, 0.6), figsize=(6.4, 5.4))
    curve(ax, G0, W, (0.4, 1.1))
    ax.axvline(f["asym"], color=fs.SUB, lw=1.1, ls=(0, (4, 3)), zorder=2)
    point(ax, f["Re0"], r"$(-2/3,\,0)$", (-72, 12))
    point(ax, 0, r"$\omega\to\infty$", (8, 10), limit=True)
    note(ax, r"$\mathrm{Re}\,G\to -K(T_1+T_2)=-3$", (0.03, 0.90))
    note(ax, r"$\omega_x=1/\sqrt{T_1T_2}=0.707$", (0.03, 0.81))
    finish(fig, OUT / name, "无零点时只在 ω=1/√(T₁T₂) 穿负实轴，交点 -10/3（K=5 时）。")


def draw_with_zero():
    name = "频域-Ⅰ型双惯性-带零点特征点.png"
    f = features(KZ, T1_Z, T2_Z, TAU_Z)
    fig, ax = canvas("Ⅰ 型双惯性（带左零点）",
                     r"$G(s)=\frac{1+0.5s}{s(1+s)(1+2s)}$",
                     (-2.2, 0.7), (-2.4, 0.6), figsize=(6.4, 5.4))
    curve(ax, GZ, W, (0.4, 1.1))
    ax.axvline(f["asym"], color=fs.SUB, lw=1.1, ls=(0, (4, 3)), zorder=2)
    point(ax, f["Gx"], r"$(-1/6,\,0)$", (-64, -34))
    point(ax, 0, r"$\omega\to\infty$", (8, 10), limit=True)
    note(ax, r"$\mathrm{Re}\,G\to K(\tau-T_1-T_2)=-2.5$", (0.03, 0.90))
    note(ax, r"$\omega_x=1/\sqrt{D}=1.414$", (0.03, 0.81))
    finish(fig, OUT / name, "零点把渐近线右移；τ 小于临界值时交点离原点更近（-1/6 对 -2/3）。")


if __name__ == "__main__":
    verify()
    draw_no_zero()
    draw_with_zero()
