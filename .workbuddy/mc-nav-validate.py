from pathlib import Path
import re,json,collections
root=Path('D:/obsidian'); base=root/'控制理论/777习题集'
files=sorted(base.glob('现控200题基础*.md')); expected={1:27,2:12,3:27,4:19,5:34}
allfiles=[p for folder in ['控制理论','数学','英语','附件'] for p in (root/folder).rglob('*') if p.is_file()]
allfiles += [root/'README.md',root/'AGENTS.md']
names=collections.defaultdict(list)
for p in allfiles: names[p.name].append(p); names[p.stem].append(p)
errors=[]; stats=[]
def err(p,msg): errors.append(p.name+': '+msg)
def resolve(target):
    for p in [root/target,root/(target+'.md')]:
        if p.is_file(): return p
    for p in names.get(Path(target).name,[]):
        if '/' not in target or p.as_posix().endswith('/'+target) or p.as_posix().endswith('/'+target+'.md'): return p
def heads(t): return re.findall(r'^#{1,6} (.+?)\s*$',t,re.M)
for p in files:
    t=p.read_text(encoding='utf-8-sig'); chapter=int(re.search(r'第(\d+)章',p.name)[1]); sol='答案与解析' in p.name
    ns=re.findall(r'^#### ✏️ (\d+-\d+)　'+('解析' if sol else '题目')+'$',t,re.M)
    want=[f'{chapter}-{n}' for n in range(1,expected[chapter]+1)]
    if ns!=want: err(p,'exercise headings not sequential/complete '+str(ns))
    peer=next(x for x in files if f'第{chapter}章' in x.name and ('（题目）' in x.name if sol else '（答案与解析）' in x.name))
    for n in want:
        if f'[[{peer.stem}#✏️ {n}　'+('题目' if sol else '解析')+'|' not in t: err(p,'missing paired link '+n)
    if not sol:
        start=t.index('## 🔎 题号直达'); end=t.index('\n## ',start+1)
        found=re.findall(r'\[\[#✏️ (\d+-\d+)　题目\\\|',t[start:end])
        if sorted(found)!=sorted(want):err(p,'question navigation incomplete')
    if len(re.findall(r'^# ',t,re.M))!=1: err(p,'H1 count')
    if t.index('> [!abstract]')<t.index('\n# '): err(p,'abstract order')
    if re.search(r'TODO|FIXME|待补|\[\[\]\]',t): err(p,'placeholder')
    if sol:
        for tag,start,end in [('nav','## 🔎 题号直达','## 答案速查'),('table','## 答案速查','\n## 【')]:
            frag=t[t.index(start):t.index(end,t.index(start)+len(start))]
            found=re.findall(r'\[\[#✏️ (\d+-\d+)　解析\\\|',frag)
            if sorted(found)!=sorted(want): err(p,tag+' coverage '+str(found))
    imagecount=0; linkcount=0
    for m in re.finditer(r'(!?)\[\[([^\]]+)\]\]',t):
        target=m[2].replace('\\|','|').split('|')[0]; fn,sep,anchor=target.partition('#')
        dest=resolve(fn) if fn else p
        if not dest: err(p,'missing '+target); continue
        if m[1]: imagecount+=1
        else: linkcount+=1
        if sep and not anchor.startswith('^'):
            ht=heads(dest.read_text(encoding='utf-8-sig'))
            if ht.count(anchor)!=1: err(p,'anchor not unique/missing '+target)
    clean=re.sub(r'^\s*> ?','',t,flags=re.M)
    blocks=re.findall(r'\$\$([\s\S]*?)\$\$',clean)
    if clean.count('$$')%2: err(p,'display delimiters')
    for b in blocks:
        stack=[]
        for m in re.finditer(r'\\(begin|end)\{([^}]+)\}',b):
            if m[1]=='begin': stack.append(m[2])
            elif not stack or stack.pop()!=m[2]: err(p,'environment nesting')
        if stack: err(p,'open environment')
        if len(re.findall(r'\\left(?![a-zA-Z])',b))!=len(re.findall(r'\\right(?![a-zA-Z])',b)): err(p,'left/right pair')
        if '[[' in b: err(p,'wikilink in math')
    for line in t.splitlines():
        if line.lstrip('> ').startswith('|'):
            if any(re.search(r'(?<!\\)\|',w) for w in re.findall(r'\[\[(.*?)\]\]',line)): err(p,'table wiki pipe unescaped')
    stats.append(dict(file=p.name,exercises=len(ns),links=linkcount,images=imagecount,math_blocks=len(blocks)))
for ch in expected:
    q=next(p for p in files if f'第{ch}章' in p.name and '（题目）' in p.name)
    a=next(p for p in files if f'第{ch}章' in p.name and '（答案与解析）' in p.name)
    imgs=lambda p:set(re.findall(r'!\[\[([^\]|]+)',p.read_text(encoding='utf-8-sig')))
    if imgs(q)-imgs(a): err(a,'question images absent '+str(imgs(q)-imgs(a)))
result=dict(files=stats,errors=errors)
(root/'.workbuddy/mc-nav-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
