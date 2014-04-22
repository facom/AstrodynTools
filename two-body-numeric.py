from util import *
from scipy.integrate import odeint

#PROP
m1=1.0
m2=0.5
M=m1+m2

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
t=linspace(0,20.0,100)
params=dict(mu=1.0)
solution=odeint(twob,y,t,args=(params,))

figure(figsize=(6,6))

plot(solution[:,0],solution[:,1])

#BODIES
r=solution[:,:2]
r1=-m2/M*r
r2=m1/M*r
plot(r1[:,0],r1[:,1],label='Body 1')
plot(r2[:,0],r2[:,1],label='Body 2')

grid()
legend()
xmin,xmax=xlim()
ymin,ymax=ylim()
ylim((min(xmin,ymin),max(xmax,ymax)))

savefig("two-body-numeric.png")


#DERIVED QUANTITIES
rdot=solution[:,2:]

hmag=[]
eps=[]
for i in xrange(len(t)):
    rp=concatenate((r[i,:],[0]))
    rd=concatenate((rdot[i,:],[0]))
    rmag=dot(rp,rp)**0.5
    
    #SPECIFIC ANGULAR MOMENTUM
    h=cross(rp,rd)
    hmag+=[dot(h,h)**0.5]

    #SPECIFIC ENERGY
    eps+=[0.5*dot(rd,rd)-1.0/rmag]

    #LAPLACE-RUNGE-LENZ
    E=cross(h,rd)+1.0*rp/rmag
    print E

figure()
plot(t,hmag)
savefig("h-t.png")

figure()
plot(t,eps)
savefig("eps-t.png")
