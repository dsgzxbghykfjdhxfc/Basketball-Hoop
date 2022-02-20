from vpython import *

class Mesh:
    Pos = vec(0,0,0)

    def __init__(self, pos):
        self.Pos = pos

    def AddVertex(self, vertexPos):
        self.vertices.append(vertexPos)

    def Build(self):
        vec(0,0,0)
        pass

