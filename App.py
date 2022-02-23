from BuildBoard import *
from vpython import *

throw_distance = 5
hoop_height = 2
hoop_backboard_distance = 0.2

#mesh = BuildBoard()
#mesh.Build()
scene = canvas(title="斜拋模擬", width=800, height=400, x=0, y=0,
                center=vec(0,0,0), background=vec(0, 0.6, 0.6))
ball = sphere(pos = vec(0,0,0))

while 1:
    rate(60)