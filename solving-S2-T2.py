from util import *

#PROPERTIES
Rp=Rearth
Mp=Mearth
Ms=Mmoon
a=rmoon

#OCEAN
B=Rearth
sigma=1E3
csi=(Ms/Mp)*(B/a)**3*B

#CORE
A=0.5*Rearth
rho=5E3
mu=1E11 #Pa

mc=4*pi/3*A**3*rho
gc=Gconst*mc/A**2
csic=(Ms/mc)*(A/a)**3*A

#OTHER
f=sigma/rho
mut=19*mu/(2*rho*gc*A)

#NUMERCIAL
a1T2=2./5*f+(A/B)**3*(1-f)
a1S2=-3./5*(A/B)**5*(1-f)
b1=csic/A

fac=1/mut*(1-f)
a2T2=fac*3./2*f
a2S2=-fac*(1.+3./2*f)+1
b2=-fac*5./2*csic/A

a=[[a1T2,a1S2],[a2T2,a2S2]]
b=[b1,b2]

print linalg.solve(a,b)

#ANALYTICAL
alpha=1+5./2*f*(A/B)**3*(1-f)
delta=(A/B)**3*(1-f)
rhom=0.5*(rho+sigma)
F=((1+mut)*(1-f)*(1+3./(2*alpha)))/(1+mut-f+(3*sigma/(2*rho))*(1-f)-9/(4*alpha)*(A/B)**5*(1-f)**2)
H=2*rhom/(5*rho)*((1+mut+3./2*(A/B)**2*F*delta)/((1+mut)*(delta+2*sigma/(5*rho))))

T2=H*(5./2)*csi/B
S2=F*(5./2)*csic/(1+mut)/A

print T2,S2

