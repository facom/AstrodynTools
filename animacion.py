from numpy import *
import matplotlib.animation as animation
from matplotlib.pyplot import *

#PROPIEDADES
r=1

#ESCENARIO
fig=figure(figsize=(8,8))
q=linspace(0,2*pi,100)
x=r*cos(q)
y=r*sin(q)
plot(x,y)

#COMPONENTE DINAMICA
#El punto
punto,=plot([1],[0],'ro',ms=10)

#RUTINA DE ANIMACION
def animacion(iframe):
    q=iframe*(10*pi/180) #Avanza a 10 grados por frame
    x=r*cos(q)
    y=r*sin(q)
    punto.set_data(x,y)
    return punto

#HACER LA ANIMACION
anim=animation.FuncAnimation(fig,animacion)
anim.save("movimiento-circular.mp4")

#MUESTRE ESCENARIO
savefig("escenario.png")
