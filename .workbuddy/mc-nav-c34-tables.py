from pathlib import Path
import re
base=Path('D:/obsidian/控制理论/777习题集')
for ch in [3,4]:
 p=next(base.glob(f'现控200题基础 第{ch}章*（答案与解析）.md'))
 raw=p.read_bytes();s=raw.decode('utf-8-sig').replace('\r\n','\n')
 start=s.index('## 答案速查');end=s.index('## 【题型1】',start)
 entries=[]
 for line in s[start:end].splitlines():
  cells=[x.strip() for x in re.split(r'(?<!\\)\|',line)[1:-1]]
  if len(cells)==4 and cells[0].startswith('[['):
   entries.append((cells[0],cells[1]))
   if cells[2]:entries.append((cells[2],cells[3]))
 assert len(entries)==(27 if ch==3 else 19)
 entries.sort(key=lambda e:int(re.search(r'✏️ \d+-(\d+)',e[0])[1]))
 table='## 答案速查\n\n| 题号 | 结论与关键结果 |\n| :-- | :-- |\n'
 table+='\n'.join(f'| {a} | {b.replace(chr(92)+"dfrac",chr(92)+"frac")} |' for a,b in entries)+'\n\n'
 s=s[:start]+table+s[end:]
 if ch==3:
  old='对偶系统的模拟结构图（信号流向整体反转）：'
  new=r'''将对偶矩阵展开，输入仍记为原题的 $r$。三个积分器的输入分别是下列状态导数，输出分别为 $x_1,x_2,x_3$：

$$
\dot x_1=-3x_3+r
$$

$$
\dot x_2=x_1-5x_3+2r
$$

$$
\dot x_3=x_2-2x_3+r
$$

$$
y=x_3
$$

因此 $r$ 按 $1,2,1$ 分配到三个加法点，$x_3$ 经 $3,5,2$ 三条支路负反馈；模拟结构图如下：'''
  assert old in s;s=s.replace(old,new)
  s=s.replace('（1）按列分解 $W(s)=[W_1(s)\\ \\ W_2(s)]$，两个子系统分别由 $u_1,u_2$ 驱动，输出相加。','（1）按列分解 $W(s)=[W_1(s)\\ \\ W_2(s)]$，两个子系统分别由 $u_1,u_2$ 驱动，输出相加。以下分别写子系统时，$u$ 表示该子系统的输入；第一列的状态 $x_1$ 是标量，第二列的状态 $x_2$ 是二阶列向量。拼合后再按三个标量状态排列。')
  # Break the two decomposition equalities at actual equality/implication signs.
  s=s.replace(r'''W_1(s)=\begin{bmatrix}\dfrac{s+2}{s+1}\\[2mm]\dfrac{5}{s+1}\end{bmatrix}
=\begin{bmatrix}1\\0\end{bmatrix}+\begin{bmatrix}1\\5\end{bmatrix}\frac{1}{s+1}
\quad\Longrightarrow\quad
\dot x_1=-x_1+u,\quad y=\begin{bmatrix}1\\5\end{bmatrix}x_1+\begin{bmatrix}1\\0\end{bmatrix}u''',r'''\begin{aligned}
W_1(s)&=\begin{bmatrix}\dfrac{s+2}{s+1}\\[2mm]\dfrac{5}{s+1}\end{bmatrix}\\
&=\begin{bmatrix}1\\0\end{bmatrix}+\begin{bmatrix}1\\5\end{bmatrix}\frac{1}{s+1}
\end{aligned}
$$

所以第一列可用一阶状态实现：

$$
\dot x_1=-x_1+u
$$

$$
y=\begin{bmatrix}1\\5\end{bmatrix}x_1+\begin{bmatrix}1\\0\end{bmatrix}u''')
  s=s.replace(r'''W_2(s)=\begin{bmatrix}\dfrac{1}{s+3}\\[2mm]\dfrac{5s+1}{s+2}\end{bmatrix}
=\begin{bmatrix}0\\5\end{bmatrix}+\begin{bmatrix}\dfrac{1}{s+3}\\[2mm]\dfrac{-9}{s+2}\end{bmatrix}''',r'''\begin{aligned}
W_2(s)&=\begin{bmatrix}\dfrac{1}{s+3}\\[2mm]\dfrac{5s+1}{s+2}\end{bmatrix}\\
&=\begin{bmatrix}0\\5\end{bmatrix}+\begin{bmatrix}\dfrac{1}{s+3}\\[2mm]\dfrac{-9}{s+2}\end{bmatrix}
\end{aligned}''')
 nl='\r\n' if b'\r\n' in raw else '\n'
 p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\n',nl).encode('utf8'))
