from edit_recent import edit
import re
def transform(t):
    t=t.replace(r'6.0206-40\lg(\omega/10)',r'20\lg2-40\lg(\omega/10)')
    t=t.replace(r'13.9794-20\lg\omega',r'20\lg5-20\lg\omega')
    t=t.replace(r'-6.0206-40\lg(\omega/10)',r'-20\lg2-40\lg(\omega/10)')
    old='横轴取 $\\lg\\omega$，下列两条折线依次为校正前、校正后：'
    t=t.replace(old,'横轴采用真实对数频率坐标，$1\to2$ 与 $2\to10$ 的横向间距按对数比例绘制；实线为校正前，虚线为校正后：')
    t,n=re.subn(r'```mermaid\nxychart-beta[\s\S]*?```','![[青大825-2006-伯德渐近线复核.png|520]]',t)
    assert n==1
    return t
edit(2006,'答案与解析',transform)
