from pathlib import Path
r=Path('D:/obsidian/.scripts/figures')
for n in ['ch5-typical-links-nyquist.py','ch5-three-plots.py','ch5-vector-method.py']:
 p=r/n;s=p.read_text(encoding='utf-8')
 if 'nyquist' in n:s=s.replace('rect=(.01,.10,.99,.91)','rect=(.01,.17,.99,.91)')
 if 'three-plots' in n:
  s=s.replace('xytext=(4, -5)','xytext=(5, 5)').replace('xytext=(-18, 10)','xytext=(22, 10)')
 if 'vector' in n:
  s=s.replace('xy=(0.35, 9.2)','xy=(0.35, 9.8)').replace('(4,(-52,-12))','(4,(-52,-32))')
 p.write_text(s,encoding='utf-8')
