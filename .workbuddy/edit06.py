from pathlib import Path
import re,json
base=Path('控制理论/自动控制原理')
stats={}
def read(prefix):
 p=next(base.glob(prefix+' *.md'));s=p.read_bytes().decode('utf-8-sig');stats[p.name]=len(s);return p,s.replace('\r\n','\n')
def save(p,s):
 old=p.read_bytes();s=re.sub(r'^modify: .*','modify: 2026-10-06',s,flags=re.M)
 p.write_bytes((b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\n','\r\n' if b'\r\n' in old else '\n').encode())
def dropcall(s,title):
 return re.sub(r'> \[!'+title+r'\][^\n]*\n(?:>[^\n]*\n)*\n','',s)
for prefix in ['06-1-1','06-1-3','06-2','06-3','06-3-c','06-4']:
 p,s=read(prefix);s=re.sub(r'> \[!tip\] 🎯 考点速记\n(?:>[^\n]*\n)*\n','',s);save(p,s)
p,s=read('06-1-1')
a=s.index('**性能与稳定性的矛盾**');b=s.index('### 6.1.2')
s=s[:a]+'增益增大通常有利于稳态精度，但动态性能还取决于对象；仅调一个参数往往不能兼顾稳、准、快。校正装置通过配置零极点整形频率特性。\n\n'+s[b:]
a=s.index('**三种方式比较**');b=s.index('### 6.1.3');s=s[:a]+s[b:]
a=s.index('**与本章其他小节的关系**');b=s.index('\n---',a);s=s[:a]+s[b:];save(p,s)
p,s=read('06-2')
s=re.sub(r'> \[!tip\] 口诀\n(?:>[^\n]*\n)*\n','',s)
a=s.index('- **P**：',s.index('### 6.2.3'));b=s.index('### 6.2.4',a)
s=s[:a]+'P 调增益，I 与 D 的作用分别见上两节。实际微分常采用 $T_ds/(1+T_fs)$ 抑制高频噪声。\n\n'+s[b:]
a=s.index('### 6.5.2 特点');b=s.index('\n---',a)
s=s[:a]+'### 6.5.2 特点\n\n局部反馈可削弱被包围环节的参数与扰动影响，但需额外检测元件；增大阻尼时应重新检查稳态误差系数。上例减半的是 $K_v$，并非所有反馈校正都固定减半。\n'+s[b:]
s=re.sub(r'> 3\. \*\*结论\*\*：\n(?:>[^\n]*\n)*\n','',s)
s=re.sub(r'例6\.1 展示[^\n]*\n\n','',s)
s=s.replace('先按上面的劳斯条件取','按下述劳斯条件取')
s=s.replace('；此时辅助方程', '；此时辅助方程')
s=s.replace('=\\frac{2\\pi}{2\\sqrt5}=1.404','=\\frac{\\pi}{\\sqrt5}')
s=s.replace('$K_p=0.6K_m=252$、$T_i=0.5T_c=0.702$、$T_d=0.125T_c=0.176$','$K_p=252$、$T_i=\\pi/(2\\sqrt5)$、$T_d=\\pi/(8\\sqrt5)$')
s=s.replace(r'G_c(s)=252\Bigl(1+\frac{1}{0.702s}+0.176s\Bigr)',r'G_c(s)=252\left(1+\frac{2\sqrt5}{\pi s}+\frac{\pi}{8\sqrt5}s\right)')
save(p,s)
p,s=read('06-4-c')
a=s.index('> **结论**');b=s.index('> [!example] ✏️ 例6.8',a);s=s[:a]+s[b:]
s=s.replace('=1.34265664',r'=\frac{2.02^3}{6.13888}')
s=s.replace('。这里的 $s$ 项系数是 $p+K$，不是 $p+Kz$，不存在“两组 $Kz$ 矛盾”。','。匹配时注意 $s$ 项系数为 $p+K$。')
s=s.replace('闭环极点约为 $-1.50891$、$-1.16455\\pm\\mathrm j2.02641$；超调约1.6514%，2%调节时间约1.99775 s','闭环极点均在左半平面；超调约1.65%，2%调节时间约2 s')
s=re.sub(r'例6\.8按目标[^\n]*\n\n','',s);save(p,s)
p,s=read('06-4-d')
a=s.index('> 3. **结论**');b=s.index('> [!example]',a)
s=s[:a]+'> **结论**：可测扰动按注入点补偿；理想逆不可实现时，采用带滤波的近似补偿或稳态补偿，并检查模型偏差。\n\n'+s[b:]
s=s.replace(r'G_p(s)=\frac{72.58065}{s+72.58065}',r'G_p(s)=\frac{288}{3.968s+288}')
s=s.replace('这里前置滤波器零点相消频率使用 $288/3.968$ 的精确比值，显示数值作舍入。','前置滤波器对消指令通道的稳定零点。')
s=s.replace('约0.1013%','约0.10%').replace('约40.08 ms','约40 ms').replace('6.9515','6.95');save(p,s)
p,s=read('06-4-b');s=s.replace('① 先明确结构与性能口径 → ② 精度定低频增益 → ③ 快速性与裕度定整形目标 → ④ 求完整校正器 → ⑤ 重算实际闭环与各扰动通道 → ⑥ 检查可实现性；不合格则回到选型或参数设计。','沿上方流程完成设计；收尾逐项对照验收清单，尤其不要把设计频率当作实际截止频率。').replace('\\6-5','§6-5').replace('\\6-6/6-7','§6-6/6-7');save(p,s)
p,s=read('06-3')
a=s.index('> [!tip] **卢京潮定点');b=s.index('### 6.3.6',a)
s=s[:a]+'> [!note] 另一条路线：六点定点法\n> 直接在原幅频线上叠加超前与滞后网络，完整过程见 [[06-3-b 滞后-超前频率法图解例题（卢京潮讲义）]]。渐近幅值平衡只给初值，实际截止频率仍须重算。\n\n'+s[b:]
save(p,s)
Path('.workbuddy/06-before.json').write_text(json.dumps(stats,ensure_ascii=False),encoding='utf-8')
