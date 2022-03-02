from BuildBoard import *
from vpython import *

throw_distance = 5
hoop_height = 2
hoop_backboard_distance = 0.2

def make_axes(length):
    xaxis = arrow(pos=vector(0,0,0),axis=length*vector(1,0,0),color=color.red)
    neg_xaxis = xaxis.clone()
    neg_xaxis.axis *= -1
    yaxis = arrow(pos=vector(0,0,0),axis=length*vector(0,1,0),color=color.green)
    neg_yaxis = yaxis.clone()
    neg_yaxis.axis *= -1
    zaxis = arrow(pos=vector(0,0,0),axis=length*vector(0,0,1),color=color.blue)
    neg_zaxis = zaxis.clone()
    neg_zaxis.axis *= -1
    fudge = 0.02*length
    label(text="x",color=xaxis.color,pos=xaxis.pos+xaxis.axis+vector(0,fudge,0),box=False)
    label(text="y",color=yaxis.color,pos=yaxis.pos+yaxis.axis+vector(fudge,0,0),box=False)
    label(text="z",color=zaxis.color,pos=zaxis.pos+zaxis.axis+vector(fudge,0,0),box=False)


scene = canvas(title='', width=1500, height=700, x=0, y=0, center=vec(0,0,0), background=vec(0.1, 0.1, 0.1))

mesh = BuildBoard()
mesh.Build()


#make_axes(10)


while 1:
    rate(100)
