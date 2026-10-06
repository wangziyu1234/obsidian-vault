from pathlib import Path
import subprocess

notes=sorted(Path('控制理论/自动控制原理').glob('0[56]*.md'))
assert len(notes)==57
sources='''bode-typical-links.py
ch5-typical-links-nyquist.py
ch5-three-plots.py
ch5-vector-method.py
freq-inverse-bode-first-order.py
freq-nyquist-example01.py
freq-05-examples.py
minimum-phase-comparison.py
type1-two-inertia.py
freq-inverse-second-order.py
ch5-frequency-bands.py
_ch6_verification.py
ch6-pid-actual.py
ch6-combined-actual.py
ch6-desired-actual.py
ch6-pid-block.tex
ch5-bode-examples.py
ch5-ex517-step.py
ch5-ex518-step.py
ch5-ex57-identification.py'''.splitlines()
pics='''奈氏-例01.png
奈氏-例512.png
自控-频域-三频段.png
自控-频域-中频斜率.png
自控-频域-闭环幅频.png
自控-频域-最小相位.png
频域-Ⅰ型双惯性-无零点特征点.png
频域-反求-一阶Bode.png
频域-反求-二阶伯德奈氏对应.png
频域-图示法-伯德图.png
频域-图示法-尼科尔斯图.png
频域-图示法-幅相曲线.png
频域-惯性环节-描点.png
频域-矢量法-s平面.png
校正-PID实际验收.png
校正-期望特性实际验收.png
校正-滞后超前实际验收.png
校正-PID例63纯结构图.png
频域-例517-阶跃响应.png
频域-例518-阶跃响应.png
频域-例57-实测幅频辨识.png'''.splitlines()
typical=sorted(Path('附件').glob('频域-典型环节-*.png'))
assert len(typical)==20,len(typical)
files=notes+[Path('.scripts/figures')/s for s in sources]+[Path('附件')/s for s in pics]+typical
assert all(p.is_file() for p in files)
subprocess.run(['git','add','--']+[p.as_posix() for p in files],check=True)
print('Staged only chapter 5/6 notes, 20 figure sources and 41 images.')
