from util import *

Omega=2*pi/(1*Day)
a=Reqearth
mp=Mearth

#PLOT DEFORMATION
def Deformation(theta):
    dr=Omega**2*Rearth**4/(2*Gconst*mp)*(sin(theta)**2-1)
    return dr

figure()
t=linspace(0,pi,100)
dr=Deformation(t)
plot(t,dr,'k-')
savefig("rotational-deformation.png")

#THEORETICAL FLATNESS
q=Omega**2*a**3/(Gconst*mp)
f=q/2
print "Predicted flatness: ",f
print "Real flatness: ",fearth

#MAXIMUM ROTATION
Omegamax=(Gconst*mp/a**3)**0.5
Pmin=2*pi/Omegamax
print "Omega max: ",Omegamax
print "Period min: ",Pmin/3600
