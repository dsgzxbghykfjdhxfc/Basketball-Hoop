from BuildBoard import *
from vpython import *

throw_distance = 5
hoop_height = 2
hoop_backboard_distance = 0.2

mesh = BuildBoard()
mesh.Build()

ball = sphere(pos = vec(0,0,0))

while 1:
    rate(60)