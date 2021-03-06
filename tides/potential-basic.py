#!/usr/bin/env python
#-*-coding:utf-8-*-
from constants import *
from numpy import *
from matplotlib.pyplot import *
close('all')

###################################################
#UTILITIES
###################################################
DEG=pi/180
RAD=180/pi

###################################################
#SCRIPT
###################################################
C=Rearth
rho=rhoearth

rint=linspace(0,C,100)
rext=linspace(C,2*C,100)

Vint=-2*pi/3*rho*Gconst*(3*C**2-rint**2)
Vext=-4*pi/3*rho*Gconst*C**3/rext

figure()
plot(rint/C,Vint,'b-',label='Interior')
plot(rext/C,Vext,'r-',label='Exterior')
axvline(1.0,color='k')
legend(loc='best')
xlabel('$r/R_p$')
ylabel('$V$ (j/kg)')
savefig("potential-shell.png")

