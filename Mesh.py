from vpython import *

class Mesh:

    def __init__(self, pos : vec, width_cnt : int, height_cnt : int):
        self.Pos = pos
        self.Vertices = [[vec(0,0,0) for i in range(height_cnt)] for j in range(width_cnt)]

    def Build(self):
        for x in range(len(self.Vertices) - 1):
            for y in range(len(self.Vertices[0]) - 1):
                triangle(v0 = vertex(pos = self.Pos + self.Vertices[x][y])
                        ,v1 = vertex(pos = self.Pos + self.Vertices[x+1][y])
                        ,v2 = vertex(pos = self.Pos + self.Vertices[x][y+1]))
                triangle(v0 = vertex(pos = self.Pos + self.Vertices[x+1][y])
                        ,v1 = vertex(pos = self.Pos + self.Vertices[x][y+1])
                        ,v2 = vertex(pos = self.Pos + self.Vertices[x+1][y+1]))

