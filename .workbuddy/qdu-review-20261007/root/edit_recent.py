from pathlib import Path
import re

BASE = Path('D:/obsidian/控制理论/青岛大学825真题')
BACKUP = Path(__file__).parent / 'before'
BACKUP.mkdir(exist_ok=True)

def edit(year, kind, transform):
    p = BASE / f'{year}年青岛大学825{kind}.md'
    raw = p.read_bytes()
    text = raw.decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in text else '\n'
    text = text.replace('\r\n', '\n')
    result = transform(text)
    if result == text:
        return
    result = re.sub(r'(?m)^modify: .*$', 'modify: 2026-10-07', result, count=1)
    backup = BACKUP / p.name
    if not backup.exists():
        backup.write_bytes(raw)
    p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + result.replace('\n', newline).encode('utf-8'))

def section(text, title, body):
    pattern = r'(?ms)^## ' + re.escape(title) + r'\n.*?(?=^## |\Z)'
    result, count = re.subn(pattern, lambda m: '## ' + title + '\n\n' + body.strip() + '\n\n', text)
    assert count == 1, (title, count)
    return result

QUESTION2 = r'''
单位负反馈系统的开环传递函数由如下 MATLAB 代码确定：

~~~matlab
num = conv(k,[1,1]);
den = [1, a, 2, 1];
G = tf(num,den);
~~~

系统的振荡频率为 $\omega_n=2\,\mathrm{rad/s}$，求参数 $k$、$a$。

A、$k=2,\ a=0.5$

B、$k=1,\ a=0.5$

C、$k=2,\ a=0.5$

D、$k=3,\ a=1$

> [!note] 回忆版条件说明
> 按常见考法，将“振荡频率”理解为闭环临界等幅振荡频率。由此求得 $k=2$、$a=3/4$，现有选项均不匹配，且 A、C 重复。PDF 第1页分母确为四个系数；不删去末项来迁就选项。

[[2024年青岛大学825答案与解析#选择第2题|查看本题解析]]
'''

ANSWER2 = r'''
> [!tip] 答案
> 按闭环临界等幅振荡理解：$k=2$、$a=3/4$；回忆版四个选项均不正确。

由代码可得三阶开环传递函数：

$$
G(s)=\frac{k(s+1)}{s^3+as^2+2s+1}
$$

单位负反馈的特征多项式为

$$
D(s)=s^3+as^2+(2+k)s+1+k
$$

临界等幅振荡对应一对虚轴根。代入 $s=j2$，有

$$
D(j2)=1+k-4a+j(2k-4)=0
$$

实部、虚部分别为零：

$$
2k-4=0
$$

$$
1+k-4a=0
$$

因此

$$
\boxed{k=2,\qquad a=\frac34}
$$

回代后可以精确因式分解：

$$
D(s)=s^3+\frac34s^2+4s+3
$$

$$
D(s)=\left(s+\frac34\right)(s^2+4)
$$

闭环极点为 $-3/4$、$\pm j2$，满足振荡频率为2且另一极点稳定的要求。四个选项均不满足。

> [!note] 回忆版的解释边界
> “振荡频率”未明确写“临界”，这里按常见临界稳定题求解。若只给一般欠阻尼响应的振荡频率而不约束实部，条件不足以唯一确定两个参数。原 PDF 没有给幅值穿越频率条件，也不是二阶分母，不能据此选 B。

[[2024年青岛大学825试题#选择第2题|返回本题题目]]
'''

def q24(t):
    t = section(t, '选择第2题', QUESTION2)
    needle = '若无阻尼自然频率 $\\omega_n=10\\,\\mathrm{rad/s}$、阻尼比 $\\zeta=0.5$，求 $k_1,k_2$。'
    assert needle in t
    t = t.replace(needle, needle + '\n\n> [!note] 回忆版条件说明\n> 本题按所给代码直接表示闭环传递函数整理。原 PDF 写“开环”，与选项冲突；若严格按单位负反馈开环理解，应得 $k_1=0.52$、$k_2=0.1$，四个选项均不匹配。')
    return t

def a24(t):
    t = section(t, '选择第2题', ANSWER2)
    t = t.replace('| [[#选择第2题\\|选择第2题]] | B：$k=1$，$a=0.5$（$|G(j\\omega_c)|=1$ 只有 B 满足） |', '| [[#选择第2题\\|选择第2题]] | 临界振荡：$k=2$、$a=3/4$；选项均不匹配 |')
    needle = '> - 参照2022同型题及本题可辨参数和选项，将所给模型确定为闭环 $\\Phi(s)$，补正 k2、num 变量；若坚持原“开环”字样会与指标选项冲突。'
    assert needle in t
    t = t.replace(needle, r'''> 原 PDF 第1页写“开环”，这里按常见二阶指标题及选项，将代码直接作为闭环模型；这是补明的解释，不是原题已经给出的条件。
>
> 若严格按开环模型并闭合单位负反馈，则闭环分母为
>
> $$
> s^2+100k_2s+200k_1-4
> $$
>
> 比较 $s^2+10s+100$ 得
>
> $$
> k_1=\frac{104}{200}=0.52
> $$
>
> $$
> k_2=0.1
> $$
>
> 此时四个选项均不匹配。采用本页明确的闭环解释才选 A。''')
    t = t.replace('五阶多项式无法逐项因式分解，因此用', '本题无需逐个求根，直接用')
    t = t.replace('首列也**没有零元素**（不需要单独讨论零根）', '常数项为6，排除了零根，首列也**没有零元素**（不需要作零首元的特殊处理）')
    return t

if __name__ == '__main__':
    edit(2024, '试题', q24)
    edit(2024, '答案与解析', a24)
