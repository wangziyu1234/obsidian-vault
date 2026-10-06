from pathlib import Path
import re
root=Path('D:/obsidian/控制理论/自动控制原理')
for prefix in ['05-4-c','05-3-a']:
 p=next(root.glob(prefix+' *.md'));raw=p.read_bytes();s=raw.decode('utf-8-sig');nl='\r\n' if '\r\n' in s else '\n';s=s.replace('\r\n','\n')
 for a,b in [('\x0crac',r'\frac'),('\x08egin',r'\begin'),('\x08oxed',r'\boxed'),('\x0barepsilon',r'\varepsilon'),('\theta',r'\theta'),('\to',r'\to')]:
  s=s.replace(a,b)
 for cmd in ['operatorname','varepsilon','mathrm','arctan','sqrt','omega','theta','infty','angle','circ','begin','end','lim','boxed','pm','approx']:
  s=re.sub(r'(?<!\\)'+cmd,lambda m:'\\'+m.group(0),s)
 s=s.replace(r'0<\omega<1\[4pt]',r'0<\omega<1\\[4pt]')
 if prefix=='05-3-a':
  s=s.replace(r'\omega_r=28.77',r'\omega_r\approx28.74').replace(r'$-78.3°$',r'$-78.0°$').replace(r'$(5.08,\ -24.64)$',r'$(5.21,\ -24.61)$')
 p.write_bytes(s.replace('\n',nl).encode('utf-8'))
