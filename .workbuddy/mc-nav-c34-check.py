from pathlib import Path
import re,collections
root=Path('D:/obsidian');base=root/'控制理论/777习题集'
files=[p for ch in [3,4] for p in base.glob(f'现控200题基础 第{ch}章*.md')]
allfiles=list(root.rglob('*.md')); byname={p.stem:p for p in allfiles}
for p in files:
 s=p.read_text('utf-8-sig');headers=re.findall(r'^#{1,6} (.*)$',s,re.M)
 ch=3 if '第3章' in p.name else 4;n=27 if ch==3 else 19
 kind='解析' if '答案与解析' in p.name else '题目'
 expected=[f'✏️ {ch}-{i}　{kind}' for i in range(1,n+1)]
 assert all(headers.count(x)==1 for x in expected)
 assert len(re.findall(r'^# ',s,re.M))==1
 for link in re.findall(r'\[\[(.*?)\]\]',s):
  target=link.replace(r'\|','|').split('|')[0];file,sep,anchor=target.partition('#')
  if file.endswith('.png'):
   assert (root/file).exists() or (root/'附件'/file).exists(),target
   continue
  targetpath=byname.get(Path(file).name,p) if file else p
  assert not file or targetpath!=p or Path(file).name==p.stem,(p.name,target)
  if sep:
   targets=re.findall(r'^#{1,6} (.*)$',targetpath.read_text('utf-8-sig'),re.M)
   assert anchor in targets,(p.name,target)
 blocks=re.findall(r'^(?:> )?\$\$\s*$',s,re.M);assert len(blocks)%2==0
 assert collections.Counter(re.findall(r'\\begin\{([^}]+)\}',s))==collections.Counter(re.findall(r'\\end\{([^}]+)\}',s))
 assert len(re.findall(r'\\left(?![a-zA-Z])',s))==len(re.findall(r'\\right(?![a-zA-Z])',s))
 assert not re.search(r'TODO|FIXME|待补|\?\?',s)
 print(ch,kind,n,'headings, anchors, links, formulas OK')
 for m in re.finditer(r'^(> )?\$\$\n(.*?)\n(?:> )?\$\$',s,re.M|re.S):
  content=m[2].replace('> ','')
  if len(content)>170 and not any(x in content for x in ['aligned','cases']):
   line=s[:m.start()].count('\n')+1
   print('LONG',ch,kind,line,len(content),content[:60].encode('ascii','replace').decode())
