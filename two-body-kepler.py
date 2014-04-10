from util import *

mu=1.0
t=linspace(0,2*pi,100)

a=1.0
e=0.3
p=a*(1-e**2)
n=(mu/a**3)**0.5

M=n*t
E=M+(e-1./8*e**3)*sin(M)+0.5*e**2*sin(2*M)+3./8*e**2*sin(2*M)+3./8*e**3*sin(3*M)
f=2*arctan(((1+e)/(1-e))**0.5*tan(E/2))
r=p/(1+e*cos(f))

x=r*cos(f)-a*e
y=r*sin(f)

figure(figsize=(6,6))
plot(x,y)

xmin,xmax=xlim()
ymin,ymax=ylim()
ylim((min(xmin,ymin),max(xmax,ymax)))

savefig("two-body-kepler.png")


