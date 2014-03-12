from util import *
from scipy.integrate import odeint
close("all")

#FORCING
def forcing(t,params):
    Fom=params['Fom']
    w=params['w']
    f=Fom*cos(w*t)
    return f

#EQUATION OF MOTION
def eom(y,t,params):
    wo=params['wo']
    w=params['w']
    itau=params['itau']
    Fom=params['Fom']
 
    dydt=[0,0]
    dydt[0]=y[1]
    dydt[1]=-wo**2*y[0]-itau*y[1]+forcing(t,params)
    return dydt

#INITIAL CONDITIONS    
y=[0,1]

#TIMES
t=linspace(0,6*pi,1000)

#REFERENCE SOLUTION: NO FORCING
params=dict(wo=1.5,w=1.0,itau=0.0,Fom=0.0)
sol_ref=odeint(eom,y,t,args=(params,))

#FORCED SOLUTION
params=dict(wo=1.5,w=1.0,itau=1.0,Fom=1.0)
sol=odeint(eom,y,t,args=(params,))

figure()

plot(t,sol_ref[:,0],'k--',label='Reference')
plot(t,sol[:,0],'k-',label='Solution')
plot(t,forcing(t,params),'b-',label='Forcing')

grid()
legend(loc='best')
savefig("forced-oscillation.png")

#THEORETICAL
factor=((params['wo']**2-params['w']**2)**2+(params['w']*params['itau'])**2)**0.5

A=params['Fom']/factor
print "Amplitude:",A

print (params['w']*params['itau'])
delta=arcsin(-(params['w']*params['itau'])/factor)
print "Phase shift:",delta


