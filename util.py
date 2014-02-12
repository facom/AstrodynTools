#!/usr/bin/env python
#-*-coding:utf-8-*-
from constants import *
from numpy import *
from matplotlib.pyplot import *
from sys import exit

###################################################
#CONSTANTS
###################################################
DEG=pi/180
RAD=180/pi

###################################################
#NUMERIC 
###################################################
#P2 Legendre Polynomial
def P2(psi):
    p=0.5*(3*cos(psi)**2-1)
    return p

###################################################
#PHYSICAL
###################################################
#Deformed Radius
def R2(Rp,eps2,theta):
    R=Rp*(1+eps2*P2(theta))
    return R

#Interior Potential
def Vint(r,theta,R,rho,eps2):
    V=-4*pi/3*R**3*rho*Gconst*((3*R**2-r**2)/(2*R**3)+3./5*(r**2/R**3)*eps2*P2(theta))
    return V

#Exterior Potential
def Vext(r,theta,R,rho,eps2):
    V=-4*pi/3*R**3*rho*Gconst*(1/r+3./5*R**2/r**3*eps2*P2(theta))
    return V

#Equilibrium Tide
def Csi(Ms,Mp,Rp,a):
    csi=(Ms/Mp)*(Rp/a)**3*Rp
    return csi

#Tide potential
def V3(r,theta,Ms,Mp,Rp,a):
    g=Gconst*Mp/Rp**2
    csi=Csi(Ms,Mp,Rp,a)
    V=-csi*g*(r/Rp)**2*P2(theta)
    return V

#Contornos
def contourPotential(V,R,range=(-1,1),levels='none'):
    N=range[2]
    X=linspace(range[0]*R,range[1]*R,N)
    Y=linspace(range[0]*R,range[1]*R,N)
    XM,YM=meshgrid(X,Y)
    VM=zeros((N,N))
    for i in xrange(N):
        x=X[i]
        for j in xrange(N):
            y=Y[j]
            theta=arctan(y/x)
            r=sqrt(x**2+y**2)
            VM[j,i]=V(r,theta)
        if levels!='none':args=dict(levels=levels)
        else:args=dict()
        contourf(XM/R,YM/R,VM,**args)

###################################################
#TEST CODE
###################################################
if __name__=='__main__':
    Ms=Mmoon
    Mp=Mearth
    Rp=Rearth
    rho=rhoearth
    a=rmoon
    eps2=0.2
    
    #TEST RD
    figure(figsize=(6,6))
    theta=linspace(0,2*pi,100)
    R=R2(Rp,eps2,theta)
    x=R*cos(theta)
    y=R*sin(theta)
    plot(x/Rp,y/Rp,'r-')
    xc=Rp*cos(theta)
    yc=Rp*sin(theta)
    plot(xc/Rp,yc/Rp,'b--')
    xlim((-1.5,1.5))
    ylim((-1.5,1.5))
    savefig("test-Rd.png")
    
    #TEST CSI
    csi=Csi(Ms,Mp,Rp,a)
    print "Equilibrium tide: %e"%csi

    #TEST V3
    r=Rp
    theta=linspace(0,pi,100)
    figure()
    plot(theta*RAD,V3(r,theta,Ms,Mp,Rp,a),'k-')
    savefig("test-V3.png")

    #TEST VINT, VEXT
    figure()
    R=Rp
    for theta in 0,30,60,90:
        theta*=DEG
        
        rint=linspace(0,R,100)
        rext=linspace(R,2*R,100)
        
        Vi=Vint(rint,theta,Rp,rho,eps2)
        Ve=Vext(rext,theta,Rp,rho,eps2)
        
        line=plot(rint/Rp,Vi,'-',label="%s"%(theta*RAD))
        color=line[0].get_color()
        plot(rext/Rp,Ve,'-',color=color)
        axvline(1.0,color='k')
        
    legend(loc='best')
    xlabel('$r/R_p$')
    ylabel('$V$ (j/kg)')
    savefig("test-VintVext.png")

