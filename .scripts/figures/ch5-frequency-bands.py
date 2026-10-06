# figure: 自控-频域-三频段.png
"""Three frequency-band illustrations; no added exercise."""
import os
import numpy as np
import control as ct
import matplotlib.pyplot as plt
import figures_style as fs

fs.use_style()
OUT = os.path.dirname(os.environ['FIGURE_OUT']) if os.environ.get('FIGURE_OUT') else str(fs.ATTACH_DIR)


def setup(title, ylabel, size=(7.4, 4.8)):
    fig, ax = plt.subplots(figsize=size)
    fig.suptitle(title, y=.97, fontsize=15)
    ax.set_xscale('log')
    ax.set_xlabel(r'$\omega$ / (rad/s)')
    ax.set_ylabel(ylabel)
    fs.tidy(ax)
    fig.subplots_adjust(left=.13,right=.97,top=.85,bottom=.20)
    return fig,ax


def save(fig, name, footer):
    fig.text(.5,.045,footer,ha='center',fontsize=10,color=fs.SUB)
    fig.savefig(os.path.join(OUT,name),dpi=fs.DPI)
    plt.close(fig)


fig,ax=setup('\u4e09\u9891\u6bb5\u5206\u6790\uff08\u2160\u578b\u6e10\u8fd1\u7ebf\u793a\u610f\uff09',r'$L(\omega)$ / dB',(8,4.5))
w=np.geomspace(.1,100,2000)
L=-20*np.log10(w/10)-20*np.log10(np.maximum(w/20,1))
ax.set_xlim(.1,100);ax.set_ylim(-40,62)
for lo,hi,col in [(.1,1.5,'#E8EFF8'),(1.5,20,'#EEF4ED'),(20,100,'#FAEFE7')]:
    ax.axvspan(lo,hi,color=col,zorder=0)
ax.plot(w,L,color=fs.MAG,lw=2.3)
ax.axhline(0,color=fs.SUB,lw=.9)
ax.axvline(10,color=fs.SUB,lw=.8,ls='--')
for x,text in [(.36,'\u4f4e\u9891\uff1a\u7cbe\u5ea6\n\u578b\u522b\u4e0e\u589e\u76ca'),(5,'\u4e2d\u9891\uff1a\u52a8\u6001\n\u622a\u6b62\u9891\u7387\u4e0e\u88d5\u5ea6'),(45,'\u9ad8\u9891\uff1a\u6297\u566a\n\u5148\u770b\u4fe1\u53f7\u901a\u9053')]:
    ax.text(x,55,text,ha='center',va='top',fontsize=11)
ax.annotate(r'$\omega_c=10$',(10,0),xytext=(10,-25),textcoords='offset points',fontsize=11)
save(fig,'\u81ea\u63a7-\u9891\u57df-\u4e09\u9891\u6bb5.png','\u5206\u533a\u4e3a\u5de5\u7a0b\u793a\u610f\uff1b\u5177\u4f53\u7a33\u5b9a\u6027\u4e0e\u6297\u566a\u6027\u80fd\u9700\u6309\u5b8c\u6574\u6a21\u578b\u786e\u8ba4\u3002')

fig,ax=setup('\u4e2d\u9891\u659c\u7387\uff1a\u7ecf\u9a8c\u63d0\u793a',r'$L_a(\omega)$ / dB')
w=np.geomspace(1,100,800)
for k,col in [(20,fs.MAG),(40,fs.SUB),(60,fs.PHA)]:
    ax.plot(w,-k*np.log10(w/10),color=col,lw=2,label=f'-{k} dB/dec')
ax.set_xlim(1,100);ax.set_ylim(-68,68)
ax.axhline(0,color=fs.SUB,lw=.8)
ax.axvline(10,color=fs.SUB,lw=.8,ls='--')
ax.plot(10,0,'o',color=fs.INK,ms=5)
ax.annotate(r'$\omega_c=10$',(10,0),xytext=(10,14),textcoords='offset points',fontsize=11)
ax.legend(loc='lower left',fontsize=11)
save(fig,'\u81ea\u63a7-\u9891\u57df-\u4e2d\u9891\u659c\u7387.png','\u659c\u7387\u4e0d\u80fd\u76f4\u63a5\u5224\u7a33\uff1b\u4ecd\u9700\u5b8c\u6574\u76f8\u9891\u6216\u5948\u6c0f\u5224\u636e\u3002')

zeta=.4
system=ct.tf([1],[1,2*zeta,1])
w=np.geomspace(.05,10,2000)
response=ct.frequency_response(system,w).frdata.ravel()
wr=np.sqrt(17)/5
wb=np.sqrt(17+np.sqrt(914))/5
mr=25/(4*np.sqrt(21))
assert np.isclose(abs(ct.evalfr(system,1j*wr)),mr)
assert np.isclose(abs(ct.evalfr(system,1j*wb)),1/np.sqrt(2))
fig,ax=setup('\u5178\u578b\u4e8c\u9636\u95ed\u73af\u5e45\u9891\uff08\u03b6 = 0.4\uff0c\u03c9n = 1\uff09',r'$M(\omega)=|\Phi(j\omega)|$')
ax.plot(w,abs(response),color=fs.MAG,lw=2.3)
ax.set_xlim(.05,10);ax.set_ylim(0,1.7)
for y in [1,1/np.sqrt(2)]:ax.axhline(y,color=fs.SUB,ls='--',lw=.8)
ax.set_yticks([0,1/np.sqrt(2),1,1.5]);ax.set_yticklabels(['0',r'$1/\sqrt{2}$','1','1.5'])
ax.plot([wr,wb],[mr,1/np.sqrt(2)],'o',color=fs.PHA,ms=5)
ax.vlines([wr,wb],0,[mr,1/np.sqrt(2)],color=fs.SUB,ls=':',lw=.9)
ax.annotate(r'$M_r,\ \omega_r=\sqrt{17}/5$',(wr,mr),xytext=(.14,1.53),fontsize=11,arrowprops=dict(arrowstyle='-',color=fs.SUB,lw=.8))
ax.annotate(r'$\omega_b=\sqrt{17+\sqrt{914}}/5$',(wb,1/np.sqrt(2)),xytext=(1.7,1.27),fontsize=11,arrowprops=dict(arrowstyle='-',color=fs.SUB,lw=.8))
save(fig,'\u81ea\u63a7-\u9891\u57df-\u95ed\u73af\u5e45\u9891.png','\u7eb5\u8f74\u4e3a\u7ebf\u6027\u5e45\u503c\uff1b\u5e26\u5bbd\u5904\u964d\u81f3\u76f4\u6d41\u5e45\u503c\u7684 1/\u221a2\uff0c\u7ea6\u4e3a\u4e0b\u964d 3 dB\u3002')
