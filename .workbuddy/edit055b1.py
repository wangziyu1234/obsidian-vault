from pathlib import Path
import re
p=next(Path('控制理论/自动控制原理').glob('05-5-b-1 *.md'))
raw=p.read_bytes();s=raw.decode('utf-8-sig').replace('\r\n','\n')
a=s.index('> **讲什么**');b=s.index('## 🧩',a)
s=s[:a]+'> 从闭环幅相图或阶跃响应反求模型，再设计校正；最后用雕刻机、磁盘驱动两例练习频域估算与实际响应对照。\n\n'+s[b:]
s=re.sub(r'> \[!tip\] 思路\n(?:>[^\n]*\n)*\n','',s)
s=re.sub(r'> \[!tip\] 两类题本质相同\n(?:>[^\n]*\n)*\n','',s)
s=s.replace('精确计算约为 $'+chr(92)+'omega_c=0.74937'+chr(92)+' '+chr(92)+'mathrm{rad/s}$、$'+chr(92)+'gamma=32.6131°$','完整频响给 $'+chr(92)+'omega_c'+chr(92)+'approx0.749'+chr(92)+' '+chr(92)+'mathrm{rad/s}$、$'+chr(92)+'gamma'+chr(92)+'approx32.6°$')
s=s.replace(chr(92)+'approx0.81650',chr(92)+'approx0.82').replace(chr(92)+'approx1.83712',chr(92)+'approx1.84')
s=s.replace('0.2375$ s（$'+chr(92)+'Delta=2'+chr(92)+'%$）','0.2375$ s（5%带近似）')
s=re.sub(r'> 注：讲义印刷分子[^\n]*','> 本解采用零点为2.5的校正器，使稳定实极点对消。',s)
s=s.replace('得 $'+chr(92)+'zeta=0.3$','得 $'+chr(92)+'zeta'+chr(92)+'approx0.3$')
s=s.replace(chr(92)+'Rightarrow'+chr(92)+'zeta=0.3',chr(92)+'Rightarrow'+chr(92)+'zeta'+chr(92)+'approx0.3')
s=s.replace(chr(92)+'Rightarrow'+chr(92)+'omega_n=3.3',chr(92)+'Rightarrow'+chr(92)+'omega_n'+chr(92)+'approx3.3')
s=s.replace(chr(92)+'Rightarrow'+chr(92)+"zeta'=0.5",chr(92)+'Rightarrow'+chr(92)+"zeta'"+chr(92)+'approx0.5')
s=s.replace('=4.5;',chr(92)+'approx4.5;').replace('=0.461',chr(92)+'approx0.461')
s=s.replace('> **(1)** $e^{-', '> **(1)** 按图读数近似反求，以下传函系数随之圆整：$e^{-')
s=s.replace('=1.273',chr(92)+'approx1.273').replace('=\\frac{4.5',chr(92)+'approx'+chr(92)+'frac{4.5')
s=s.replace('> 由此估 $'+chr(92)+'sigma'+chr(92)+'%'+chr(92)+'approx40'+chr(92)+'%$、$t_s'+chr(92)+'approx17.96$ s（$'+chr(92)+'Delta=2'+chr(92)+'%$）；原三阶系统仿真实为 $'+chr(92)+'sigma'+chr(92)+'%'+chr(92)+'approx39'+chr(92)+'%$、$t_p'+chr(92)+'approx4$ s、$t_s'+chr(92)+'approx16$ s——二阶近似可用。',
'> 由二阶近似估超调约40%。按5%带经验式，调节时间约为 $3.5/(0.28'+chr(92)+'times0.87)$，即14.4 s；原三阶完整响应约为超调38.9%、峰值时间4.08 s、5%调节时间12.3 s。近似可用于初估。')
s=s.replace('ts(2%) ≈ 16 s，与教材仿真（39%、4 s、16 s）一致。','ts(5%) ≈ 12.3 s；调节时间须在相同误差带下比较。')
s=s.replace('> 实际仿真为 $'+chr(92)+'sigma'+chr(92)+'%'+chr(92)+'approx31'+chr(92)+'%$、$t_s'+chr(92)+'approx9.2$ ms（$'+chr(92)+'Delta=2'+chr(92)+'%$）——估算**明显偏保守**。',
'> 同一完整模型密集采样复核：超调约31.4%、5%调节时间约5.69 ms。与同为5%带的经验估算比较，本例估算偏保守。')
s=s.replace('ts(2%) ≈ 8.4 ms（教材仿真 31%、9.2 ms）。','ts(5%) ≈ 5.69 ms；实际值以完整响应的最后越界时刻确定。')
a=s.index('## ⚠️ 边界与易错');b=s.index('> 相关：',a)
s=s[:a]+'''## ⚠️ 边界与易错

- 先确认标准二阶模型及频率标定；峰值反求和测速反馈的适用条件见各题步骤，不凭曲线外形判断。
- 校正器须因果可实现，避免不稳定隐对消；增益改变后重算稳定性、稳态精度与动态指标。
- 比较估算和实际调节时间，必须统一误差带。本页两教材案例统一采用5%。
- 磁盘例的10.1 ms为教材估读值；若固定使用截止频率1200和系数4.04，代入经验式约得10.6 ms，勿当成严格等式。

'''+s[b:]
s=re.sub(r'^modify: .*','modify: 2026-10-06',s,flags=re.M)
p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode())
