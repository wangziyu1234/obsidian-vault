"""Actual loop responses for chapter 6 design verification figures."""
import control as ct
import numpy as np
import matplotlib.pyplot as plt
import figures_style as fs

def plot_case(case, name):
    fs.use_style()
    s = ct.tf('s')
    if case == 'pid':
        loops = [10*(.3*s*s+1.426*s+1)/(s*(s+1)*(s/5+1)*(s/30+1))]
        labels = ['PID']; colors=[fs.MAG]; expected=[(13.35,13.37)]
        target=15.; title='PID\u6821\u6b63\uff1a\u5b9e\u9645\u622a\u6b62\u9891\u7387'
    elif case == 'combined':
        g=126/(s*(s/10+1)*(s/60+1))
        loops=[g*(1+s/2)*(1+s/10.81)/((1+s/p)*(1+s/37)) for p in [.343,.41]]
        labels=[r'$p=0.343$',r'$p=0.41$']; colors=[fs.SUB,fs.MAG]
        expected=[(17.73,17.75),(20.26,20.29)];target=20.
        title='\u6ede\u540e\u2014\u8d85\u524d\uff1a\u4fee\u6b63\u540e\u518d\u9a8c\u6536'
    else:
        loops=[200*(1+s/z)/(s*(1+s/50)*(1+s/100)*(1+s/200)*(1+s/p)*(1+s/h)) for p,z,h in [(.0844,1.3,154),(.195,3,154),(.0845,1.3,65)]]
        labels=['\u521d\u59cb\u65b9\u6848','\u6ede\u540e\u53f3\u79fb','\u9ad8\u9891\u538b\u4f4e']
        colors=[fs.MAG,fs.PHA,'#448273'];expected=[(12.49,12.51),(12.75,12.78),(12.33,12.37)]
        target=13.;title='\u671f\u671b\u7279\u6027\uff1a\u4e09\u65b9\u6848\u5b9e\u9645\u9a8c\u6536'
    fig,(am,ap)=plt.subplots(2,1,figsize=(7.8,6.1),sharex=True)
    fig.subplots_adjust(left=.12,right=.75,bottom=.16,top=.86,hspace=.18)
    fig.suptitle(title,y=.97,fontsize=15)
    w=np.logspace(0,2,1800)
    results=[]
    for i,(loop,label,color,interval) in enumerate(zip(loops,labels,colors,expected)):
        gm,pm,wx,wc=ct.margin(loop)
        assert interval[0]<wc<interval[1],(case,wc)
        assert np.max(ct.poles(ct.feedback(loop)).real)<0
        mag,pha,ww=ct.frequency_response(loop,w)
        am.semilogx(w,20*np.log10(np.squeeze(mag)),color=color,lw=1.8,label=label,ls='--' if case=='combined' and i==0 else '-')
        ap.semilogx(w,np.unwrap(np.squeeze(pha))*180/np.pi,color=color,lw=1.8)
        am.plot(wc,0,'o',color=color,ms=5)
        ap.plot(wc,pm-180,'o',color=color,ms=5)
        results.append((wc,pm))
    for ax in [am,ap]:
        fs.tidy(ax,which='major'); ax.set_xlim(1,100)
        ax.axvline(target,color='#A6ABB1',ls=':',lw=1)
    am.axhline(0,color=fs.SUB,lw=.8)
    ap.axhline(-180,color=fs.SUB,lw=.8)
    am.set_ylim(-40,35);ap.set_ylim(-240,-65)
    am.set_ylabel(r'$L(\omega)$ / dB')
    ap.set_ylabel(r'$\varphi(\omega)$ / $^\circ$')
    ap.set_xlabel(r'$\omega$ / (rad/s)')
    am.tick_params(labelbottom=False)
    fig.legend(*am.get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.45,.93),ncol=len(labels),fontsize=10)
    fig.text(.78,.82,'\u5b9e\u9645\u622a\u6b62',fontsize=11)
    for i,(wc,pm) in enumerate(results):
        fig.text(.78,.76-i*.052,rf'$\omega_c={wc:.2f}$',fontsize=11,color=colors[i])
    fig.text(.78,.40,'\u5b9e\u9645\u88d5\u5ea6',fontsize=11)
    for i,(wc,pm) in enumerate(results):
        fig.text(.78,.34-i*.052,rf'$\gamma={pm:.1f}^\circ$',fontsize=11,color=colors[i])
    fig.text(.12,.018,'\u5706\u70b9\uff1a\u5b9e\u9645\u622a\u6b62\u70b9\u3000\u7ad6\u865a\u7ebf\uff1a\u8bbe\u8ba1\u9891\u7387',fontsize=10,color=fs.SUB)
    if case=='combined': assert results[-1][0]>20 and results[-1][1]>35
    fs.save(fig,name)
