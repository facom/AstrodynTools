#!/usr/bin/env python
#-*-coding:utf-8-*-
from constants import *
from numpy import *
from matplotlib.pyplot import *

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

#POINT
tp=90.0*DEG
fp=0.0*DEG

#MOON 
tm=90.0*DEG
fm=90.0*DEG

#PHASE
phase=\
0.5*(3*cos(tp)**2-1)*0.5*(3*cos(tm)**2-1)+\
0.75*sin(tp)**2*sin(tm)**2*cos(2*(fp-fm))+\
0.75*sin(2*tp)*sin(2*tm)*cos(tp-tm)

#TIDE
heq=csi*phase
print heq

