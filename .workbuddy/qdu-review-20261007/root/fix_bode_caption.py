from edit_recent import edit
import re
def f(t):
    return re.sub(r'横轴采用真实对数频率坐标，.*?的横向间距按对数比例绘制；实线为校正前，虚线为校正后：','横轴采用真实对数频率坐标，1 到 2 与 2 到 10 的横向间距按对数比例绘制；实线为校正前，虚线为校正后：',t)
edit(2006,'答案与解析',f)
