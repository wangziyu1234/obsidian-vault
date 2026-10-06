from pathlib import Path
import re
base=Path('控制理论/自动控制原理')
skip=['06 第6章','06-1-2 ','06-1-b ','06-1-c ']
for p in base.glob('06*.md'):
 if any(p.name.startswith(v) for v in skip):continue
 old=p.read_bytes();s=old.decode('utf-8-sig').replace('\r\n','\n');before=s
 # Independent equations separated by qquad get their own display blocks.
 def fmt(m):
  pre=m.group(1);body=m.group(2);clean='\n'.join(l.removeprefix(pre) for l in body.splitlines()).strip()
  if '\\begin' in clean:return m.group(0)
  depth=0;cut=[]
  for match in re.finditer(r'[{}]|\\qquad',clean):
   tok=match.group()
   if tok=='{':depth+=1
   elif tok=='}':depth-=1
   elif depth==0:cut.append(match.span())
  if not cut:return m.group(0)
  parts=[];start=0
  for a,b in cut:parts.append(clean[start:a].rstrip(' ,，'));start=b
  parts.append(clean[start:])
  # Split only true equation pairs; keep conditions attached.
  if not all('=' in x or '\\Rightarrow' in x for x in parts):return m.group(0)
  return ('\n'+pre.rstrip()+'\n').join(pre+'$$\n'+'\n'.join(pre+l for l in part.strip().splitlines())+'\n'+pre+'$$' for part in parts)
 s=re.sub(r'^(>\s*|)\$\$\n(.*?)^\1\$\$',fmt,s,flags=re.M|re.S)
 if p.name.startswith('06-1-d'):
  s=s.replace('0.003024','0.003025').replace(r'\omega_{g0}',r'\omega_{c,h}')
  s=s.replace(r'> \lvert G(\mathrm{j}1.36)\rvert=\frac{10\sqrt{\left(\dfrac{1.36}{0.055}\right)^2+1}}{1.36\sqrt{1.36^2+1}\sqrt{\left(\dfrac{1.36}{2}\right)^2+1}\sqrt{\left(\dfrac{1.36}{0.003025}\right)^2+1}}=0.1983',r'''> \begin{aligned}
> |G(\mathrm j1.36)|
> &=\frac{10}{1.36\sqrt{1+1.36^2}\sqrt{1+(1.36/2)^2}}\\
> &\quad\times\sqrt{\frac{1+(1.36/0.055)^2}{1+(1.36/0.003025)^2}}\\
> &\approx0.1983
> \end{aligned}''')
 if p.name.startswith('06-3-c'):
  s=s.replace(r'> G(s)=\frac{200\left(\dfrac{s}{1.3}+1\right)}{s\left(\dfrac{s}{50}+1\right)\left(\dfrac{s}{100}+1\right)\left(\dfrac{s}{200}+1\right)\left(\dfrac{s}{0.0844}+1\right)\left(\dfrac{s}{154}+1\right)}',r'''> \begin{aligned}
> G(s)&=\frac{200(1+s/1.3)}{s(1+s/0.0844)(1+s/154)}\\
> &\quad\times\frac{1}{(1+s/50)(1+s/100)(1+s/200)}
> \end{aligned}''')
 if s!=before:
  s=re.sub(r'^modify: .*','modify: 2026-10-06',s,flags=re.M)
  p.write_bytes((b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\n','\r\n' if b'\r\n' in old else '\n').encode())
