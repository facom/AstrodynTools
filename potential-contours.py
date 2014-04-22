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
C=Rearth
rho=rhoearth
eps2=0.2*0

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#GRID
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Nx=100
X=linspace(-1.2*C,1.2*C,100)
Ny=100
Y=linspace(-1.2*C,1.2*C,100)
XM,YM=meshgrid(X,Y)

VM=zeros((Nx,Ny))
for i in xrange(Nx):
    x=X[i]
    for j in xrange(Ny):
        y=Y[j]
        theta=arctan(y/x)
        r=sqrt(x**2+y**2)
        if r<C:
            V=-4*pi/3*C**3*rho*Gconst*((3*C**2-r**2)/(2*C**3)+3./5*(r**2/C**3)*eps2*P2(theta))
        else:
            V=-4*pi/3*C**3*rho*Gconst*(1/r+3./5*C**2/r**3*eps2*P2(theta))
        VM[j,i]=V


close("all")
figure(figsize=(8,8))
contour(XM/C,YM/C,VM)
savefig("potential-contour.png")
