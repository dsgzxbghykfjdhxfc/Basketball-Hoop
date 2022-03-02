from BuildBoard import *
from vpython import *

throw_distance = 5
hoop_height = 2
hoop_backboard_distance = 0.2

def make_axes(length):
    global axes
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
    xlabel = label(text="x",color=xaxis.color,pos=xaxis.pos+xaxis.axis+vector(0,fudge,0),box=False)
    ylabel = label(text="y",color=yaxis.color,pos=yaxis.pos+yaxis.axis+vector(fudge,0,0),box=False)
    zlabel = label(text="z",color=zaxis.color,pos=zaxis.pos+zaxis.axis+vector(fudge,0,0),box=False)
    axes = [xaxis,neg_xaxis,yaxis,neg_yaxis,zaxis,neg_zaxis,xlabel,ylabel,zlabel]
    for shape in axes:
        shape.visible = True


scene = canvas(title="斜拋模擬", width=800, height=400, x=0, y=0,
                center=vec(0,0,0), background=vec(0.1, 0.1, 0.1))

mesh = BuildBoard()
mesh.Build()

"""
G, theta, disX, disY, disZ = 9.81, 45, 0, 3, 10
ball = sphere(pos = vec(0,0,disZ))
target = sphere(pos = vec(disX, disY, 0), radius = 1)
target.color = vec(1, 0, 0)
#tan_theta = tan(radians(theta))
disXZ = sqrt(disX * disX + disZ * disZ)
#speed = sqrt(G * (disX * disX + disZ * disZ) * (1 + tan_theta * tan_theta) * 0.5 / (disXZ * tan_theta - disY))
speed = 15
smthing = sqrt(speed ** 4 - 2 * G * disY * speed ** 2 - G ** 2 * disXZ ** 2)
tan_theta = (speed ** 2 - smthing) / G / disXZ
theta = atan(tan_theta)
ball.velocity = vec(speed * cos(theta) * disX / disXZ,
                    speed * sin(theta),
                    -speed * cos(theta) * disZ / disXZ)

print(degrees(theta), ball.velocity)
"""

scene.camera.pos = vec(0,0,0)
scene.camera.axis = vec(0,0,-100)

#make_axes(10)

dt = 0.004
sleep(1)
while 1:
    rate(100)
