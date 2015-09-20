from util import *

#PROPERTIES
Rp=Rearth
Mp=Mearth
Ms=Mmoon
a=rmoon

#OCEAN
sigma=4.9E3
rho=5E3
A=0.5
B=1.0

#ANALYTICAL
mut=0
f=sigma/rho
alpha=1+5./2*f*(A/B)**3*(1-f)
delta=(A/B)**3*(1-f)
rhom=0.5*(rho+sigma)
F=((1+mut)*(1-f)*(1+3./(2*alpha)))/(1+mut-f+(3*sigma/(2*rho))*(1-f)-9/(4*alpha)*(A/B)**5*(1-f)**2)
H=2*rhom/(5*rho)*((1+mut+3./2*(A/B)**2*F*delta)/((1+mut)*(delta+2*sigma/(5*rho))))

print H

