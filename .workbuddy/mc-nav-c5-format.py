from pathlib import Path
import re
base=Path('D:/obsidian/控制理论/777习题集')
for p in base.glob('现控200题基础 第5章*.md'):
    raw=p.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n'
    s=raw.decode('utf-8').replace('\r\n','\n')
    s=re.sub(r'^\*\*5-\d+　答案[： ]?(.*?)\*\*（考点：(.*?)）$',lambda m:'**答案：** '+m[1]+'\n\n**考点：** '+m[2],s,flags=re.M)
    # Move matrix/long inline expressions out of prose, keeping quote depth.
    out=[];inside=False
    for line in s.splitlines():
        prefix=re.match(r'^(?:> ?)*',line)[0]
        body=line[len(prefix):]
        if body.strip()=='$$':
            inside=not inside;out.append(line);continue
        if inside or body.startswith(('|','#')):
            out.append(line);continue
        matches=list(re.finditer(r'\$([^$\n]+)\$',body))
        large=[m for m in matches if ('\\begin{' in m[1] or len(m[1])>85)]
        if not large:
            out.append(line);continue
        cursor=0
        for m in large:
            before=body[cursor:m.start()].strip()
            before=before.lstrip('，；、')
            if before: out.append(prefix+before)
            out.extend([prefix.rstrip(),prefix+'$$',prefix+m[1],prefix+'$$',prefix.rstrip()])
            cursor=m.end()
        after=body[cursor:].strip().lstrip('，；、')
        if after and after not in ('。','：'):out.append(prefix+after)
    s='\n'.join(out)+'\n'
    # Separate independent expressions previously packed into one display.
    def split_block(m):
        prefix=m[1];text=m[2]
        plain='\n'.join(x[len(prefix):] if x.startswith(prefix) else x for x in text.splitlines()).strip()
        if any(z in plain for z in ('\\begin{aligned}','\\begin{cases}')):return m[0]
        parts=re.split(r'[,;；]\\q(?:quad|uad)\s*',plain)
        if len(parts)<2:return m[0]
        return ('\n'+prefix.rstrip()+'\n').join(prefix+'$$\n'+prefix+t.strip()+'\n'+prefix+'$$' for t in parts)
    s=re.sub(r'^((?:> ?)*)\$\$\n(.*?)\n\1\$\$',split_block,s,flags=re.M|re.S)
    # Reduce the two longest quick-reference cells to their useful result.
    if '答案' in p.name:
        s=re.sub(r'^\| \[\[#✏️ 5-30　解析\\\|5-30\]\] \|.*$',r'| [[#✏️ 5-30　解析\\|5-30]] | 降维增益 $G=[3\\ \\ 4]^T$；动态方程与 $u$、$y$ 通道系数见本题正文 |',s,flags=re.M)
        s=re.sub(r'^\| \[\[#✏️ 5-34　解析\\\|5-34\]\] \|.*$',lambda m:r'| [[#✏️ 5-34　解析\|5-34]] | 误差坐标下输入为 $[B^T\ \ 0]^T v$；零初态传函 $W=C[sI-(A-BK)]^{-1}B$ |',s,flags=re.M)
    p.write_bytes(s.replace('\n',nl).encode('utf-8'))
print('formatted chapter 5')
