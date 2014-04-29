from util import *
import numpy as np
import matplotlib.animation as animation
from matplotlib.pyplot import *
from matplotlib.patches import *
from os import system

#########################################
#CLEAN
#########################################
system("rm -rf _tmp*.png")

#########################################
#PROPERTIES
#########################################
#PHYSICAL
mu=1.0

#ORBIT GEOMETRIC
a=1.0
e=0.5
b=a*sqrt(1-e**2)

#ORBIT DYNAMICAL
n=sqrt(mu/a**3)
P=2*pi/n

#TOTAL SIMULATION TIME
T=1*P

#SIMULATION PROPERTIES
nframes=50
nanim=T/nframes
dtframe=20
fps=10

#########################################
#ROUTINES
#########################################
def Eseries(M,e):
    E=M+(e-1./8*e**3)*sin(M)+0.5*e**2*sin(2*M)+3./8*e**2*sin(2*M)+3./8*e**3*sin(3*M)
    return E

#########################################
#INITIALIZE FIGURE
#########################################
fig=figure(figsize=(6,6))
ax=fig.add_axes([0,0,1,1],xlim=(-2,2),ylim=(-2,2))
ax.set_xticks([])
ax.set_yticks([])

#########################################
#SCENARIO
#########################################
f=linspace(0,2*pi,100)
r=a*(1-e**2)/(1+e*cos(f))
x=r*cos(f)
y=r*sin(f)
ax.plot(x,y)
ax.axhline(0,linestyle='--',color='k')
ax.axvline(0,linestyle='--',color='k')
mean=Circle((0,0),a,facecolor='none',edgecolor='r',linestyle='dashed')
cinscribed=Circle((-a*e,0),a,facecolor='none',edgecolor='b',linestyle='dashed')
ax.add_patch(inscribed)
ax.add_patch(cinscribed)

#########################################
#MOVING PLANET
#########################################
particle_real,=ax.plot([],[],'ro',ms=6,label='Real')
particle_eccentric,=ax.plot([],[],'bo',ms=6,label='Eccentric')
particle_mean,=ax.plot([],[],'go',ms=6,label='Mean')
ax.legend(loc='upper right')

#########################################
#INIT
#########################################
def init():
    particle_real.set_data([],[])
    particle_eccentric.set_data([],[])
    particle_mean.set_data([],[])
    return particle_real,particle_eccentric,particle_mean

#########################################
#ANIMATE FUNCTION
#########################################
def animate(iframe):
    t=nanim*iframe
    M=n*t

    E=Eseries(M,e)

    x=a*(cos(E)-e)
    y=b*sin(E)
    particle_real.set_data(x,y)

    x=a*(cos(E)-e)
    y=a*sin(E)
    particle_eccentric.set_data(x,y)

    x=a*cos(M)
    y=b*sin(M)
    particle_mean.set_data(x,y)

    return particle_real,particle_eccentric,particle_mean

#########################################
#ANIMATION
#########################################
#"""
anim=animation.FuncAnimation(fig,animate,init_func=init,frames=nframes,interval=dtframe,blit=True)
anim.save("orbit.mp4",fps=fps)
#"""

#########################################
#SAVE FIGURE
#########################################
savefig("scenario.png")
