# figure: 奈氏-例01.png
"""Example 5.10: actual frequency response, crossing and low-frequency limit."""
import numpy as np
import control as ct
import matplotlib.pyplot as plt
import figures_style as fs
from _nyquist_style import response, curve

fs.use_style()
s=ct.tf('s')
sys=5/(s*(1+s)*(1+0.5*s))
w=np.geomspace(1e-5,1e5,12000)
wx=np.sqrt(2)
assert abs(response(sys,[wx])[0]+5/3)<1e-12
assert abs(response(sys,[1e-6])[0].real+7.5)<1e-8
assert np.count_nonzero(np.real(ct.poles(ct.feedback(sys)))>0)==2
fig,axs=plt.subplots(1,2,figsize=(10.0,4.8))
box=dict(facecolor='white',edgecolor='none',pad=1.5)
for ax in axs:
    ax.axhline(0,color=fs.SUB,lw=.8)
    ax.axvline(0,color=fs.SUB,lw=.8)
    ax.spines[['top','right']].set_visible(False)
    ax.grid(True,color=fs.GRID,lw=.5,alpha=.6)
    ax.set_xlabel(r'$\mathrm{Re}\,G(j\omega)$')
    ax.set_ylabel(r'$\mathrm{Im}\,G(j\omega)$')
    ax.plot(-1,0,'x',color=fs.INK,ms=7)
    ax.plot(-5/3,0,'o',color=fs.PHA,ms=5)
curve(axs[0],sys,w,(.25,.6,1.7))
axs[0].set_xlim(-8.2,1)
axs[0].set_ylim(-20,2)
axs[0].axvline(-7.5,color=fs.SUB,ls='--',lw=.8)
axs[0].set_title('正频率支：从无穷远到原点',fontsize=12)
axs[0].text(-5,-18,r'$\omega\to0^+:\ \mathrm{Re}\,G\to-7.5$',fontsize=10,bbox=box)
axs[0].annotate('',xy=(-7.45,-19.5),xytext=(-7.45,-17),
                arrowprops=dict(arrowstyle='->',color=fs.MAG,lw=1.2))
curve(axs[1],sys,w,(1.1,2.4))
axs[1].set_xlim(-2.8,.4)
axs[1].set_ylim(-.9,1.05)
axs[1].set_aspect('equal',adjustable='box')
axs[1].set_title('负实轴附近：自下而上穿越',fontsize=12)
axs[1].annotate(r'$(-5/3,0)$',(-5/3,0),xytext=(-2.65,.4),fontsize=11,
                color=fs.PHA,bbox=box,arrowprops=dict(arrowstyle='-',color=fs.PHA,lw=.7))
axs[1].text(-1.13,-.48,r'$(-1,0)$',fontsize=11,bbox=box)
axs[1].text(-2.65,.82,r'$\omega_x=\sqrt{2},\quad N=-1$',fontsize=11,bbox=box)
fig.suptitle(r'$G(s)=5/[s(1+s)(1+0.5s)]$',fontsize=15,y=.97)
fig.text(.5,.035,'Ⅰ型原点补弧在第四象限，无负实轴穿越；计数得 Z = 2，闭环不稳定。',
         ha='center',fontsize=10,color=fs.SUB)
fig.subplots_adjust(left=.075,right=.98,top=.82,bottom=.19,wspace=.32)
fs.save(fig,'奈氏-例01.png')
plt.close(fig)
