"""
See this interesting tutorial:
http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial

More examples at:
http://matplotlib.org/1.3.1/examples/animation/index.html
"""
from util import *
import numpy as np
import matplotlib.animation as animation
from matplotlib.pyplot import *

#########################################
#INITIALIZE FIGURE
#########################################
fig=figure()
ax=axes(xlim=(0,2*pi),ylim=(-1,1))
line1,=ax.plot([],[])
line2,=ax.plot([],[])

#########################################
#INITIALIZATION FUNCTION
#########################################
def init():
    line1.set_data([],[])
    line2.set_data([],[])
    return line1,line2

#########################################
#ANIMATION FUNCTION
#########################################
x=linspace(0,2*pi,100)
def animate(iframe):
    y1=sin(x+0.1*iframe)
    y2=cos(x+0.1*iframe)
    line1.set_data(x,y1)
    line2.set_data(x,y2)
    return line1,line2

#########################################
#PLOT
#########################################
anim=animation.FuncAnimation(fig,animate,init_func=init,frames=100,interval=100,blit=True)

#########################################
#SAVE IMAGE
#########################################
anim.save("animation.mp4",fps=20)
