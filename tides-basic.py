#!/usr/bin/env python
#-*-coding:utf-8-*-
from constants import *
from numpy import *
from matplotlib.pyplot import *

###################################################
#UTILITIES
###################################################
def P2(psi):
    p=0.5*(3*cos(psi)**2-1)
    return p

###################################################
#SCRIPT
###################################################
#"""MOON-EARTH
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

csi=ms/mp*(Rp/a)**3*Rp
g=Gconst*mp/Rp**2

psi=linspace(0,pi,100)
heq=csi*P2(psi)
V3=-g*heq

figure()
plot(psi*180/pi,V3,label="V3")
title("Tidal Potential")
xlabel("$\Psi$")
ylabel("$V$")
legend()
grid()
savefig("tidal-potential.png")

figure()
plot(psi*180/pi,heq,label="$h_{eq}$")
title("Equilibrium Tide")
xlabel("$\Psi$")
ylabel("$h$")
legend()
grid()
savefig("equilibrium-tide.png")

figure()
psi=linspace(0,2*pi,100)
Rg=Rp/10000000
xt=(Rg+csi*P2(psi))*cos(psi)
yt=(Rg+csi*P2(psi))*sin(psi)
plot(xt,yt,label='Tide')
plot(Rg*cos(psi),Rg*sin(psi),label='Equilibrium')
legend()
savefig("tide-figure.png")

###################################################
#CHALLENGES
###################################################
"""
*) Calculate the amplitude of the tides by the Sun on Earth

*) Calculate the amplitude of the tides by the Sun on Mercury

*) Calculate the amplitude of the tides by Jupiter on Europa

*) Plot equilibrium tides by the Sun

*) Plot maximum amplitude for different pair of bodies in the Solar
   System
"""
