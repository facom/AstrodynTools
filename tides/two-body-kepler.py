from util import *

#SYSTEM PROPERTIES
MU=1.0

#TIME
t=linspace(0,2*pi,100)

#ORBIT PROPERTIES
a=1.0
e=0.7
p=a*(1-e**2)
n=(MU/a**3)**0.5

#SERIES
M=n*t

#ECCENTRIC ANOMALY
def Eseries(M,e):
    E=M+(e-1./8*e**3)*sin(M)+0.5*e**2*sin(2*M)+3./8*e**2*sin(2*M)+3./8*e**3*sin(3*M)
    return E

E=Eseries(M,e)

#TRUE ANOMALY
f=2*arctan(((1+e)/(1-e))**0.5*tan(E/2))
r=p/(1+e*cos(f))

#TRAJECTORY
x=r*cos(f)
y=r*sin(f)

figure(figsize=(6,6))
plot(x,y,'b+')
xmin,xmax=xlim()
ymin,ymax=ylim()
ylim((min(xmin,ymin),max(xmax,ymax)))
savefig("two-body-kepler.png")

#SOLVE KEPLER EQUATION
from scipy.optimize import bisect

def keplerEquation(E,M,e):
    fe=E-e*sin(E)-M
    return fe

#COMPARE SERIES
M=np.linspace(0,2*pi)
Ebis=[bisect(keplerEquation,0.0,2*pi,args=(Mv,e)) for Mv in M]
Eser=Eseries(M,e)

figure()
plot(M,Ebis,label='Bisection')
plot(M,Eser,label='Series')
legend(loc='best')
savefig("kepler-equation.png")

