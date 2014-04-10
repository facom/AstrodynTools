from util import *
from scipy.integrate import odeint

#
def twob(y,t,params):
    mu=params['mu']
    dydt=[0.0,0.0,0.0,0.0]
    dydt[0]=y[2]
    dydt[1]=y[3]
    r2=y[0]**2+y[1]**2
    dydt[2]=-mu/r2**1.5*y[0]
    dydt[3]=-mu/r2**1.5*y[1]
    return dydt
    
y=[1.0,0.0,0.0,1.2]
t=linspace(0,2*pi,100)
params=dict(mu=1.0)
solution=odeint(twob,y,t,args=(params,))

figure(figsize=(6,6))
plot(solution[:,0],solution[:,1])

xmin,xmax=xlim()
ymin,ymax=ylim()
ylim((min(xmin,ymin),max(xmax,ymax)))

savefig("two-body-numeric.png")
