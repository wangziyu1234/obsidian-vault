from pathlib import Path
import re

labels={
    r'幅角原理、$Z=P-2N$、补弧与穿越计数':'幅角原理、补弧与穿越计数',
    r'在 $L(\omega)>0$ 段数相频穿越':'在正分贝区间统计相频穿越',
    r'$\gamma$、$h$ 的定义、读法、三条求法与三个边界':'相角与幅值裕度：定义、求法及边界',
    r'例5.11 延迟定 $\tau$':'例5.11 确定允许延迟',
    r'幅角原理与 $Z=P-2N$':'幅角原理与奈氏判据',
    r'$\gamma$ 与 $h$ 定义':'相角裕度与幅值裕度的定义',
    r'例5.21 $\gamma$—$\zeta$ 精确关系':'例5.21 相角裕度与阻尼比的精确关系',
    r'$Z=P-2N$ 与补弧':'奈氏判据与补弧',
    r'$\gamma$ 与 $h$':'相角裕度与幅值裕度',
    r'三频段与 $M_r$':'三频段与谐振峰值',
    r'$\gamma$、$h$ 的定义与读法':'相角与幅值裕度的定义与读法',
}
count=0
changed=[]
for p in Path('控制理论/自动控制原理').glob('0[56]*.md'):
    raw=p.read_bytes(); text=raw.decode('utf-8')
    def change(m):
        global count
        fields=re.split(r'(\\?\|)',m[1],maxsplit=1)
        if len(fields)<3 or '$' not in fields[2]: return m[0]
        assert fields[2] in labels,fields[2]
        count+=1
        return '[['+fields[0]+fields[1]+labels[fields[2]]+']]'
    result=re.sub(r'\[\[(.*?)\]\]',change,text)
    if result!=text:
        before=[re.split(r'\\?\|',m[1],maxsplit=1)[0] for m in re.finditer(r'\[\[(.*?)\]\]',text)]
        after=[re.split(r'\\?\|',m[1],maxsplit=1)[0] for m in re.finditer(r'\[\[(.*?)\]\]',result)]
        assert before==after
        result=re.sub(r'(?m)^modify: [^\r\n]+','modify: 2026-10-06',result,count=1)
        p.write_bytes(result.encode('utf-8')); changed.append(p.name)
assert count==12,count
print('Fixed',count,'labels;',len(changed),'files; all link targets unchanged.')
for n in changed: print(n)
