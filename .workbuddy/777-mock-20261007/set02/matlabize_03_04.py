from pathlib import Path
import json
root=Path('D:/obsidian/控制理论/青岛大学825真题/777改编模拟卷/Markdown笔记')
maps=[]
def alter(no,q,old,new,models,codes,params=None):
    path=root/f'{no:02d} 青大825模拟卷（试题）.md'
    raw=path.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); txt=raw.decode('utf-8-sig')
    nl='\r\n' if b'\r\n' in raw else '\n'; txt=txt.replace('\r\n','\n')
    start=txt.index(f'## 第{q}题'); end=txt.find('\n## 第',start+1)
    if end<0:end=len(txt)
    part=txt[start:end]
    assert part.count(old)==1,(no,q,old)
    part=part.replace(old,new)
    txt=txt[:start]+part+txt[end:]
    path.write_bytes((b'\xef\xbb\xbf' if bom else b'')+txt.replace('\n',nl).encode('utf-8'))
    maps.append(dict(set=no,question=q,original_models=models,matlab_code=codes,parameters=params or {},old_text=old,new_text=new))
alter(3,1,'某闭环传递函数由 MATLAB 代码给出：','某闭环传递函数由 MATLAB 代码给出，执行前实参数 `k1`、`k2` 已赋值：',{'Phi':'9*k1/(2*s^2+6*k2*s+9*k1-2)'},'num = 9*k1;\nden = [2, 6*k2, 9*k1-2];\nPhi = tf(num, den);',{'k1':2,'k2':1})
alter(3,4,r'''单位负反馈系统的开环传递函数为

$$
G(s)=\frac{\sqrt2e^{-\tau s}}{s(s+1)},\qquad0\le\tau<\frac\pi4.
$$''',r'''单位负反馈系统的开环模型由以下代码定义。执行前 `tau` 已赋值，且 $0\le\tau<\pi/4$。

```matlab
G = tf(sqrt(2),[1 1 0],'InputDelay',tau);
```''',{'G':'sqrt(2)*exp(-tau*s)/(s*(s+1))'},"G = tf(sqrt(2),[1 1 0],'InputDelay',tau);",{'tau':0.2})
alter(3,6,r'''零输入系统

$$
\dot x=\begin{bmatrix}-1&2\\0&-1\end{bmatrix}x,\qquad x(0)=\begin{bmatrix}0\\1\end{bmatrix}
$$''',r'''零输入系统的状态矩阵和初始状态由以下代码给出：

```matlab
A = [-1 2; 0 -1];
x0 = [0; 1];
```

系统满足 $\dot x=Ax$、$x(0)=\texttt{x0}$，''',{'A':[[-1,2],[0,-1]],'x0':[[0],[1]]},'A = [-1 2; 0 -1];\nx0 = [0; 1];')
alter(3,8,r'''单位负反馈系统开环传递函数为

$$
G(s)=\frac{2s+3}{s(s+1)(Ts+1)}.
$$''',r'''单位负反馈系统的开环模型由以下代码定义。执行前实参数 `T` 已赋值，且 $T\ge0$。

```matlab
s = tf('s');
G = (2*s+3)/(s*(s+1)*(T*s+1));
```''',{'G':'(2*s+3)/(s*(s+1)*(T*s+1))'},"s = tf('s');\nG = (2*s+3)/(s*(s+1)*(T*s+1));",{'T':2})
alter(3,10,r'''理想 PD 控制器为 $G_c(s)=K_p+K_ds$，其中 $K_p,K_d>0$。下列说法正确的是（　）。''',r'''理想 PD 控制器由以下代码定义。执行前 `Kp`、`Kd` 已赋正值，分别对应 $K_p,K_d$。

```matlab
Gc = tf([Kd Kp],1);
```

下列说法正确的是（　）。''',{'Gc':'Kp+Kd*s'},'Gc = tf([Kd Kp],1);',{'Kp':2,'Kd':1})
alter(3,12,r'''某系统 $A=\operatorname{diag}(-1,-2)$，$C=[1\ 2]$。设计全维观测器''',r'''某连续系统的相关矩阵由以下代码给出：

```matlab
A = diag([-1 -2]);
C = [1 2];
```

设计全维观测器''',{'A':[[-1,0],[0,-2]],'C':[[1,2]]},'A = diag([-1 -2]);\nC = [1 2];')
alter(3,13,r'''单位负反馈系统的开环传递函数为

$$
G(s)=\frac{k(1-s)}{s(s+2)},\qquad k>0.
$$''',r'''单位负反馈系统的开环模型由以下代码定义。执行前参数 `k` 已赋值，且 $k>0$。

```matlab
G = tf([-k k],[1 2 0]);
```''',{'G':'k*(1-s)/(s*(s+2))'},'G = tf([-k k],[1 2 0]);',{'k':1})
alter(3,15,r'''零输入非线性负反馈环路定义为 $e(t)=-c(t)$、$v(t)=2\operatorname{sgn}e(t)$。线性环节输入为 $v$、输出为 $c$，其传递函数为

$$
G(s)=\frac{k}{s(s+1)(s+2)},\qquad k>0.
$$''',r'''零输入非线性负反馈环路定义为 $e(t)=-c(t)$、$v(t)=2\operatorname{sgn}e(t)$。线性环节输入为 $v$、输出为 $c$，其模型由以下代码定义。执行前参数 `k` 已赋正值。

```matlab
G = zpk([],[0 -1 -2],k);
```''',{'G':'k/(s*(s+1)*(s+2))'},'G = zpk([],[0 -1 -2],k);',{'k':1})
alter(3,16,r'''单位负反馈数字控制系统的连续对象为 $P(s)=1/s$，对象前接零阶保持器，采样周期 $T=1/2\,\mathrm s$。采样时刻先读取 $c[k]=c(kT)$，计算偏差 $e[k]=r[k]-c[k]$，数字控制器为

$$
D(z)=\frac{U(z)}{E(z)}=K\frac{z-a}{z-1},\qquad K>0.
$$''',r'''单位负反馈数字控制系统的连续对象 `P` 与数字控制器 `Dc` 由以下代码定义。`Dc` 对应 $U(z)/E(z)$。执行前参数 `K`、`a` 已赋值，且 $K>0$。

```matlab
Ts = 1/2;
P = tf(1,[1 0]);
Dc = tf(K*[1 -a],[1 -1],Ts);
```

对象前接零阶保持器，采样周期 $T=\texttt{Ts}=1/2\,\mathrm s$。采样时刻先读取 $c[k]=c(kT)$，计算偏差 $e[k]=r[k]-c[k]$。''',{'P':'1/s','Dc':'K*(z-a)/(z-1)','Ts':0.5},'Ts = 1/2;\nP = tf(1,[1 0]);\nDc = tf(K*[1 -a],[1 -1],Ts);',{'K':2,'a':0.75})
alter(3,17,r'''连续系统为

$$
\dot x=\begin{bmatrix}0&1\\0&-2\end{bmatrix}x
+\begin{bmatrix}0\\1\end{bmatrix}u,
$$

$$
y=x_1+x_2.
$$''',r'''连续系统由以下代码定义，状态顺序为 $x=[x_1\ x_2]^T$：

```matlab
A = [0 1; 0 -2];
B = [0; 1];
C = [1 1];
D = 0;
sys = ss(A,B,C,D);
```''',{'A':[[0,1],[0,-2]],'B':[[0],[1]],'C':[[1,1]],'D':0},'A = [0 1; 0 -2];\nB = [0; 1];\nC = [1 1];\nD = 0;\nsys = ss(A,B,C,D);')
alter(4,3,r'''零初始条件下，系统闭环传递函数为

$$
\Phi(s)=\frac{18}{s^2+4s+8}.
$$''',r'''零初始条件下，系统闭环模型由以下代码定义：

```matlab
Phi = tf(18,[1 4 8]);
```''',{'Phi':'18/(s^2+4*s+8)'},'Phi = tf(18,[1 4 8]);')
alter(4,4,r'''连续系统的状态矩阵与输出矩阵为

$$
A=\begin{bmatrix}0&1\\-2&-3\end{bmatrix},\qquad C=\begin{bmatrix}1&c\end{bmatrix},
$$

其中 $c$ 为实数。系统完全能观的充要条件为（　）。''',r'''连续系统的状态矩阵与输出矩阵由以下代码给出。执行前实参数 `c` 已赋值。

```matlab
A = [0 1; -2 -3];
C = [1 c];
```

系统完全能观的充要条件为（　）。''',{'A':[[0,1],[-2,-3]],'C':'[1 c]'},'A = [0 1; -2 -3];\nC = [1 c];',{'c':0.25})
alter(4,6,r'''单位负反馈系统的原开环传递函数及串联校正装置为

$$
G_0(s)=\frac1{s(s+1)}.
$$

$$
G_c(s)=10\frac{10s+1}{100s+1}.
$$''',r'''单位负反馈系统的原开环模型 `G0` 及串联校正装置 `Gc` 由以下代码定义：

```matlab
G0 = tf(1,[1 1 0]);
Gc = 10*tf([10 1],[100 1]);
```''',{'G0':'1/(s*(s+1))','Gc':'10*(10*s+1)/(100*s+1)'},'G0 = tf(1,[1 1 0]);\nGc = 10*tf([10 1],[100 1]);')
alter(4,9,r'''单位负反馈系统开环传递函数为

$$
G(s)=\frac{K(s+2)}{s(s+1)(s+3)},\qquad K>0.
$$''',r'''单位负反馈系统的开环模型由以下代码定义。执行前参数 `K` 已赋正值。

```matlab
G = zpk(-2,[0 -1 -3],K);
```''',{'G':'K*(s+2)/(s*(s+1)*(s+3))'},'G = zpk(-2,[0 -1 -3],K);',{'K':1})
alter(4,11,r'''零输入系统

$$
\dot x=\begin{bmatrix}0&1\\-1&0\end{bmatrix}x
$$

的原点是（　）。''',r'''零输入系统满足 $\dot x=Ax$，状态矩阵由以下代码给出：

```matlab
A = [0 1; -1 0];
```

其原点是（　）。''',{'A':[[0,1],[-1,0]]},'A = [0 1; -1 0];')
alter(4,14,r'''单位负反馈系统开环传递函数为

$$
G(s)=\frac{k}{s(s^2+4s+8)},\qquad k>0.
$$''',r'''单位负反馈系统的开环模型由以下代码定义。执行前参数 `k` 已赋正值。

```matlab
G = tf(k,[1 4 8 0]);
```''',{'G':'k/(s*(s^2+4*s+8))'},'G = tf(k,[1 4 8 0]);',{'k':16})
alter(4,15,r'''单位负反馈系统的开环传递函数为

$$
G_1(s)=\frac{k_1}{s(T_1s+1)},\qquad k_1,T_1>0.
$$

调整参数后变为

$$
G_2(s)=\frac{k_2}{s(T_2s+1)},\qquad k_2,T_2>0.
$$''',r'''单位负反馈系统调整前后的开环模型分别为 `G1`、`G2`。执行前参数 `k1`、`T1`、`k2`、`T2` 已赋正值，分别对应 $k_1,T_1,k_2,T_2$。

```matlab
G1 = tf(k1,[T1 1 0]);
G2 = tf(k2,[T2 1 0]);
```''',{'G1':'k1/(s*(T1*s+1))','G2':'k2/(s*(T2*s+1))'},'G1 = tf(k1,[T1 1 0]);\nG2 = tf(k2,[T2 1 0]);',{'k1':1.4142135623730951,'T1':1,'k2':2.8284271247461903,'T2':0.5})
alter(4,16,r'''连续系统有两个独立输入：

$$
\dot x=Ax+Bu,
$$

$$
A=\begin{bmatrix}0&1\\0&-2\end{bmatrix},
\qquad B=\begin{bmatrix}1&0\\0&1\end{bmatrix}.
$$

$$
y=[1\ 0]x.
$$''',r'''连续系统有两个独立输入，由以下代码定义。状态顺序为 $x=[x_1\ x_2]^T$，输入顺序为 $u=[u_1\ u_2]^T$。

```matlab
A = [0 1; 0 -2];
B = eye(2);
C = [1 0];
D = zeros(1,2);
sys = ss(A,B,C,D);
```''',{'A':[[0,1],[0,-2]],'B':[[1,0],[0,1]],'C':[[1,0]],'D':[[0,0]]},'A = [0 1; 0 -2];\nB = eye(2);\nC = [1 0];\nD = zeros(1,2);\nsys = ss(A,B,C,D);')
alter(4,17,r'''被控对象的输入输出关系为

$$
G(s)=\frac2{(s+1)(s+2)}.
$$''',r'''被控对象的输入输出模型由以下代码定义：

```matlab
G = zpk([],[-1 -2],2);
```''',{'G':'2/((s+1)*(s+2))'},'G = zpk([],[-1 -2],2);')
Path(__file__).with_name('matlab_models_03_04.json').write_text(json.dumps(maps,ensure_ascii=False,indent=2),encoding='utf-8')
print('converted',len(maps),'models/contexts')
