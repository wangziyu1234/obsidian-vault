from pathlib import Path
import re
root=Path('D:/obsidian');base=root/'控制理论/777习题集'
paths=list(base.glob('现控200题基础 第5章*.md'))
for p in paths:
    s=p.read_text(encoding='utf-8')
    title='题目' if '（题目）' in p.stem else '解析'
    heads=re.findall(r'^#### (.*)$',s,re.M)
    assert heads==[f'✏️ 5-{i}　{title}' for i in range(1,35)]
    for link in re.findall(r'\[\[([^\]]+)\]\]',s):
        target=link.replace('\\|','|').split('|')[0]
        if '#' in target:
            name,anchor=target.split('#',1)
            other=p if not name else base/(name+'.md')
            assert other.exists(),target
            assert anchor in re.findall(r'^#{1,6} (.*)$',other.read_text(encoding='utf-8'),re.M),target
        elif target.endswith('.png'):
            assert (root/'附件'/target).exists(),target
    assert s.count('$$')%2==0
    assert len(re.findall(r'^# ',s,re.M))==1
    if title=='解析':
        assert s.count('> [!note]- 本题题设')==34
        for i in (8,15,26,27,34):
            section=s.split(f'#### ✏️ 5-{i}　解析')[1].split('\n#### ')[0]
            assert f'![[现控5-{i}-' in section
    print(p.name, 'PASS')
