from pathlib import Path
import re,subprocess,json
base=Path('控制理论/自动控制原理');rows=[];oldtotal=newtotal=0
for p in sorted(base.glob('06*.md')):
 old=subprocess.check_output(['git','show','HEAD:'+p.as_posix()]).decode('utf-8-sig');new=p.read_text(encoding='utf-8-sig')
 changed=old.replace('\r\n','\n')!=new
 if changed:oldtotal+=len(old);newtotal+=len(new)
 rows.append(f'| {p.name} | '+('已整理' if changed else '检查衔接，保留既有样板/简短入口')+f' | {len(old)} → {len(new)} |')
names=json.loads(Path('.workbuddy/images06.json').read_text(encoding='utf-8'))
out='''# 第六章整理报告

## 覆盖

17篇均读取或对照衔接；12篇正文改动，原文件名、主要标题和题目保留。删除重复考点速记、冗长历史和重复结论；同题6-5计算集中06-1-d，方法篇保留结果和两种裕度读法。

| 文件 | 操作 | 字符数（含公式） |
|:--|:--|:--|
'''+ '\n'.join(rows)+f'\n\n修改文件总字符：{oldtotal} → {newtotal}，减少{(oldtotal-newtotal)/oldtotal:.1%}。为独立公式扩行，行数不作为压缩指标。\n'+'''
## 数学变化，供主代理复推

- 06-2-b PID：原网络 wc≈13.3586，gamma≈70.868；5% ts≈0.1664、无超调，Kv=10。经验目标13.6不是原题必要条件，原时域题可验收合格。删除把15当实际截止的勾选。
- 06-3-b：原网络wc≈17.741低于明确要求20，不能合格。定义A20为去掉迟后极点后的20处幅值，p=20/sqrt(A20²-1)≈0.402516；选0.41给wc≈20.2716、gamma≈36.3265、Kv126，满足全题。原图参数注明初值。
- 06-3-c：三个网络5%ts≈0.626、0.549、0.638；超调≈15.84%、27.28%、23.22%，Kv200，均满足原时域题。给出真实验收，避免仅看经验wc目标。
- 06-1-d：开环迟后极点时间常数不能推出闭环ts≈123.5，已撤。例2 b改为本章定义0.055；“增益放大后恰临界”改为判仍稳定，渐近增益法只作辅助。g穿越符号统一x，放大后的截止单记c,h。
- 06-2：临界PID Ti、Td改为含pi精确值；原小数为计算值而非题设；局部反馈只在上例Kv减半不泛化。
- 06-4-c/d：精确比例替代长机器小数，验收表适当舍入。

复算脚本 .workbuddy/check06.py；MathJax实际解析17篇1058段，0错误（图片尚未替换）。

## 图片覆盖与建议

以下23图均在联系表目视；PID验算、组合图解、教材PID结构截图另原尺寸目视。联系表 .workbuddy/contact06-0.png、contact06-1.png。

优先由主代理处理：PID实际验收图、组合校正从0.343到0.41的实际验收图、整页教材PID结构截图、期望法实际验收图。讲义构造图可保留折叠参考，避免用旧图上的渐近截止代替实际值。未修改任何图片或共享源。

'''+ '\n'.join('- '+n+'：已目视。' for n in names)
Path('.workbuddy/extend-06-report.md').write_text(out,encoding='utf-8')
print(f'characters {oldtotal} -> {newtotal} ({(oldtotal-newtotal)/oldtotal:.1%})')
