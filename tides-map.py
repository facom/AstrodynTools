#!/usr/bin/env python
#-*-coding:utf-8-*-
from constants import *
from numpy import *
from matplotlib.pyplot import *
from mpl_toolkits.basemap import Basemap as map,shiftgrid as grid
from sys import exit

close("all")

###################################################
#UTILITIES
###################################################
DEG=pi/180
RAD=180/pi
def P2(psi):
    p=0.5*(3*cos(psi)**2-1)
    return p

###################################################
#SCRIPT
###################################################
#"""
mp=Mearth
Rp=Rearth
a=rmoon
ms=Mmoon
#"""

"""SUN-EARTH
mp=Mearth
Rp=Rearth
a=rsun
ms=Msun
#"""

#EQUILIBRIUM
csi=ms/mp*(Rp/a)**3*Rp
g=Gconst*mp/Rp**2

def tide(tp,fp,tm,fm):
    phase=\
        0.5*(3*cos(tp)**2-1)*0.5*(3*cos(tm)**2-1)+\
        0.75*sin(tp)**2*sin(tm)**2*cos(2*(fp-fm))+\
        0.75*sin(2*tp)*sin(2*tm)*cos(fp-fm)
    print "\ttp=",tp,"phase=",phase
    heq=csi*phase
    return heq

#CREATE MAP
m=map(projection="robin",lon_0=0)
m.drawmapboundary()
parallels=arange(-75.0,90.0,15.)
meridians=arange(-360.0,360.0,60.0)
parallels=m.drawparallels(parallels,labels=[1,1,0,0],labelstyle="+/-",fontsize=8)
meridians=m.drawmeridians(meridians,labels=[0,0,1,1],labelstyle="+/-",fontsize=8)
m.drawcountries(linewidth=0.25)
m.drawcoastlines(linewidth=0.25)
m.fillcontinents()

#CREATE GRID
nlons=5
lons=linspace(0.0,360.0,nlons)
nlats=5
lats=linspace(-60.0,60.0,nlats)

#CALCULATE TIDES
H=zeros((nlats,nlons))
for i in xrange(nlats):
    for j in xrange(nlons):
        tp=(90.0-lats[i])*DEG
        fp=lons[j]*DEG
        print "Calculating at: lat = %e, theta = %e"%(lats[j],tp)
        H[i,j]=tide(tp,fp,90.0*DEG,90.0*DEG)
        print "\tTide: %e"%H[i,j]
    #exit(0)

H,lons=grid(180.0,H,lons,start=False)
LONS,LATS=meshgrid(lons,lats)
xlons,xlats=m(LONS,LATS)
c=m.contour(xlons,xlats,H,10,linewidths=0.5)
#c=m.contourf(xlons,xlats,H,c.levels)

#BAR
cax=axes([0.05,0.1,0.9,0.1])
cbar=colorbar(c,drawedges=False,cax=cax,orientation='horizontal',
              format='%+.1e')
cbar.ax.tick_params(labelsize=8) 

#SAVE FIGURE
savefig("tides-map.png")
