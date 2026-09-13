# figure: 自控-频域-最小相位.png
"""Stable/unstable first-order Bode comparison from control.frequency_response."""
import numpy as np
import control as ct
import matplotlib.pyplot as plt
import figures_style as fs

fs.use_style()
s = ct.tf("s")
w = np.geomspace(0.01,100,2000)
stable = np.asarray(ct.frequency_response(1/(1+s),w).frdata).reshape(-1)
unstable = np.asarray(ct.frequency_response(1/(1-s),w).frdata).reshape(-1)
np.testing.assert_allclose(unstable,np.conj(stable),rtol=1e-13,atol=1e-14)
fig, (axm,axp) = fs.new_bode_axes(figsize=(6.8,6.4))
for ax in (axm,axp):
    ax.set_xscale("log")
    ax.set_xlim(w[0],w[-1])
    fs.tidy(ax,(1,))
    ax.axhline(0,color=fs.SUB,lw=0.8,ls=(0,(3,3)))
axm.plot(w,20*np.log10(np.abs(stable)),color=fs.MAG,lw=2.2)
axm.set_ylim(-42,5)
axm.text(0.04,0.10,"两者的幅频曲线完全重合",transform=axm.transAxes,fontsize=12,
         bbox=dict(facecolor="white",edgecolor="none",pad=2))
axp.plot(w,np.degrees(np.angle(stable)),color=fs.MAG,lw=2.2,label=r"$1/(1+s)$")
axp.plot(w,np.degrees(np.angle(unstable)),color=fs.PHA,lw=2.2,label=r"$1/(1-s)$")
axp.set_ylim(-100,100)
axp.set_yticks([-90,-45,0,45,90])
axp.legend(loc="center right",fontsize=12,facecolor="white",framealpha=1,frameon=True)
fig.suptitle("惯性与不稳定惯性：同幅、反相（T = 1）",y=0.98,fontsize=14)
fig.tight_layout(rect=(0,0,1,0.94))
fs.save(fig,"自控-频域-最小相位.png")
plt.close(fig)
