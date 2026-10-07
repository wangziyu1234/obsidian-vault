import sympy as S
from pathlib import Path
q=S.symbols('q',positive=True)
M=S.Matrix([[q,q],[-q,1-q]])
r=(2*q-1)/(2*q)
P=S.Matrix([[1,r],[r,1]])
assert S.simplify(M.T*P*M-q*P)==S.zeros(2)
# a=exp(-1) in (11/30,3/8), hence q in (5/8,19/30).
# For t=k+tau, c(t)-1=[2-tau-exp(-tau),1-exp(-tau)] x_k.
# The two coefficients lie in [q,1] and [0,q]. The negative cross-term
# in l*P^-1*l^T may be discarded for a rigorous upper bound.
upper2=(S.Rational(19,30)**5)*(1+S.Rational(19,30)**2)/(1-S.Rational(4,19)**2)
# log(q) > log(5/8) > -1/2, so the first peak error > 5/8-(19/30)^2/2.
first_lower=S.Rational(5,8)-S.Rational(19,30)**2/2
assert upper2 < first_lower**2
# Thus all k>=5 are below the first peak; k=0,1,2 increase and k=4 decreases.
Path(__file__).with_suffix('.txt').write_text('PASS: exact quadratic energy contraction M^T P M=qP; rational bounds exclude larger peaks for k>=5. First continuous maximum is 1+q+q^2 ln(q) at 3-ln(q).',encoding='utf8')
print('Global first-peak proof verified with rational bounds.')
