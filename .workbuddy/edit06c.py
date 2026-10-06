from pathlib import Path
exec(Path('.workbuddy/edit06.py').read_text(encoding='utf-8').split("for prefix in")[0])
p,s=read('06-3-b')
s=re.sub(r'> 卢京潮讲义《频率法串联迟后超前校正01》[^\n]*','> 相角裕度不足且截止频率受下限约束时，用六点图解给初值，再以完整频响修正并验收。',s)
s=s.replace('两转折几何平均处穿越','在两转折之间的渐近段求截止频率')
s=s.replace('**不行**；','工程上不宜采用；').replace('⑤ 验算：$\\omega_c=\\omega_c^*=20$ ✓；','⑤ 在设计频率20处试算相角（尚未验收实际截止频率）：')
a=s.index('> [!note] **例1 复核**');b=s.index('> 相关：',a)
s=s[:a]+r'''> **⑥ 修正幅值并最终验收。** 初值网络的实际截止频率约17.74 rad/s，低于20，不能判合格。保留两个零点与超前极点，只将滞后极点记作 $p$。先定义
>
> $$
> A_{20}=left|rac{G_0(mathrm j20)(1+mathrm j20/2)(1+mathrm j20/10.81)}{1+mathrm j20/37}ight|
> $$
>
> 令完整开环在20处幅值为1：
>
> $$
> rac{A_{20}}{sqrt{1+(20/p)^2}}=1
> $$
>
> $$
> p=rac{20}{sqrt{A_{20}^2-1}}approx0.403
> $$
>
> 为截止频率留少量余量，取 $p=0.41$，最终校正器为
>
> $$
> G_c(s)=rac{(1+s/2)(1+s/10.81)}{(1+s/0.41)(1+s/37)}
> $$
>
> 完整频响给实际 $omega_capprox20.27$ rad/s、$gammaapprox36.3^circ$；闭环稳定，$K_v=126$、斜坡误差为 $1/126$。**三项要求均满足，最终采用0.41，不采用图解初值0.343。**

> [!note]- 讲义对照
> 图中0.343为渐近初值；零点10.81在讲义部分公式中误排为10.18，本页统一按图解计算的10.81。教材例6-6采用稳定极点对消，本例直接叠加零极点；两种方法都要重算实际截止频率。

'''+s[b:]
save(p,s)
# Promote the actual lag result into the main derivation, rather than a second answer.
p,s=read('06-1-d')
s=s.replace('⑤ 验算：$\\omega_c=2.7>2.3$ ✓；','⑤ 先在设计频率2.7处试算相角：')
s=s.replace('> 满足要求。校正后 $G(s)=G_cG_0$','> 实际验收见下方：$\\omega_c\\approx2.39>2.3$、$\\gamma\\approx45.2^\\circ>40^\\circ$，满足要求。校正后 $G(s)=G_cG_0$')
save(p,s)
