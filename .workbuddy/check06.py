import control as ct
import numpy as np
s=ct.tf('s')
def show(name,L):
 print(name,ct.margin(L),ct.step_info(ct.feedback(L),SettlingTimeThreshold=.05))
G=10/((s+1)*(s/5+1)*(s/30+1))
show('pid',G*(.3*s*s+1.426*s+1)/s)
show('pid-simple',G*(s*s/3+1.5*s+1)/s)
for f in [.343,.38,.39]:
 show('combo'+str(f),126/(s*(s/10+1)*(s/60+1))*(s/2+1)*(s/10.81+1)/((s/f+1)*(s/37+1)))
for f,z,p in [(.0844,1.3,154),(.195,3,154),(.0845,1.3,65)]:
 show('desired',200*(s/z+1)/(s*(s/50+1)*(s/100+1)*(s/200+1)*(s/f+1)*(s/p+1)))
show('lag',30/(s*(s/5+1)*(s/10+1))*(s/.27+1)/(s/.0243+1))
