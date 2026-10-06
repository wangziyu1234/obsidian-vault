# figure: 频域-典型环节-比例Nyquist.png
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
('\u6bd4\u4f8b',ct.tf([2],[1]),r'$G(s)=2$',(-.4,3),(-1,1),[],2,2,None,'\u6240\u6709\u9891\u7387\u90fd\u5bf9\u5e94\u540c\u4e00\u70b9 (2, 0)\u3002'),
('\u79ef\u5206',1/s,r'$G(s)=1/s$',(-.7,.7),(-2.6,.5),[.65],None,0,None,'\u4ece\u8d1f\u865a\u8f74\u65e0\u7a77\u8fdc\u51fa\u53d1\uff0c\u6cbf\u7bad\u5934\u8d8b\u5411\u539f\u70b9\u3002'),
('\u5fae\u5206',s,r'$G(s)=s$',(-.7,.7),(-.5,2.6),[1.4],0,None,None,'\u4ece\u539f\u70b9\u51fa\u53d1\uff0c\u6cbf\u6b63\u865a\u8f74\u7ee7\u7eed\u8d8b\u5411\u65e0\u7a77\u8fdc\u3002'),
('\u60ef\u6027',1/(s+1),r'$G(s)=1/(s+1),\quad T=1$',(-.25,1.3),(-.75,.3),[.65,2],1,0,-.5j+.5,'\u7ea2\u70b9\u4e3a\u8d77\u70b9 (1, 0)\uff1b\u6700\u4f4e\u70b9 (1/2, -1/2)\u3002'),
('\u4e00\u9636\u5fae\u5206',1+s,r'$G(s)=1+s,\quad T=1$',(-.3,2),(-.5,2.6),[1.4],1,None,1+1j,'\u4ece (1, 0) \u6cbf Re = 1 \u5411\u4e0a\uff0c\u7ee7\u7eed\u8d8b\u5411\u65e0\u7a77\u8fdc\u3002'),
('\u632f\u8361',1/(s*s+s+1),r'$G(s)=1/(s^2+s+1),\quad \zeta=1/2$',(-.65,1.3),(-1.4,.35),[.55,1.4],1,0,-1j,'\u7a7f\u865a\u8f74\u70b9 (0, -1) \u5bf9\u5e94 \u03c9n = 1\uff1b\u672b\u7aef\u8d8b\u5411\u539f\u70b9\u3002'),
('\u4e8c\u9636\u5fae\u5206',s*s+s+1,r'$G(s)=s^2+s+1,\quad \zeta=1/2$',(-2.7,1.5),(-.5,2.5),[.6,1.5],1,None,1j,'\u7a7f\u865a\u8f74\u70b9 (0, 1) \u5bf9\u5e94 \u03c9n = 1\uff1b\u7ee7\u7eed\u5411\u5de6\u4e0a\u65b9\u65e0\u7a77\u8fdc\u3002'),
('\u4e0d\u7a33\u5b9a\u60ef\u6027',1/(1-s),r'$G(s)=1/(1-s),\quad T=1$',(-.25,1.3),(-.3,.75),[.65,2],1,0,.5+.5j,'\u60ef\u6027\u66f2\u7ebf\u5173\u4e8e\u5b9e\u8f74\u7684\u955c\u50cf\uff1b\u76f8\u89d2\u7531 0\u00b0 \u8d8b\u5411 +90\u00b0\u3002'),
('\u4e0d\u7a33\u5b9a\u632f\u8361',1/(s*s-s+1),r'$G(s)=1/(s^2-s+1),\quad \zeta=1/2$',(-.65,1.3),(-.35,1.4),[.55,1.4],1,0,1j,'\u632f\u8361\u66f2\u7ebf\u5173\u4e8e\u5b9e\u8f74\u7684\u955c\u50cf\uff1b\u76f8\u89d2\u7531 0\u00b0 \u8d8b\u5411 +180\u00b0\u3002')]
for name,sys,formula,xlim,ylim,arrows,start,end,cross,desc in items:
 fig,ax=canvas(name+'\u73af\u8282',formula,xlim,ylim,figsize=(6.3,5.3))
 z=curve(ax,sys,w,arrows)
 if start is not None:point(ax,start,'')
 if end is not None and end!=start:point(ax,end,'',limit=True)
 if cross is not None:point(ax,cross,'',color=fs.MAG)
 fig.text(.5,.067,desc,ha='center',fontsize=9.5)
 finish(fig,os.path.join(out,'\u9891\u57df-\u5178\u578b\u73af\u8282-'+name+'Nyquist.png'),footer='\u7bad\u5934\u6cbf\u66f2\u7ebf\u8868\u793a\u9891\u7387\u589e\u5927\uff1b\u7a7a\u5fc3\u70b9\u4e3a\u6781\u9650\u3002',rect=(.01,.17,.99,.91))
 assert np.isfinite(z).all()
assert np.allclose(response(1/(s*s+s+1),[1]),[-1j])
assert np.allclose(response(1/(s+1),[1]),[.5-.5j])
fig,ax=canvas('\u5ef6\u8fdf\u73af\u8282',r'$G(s)=e^{-s},\quad \tau=1$',(-1.3,1.3),(-1.3,1.3),figsize=(6.3,5.3))
q=np.linspace(0,2*np.pi,1200);z=np.exp(-1j*q)
ax.plot(z.real,z.imag,color=fs.MAG,lw=2.3)
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MplPath
for at in [1.2,3.6,5.5]:
 zz=np.exp(-1j*np.linspace(at-.12,at+.12,35))
 ax.add_patch(FancyArrowPatch(path=MplPath(np.c_[zz.real,zz.imag]),arrowstyle='-|>',mutation_scale=15,color=fs.MAG,lw=1.7))
point(ax,1,'')
fig.text(.5,.067,'\u5e45\u503c\u6052\u4e3a 1\uff1b\u4ece (1, 0) \u51fa\u53d1\uff0c\u987a\u65f6\u9488\u65e0\u9650\u7ed5\u8f6c\u3002',ha='center',fontsize=9.5)
finish(fig,os.path.join(out,'\u9891\u57df-\u5178\u578b\u73af\u8282-\u5ef6\u8fdfNyquist.png'),rect=(.01,.17,.99,.91))
assert np.allclose(abs(z),1)
