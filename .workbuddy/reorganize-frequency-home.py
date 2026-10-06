from pathlib import Path
import re

p=Path('控制理论/自动控制原理/05 第5章 线性系统的频域分析法.md')
raw=p.read_bytes()
nl='\r\n' if b'\r\n' in raw else '\n'
text=raw.decode('utf-8').replace('\r\n','\n')
heads=list(re.finditer(r'^## .+$',text,re.M))
assert len(heads)==6
sections=[(m.group(),text[m.end():heads[i+1].start() if i+1<len(heads) else len(text)].strip()) for i,m in enumerate(heads)]
intro=text[text.index('> [!abstract]'):heads[0].start()].strip()
prefix=text[:text.index('> [!abstract]')].replace('modify: 2026-09-24','modify: 2026-10-06')

main='''> [!abstract] 本章定位
> 从频率特性出发，学会画图、判稳、求裕度，再联系闭环性能。首轮沿下面六步走，每步只做一道代表题；完整索引留在后面的查阅区。

## 🧭 学习主线

先认清题目要的是**环路频响、闭环输出还是偏差**。每步先看方法，再遮住解析做代表题；达到“做到”这一条，再往下走。

**① 正弦稳态：先写对输入到输出、偏差的通道。**

读 [[05-1-1 频率特性的基本概念|频率特性基本概念]]，做 [[05-1-1-b-1 正弦稳态输出与稳态偏差#✏️ 例5.2（习题5-3 厦门大学2012）正弦稳态输出与稳态偏差|例5.2：正弦稳态输出与偏差]]。

做到：先列两条传递函数，再求各自的幅值与相位；分清稳态正弦与暂态响应。

**② 正向画图：把传递函数变成伯德图。**

读 [[05-2-1 开环伯德图（画法·相频·修正）|开环伯德图画法]]，做 [[05-2-d 伯德图绘图例题#例5.25（课程例）化尾1标准型并绘制开环伯德图|例5.25：标准化与绘图]]。

做到：独立完成尾1标准化、增益、转折频率和分段斜率；画完用低频起点与高频终态自检。

**③ 由图反求：把图上的信息还原成参数。**

读 [[05-2-b 由伯德图反求（方法与口径）|伯德图反求方法]]，做 [[05-2-e 伯德图反求例题#例5.23（课程例）由伯德图确定一阶系统传函|例5.23：一阶系统反求]]。

做到：说清斜率、折点、高度分别确定什么；区分渐近线读数与精确频响，写出的传函能回代核对。

**④ 奈氏判稳：用完整曲线判断闭环稳定性。**

读 [[05-4-1 奈氏判据|奈氏判据]]，做 [[05-4-b 频域判稳例题#✏️ 例5.10（教材例5-2 数值化）Ⅰ 型系统数穿越、定临界增益|例5.10：数穿越与临界增益]]。

做到：交代开环右半平面极点数、虚轴极点的补弧和穿越方向，得到完整的稳定增益范围。画曲线卡住时再查 [[05-3-1 幅相曲线的画法与最小相位|幅相曲线画法]]。

**⑤ 稳定裕度：分开求两种频率、两种裕度。**

读 [[05-4-3 稳定裕度|稳定裕度方法]]，做 [[05-4-b 频域判稳例题#✏️ 例5.12（教材例5-12）$K/(s+1)^3$ 的相角裕度与幅值裕度|例5.12：相角裕度与幅值裕度]]。

做到：知道哪个频率由幅值条件确定、哪个由相角条件确定；先确认稳定性，再解释裕度的意义。

**⑥ 联系性能：说明频域指标能告诉你什么。**

读 [[05-5-1 三频段与闭环频域指标|三频段与闭环指标]]，做 [[05-5-b-2 二阶相角裕度与时域指标例题#✏️ 例5.21（教材例5-13）相角裕度与阻尼比的精确关系|例5.21：相角裕度与阻尼比]]。

做到：从标准二阶模型说明裕度与阻尼的关系，区分精确公式与经验估算，知道何时不能直接套用。

走完后，拿其中一道题复述“对象 → 画图 → 判稳 → 裕度 → 性能”。这条链能独立完成，就接着读 [[06 第6章 线性系统的校正方法|第六章：根据指标设计校正器]]。

## 📚 查阅区

需要更多题、特殊情形、教材页码或课程讲次时，再展开对应一栏。下面保留原索引和题号。
'''

labels=['按课件讲次、术语查找；查看补充题线索','完整专题路线与分册入口','环路、闭环与偏差通道对照','教材节次、页码与原分册说明','全部31道例题及来源对照','完整解题流程与易错边界']
def fold(body):
    return '\n'.join('> '+line if line else '>' for line in body.splitlines())
parts=[prefix+main]
for i,((heading,body),label) in enumerate(zip(sections,labels)):
    if i==3:
        body+='\n\n**原分册说明与教材范围**\n\n'+intro
    parts.append(heading+'\n\n> [!note]- '+label+'\n'+fold(body)+'\n')
result='\n'.join(parts).rstrip()+'\n'
assert all(heading in result for heading,_ in sections)
old_links=set(re.findall(r'\[\[(.*?)\]\]',text))
new_links=set(re.findall(r'\[\[(.*?)\]\]',result))
assert old_links<=new_links, old_links-new_links
p.write_bytes(result.replace('\n',nl).encode('utf-8'))
print('Updated chapter 5 home; preserved all original links and six section anchors.')
