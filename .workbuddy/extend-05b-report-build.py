from pathlib import Path
import re,subprocess,json
root=Path('D:/obsidian'); folder=root/'控制理论/自动控制原理'
out=['# 第五章奈氏与判稳组整理记录','','范围：05-3*、05-4* 共18篇；修改15篇，05-4-3、05-4-a、05-4-e仅审查。未提交。','','## 正文整理','','删除方法篇重复的篇首速记、重复警告和篇尾相同总结；保留题目、关键推导、计算、边界、原文件名、H2及图片引用。将虚轴零点小弧扩展推导折叠，其余影响结论的验证仍在正文。','','| 文件 | 原行数 | 新行数 |','|:--|--:|--:|']
errs=[];tot=[0,0]
for p in sorted(folder.glob('05-[34]*.md')):
 old=subprocess.check_output(['git','show','HEAD:'+p.relative_to(root).as_posix()],cwd=root).decode('utf-8-sig');s=p.read_text(encoding='utf-8-sig')
 a,b=len(old.splitlines()),len(s.splitlines());tot[0]+=a;tot[1]+=b;out.append(f'| {p.name} | {a} | {b} |')
 if s.count('$$')%2:errs.append((p.name,'odd display'))
 if len(re.findall(r'^# ',s,re.M))!=1:errs.append((p.name,'H1'))
 if any(ord(c)<32 and c not in '\r\n\t' for c in s):errs.append((p.name,'control char'))
out+=['',f'合计 {tot[0]} → {tot[1]} 行；缩短 {tot[0]-tot[1]} 行。','','## 数学变更证据','','- 05-3 总览原把穿越符号写反；教材PDF236（书228）规定奈氏上向下为正、下向上为负，与 Z=P−2N 一致。已查看已有渲染页 arc-audit-233、235、236。','- 05-4-1/05-4-c：曲线经过零点连续，不代表相角连续；简单零点两侧相角差π，零点处相角无定义。','- 05-4-c：j(j+5)=−1+5j；局部系数为2jk/(−1+5j)，原先误略常数−1。k=0特征式s(s+5)，原写5s。','- 05-3-9：带零点高频 G≈Kτ/[T(jω)^ν]，无零点则K/[T(jω)^(ν+1)]，已分开。相应ν=1/2高频角为−90°/−180°（τ>0）。','- 05-3-9：τ=T相消后Ⅰ型闭环s+K，根−K稳定；仅Ⅱ型有±j√K边界。表中h=∞已明确排除τ=T。','- 05-3-a：由(900−ω²)²+(12.18ω)²=9000²得ωc=99.08939923；ω=94.9时幅值1.09916855。ωr=√(900−12.18²/2)=28.73715017，A=(5.21490085,−24.60778142)。表同步到同一模型。','- 05-3-4：删除“ν越大越贴原点”无条件断言；每添积分幅值除ω，低频反而变大。','- 05-3-8/9：根据教材PDF235中的ωx统一笔记符号，未动真题/答案原件。','','## 图片逐张审查','','36张唯一引用图片均经过联系表目视；最小相位和Ⅰ型无零点图又看了原图。以下问题已交主代理统一处理，本代理未改绘图源码。','','| 图片 | 审查结果 |','|:--|:--|']
special={'奈氏-例01.png':'主代理接手：默认工具标题、巨大补弧挤压正常支，需要突出实频支。','奈氏-例512.png':'主代理接手：正常支大段裁切；整理完整轨迹与局部判稳区域。','自控-频域-最小相位.png':'原图确认刻度位置异常、图注压曲线；主代理接手重绘。','频域-Ⅰ型双惯性-无零点特征点.png':'原图确认底注压横轴标签；type1-two-inertia.py，主代理接手。','频域-反求-二阶伯德奈氏对应.png':'图中wc已正确标99.1，正文已同步；原图wr标28.77建议随同模型改28.74（已报主代理）。'}
for name in json.loads((root/'.workbuddy/extend-05b-images.json').read_text(encoding='utf-8')):
 out.append(f'| {name} | {special.get(name,"联系表可辨认，未见需强制重画的问题；保留。")} |')
out+=['','## 检查','','- MathJax实际解析18篇1682段公式，0错误（2026-10-06）。','- basename/短路径链接扫描：0断链；唯一H1检查通过。',f'- $$配对与控制字符检查：{errs or "通过"}。','- 本组图片尺寸中两张620已改520；表格公式改用frac。','- 题号与主要H2保留；完整单题不拆分。','- 编辑脚本曾发生JS字符串转义丢失，已修复并额外检查控制字符与裸命令；最终MathJax通过。不要重跑extend-05b-final.py（旧草稿），最终笔记才是交付。']
(root/'.workbuddy/extend-05b-report.md').write_text('\n'.join(out),encoding='utf-8')
print(json.dumps({'structural_errors':errs,'lines':tot}))
