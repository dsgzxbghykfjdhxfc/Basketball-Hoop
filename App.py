from BuildBoard import *
from vpython import *


scene = canvas(title='', width=1500, height=700, x=0, y=0, center=vec(0,0,0), background=vec(0.1, 0.1, 0.1))

mesh = BuildBoard(throw_distance = 5, hoop_height = 3, hoop_backboard_distance = 0.3, throw_height = 2
                 , board_width = 1, board_height = 0.7, step_size = 0.05)
mesh.Build()

while 1:
    rate(100)
