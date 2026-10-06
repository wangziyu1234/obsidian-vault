from pathlib import Path
base=Path('控制理论/777习题集')
p=next(base.glob('现控200题基础 第1章*答案*.md'));s=p.read_bytes().decode('utf-8')
s=s.replace('两处与原书答案不同、经 sympy 复算确认的勘误用「⚠️ 复算」标出：','原书勘误与题面核对说明：')
old=r'**1-21** 官方勘误将输入向量末分量 $4$ 改为 $0$，$x_5x_6$ 块改判既不能控也不能观；'
new=r'**1-21** 官方仅修正 $\dot x_4$ 的下标，输入末分量仍为 $4$，$x_5x_6$ 能控不能观，旧记“改为0”已撤下；'
assert old in s;s=s.replace(old,new)
s=s.replace('全章矩阵结论均经 sympy 数值复验。','本轮逐题回查后，另修正了 1-13 题面、1-20 逆矩阵符号与 1-22 闭环传递矩阵，并补齐 1-5、1-9、1-21 的模拟图。')
p.write_bytes(s.encode('utf-8'))
p=next(base.glob('现控200题基础 第5章*答案*.md'));s=p.read_bytes().decode('utf-8')
old=r'$W=\frac{b}{s^2+s+b}$，$b\gt0$';new=r'$a=0$ 时独立讨论 BIBO：$b\ge0$'
assert old in s;s=s.replace(old,new).replace(r'A³B 末元 $\approx959.84$',r'A³B 末元 $959.84$')
p.write_bytes(s.encode('utf-8'));print('summaries synchronized')
