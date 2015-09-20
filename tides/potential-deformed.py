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
eps2=0.2

theta=linspace(0,2*pi)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#SHAPE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#REFERENCE
R=C/C
xr=R*cos(theta)
yr=R*sin(theta)

#DEFORMED
R=C*(1+eps2*P2(theta))/C
xd=R*cos(theta)
yd=R*sin(theta)

figure(figsize=(6,6))
plot(xr,yr,'r-',label='Reference')
plot(xd,yd,'b-',label='Deformed')
legend(loc='best')
xlim((-1.5,1.5))
ylim((-1.5,1.5))
grid()
savefig("shape-deformed.png")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#POTENTIAL REFERENCE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure()

rint=linspace(0,C,100)
rext=linspace(C,2*C,100)

Vinto=-2*pi/3*rho*Gconst*(3*C**2-rint**2)
Vexto=-4*pi/3*rho*Gconst*C**3/rext

plot(rint/C,Vinto,'k-',label='Reference')
plot(rext/C,Vexto,'k-')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#POTENTIAL DEFORMED
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
R=C
for theta in 0,30,60,90:
    theta*=DEG
    
    #R=C*(1+eps2*P2(theta))
    rint=linspace(0,R,100)
    rext=linspace(R,2*R,100)

    Vint=-4*pi/3*C**3*rho*Gconst*((3*C**2-rint**2)/(2*C**3)+3./5*(rint**2/C**3)*eps2*P2(theta))
    Vext=-4*pi/3*C**3*rho*Gconst*(1/rext+3./5*C**2/rext**3*eps2*P2(theta))
    
    line=plot(rint/C,Vint,'-',label=theta*RAD)
    color=line[0].get_color()
    plot(rext/C,Vext,'-',color=color)
    axvline(1.0,color='k')

legend(loc='best')
xlabel('$r/R_p$')
ylabel('$V$ (j/kg)')
savefig("potential-deformed.png")
