from util import *

#PROPERTIES
Rp=Rearth
Mp=Mearth
Ms=Mmoon
a=rmoon

#OCEAN
B=Rearth
T2=0.3
sigma=1E3

#CORE
A=0.5*Rearth
S2=0.2
rho=5E3

mc=4*pi/3*A**3*rho
gc=Gconst*mc/A**2
csic=(Ms/mc)*(A/a)**3*A

A=[[1,2],[3,-4]]
b=[2,3]

print linalg.solve(A,b)
