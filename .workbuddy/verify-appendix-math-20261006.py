import sympy as s

w, tau, T, a, K, z = s.symbols('w tau T a K z', positive=True)
g = (1-s.I*tau*w)**2/(1+s.I*T*w)**2
assert s.simplify(s.limit(g, w, s.oo) - (tau/T)**2) == 0
assert s.simplify(g.subs({tau:T, w:1/T}) + 1) == 0
assert s.simplify(s.limit(s.im(s.expand_complex(g))*w,w,s.oo) - 2*tau*(T+tau)/T**3) == 0
gd = K*((a*T-1+s.exp(-a*T))*z + 1-s.exp(-a*T)-a*T*s.exp(-a*T))/(a*a*(z-1)*(z-s.exp(-a*T)))
assert s.simplify(s.limit(gd,a,0) - K*T*T*(z+1)/(2*(z-1)**2)) == 0
for delta in [s.Rational(1,20), s.Rational(1,50), s.Rational(1,2)]:
    t = -T*s.log(delta)
    assert s.simplify(s.exp(-t/T)-delta) == 0
print('PASS: finite endpoint, approach side, nonconstant all-pass, ZOH limit, exact first-order times.')
