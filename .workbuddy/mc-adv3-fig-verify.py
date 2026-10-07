from pathlib import Path
import sympy as S
from PIL import Image
import numpy as np

s=S.symbols('s')
M=S.Matrix
I=S.eye
root=Path('D:/obsidian')

# Figure 3-5: x1dot=x2+w, x2dot=-2*x1-3*x2-2*w.
A=M([[0,1],[-2,-3]]); D=M([1,-2]); C=M([[6,3]])
assert S.simplify((C*(s*I(2)-A).inv()*D)[0])==0
assert S.factor(A.charpoly(s).as_expr())==(s+1)*(s+2)

# Figure 3-20: plant and positive innovation observer, u=v-K*xhat.
A=M([[-1,1],[-2,-4]]);B=M([0,1]);C=M([[1,0]])
K=M([[10,4]]);G=M([13,22])
assert A-G*C==M([[-14,1],[-24,-4]])
assert S.expand((A-B*K).charpoly(s).as_expr()-(s+4)*(s+5))==0
assert S.expand((A-G*C).charpoly(s).as_expr()-(s+8)*(s+10))==0
AA=(A.row_join(-B*K)).col_join((G*C).row_join(A-B*K-G*C))
BB=B.col_join(B);CC=C.row_join(S.zeros(1,2))
assert S.factor((CC*(s*I(4)-AA).inv()*BB)[0])==1/((s+4)*(s+5))

# Figure 3-24: five scalar integrators, states x1,x2,x3,omega1,omega2.
A=M([[0,1,0],[0,0,1],[0,-2,-3]]); B=M([0,0,1]); C=M([[1,0,0]])
K=M([[3,2,1]]);F=M([[-3,-4],[1,-7]]);Bd=M([1,0]);L=M([-34,-47])
R=M([[0,0],[0,1],[1,0]]);N=M([1,7,2])
assert K*R==M([[1,2]]) and K*N==M([19])
assert S.expand(F.charpoly(s).as_expr()-(s+5)**2)==0
AA=(A-B*K*N*C).row_join(-B*K*R)
AA=AA.col_join(((L-Bd*K*N)*C).row_join(F-Bd*K*R))
BB=B.col_join(Bd);CC=C.row_join(S.zeros(1,2))
expected=(s+3)*(s*s+s+1)*(s+5)**2
assert S.expand(AA.charpoly(s).as_expr()-expected)==0
assert S.factor((CC*(s*I(5)-AA).inv()*BB)[0])==1/((s+3)*(s*s+s+1))
print('PASS: 3-5 zero disturbance transfer; 3-20 feedback/observer poles; 3-24 five-state transfer and poles.')

# Confirm the saved figures have visible whitespace on every canvas boundary.
for name in ['现控强化3-3-开环系统结构图.png','现控强化3-22-状态反馈系统框图.png',
             '现控强化3-5-ans-状态变量图.png','现控强化3-20-完整闭环结构图.png',
             '现控强化3-24-降维观测反馈结构图.png']:
    im=Image.open(root/'附件'/name).convert('RGBA')
    bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im)
    grey=np.asarray(bg.convert('L')); ink=grey<200
    ys,xs=np.where(ink)
    margins=(int(xs.min()),int(ys.min()),im.width-1-int(xs.max()),im.height-1-int(ys.max()))
    assert min(margins)>=10,(name,margins)
    print(name,im.size,'ink margins:',margins)
print('PASS: 5 image canvas-boundary checks. TikZ line/label layout additionally inspected visually.')
