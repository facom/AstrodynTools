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

#DEFORMING PRESSURE DUE TO POTENTIAL
def Pdef(psi):
    Z=(gc/A)*(csic/A+3./5*sigma/rho*(T2-S2)+3.*S2/5)
    P=rho*Z*A**2*P2(psi)
    return P

figure()
psi=linspace(0,pi,100);
plot(psi*RAD,Pdef(psi),'b-')
savefig("deforming-pressure.png")

#HYDROSTATIC LOAD DUE TO OCEAN TIDES
def Poc(psi):
    P=sigma*A*gc*(csic/A+3./5*sigma/rho*(T2-S2)-2.*S2/5)*P2(psi)
    return P

figure()
psi=linspace(0,pi,100);
plot(psi*RAD,Poc(psi),'b-')
savefig("ocean-tide-load.png")

#HYDROSTATIC LOAD DUE TO CORE TIDES
def Pc(psi):
    P=rho*gc*A*S2*P2(psi)
    return P

figure()
psi=linspace(0,pi,100);
plot(psi*RAD,Pc(psi),'b-')
savefig("core-tide-load.png")

figure()
plot(psi*RAD,Pdef(psi),'b-',label="Deforming")
plot(psi*RAD,Poc(psi),'r-',label="Ocean Tide")
plot(psi*RAD,Pc(psi),'g-',label="Core Tide")
legend()
savefig("all-pressures.png")

figure()
plot(psi*RAD,Pdef(psi),'b-',label="Deforming")
plot(psi*RAD,Poc(psi),'r-',label="Ocean Tide")
plot(psi*RAD,Pc(psi),'g-',label="Core Tide")
plot(psi*RAD,Pdef(psi)-Poc(psi)-Pc(psi),'k-',label="Total",linewidth=2)
legend()
savefig("total-pressure.png")

