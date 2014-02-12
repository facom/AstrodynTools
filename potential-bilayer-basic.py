from util import *

#PROPERTIES
Rp=Rearth
Mp=Mearth
Ms=Mmoon
a=rmoon

#OCEAN
B=Rearth
T2=0.2
sigma=1E3

#CORE
A=0.5*Rearth
S2=0.3
rho=5E3

#SHAPE
figure(figsize=(6,6))

theta=linspace(0,2*pi)

R=R2(B,T2,theta)
plot(R*cos(theta)/Rp,R*sin(theta)/Rp,'r-')
plot(B*cos(theta)/Rp,B*sin(theta)/Rp,'b--')

R=R2(A,S2,theta)
plot(R*cos(theta)/Rp,R*sin(theta)/Rp,'r-')
plot(A*cos(theta)/Rp,A*sin(theta)/Rp,'b--')

xlim((-1.5,1.5))
ylim((-1.5,1.5))
savefig("bilayer-shape.png")

#OCEAN POTENTIAL
figure()

def Vo(r,theta):
    Vtid=V3(r,theta,Ms,Mp,B,a)
    Vinto=Vint(r,theta,B,rho,T2)
    Vextc=Vext(r,theta,A,rho-sigma,S2)
    V=Vtid+Vinto+Vextc
    return V

r=linspace(A,B,100)
for theta in [0,45,90]:
    V=Vo(r,theta*DEG)
    plot(r/Rp,V,'-',label="%s"%(theta))

legend()
savefig("ocean-potential.png")

#OCEAN POTENTIAL CONTOURS
figure()
range=(-1.2,1.2,100)
contourPotential(Vo,B,range=range,levels=linspace(Vo(A,0),Vo(B,0),10))
xlim((range[0],range[1]))
ylim((range[0],range[1]))
savefig("ocean-potential-contours.png")

#CORE POTENTIAL
figure()

def Vc(r,theta):
    Vtid=V3(r,theta,Ms,Mp,A,a)
    Vinto=Vint(r,theta,B,rho,T2)
    Vintc=Vint(r,theta,A,rho-sigma,S2)
    V=Vtid+Vinto+Vintc
    return V

r=linspace(0,A,100)
for theta in [0,45,90]:
    V=Vc(r,theta*DEG)
    plot(r/Rp,V,'-',label="%s"%(theta))

legend()
savefig("core-potential.png")

#OCEAN POTENTIAL CONTOURS
figure()
range=(-1.2,1.2,100)
contourPotential(Vc,B,range=range,levels=linspace(Vc(0,0),Vc(A,0),10))
xlim((range[0],range[1]))
ylim((range[0],range[1]))
savefig("core-potential-contours.png")

#FULL POTENTIAL
figure()
rc=linspace(0,A,100)
ro=linspace(A,B,100)
for theta in [0,45,90]:
    Vcore=Vc(rc,theta*DEG)
    Vocean=Vo(ro,theta*DEG)
    line=plot(rc/Rp,Vcore,'-',label="%s"%(theta))
    plot(ro/Rp,Vocean,'-',color=line[0].get_color())

legend()
savefig("full-potential.png")
