from scipy import optimize as op
import numpy as np
c=np.array([35,17,9,5,2])
A_ub=np.array([[8,2,13,6,8]])
B_ub=np.array([25])
res=op.linprog(-c,A_ub,B_ub,bounds=((0,0.5),(0,0.5),(0,0.5),(0,0.5),(0,0.5)) )
print(res)