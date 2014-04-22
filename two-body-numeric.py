from util import *
from scipy.integrate import odeint

#SYSTEM PROPERTIES
m1=1.0
m2=0.5
M=m1+m2
MU=1.0

#EOS
def twob(y,t,params):
    mu=params['mu']
    dydt=[0.0,0.0,0.0,0.0]
    dydt[0]=y[2]
    dydt[1]=y[3]
    r2=y[0]**2+y[1]**2
    dydt[2]=-mu/r2**1.5*y[0]
    dydt[3]=-mu/r2**1.5*y[1]
    return dydt
    
#NUMERIC SOLUTION
y=[1.0,0.0,0.0,1.2]
t=linspace(0,20.0,100)
params=dict(mu=MU)
solution=odeint(twob,y,t,args=(params,))

#PLOTTING SOLUTION FOR RELATIVE SYSTEM AND INDEPENDENT BODIES
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


#DERIVED QUANTITIES FOR THE SYSTEM
rdot=solution[:,2:]

hmag=[]
eps=[]
for i in xrange(len(t)):
    rp=vec2to3(r[i,:])
    rd=vec2to3(rdot[i,:])
    rmag=dot(rp,rp)**0.5
    
    #SPECIFIC ANGULAR MOMENTUM
    h=cross(rp,rd)
    hmag+=[dot(h,h)**0.5]

    #SPECIFIC ENERGY
    eps+=[0.5*dot(rd,rd)-1.0/rmag]

    #LAPLACE-RUNGE-LENZ
    E=-(cross(h,rd)+1.0*rp/rmag/MU)

#ENERGY AND ANGULAR MOMENTA CONSERVATION
figure()
plot(t,hmag)
savefig("h-t.png")

figure()
plot(t,eps)
savefig("eps-t.png")

#CONSTANTS
h=array(hmag).mean()
epsilon=array(eps).mean()

#PROPERTIES OF THE ORBIT
e=magvec(E)
p=h**2/MU
a=p/(1-e**2)

print "Angular momentum: %e"%h
print "Energy: %e"%epsilon
print "Eccentricity: %e"%e
print "Semi latus rectum: %e"%p
print "Semi major axis: %e"%a

#COMPARE NUMERIC WITH GEOMETRICAL SOLUTION
f=linspace(0,2*pi,100)
r=p/(1+e*cos(f))
x=r*cos(f)
y=r*sin(f)

figure()
plot(solution[:,0],solution[:,1],label='Numeric')
plot(x,y,label='Geometric')
legend(loc='best')
savefig("two-body-numeric-geometric.png")

#VIS-VIVA
r=(solution[:,0]**2+solution[:,1]**2)**0.5
v2=(solution[:,2]**2+solution[:,3]**2)
v2visviva=MU*(2/r-1/a)
figure()
plot(t,v2,label='Numeric')
plot(t,v2visviva,label='Vis-viva')
legend(loc='best')
savefig("two-body-visviva.png")
