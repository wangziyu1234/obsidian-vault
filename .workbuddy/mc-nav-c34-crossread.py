from pathlib import Path
import re,subprocess,difflib,collections
base=Path('D:/obsidian/控制理论/777习题集')
def norm(s):
 s=re.sub(r'^> ?', '',s,flags=re.M)
 forms=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$([^$]+)\$(?!\$)',s,re.S)
 s=''.join(a or b for a,b in forms)
 s=re.sub(r'\\(?:begin|end)\{aligned\}|\\(?:quad|qquad|,|;)|[\s&]|\\\\','',s)
 return s.replace('\\dfrac','\\frac')
for ch in [1,5]:
 qpath=next(base.glob(f'现控200题基础 第{ch}章*（题目）.md'));apath=next(base.glob(f'现控200题基础 第{ch}章*（答案与解析）.md'))
 q=qpath.read_text('utf-8-sig');a=apath.read_text('utf-8-sig')
 qs={m[1]:m[2] for m in re.finditer(rf'^#### ✏️ ({ch}-\d+)　题目\n(.*?)(?=^#### |^## |\Z)',q,re.M|re.S)}
 ans={m[1]:m[2] for m in re.finditer(rf'^#### ✏️ ({ch}-\d+)　解析\n(.*?)(?=^#### |^## |\Z)',a,re.M|re.S)}
 print('CHAPTER',ch,'COUNTS',len(qs),len(ans))
 for num,aq in ans.items():
  m=re.search(r'^> \[!note\]- 本题题设\n((?:>[^\n]*\n?)*)',aq,re.M)
  if not m:print(num,'MISSING FOLD');continue
  fold=m[1]; qf=qs[num]
  # Remove non-question callouts from q page for source comparison.
  qf=re.sub(r'^>.*(?:\n>.*)*','',qf,flags=re.M)
  x,y=norm(qf),norm(fold)
  if x!=y:
   print(num,'FORMULA DIFF')
   for op,i,j,k,l in difflib.SequenceMatcher(None,x,y).get_opcodes():
    if op!='equal':print(op,repr(x[max(i-15,0):j+15]),'=>',repr(y[max(k-15,0):l+15]))
  imgq=re.findall(r'!\[\[([^|\]]+)',qf);imga=re.findall(r'!\[\[([^|\]]+)',aq)
  if set(imgq)-set(imga):print(num,'MISSING IMAGES',set(imgq)-set(imga))
 # Compare all matrix contents against HEAD after removing new question folds.
 old=subprocess.check_output(['git','show','HEAD:'+apath.relative_to(base.parent.parent).as_posix()]).decode('utf8')
 old=re.sub(r'^\*\*\d+-\d+.*$', '',old,flags=re.M)
 anew=re.sub(r'^> \[!note\]- 本题题设\n(?:>[^\n]*\n?)*','',a,flags=re.M)
 def mats(s):return collections.Counter(re.sub(r'\s|\\(?:quad|qquad)','',m) for m in re.findall(r'\\begin\{(?:bmatrix|pmatrix)\}(.*?)\\end\{(?:bmatrix|pmatrix)\}',s,re.S))
 gone=mats(old)-mats(anew);added=mats(anew)-mats(old)
 print('MATRICES REMOVED',gone)
 print('MATRICES ADDED',added)
