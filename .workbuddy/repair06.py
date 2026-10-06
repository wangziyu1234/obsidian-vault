from pathlib import Path
import re
p=next(Path('控制理论/自动控制原理').glob('06-3-b *.md'))
s=p.read_text(encoding='utf-8-sig');a=s.index('> **⑥');b=s.index('> [!note]-',a)
t='''> **⑥ 修正幅值并最终验收。** 初值网络的实际截止频率约17.74 rad/s，低于20，不能判合格。保留两个零点与超前极点，只将滞后极点记作 $p$。先定义
>
> $$
> A_{20}=BSleft|BSfrac{G_0(BSmathrm j20)(1+BSmathrm j20/2)(1+BSmathrm j20/10.81)}{1+BSmathrm j20/37}BSright|
> $$
>
> 令完整开环在20处幅值为1：
>
> $$
> BSfrac{A_{20}}{BSsqrt{1+(20/p)^2}}=1
> $$
>
> $$
> p=BSfrac{20}{BSsqrt{A_{20}^2-1}}BSapprox0.403
> $$
>
> 为截止频率留少量余量，取 $p=0.41$，最终校正器为
>
> $$
> G_c(s)=BSfrac{(1+s/2)(1+s/10.81)}{(1+s/0.41)(1+s/37)}
> $$
>
> 完整频响给实际 $BSomega_cBSapprox20.27$ rad/s、$BSgammaBSapprox36.3^BScirc$；闭环稳定，$K_v=126$、斜坡误差为 $1/126$。**三项要求均满足，最终采用0.41，不采用图解初值0.343。**

'''.replace('BS',chr(92))
s=s[:a]+t+s[b:]
p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
for p in Path('控制理论/自动控制原理').glob('06*.md'):
 s=p.read_text(encoding='utf-8-sig')
 bad=[(i,ord(c)) for i,c in enumerate(s) if ord(c)<32 and c not in '\t\n\r']
 if bad:print(p.name,bad[:10])
