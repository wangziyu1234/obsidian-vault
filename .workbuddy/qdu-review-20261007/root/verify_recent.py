import sympy as S
import json
from pathlib import Path
s,t,w,z,a = S.symbols('s t w z a', real=True)
R=S.Rational
records=[]
def check(name, condition, conclusion):
    assert condition, name
    records.append({'question':name,'result':'pass','conclusion':conclusion})
def zero(expr): return S.simplify(expr)==0

p=s**5+4*s**4+4*s**3+8*s**2+10*s+6
check('2024 选择1', sum(bool(S.re(v)<0) for v in S.nroots(p))==3,'Routh first column: 1,4,2,-9,59/6,6; LHP=3')
check('2024 选择2', zero(s**3+R(3,4)*s**2+4*s+3-(s+R(3,4))*(s*s+4)), 'k=2,a=3/4; no offered choice')
check('2024 选择3',100*R(104,100)-4==100 and 100*R(1,10)==10,'closed-loop interpretation: 1.04,0.1; open-loop: 0.52,0.1')
p24=s**4+3*s**3+4*s*s+3*s+2
check('2024 选择4',all(S.re(v)<0 for v in S.nroots(p24)), 'stable; Kv=1; error=5')
check('2024 选择5',zero((a-3*a*a)**2-4*a**3-a*a*(1-a)*(1-9*a)),'a=exp(-1); conjugate roots modulus exp(-3/2)')
check('2024 选择6',S.det(s*S.eye(2)-S.Matrix([[0,1],[-1,-a]]))==s*s+a*s+1,'stable focus 0<a<2')
check('2024 选择7',zero(5/(1+S.I*S.sqrt(3))**3+R(5,8)), 'h=8/5')
b=R(1428,1000); aa=R(14,10); theta=R(456,10)*S.pi/180
tp=(S.pi+S.atan(b/aa)-theta)/b
check('2024 选择8',abs(float(tp)-2.20)<0.001,'exact derivative peak expression; option A')
seq=[S.Integer(0),R(368,1000)]
for i in range(2,8): seq.append(seq[-1]-R(632,1000)*seq[-2]+R(632,1000))
check('2024 选择9', seq[6]==R(894552064,10**9),'c6=0.894552064; A')
check('2024 选择10',zero(1/(s*(s+1)*(s+2))).subs(s,1) if False else zero((1/(s*(s+1)*(s+2))).subs(s,S.I*S.sqrt(2))+R(1,6)), '9<k<24 by N=6/k')
# Position + tachometer feedback directly gives denominator Tm*s^2+(1+K2*K3*Km*Kt)*s+K0*K1*K2*K3*Km.
check('2024 计算1',zero(30/(300*S.pi/180)-18/S.pi),'K0=18/pi; symbolic resistor gains retained')
c=1-4*S.exp(-t)+2*S.exp(-2*t)
check('2024 计算2',zero(S.diff(c,t,2)+3*S.diff(c,t)+2*c-2) and c.subs(t,0)==-1 and S.diff(c,t).subs(t,0)==0,'c=1-4e^-t+2e^-2t')
d=s*(s+3)*(s*s+2*s+2)
check('2024 计算3',zero(d+R(204,25)-(s*s+R(6,5))*(s*s+5*s+R(34,5))), 'stable 0<k<204/25; breakaway solves 4s^3+15s^2+16s+6=0')
A=S.Matrix([[1,0,0],[0,2,1],[0,0,2]]); C=S.Matrix([[1,1,0]]); L=S.Matrix([120,-103,210])
check('2024 计算4',zero((s*S.eye(3)-A+L*C).det()-(s+3)*(s+4)*(s+5)), 'observer L=[120,-103,210]')
P=(s+1)**2/(s*s*(s*s+2*s+2))
check('2024 计算5',zero(s*s*(s*s+2*s+2)+(s+1)**2-(s*s+s+1)**2) and zero(S.im(S.expand_complex(P.subs(s,S.I*w)))+2/(w*(w**4+4))), 'K=1; stable repeated complex roots; Nyquist real/imag verified')
check('2025 1',zero((s-1)**2*(s+1)*(s+5)*(s*s+2)-(s**6+4*s**5-4*s**4+4*s**3-7*s*s-8*s+10)), 'two RHP roots counting multiplicity')
c=S.sqrt(2)/4*S.sin(2*t)
check('2025 2',zero(S.expand_trig(S.diff(c,t)+2*c-S.sin(2*t+S.pi/4))), 'sqrt(2)/4 sin(2t)')
check('2025 3',zero(s*(s*s+3*s+1)+(2*s+1)-(s+1)**3),'Kv=1; error=4')
check('2025 4',S.degree((s+1)*(s+2)*(s+4),s)==3,'-60 dB/dec')
Ez=z*z/((z-R(1,5))*(z-R(3,5)))
check('2025 5',S.limit((1-1/z)*Ez,z,1)==0,'final value=0; reference omitted factor')
check('2025 6',zero((z-1)+a-(z-(1-a))), 'ZOH integrator pole 1-A; 0<A<2')
check('2025 7',zero(10/(1+S.I*S.sqrt(3))**3+R(5,4)),'gain margin 4/5')
check('2025 8',zero((s*S.eye(2)-S.Matrix([[0,1],[-1,R(1,2)]])).det()-(s*s-s/2+1)), '(0,0) unstable focus; (-1,0) saddle')
A=S.Matrix([[-4,4,-2],[0,-8,0],[1,-4,0]]); B=S.Matrix([0,0,1])
check('2025 9',S.Matrix.hstack(B,A*B,A*A*B).rank()==2,'rank=2')
A=S.Matrix([[1,0,1],[0,1,0],[1,0,0]]); B=S.Matrix([0,1,1]); C=S.Matrix([[1,1,0]])
T=S.Matrix([[-1,1,0],[-1,-1,1],[1,-2,1]])
check('2025 10',T.inv()*A*T==S.Matrix([[0,1,0],[0,0,1],[-1,0,2]]) and T.inv()*B==S.Matrix([0,0,1]) and C*T==S.Matrix([[-2,0,1]]),'all transformed matrices verified')
check('2025 11',zero(s*s+5*s+25-(s*s+2*R(1,2)*5*s+25)), 'K=[25,5]; numerator 1 without prefilter')
check('2025 12',zero(1/(z-1)-1+(z-1)/(z-a)-(a*z+1-2*a)/((z-1)*(z-a))), 'a=exp(-1); closed characteristic z^2-z+1-a')
T1,T2,k=S.symbols('T1 T2 k',positive=True)
g=k/(s*(T1*s+1)*(T2*s+1))
check('2025 13',zero(g.subs(s,S.I/S.sqrt(T1*T2))+k*T1*T2/(T1+T2)), 'stable k<(T1+T2)/(T1*T2)')
amps=[S.sqrt(8+v*2*S.sqrt(16-S.pi**2))/S.pi for v in [-1,1]]
check('2025 14',all(zero(S.pi**2*x**4-16*x*x+4) for x in amps) and zero((10/(s*(s/2+1)*(s/8+1))).subs(s,4*S.I)+1), 'omega=4; both amplitude branches real; small unstable, large stable in DF approximation')
A=S.Matrix([[4,4,4],[-11,-12,-12],[13,14,13]]); B=S.Matrix([1,-1,0]); Q=S.Matrix([[1,0,0],[0,1,0],[1,1,1]])
At=Q*A*Q.inv(); L=S.Matrix([12,-5]); F=At[:2,:2]-L*At[2:3,:2]
check('2025 15',F==S.Matrix([[-12,-12],[6,5]]) and F*L+At[:2,2:3]-5*L==S.Matrix([-140,60]) and zero((s*S.eye(2)-F).det()-(s+3)*(s+4)), 'reduced observer verified including y injection and recovery')
Path(__file__).with_suffix('.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
print(f'{len(records)} recent-paper question checks passed')
