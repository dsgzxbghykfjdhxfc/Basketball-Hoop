from vpython import *

class Mesh:

    def __init__(self, pos : vec, width_cnt : int, height_cnt : int):
        self.Pos = pos
        self.Vertices = [[vec(0,0,0) for i in range(height_cnt)] for j in range(width_cnt)]

    def Build(self):
        for row in self.Vertices:
            curve(pos = row)
        for column in range(len(self.Vertices[0])):
            curve(pos = [row[column] for row in self.Vertices])

                

