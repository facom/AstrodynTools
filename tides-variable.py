#!/usr/bin/env python
#-*-coding:utf-8-*-
from constants import *
from numpy import *
from matplotlib.pyplot import *
from sys import exit

###################################################
#UTILITIES
###################################################
DEG=pi/180
RAD=180/pi
def P2(psi):
    p=0.5*(3*cos(psi)**2-1)
    return p

###################################################
#SCRIPT
###################################################
#"""
mp=Mearth
Rp=Rearth
a=rmoon
ms=Mmoon
#"""

"""SUN-EARTH
mp=Mearth
Rp=Rearth
a=rsun
ms=Msun
#"""

#EQUILIBRIUM
csi=ms/mp*(Rp/a)**3*Rp
g=Gconst*mp/Rp**2

#FREQUENCIES
Omega=2*pi/Day
n=2*pi/(Month*Day)

#MOON ORBIT INCLINATION 
i=5*DEG

#CALCULATE ANGLES AS A FUNCTION OF TIME
t=linspace(0,Month*Day,1000)
fp=Omega*t
tp=90.0*DEG

#COLATITUDE (SPHERICAL TRIGONOMETRY)
fm=n*t
B=1/sin(i)**2
A=cos(fm)**2
tm=arcsin(sqrt((B-1)/(B-A)))

#ARTIFICIAL ENHACEMENT FACTORS
A=1.0E0
B=1.0E0
C=1.0E17

#"""
phase=\
A*0.50*(3*cos(tp)**2-1)*0.5*(3*cos(tm)**2-1)+\
B*0.75*sin(tp)**2*sin(tm)**2*cos(2*(fp-fm))+\
C*0.75*sin(2*tp)*sin(2*tm)*cos(fp-fm)
#"""

#TIDE
heq=csi*phase

figure()
plot(t/Day,heq)
xlabel("$t$ (Day)")
ylabel("Tide (m)")
savefig("tides-oscillation.png")
