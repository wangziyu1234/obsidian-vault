# figure: 频域-奈氏-习题5-9原题.png
"""Parameterized type-II Nyquist exercise and reproducible verification.

G = K(1+tau*s)/[s**2(1+T1*s)(1+T2*s)], all four parameters positive.
The figure shows the original K=1, tau=4, T1=1, T2=2 positive-frequency
branch only. Actual indented-contour winding is verified numerically.
"""
from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import control as ct
import sympy as sp
from scipy import signal
import figures_style as fs
from _nyquist_style import canvas, curve, response, point, note, finish, BOX

s = ct.tf("s")


def model(k, tau, t1, t2):
    return k*(1+tau*s)/(s*s*(1+t1*s)*(1+t2*s))


def critical_gain(tau, t1, t2):
    total = t1+t2
    return total*(tau-total)/(t1*t2*tau*tau)


def winding(system, tau, t1, t2):
    """CCW image winding on the clockwise, origin-indented RHP boundary."""
    eps = 1e-5/max(tau,t1,t2)
    radius = 1e5/min(tau,t1,t2)
    w = np.geomspace(eps,radius,16000)
    indent = eps*np.exp(1j*np.linspace(-np.pi/2,np.pi/2,3000))
    outside = radius*np.exp(1j*np.linspace(np.pi/2,-np.pi/2,1000))
    contour = np.concatenate((-1j*w[::-1],indent,1j*w,outside))
    values = 1+np.asarray(system(contour)).reshape(-1)
    angles = np.unwrap(np.angle(values))
    assert np.max(np.abs(np.diff(angles))) < np.pi/2
    return (angles[-1]-angles[0])/(2*np.pi)


def verify():
    z,w,k,tau,t1,t2 = sp.symbols("z w k tau t1 t2",positive=True)
    total=t1+t2
    product=t1*t2
    d=(1+t1*t1*w*w)*(1+t2*t2*w*w)
    g=k*(1+tau*z)/(z*z*(1+t1*z)*(1+t2*z))
    g_jw=sp.expand_complex(g.subs(z,sp.I*w))
    x=-k*(1+(tau*total-product)*w*w)/(w*w*d)
    y=k*((total-tau)+tau*product*w*w)/(w*d)
    assert sp.factor(sp.re(g_jw)-x)==0
    assert sp.factor(sp.im(g_jw)-y)==0
    wx2=(tau-total)/(tau*product)
    assert sp.factor(x.subs(w*w,wx2)+k*product*tau*tau/(total*(tau-total)))==0
    kc=total*(tau-total)/(product*tau*tau)
    characteristic=product*z**4+total*z**3+z*z+k*tau*z+k
    factored=(z*z+wx2)*(product*z*z+total*z+total/tau)
    assert sp.factor(characteristic.subs(k,kc)-factored)==0
    assert sp.simplify(sp.diff(kc,tau)-total*(2*total-tau)/(product*tau**3))==0

    for a,b in ((1,2),(0.5,3),(1,1),(2,4)):
        total_ab=a+b
        for ta in (0.5*total_ab,total_ab,1.2*total_ab,2*total_ab,4*total_ab):
            cap=critical_gain(ta,a,b)
            gains=(0.03/(a*b),0.7/(a*b)) if ta<=total_ab else (0.4*cap,cap,1.8*cap)
            for gain in gains:
                roots=ct.poles(ct.feedback(model(gain,ta,a,b),1))
                if ta>total_ab and np.isclose(gain,cap,rtol=1e-12,atol=0):
                    assert np.count_nonzero(np.abs(roots.real)<1e-7)==2
                    assert np.count_nonzero(roots.real<-1e-7)==2
                else:
                    expected=0 if ta>total_ab and gain<cap else 2
                    assert np.count_nonzero(roots.real>1e-7)==expected

    for gain,ta in ((1,4),(0.05,4),(0.2,4),(0.1,2),(0.01,3),(0.02,1),(0.08,6)):
        system=model(gain,ta,1,2)
        poles=ct.poles(ct.feedback(system,1))
        z_count=np.count_nonzero(poles.real>1e-7)
        assert abs(winding(system,ta,1,2)+z_count)<1e-8

    original=model(1,4,1,2)
    sample=np.geomspace(1e-4,1e4,2000)
    z_control=response(original,sample)
    _,z_scipy=signal.freqresp((original.num[0][0],original.den[0][0]),sample)
    assert np.max(np.abs(z_control-z_scipy)/(1+np.abs(z_control)))<1e-12
    np.testing.assert_allclose(response(original,[1/np.sqrt(8)]),[-32/3],atol=1e-12)
    print("PASS: symbolic crossing and boundary factorization; 52 pole checks; 7 actual Nyquist contours")


def draw():
    original=model(1,4,1,2)
    w=np.unique(np.r_[np.geomspace(1e-4,1e4,18000),1/np.sqrt(8)])
    fig,ax=canvas("习题5-9原题：Ⅱ型带零点（K = 1）",
        r"$G(s)=(1+4s)/[s^2(1+s)(1+2s)]$",
        (-24,2.4),(-7,5),figsize=(7.0,4.9))
    curve(ax,original,w,(0.255,0.5,1.2))
    point(ax,-32/3,r"$(-32/3,\,0)$",(-41,-26))
    ax.plot(-1,0,marker="x",color=fs.INK,markersize=7,zorder=8)
    ax.annotate(r"$(-1,\,0)$",(-1,0),xytext=(-53,-44),textcoords="offset points",
                fontsize=11,color=fs.INK,bbox=BOX,zorder=9)
    point(ax,0,r"$\omega\to\infty$",(-10,-25),limit=True)
    note(ax,r"$\omega_x=1/(2\sqrt{2})$",(0.045,0.82))
    note(ax,r"$N=-1,\qquad Z=2$",(0.05,0.10))
    out=Path(os.environ.get("FIGURE_OUT",fs.ATTACH_DIR/"频域-奈氏-习题5-9原题.png"))
    finish(fig,out,"仅正频率支；原点二重极点的绕行补弧与完整计数见正文。")


if __name__=="__main__":
    verify()
    draw()
