---
create: 2026-09-26
modify: 2026-09-26
tags: [知识点, 自动控制原理, 公式速查]
type: example
---

> 返回：[[06-2 PID与反馈前馈校正]] | 返回目录：[[自动控制原理]]

# 第6章（二-b）PID 频率法设计例题（卢京潮讲义）

> [!abstract] 本讲定位
> 卢京潮讲义《串联PID校正01》例1：**0 型对象 + PID 升型消差**的频域完整设计——查经验曲线定 $\gamma^*,\omega_c^*$，选 $\omega_c$ 后按「第一零点吃满 $\varphi_m$、零点乘积由幅值平衡定」定点展开出 $K_D,K_P,K_I$。配图为讲义原图裁件，全部数值经精确复算复核。

## 📐 6.12 PID 频率法设计例题（卢京潮讲义）

> [!tip] **PID 频率法设计五步（先方法后例题）**
> ① **定增益与型别**：PID 的积分支路升型一级（0 型 → Ⅰ 型），斜坡误差 $e_{ss}=\dfrac{1}{K_I K}$，据此配定 $K$ 与 $K_I$。
> ② **查经验曲线**（教材 P173 图 5-56，理论依据即 [[06-1-1 校正基础与性能换算]] 的高阶经验式）：由 $\sigma\%$ 查 $\gamma^*$，由 $t_s=\dfrac{K(\gamma)}{\omega_c}$ 查 $\omega_c^*$（$\gamma=65°$ 档系数 $6.8$）。
> ③ **画 $L_0$、判缺口**：渐近幅值方程解 $\omega_{c0}$ 与 $\gamma_0$；选 $\omega_c>\omega_c^*$，需补相角 $\varphi_m=\gamma^*-\gamma_0(\omega_c)+5°\sim10°$。
> ④ **「二零一极」定点**（两个零点一个积分极点，$G_c=\dfrac{(\frac{s}{\omega_1}+1)(\frac{s}{\omega_2}+1)}{s}$）：
>    第一零点吃满 $\varphi_m$：$\arctan\dfrac{\omega_c}{\omega_2}=\varphi_m\ \Rightarrow\ \omega_2=\dfrac{\omega_c}{\tan\varphi_m}$；
>    零点乘积由幅值平衡定：$\omega_1\omega_2=\omega_0=\dfrac{\omega_{c0}^2}{\omega_c}$（等价写法 $\dfrac{\omega_c}{\omega_{c0}}=\dfrac{\omega_{c0}}{\omega_0}$），再 $\omega_1=\dfrac{\omega_0}{\omega_2}$。
> ⑤ **展开定参、验算**：$G_c=\dfrac{K_Ds^2+K_Ps+K_I}{s}$，验算 $\gamma\ge\gamma^*$、$\omega_c\ge\omega_c^*$。

> [!example] ✏️ **例1（卢京潮讲义《串联PID校正01》）0 型对象的 PID 设计**
>
> **题目**：单位反馈系统
>
> $$
> G(s)=\frac{K}{(s+1)\left(\dfrac{s}{5}+1\right)\left(\dfrac{s}{30}+1\right)}
> $$
>
> 要求 $r(t)=t$ 时 $e_{ss}^*\le0.1$、$\sigma\%\le20\%$、$t_s\le0.5$，试设计 PID 控制器 $G_c(s)$。
>
> **解**：
>
> ① 指标换算：PID 积分使系统升为 Ⅰ 型，$e_{ss}=\dfrac{1}{K_I K}$，取 $K=10$、$K_I=1$（$e_{ss}=0.1$ ✓）。查图 5-56：
>
> $$
> \sigma\%\le20\%\ \Rightarrow\ \gamma^*\ge65°,\qquad t_s=\frac{6.8}{\omega_c^*}\le0.5\ \Rightarrow\ \omega_c^*\ge13.6
> $$
>
> ② 作 $L_0(\omega)$（转折 $1,5,30$）：穿越落在 $5\sim30$ 的 $-40$ 段，渐近幅值 $20\lg\dfrac{K\cdot5}{\omega^2}=0$ 给
>
> $$
> \omega_{c0}=\sqrt{5\times10}=7.07<13.6\ (\text{快速性不足})
> $$
>
> $$
> \gamma_0=180°-81.95°-54.74°-13.26°=30°<65°\ (\text{平稳性不足})
> $$
>
> 快速性、平稳性双缺口，且需积分升型消差 ⟹ 选 **PID**（$\gamma_0(\omega_c^*)=\gamma_0(13.6)\approx0°$，同样远小于 $65°$）。
>
> ③ 选 $\omega_c=15>13.6$。由 $\gamma_0(15)=180°-86.2°-71.6°-26.5°=-4.3°$ 得需补相角：
>
> $$
> \varphi_m=\gamma^*-\gamma_0(\omega_c)+6°=65°+4.3°+6°=75.3°
> $$
>
> ![[校正-讲义例1PID构造图.png|430]]
> *A—B 定点：$L_c$（红）在 $\omega_1\sim\omega_2$ 走 0 dB 平段，$\omega_2$ 后以 $+20$ dB/dec 上穿 $L_0$（蓝），把穿越从 $\omega_{c0}=7.07$ 拉到 $\omega_c=15$。*
>
> ④ 定转折（「二零一极」结构）：
>
> $$
> \arctan\frac{15}{\omega_2}=\varphi_m=75.3°\ \Rightarrow\ \omega_2=\frac{15}{\tan75.3°}=3.9
> $$
>
> $$
> \omega_0=\frac{\omega_{c0}^2}{\omega_c}=\frac{50}{15}=\frac{10}{3},\qquad \omega_1=\frac{\omega_0}{\omega_2}=\frac{10}{3\times3.9}=0.855
> $$
>
> ![[校正-讲义例1PID相角定点图.png|520]]
> *相角定点：第一零点 $\frac{s}{\omega_2}+1$ 在 $\omega_c$ 处提供的相角 $\arctan\frac{\omega_c}{\omega_2}$ 恰取满 $\varphi_m=75.3°$（品红为零点相频曲线，红为直线近似）。*
>
> ⑤ 写出并展开：
>
> $$
> G_c(s)=\frac{\left(\dfrac{s}{0.855}+1\right)\left(\dfrac{s}{3.9}+1\right)}{s}=\frac{0.3s^2+1.426s+1}{s}=\frac{K_Ds^2+K_Ps+K_I}{s}
> $$
>
> $$
> K_D=0.3,\qquad K_P=1.426,\qquad K_I=1
> $$
>
> 验算（$\omega_c=15\ge13.6$ ✓）：
>
> $$
> \gamma=180°+86.7°+75.4°-90°-86.2°-71.6°-26.5°=67.85°>65°=\gamma^*\quad\checkmark
> $$
>
> ![[校正-讲义例1PID验算图.png|430]]
> *验算：$L$（黑）在 $\omega_c=15$ 处过 0 dB，$\gamma$ 标注于下方。*

> [!note] **例1 复核**
> 渐近口径全部吻合：$\gamma_0=30.06°$、$\varphi_m=75.32°$、$\omega_1=0.855$、$K_D=0.300$、$K_P=1.426$、$\gamma=67.85°$。
> 讲义两处笔误：① $\gamma_0(\omega_c^*)$ 一式印作「$=4.789°$」，但其自印的三项 $180°-85.79°-69.81°-24.39°$ 加总应为 $\approx0°$（精确 $-0.004°$），判断（$\ll65°$）不受影响；
> ② 验算式 $\arctan\dfrac{15}{3.9}$ 印 $74.5°$，应 $75.4°$（终值 $67.85°$ 按 $75.4°$ 才闭合）。
> 精确解：实际穿越 $\omega_c\approx13.4$（$\lvert G(\mathrm{j}15)\rvert=-1.15$ dB），该处 $\gamma\approx70.9°$——设计频率与实际穿越分开写（同 [[06-1-3 滞后校正与图解设计|教材例 6-5]] 复核口径）。
> **一个设计细节**：$G_c$ 在 $\omega_c$ 处实供相角 $72.2°$，比 $\varphi_m=75.3°$ 少 $3.1°$（第二零点的贡献没有单零点定点式隐含的富余），但需求量只是 $\gamma^*-\gamma_0=69.3°$，缺口由预留的 $6°$ 吸收——这正是 $\varphi_m$ 式中 $+5°\sim10°$ 余量的作用。

> 相关：方法篇 [[06-2 PID与反馈前馈校正]] · 滞后例题 [[06-1-d 频率法滞后校正例题（卢京潮讲义）]] · 期望特性设计 [[06-3-c 期望特性设计法（卢京潮讲义）]] · 本讲 [[06 第6章 线性系统的校正方法]] · 速查 [[自动控制原理]]
