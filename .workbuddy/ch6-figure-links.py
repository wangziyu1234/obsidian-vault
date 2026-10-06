from pathlib import Path
src=Path('.scripts/figures/block-pid-6-3.tex').read_text(encoding='utf-8-sig')
src=src[src.index(chr(92)+'documentclass'):]
src=src.replace(chr(92)+'dfrac{K}{s(s+1)(s+20)}',chr(92)+'dfrac{1}{s(s+1)(s+20)}')
Path('.scripts/figures/ch6-pid-block.tex').write_text('% figure: 校正-PID例63纯结构图.png\n'+src,encoding='utf-8')
base=Path('控制理论/自动控制原理')
def edit(prefix,fun):
 p=next(base.glob(prefix+' *.md'));raw=p.read_bytes();s=raw.decode('utf-8-sig').replace('\r\n','\n');s=fun(s);p.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode())
def pid(s):
 old='> ![[校正-讲义例1PID验算图.png|430]]\n> *讲义渐近验算图；最终以完整频响与阶跃响应验收。*'
 s=s.replace(old,'> ![[校正-PID实际验收.png|520]]\n> *圆点为实际截止点，虚线为设计频率15；裕度按实际截止点计算。*\n\n> [!note]- 讲义渐近图对照\n> ![[校正-讲义例1PID验算图.png|520]]')
 return s
edit('06-2-b',pid)
def combo(s):
 a=s.index('> ![[校正-讲义例4迟后超前图解.png');b=s.index('\n\n',a)
 old=s[a:b];s=s[:a]+s[b:]
 marker='> [!note]- 讲义对照'
 s=s.replace(marker,'> ![[校正-滞后超前实际验收.png|520]]\n> *蓝色为最终方案，灰色为初值；提高迟后极点后满足截止频率下限。*\n\n'+marker+'\n'+old)
 return s
edit('06-3-b',combo)
def desired(s):
 old='> ![[校正-讲义例2期望验算图.png|430]]\n> *验算：$L$（黑）在 $'+chr(92)+'omega_c=13$ 处过 0 dB，$'+chr(92)+'gamma$ 标注于中部。*'
 s=s.replace(old,'> [!note]- 讲义渐近验算图\n> ![[校正-讲义例2期望验算图.png|520]]\n> 13是设计频率，实际截止见下方三方案对比。')
 marker='> [!note] **三方案对比'
 s=s.replace(marker,'![[校正-期望特性实际验收.png|520]]\n\n'+marker)
 return s
edit('06-3-c',desired)
def block(s):
 a=s.index('> ![[自控-教材例6-3PID结构图.png');b=s.index('\n>\n',a)
 s=s[:a]+'> ![[校正-PID例63纯结构图.png|520]]\n> *按本例解答取对象增益为1；比例增益统一计入控制器。*'+s[b:]
 marker='> **① 令'
 a=s.index(marker)
 s=s[:a]+'> 原教材页见 [[自控-教材例6-3PID结构图.png|图6-20与原题]]。\n>\n'+s[a:]
 return s
edit('06-2',block)
