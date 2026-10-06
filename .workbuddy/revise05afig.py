from pathlib import Path
r=Path('D:/obsidian/.scripts/figures')
def write(name,s):
 # Keep source ASCII, except output declaration required by the vault.
 lines=s.splitlines();body='\n'.join(lines[1:])+'\n'
 body=''.join(c if ord(c)<128 else '\\u%04x'%ord(c) for c in body)
 (r/name).write_text(lines[0]+'\n'+body,encoding='utf-8')
p=r/'bode-typical-links.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace('# -*- coding: utf-8 -*-','# figure: 频域-典型环节-比例Bode.png',1)
s=s.replace('import os','import os\nimport control as ct',1)
s=s.replace('    if note:\n        axm.annotate(note, xy=(0.02, 0.06), xycoords="axes fraction",\n                     color=fs.INK, fontsize=11)','    if note:\n        fig.text(0.5, 0.025, note, ha="center", fontsize=10)\n    fig.subplots_adjust(left=0.16, right=0.96, top=0.85, bottom=0.15, hspace=0.25)\n    axm.tick_params(labelbottom=False)')
s=s.replace('"比例环节\\nK"','"比例环节（K = 2）\\nG(s) = K"').replace('np.full_like(W, 0.0), np.zeros_like(W)','np.full_like(W, 20*np.log10(2)), np.zeros_like(W)').replace('L ≡ 20lgK = 0 dB，φ ≡ 0°','L = 20lg2 dB；相角恒为 0°')
s=s.replace('转折频率 ωn = 1：φ = −90°、L = −20lg(2ζ)；本例 ζ = 0.5','ωn = 1，ζ = 0.5；转折处相角 −90°，幅值 0 dB').replace('转折频率 ωn = 1：φ = +90°、L = 20lg(2ζ)；本例 ζ = 0.5','ωn = 1，ζ = 0.5；转折处相角 +90°，幅值 0 dB')
s=s.replace('幅频与惯性完全相同；相频 +arctan(Tω)：0° → +90°（滞后变超前）','T = 1；与惯性幅频相同，相角反号').replace('L ≡ 0 dB；φ = −ωτ(rad)，无相角限位（图中已越过 −360°）','τ = 1；幅值恒为 0 dB，相角继续减小而无下界')
s+='\n# Independent library check of the oscillator and unbounded delay phase.\nsys_check=ct.tf([1],[1,1,1])\nz_check=ct.frequency_response(sys_check,W1).frdata.ravel()\nassert np.allclose(20*np.log10(abs(z_check)),mag_osc)\nassert -np.degrees(WD[-1]) < -360\n'
p.write_text(s,encoding='utf-8')
write('ch5-typical-links-nyquist.py',r'''# figure: 频域-典型环节-比例Nyquist.png
import os
import numpy as np
import control as ct
import matplotlib.pyplot as plt
import figures_style as fs
from _nyquist_style import canvas,curve,point,finish,response
fs.use_style()
out=os.path.dirname(os.environ['FIGURE_OUT']) if os.environ.get('FIGURE_OUT') else str(fs.ATTACH_DIR)
s=ct.tf('s');w=np.geomspace(1e-5,1e5,12000)
items=[
('比例',ct.tf([2],[1]),r'$G(s)=2$',(-.4,3),(-1,1),[],2,2,None,'所有频率都对应同一点 (2, 0)。'),
('积分',1/s,r'$G(s)=1/s$',(-.7,.7),(-2.6,.5),[.65],None,0,None,'从负虚轴无穷远出发，沿箭头趋向原点。'),
('微分',s,r'$G(s)=s$',(-.7,.7),(-.5,2.6),[1.4],0,None,None,'从原点出发，沿正虚轴继续趋向无穷远。'),
('惯性',1/(s+1),r'$G(s)=1/(s+1),\quad T=1$',(-.25,1.3),(-.75,.3),[.65,2],1,0,-.5j+.5,'红点为起点 (1, 0)；最低点 (1/2, -1/2)。'),
('一阶微分',1+s,r'$G(s)=1+s,\quad T=1$',(-.3,2),(-.5,2.6),[1.4],1,None,1+1j,'从 (1, 0) 沿 Re = 1 向上，继续趋向无穷远。'),
('振荡',1/(s*s+s+1),r'$G(s)=1/(s^2+s+1),\quad \zeta=1/2$',(-.65,1.3),(-1.4,.35),[.55,1.4],1,0,-1j,'穿虚轴点 (0, -1) 对应 ωn = 1；末端趋向原点。'),
('二阶微分',s*s+s+1,r'$G(s)=s^2+s+1,\quad \zeta=1/2$',(-2.7,1.5),(-.5,2.5),[.6,1.5],1,None,1j,'穿虚轴点 (0, 1) 对应 ωn = 1；继续向左上方无穷远。'),
('不稳定惯性',1/(1-s),r'$G(s)=1/(1-s),\quad T=1$',(-.25,1.3),(-.3,.75),[.65,2],1,0,.5+.5j,'惯性曲线关于实轴的镜像；相角由 0° 趋向 +90°。'),
('不稳定振荡',1/(s*s-s+1),r'$G(s)=1/(s^2-s+1),\quad \zeta=1/2$',(-.65,1.3),(-.35,1.4),[.55,1.4],1,0,1j,'振荡曲线关于实轴的镜像；相角由 0° 趋向 +180°。')]
for name,sys,formula,xlim,ylim,arrows,start,end,cross,desc in items:
 fig,ax=canvas(name+'环节',formula,xlim,ylim,figsize=(6.3,5.3))
 z=curve(ax,sys,w,arrows)
 if start is not None:point(ax,start,'')
 if end is not None and end!=start:point(ax,end,'',limit=True)
 if cross is not None:point(ax,cross,'',color=fs.MAG)
 fig.text(.5,.067,desc,ha='center',fontsize=9.5)
 finish(fig,os.path.join(out,'频域-典型环节-'+name+'Nyquist.png'),footer='箭头沿曲线表示频率增大；空心点为极限。',rect=(.01,.10,.99,.91))
 assert np.isfinite(z).all()
assert np.allclose(response(1/(s*s+s+1),[1]),[-1j])
assert np.allclose(response(1/(s+1),[1]),[.5-.5j])
fig,ax=canvas('延迟环节',r'$G(s)=e^{-s},\quad \tau=1$',(-1.3,1.3),(-1.3,1.3),figsize=(6.3,5.3))
q=np.linspace(0,2*np.pi,1200);z=np.exp(-1j*q)
ax.plot(z.real,z.imag,color=fs.MAG,lw=2.3)
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MplPath
for at in [1.2,3.6,5.5]:
 zz=np.exp(-1j*np.linspace(at-.12,at+.12,35))
 ax.add_patch(FancyArrowPatch(path=MplPath(np.c_[zz.real,zz.imag]),arrowstyle='-|>',mutation_scale=15,color=fs.MAG,lw=1.7))
point(ax,1,'')
fig.text(.5,.067,'幅值恒为 1；从 (1, 0) 出发，顺时针无限绕转。',ha='center',fontsize=9.5)
finish(fig,os.path.join(out,'频域-典型环节-延迟Nyquist.png'),rect=(.01,.10,.99,.91))
assert np.allclose(abs(z),1)
''')
p=r/'ch5-three-plots.py';s=p.read_text(encoding='utf-8-sig');s=s.replace('# -*- coding: utf-8 -*-','# figure: 频域-图示法-幅相曲线.png',1).replace('w = np.logspace(-2, 2, 3000)','w = np.logspace(-5, 4, 6000)')
s=s.replace('xytext=(8, -36)','xytext=(-108, -38)').replace('ax.set_xlim(w[0], w[-1])','ax.set_xlim(0.01, 100)').replace('a.set_xlim(w[0], w[-1])','a.set_xlim(0.01, 100)')
s=s.replace('    fig.savefig(path, dpi=fs.DPI)','    if len(fig.axes)==1:\n        fig.subplots_adjust(left=0.16,right=0.95,bottom=0.15,top=0.80)\n    else:\n        fig.subplots_adjust(left=0.16,right=0.96,bottom=0.14,top=0.84,hspace=0.25)\n    fig.savefig(path, dpi=fs.DPI)')
s=s.replace('xytext=(14, -5)','xytext=(4, -5)').replace('xytext=(11, -10)','xytext=(4, -10)')
s+='\nassert np.allclose(complex(ct.evalfr(sys,2j)), .5-.5j)\n'
p.write_text(s,encoding='utf-8')
p=r/'ch5-vector-method.py';s=p.read_text(encoding='utf-8-sig');s=s.replace('# -*- coding: utf-8 -*-','# figure: 频域-矢量法-s平面.png',1)
s=s.replace('|矢量| = √8 = 2.828','|矢量| = 2√2').replace('A = 2/2.828 = 0.707','A = 1/√2')
s=s.replace('    fig.savefig(path, dpi=fs.DPI)','    fig.subplots_adjust(left=0.14,right=0.96,bottom=0.17,top=0.82)\n    fig.savefig(path, dpi=fs.DPI)')
a=s.index('pts = [');b=s.index('save(fig, "频域-惯性环节-描点.png")',a)
s=s[:a]+'''# Frequency labels only; exact coordinates remain in the note table.
pts=[(0,(8,12)),(.6,(12,8)),(1,(12,-12)),(2,(-20,-24)),(4,(-52,-12)),(8,(-52,8))]
for wv,off in pts:
    g=2/(2+1j*wv)
    ax.plot(g.real,g.imag,'o',color=fs.PHA,ms=5)
    ax.annotate('ω = %g'%wv,(g.real,g.imag),xytext=off,textcoords='offset points',fontsize=10)
ax.annotate('ω → ∞',(0,0),xytext=(-32,12),textcoords='offset points',fontsize=10)
from _nyquist_style import curve
import control as ct
curve(ax,ct.tf([2],[1,2]),np.geomspace(1e-4,1e4,3000),arrows=(1.4,5.5))
fig.text(.5,.035,'各点的复数坐标见正文表；箭头表示频率增大。',ha='center',fontsize=10)
assert abs(2/(2+2j)-(.5-.5j))<1e-12
''' +s[b:]
p.write_text(s,encoding='utf-8')
p=r/'freq-inverse-bode-first-order.py';s=p.read_text(encoding='utf-8-sig').replace('WC = 2 * 10 ** 1.5','WC = 2 * np.sqrt(999)').replace(r'\frac{31.6}{0.5s+1}',r'\frac{10\sqrt{10}}{0.5s+1}').replace('C 截止频率 ωc=63.2（0 dB）','C 实际截止频率 ωc = 2√999').replace('B 渐近线读数校验点','B 幅值校验点')
s+='\nassert np.isclose(abs(at(WC)),1)\n'
p.write_text(s,encoding='utf-8')
