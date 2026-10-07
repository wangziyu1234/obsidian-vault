from pathlib import Path
import re,json,shutil

root=Path('D:/obsidian/控制理论/青岛大学825真题')
base=root/'777改编模拟卷'
notes=base/'Markdown笔记'
old=root/'Markdown笔记/选择题练习'
work=Path(__file__).parent
backup=work/'before-assembly';backup.mkdir(exist_ok=True)
manifest=json.loads((work/'choice_reuse.json').read_text(encoding='utf8'))
new_pick={1:[1,3,7,8,10,12],2:[1,3,5,6,9,10],3:[1,5,6,7,9,12],4:[1,3,4,9,11,12],5:[7,8,9,10,11,12]}

def sections(text):
    return {int(m[1]):m[2].strip() for m in re.finditer(r'^## 第(\d+)题(?:（\d+分）)?\n([\s\S]*?)(?=^## |\Z)',text,re.M)}
def clean(s):
    s=re.sub(r'^\[\[[^\n]*(?:返回|查看)[^\n]*\]\]\s*$', '',s,flags=re.M)
    s=re.sub(r'^####\s+(.*)$',lambda m:'**'+m[1].replace('^*',r'^{\ast}')+'**',s,flags=re.M)
    out=[]
    for line in s.splitlines():
        if re.match(r'^A[.．、]',line):line=re.sub(r'\s+([B-D][.．、])',r'\n\n\1',line)
        out.append(line)
    return '\n'.join(out).strip()

assembled=[]
for spec in manifest['sets']:
    sid=spec['set']; texts={};src={};out={};answers=[];maprows=[]
    for kind in ['试题','答案与解析']:
        path=notes/f'{sid:02d} 青大825模拟卷（{kind}）.md'
        shutil.copy2(path,backup/path.name)
        texts[kind]=path.read_text(encoding='utf-8-sig').replace('\r\n','\n')
        src[kind]=sections(texts[kind]);out[kind]={}
    for i,entry in enumerate(spec['questions'],1):
        for kind,key in [('试题','source_question_file'),('答案与解析','source_answer_file')]:
            path=old/entry[key]
            target=backup/'old-choice'/path.name;target.parent.mkdir(exist_ok=True)
            if not target.exists():shutil.copy2(path,target)
            block=sections(path.read_text(encoding='utf8').replace('\r\n','\n'))[entry['source_question']]
            out[kind][i]=clean(block)
            if kind=='答案与解析':out[kind][i]+=f"\n\n复用记录：原选择题练习第{entry['source_group']}组第{entry['source_question']}题，保留原题设、选项与考点参考；仅调整排版与卷内题号。"
        answers.append(entry['answer'])
        maprows.append({'number':i,'source':'existing','group':entry['source_group'],'question':entry['source_question'],'answer':entry['answer'],'topic':entry['topic']})
    for i,original in enumerate(new_pick[sid],7):
        for kind in out:out[kind][i]=clean(src[kind][original])
        ans=re.search(r'答案[：:]\s*([ABCD])',out['答案与解析'][i])
        assert ans,(sid,i)
        answers.append(ans[1]);maprows.append({'number':i,'source':'new','original_draft_question':original,'answer':ans[1]})
    for i in range(13,18):
        for kind in out:out[kind][i]=clean(src[kind][i])
    figmap={1:{14:'根轨迹'},2:{14:'根轨迹',16:'相轨迹'},3:{13:'根轨迹',14:'伯德渐近线'}}
    for number,label in figmap.get(sid,{}).items():
        out['答案与解析'][number]+=f'\n\n![[青大825-777模拟{sid:02d}-{label}.png|430]]'
    if sid==5:
        for kind in out:
            out[kind][13]=re.sub(r'!\[\[[^\]]*777-2-38[^\]]*\]\]', '![[青大825-777模拟05-运放电路.png|430]]',out[kind][13])
    for kind in out:
        typ='exam-paper' if kind=='试题' else 'exam-solutions'
        intro=f'''---
create: 2026-10-07
modify: 2026-10-07
tags: [控制理论, 青岛大学825, 777改编模拟卷]
type: {typ}
---

> 返回目录：[[777改编模拟卷目录]]

# {sid:02d} 青大825模拟卷（{kind}）

> [!abstract] 本卷定位
> 青大近年风格训练卷，满分150分，考试时间180分钟。第1—12题为单项选择，每题5分；第13—17题为综合题，每题18分。不得使用计算器，结果优先保留精确形式。

'''
        if kind=='试题':intro+='除题目另有说明外，输入输出响应按零初始条件计算。每道选择题仅有一个正确选项。\n\n'
        else:
            intro+='建议选择题45分钟、综合题120分钟、检查15分钟。题源区分既有自编选择题与777原型改编；本套不是官方试卷或押题预测。\n\n## 答案速查\n\n'
            intro+='| 题号 | '+' | '.join(str(i) for i in range(1,13))+' |\n| :-- | '+' | '.join(':--:' for _ in range(12))+' |\n| 答案 | '+' | '.join(answers)+' |\n\n'
        content=intro+'\n\n'.join(f'## 第{i}题（{5 if i<=12 else 18}分）\n\n'+out[kind][i] for i in range(1,18))+'\n'
        (notes/f'{sid:02d} 青大825模拟卷（{kind}）.md').write_text(content,encoding='utf8')
    assembled.append({'set':sid,'answers':answers,'choices':maprows,'points':150})
(work/'assembled.json').write_text(json.dumps(assembled,ensure_ascii=False,indent=2),encoding='utf8')
print('5 sets assembled: 30 reused choices + 30 new choices + 25 comprehensive problems.')
