from pathlib import Path
import difflib
import re

root = Path(__file__).resolve().parents[1]
answer = next((root / '控制理论/777习题集').glob('基础300题 第8章*答案与解析*.md'))
old = answer.read_text(encoding='utf-8-sig')
new = old

for a, b in [(14, 19), (20, 25), (32, 37)]:
    start = re.search(rf'^\*\*8-{a}　解析\*\*', new, re.M).start()
    end = re.search(rf'^\*\*8-{b+1}　解析\*\*', new, re.M).start()
    headings = list(re.finditer(r'^## .*$', new[start:end], re.M))
    if headings:
        pos = start + headings[-1].start()
        if not re.search(r'^\*\*8-\d+　解析\*\*', new[pos:end], re.M):
            end = pos
    draft = (root / '.workbuddy' / f'c8-review-{a}-{b}.md').read_text(encoding='utf-8-sig').strip()
    assert draft.startswith(f'**8-{a}　解析**')
    new = new[:start] + draft + '\n\n' + new[end:]

new = new.replace('modify: 2026-10-05', 'modify: 2026-10-06', 1)
abstract_start = new.index('> 本章 43 题')
abstract_end = new.index('\n', abstract_start)
new = new[:abstract_start] + (
    '> 本章 43 题按题号连续排列，保留原书考点与难度。已对照原题、原解 PDF 及本地保存的官方勘误图复核；12 处官方勘误涉及的正文与题图已落实，另对原解不严谨处给出复算说明。公式保留适合手算的精确形式。\n'
    '> 描述函数法的幅值、频率与周期解稳定性均是基波近似预测；相平面法中另有精确结论。稳定周期解、不稳定周期解和非孤立闭轨族分别标明。\n'
    '> 勘误汇总见 [[777习题集官方勘误摘录]]；概念配合 [[08 第8章 非线性控制系统分析]] 使用。'
) + new[abstract_end:]

table = r'''## 答案速查

下表频率单位均为 $\mathrm{rad/s}$；$A$ 的测量位置以对应题解为准，输出振幅另用 $A_c$ 标出。描述函数题按基波近似口径阅读，临界边界见正文。

| 题号 | 结论与关键结果 |
| :-- | :-- |
| 8-1 | 原题非线性项为 $x^2$；$(0,0)$ 稳定焦点，$(-2,0)$ 鞍点 |
| 8-2 | 等倾线 $(2\alpha+1)\dot x+2x+x^2=0$；$(0,0)$ 稳定焦点，$(-2,0)$ 鞍点 |
| 8-3 | 原点为中心；第一积分 $\mathrm e^x(\dot x^2+x-1)=C$，仅 $-1<C<0$ 为非平衡闭轨道 |
| 8-4 | 六种线性化类型：稳定焦点、不稳定焦点、稳定节点、不稳定节点、中心、鞍点 |
| 8-5 | $(0,0)$ 不稳定焦点，$(-1,0)$ 鞍点 |
| 8-6 | $\dot e=\mp\frac{2k}{4+\alpha}$（$e\gtrless0$，$\alpha\ne-4$） |
| 8-7 | 等倾线 $x+(1+\alpha)\dot x=1$；$(1,0)$ 稳定焦点 |
| 8-8 | 开关线 $y+k\dot y=0$；分区圆弧，$k>0$ 时输出趋零（理想滑动解释） |
| 8-9 | $\beta=0$ 为闭轨族；$\beta<0$ 发散，$\beta>0$ 收敛（理想滑动解释） |
| 8-10 | 开关线 $e=\pm0.7$；抛物线与水平线拼接成闭轨族，死区内有平衡点集合 |
| 8-11 | 开关线 $e+\dot e=\pm1$；原点稳定节点，状态趋零 |
| 8-12 | 补内反馈负号后，$(\frac38,0)$ 稳定焦点；$e_{\mathrm{ss}}=\frac38$，$c_{\mathrm{ss}}=\frac58$ |
| 8-13 | 整段 $\{(e,0):\lvert e\rvert\le2\}$ 为平衡点；给定初态为闭轨，周期 $2\pi+4$ |
| 8-14 | $N(A)=\frac{4M}{\pi A}$；稳定自振 $A=\frac{20M}{3\pi}$，$\omega=\sqrt2$ |
| 8-15 | $N(A)=\frac{3A^2}{4}$；不稳定周期解 $A=2\sqrt2$，$\omega=\sqrt2$ |
| 8-16 | $K>\pi h$ 时小幅值周期解不稳定、大幅值周期解稳定；$\omega=1$；等号为相切临界 |
| 8-17 | 稳定自振：继电输入 $A=\frac{k}{5\pi}$，输出 $A_c=\frac{k\sqrt5}{5\pi}$，$\omega=2$ |
| 8-18 | 稳定自振 $\omega=\sqrt2$，振幅取方程的大根；严格无交点条件 $3\pi h>4M$ |
| 8-19 | 唯一稳定周期候选；$\omega^5+5\omega^3+4\omega=\frac{240}{\pi}$，幅值方程见正文 |
| 8-20 | 稳定自振；$\omega^3+\omega=\frac{200}{\pi}$，继电输入 $A=\frac{\sqrt{1+\omega^2}}5$，输出 $A_c=A/5$ |
| 8-21 | 唯一稳定周期候选，$0<\omega<4\sqrt2$；只能由 $h/M=1/2$ 确定频率与 $A/h$ |
| 8-22 | 不稳定，无有限正振幅谐波平衡解；负倒轨迹为 $(-2,0)$ |
| 8-23 | 不稳定周期解 $A=\frac4\pi$、$\omega=1$；近似稳定初始基波振幅范围 $0<A<\frac4\pi$ |
| 8-24 | $K_1=5$ 时稳定自振、$\omega=5$；按描述函数判据，稳定工作区为 $0<K_1<\frac52$，等号临界 |
| 8-25 | $0<k<\frac23$ 稳定；$\frac23<k<2$ 稳定自振，$A=\frac{6k-4}{2-k}$、$\omega=1$；$k\ge2$ 不稳定；$k=\frac23$ 另见正文 |
| 8-26 | $-1<b<0$ 有稳定自振；$b=-0.5$ 时频率方程取 $\omega>2$ 的唯一根 |
| 8-27 | 稳定周期解 $A=\frac12$，不稳定周期解 $A=2$；均有 $\omega=\frac12$ |
| 8-28 | 按原题相位 $-\pi/3$：稳定自振，$\omega=\frac2{\sqrt3}$，$A=\frac{45}4$ |
| 8-29 | 稳定自振：$A_e=\frac5{2\pi}$，$A_c=\frac{\sqrt2}{\pi}$，$\omega=2$ |
| 8-30 | 稳定自振：$A_c=\frac{4K}{\pi}$，$\omega=\frac1{\sqrt2}$；题给 $K=0.75\pi$ 时 $A_c=3$ |
| 8-31 | 稳定自振：$A=\frac8{3\pi}$，$\omega=\sqrt3$ |
| 8-32 | 稳定自振；指定输出振幅时 $K=4$、$\omega=2$；首相角分支上 $\tau$ 增大使频率减小、振幅增大 |
| 8-33 | 第（2）问 $k=\frac{3\pi}4$、$\omega=\sqrt2$；第（3）问 $k=\frac{\pi\sqrt{10}}4$，延迟须满足相位条件 |
| 8-34 | 严格无交点条件 $8b<3\pi a$；等号为相切临界 |
| 8-35 | 描述函数等效闭环稳定，无有限频率自振 |
| 8-36 | 稳定自振条件 $K_1K_2<\frac{T_1+T_2}{T_1T_2}$；$\omega=\frac1{\sqrt{T_1T_2}}$，振幅见正文 |
| 8-37 | $G_3=1$ 时稳定自振 $A=\frac{\sqrt{32+8\sqrt{16-\pi^2}}}{\pi}$、$\omega=1$；$G_3=s$ 消除自振，但保留静止点族 |
| 8-38 | 稳定自振：$A=\frac4\pi$，$\omega=\sqrt3$ |
| 8-39 | 稳定自振：$A=\frac{\sqrt{800+20\sqrt{1600-\pi^2}}}{\pi}$，$\omega=1$；小根不稳定 |
| 8-40 | 稳定自振：$A_c=\frac{\sqrt{8+2\sqrt{16-\pi^2}}}{\pi}$，$\omega=1$；小根不稳定 |
| 8-41 | 稳定自振：$A_x=\frac{16}{5\pi}$，$A_c=\frac8\pi$，$\omega=2$ |
| 8-42 | 相平面法证明状态趋向原点，$e_{\mathrm{ss}}=0$；描述函数法无自振 |
| 8-43 | 第（1）问稳定周期解取大根，$\omega=4$；第（2）问收敛到死区平衡集合，$\lvert e_{\mathrm{ss}}\rvert\le0.5$ |

'''
begin = new.index('## 答案速查')
end = new.index('## 【知识点一】')
new = new[:begin] + table + new[end:]

assert re.findall(r'^\*\*8-(\d+)　解析\*\*', new, re.M) == [str(i) for i in range(1, 44)]
assert len(re.findall(r'^## 【知识点', new, re.M)) == 11
diff = ''.join(list(difflib.unified_diff(old.splitlines(True), new.splitlines(True), n=3))[2:])
diff = re.sub(r'^@@.*@@.*$', '@@', diff, flags=re.M)
print('*** Begin Patch')
print('*** Update File: ' + answer.as_posix())
print(diff, end='')
print('*** End Patch')
