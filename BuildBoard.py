from Mesh import *

def BuildBoard(throw_distance = 5, hoop_height = 2, hoop_backboard_distance = 0.2
              , board_width = 1, board_height = 0.7, step_size = 0.05):

    # Not finished
    def CalcNextPosOnCenterLane(prev, current):
        current = vec(0,0,0)

    # Not finished
    def CalcLeftSideBottomPos(right, current):
        current = vec(0,0,0)

    # Not finished
    def CalcNextPosOnLeftSide(bottom, right, current):
        current = vec(0,0,0)

    # Not finished
    def CalcNextPosOnRightSide(bottom, left, current):
        current = vec(0,0,0)



    width_vertices_count = int(board_width / step_size) + 1 
    height_vertices_count = int(board_height / step_size) + 1
    
    mesh = Mesh(vec(0,hoop_height,0), width_vertices_count, height_vertices_count)

    # Build the middle line of vertices first
    mid_lane = width_vertices_count // 2

    mesh.Vertices[mid_lane][0] = vec(0, 0, 0)

    for h in range(1, height_vertices_count):
        # Use previous z value as begin value for binary search
        mesh.Vertics[mid_lane][h] = vec(0, step_size * h, mesh.Vertices[mid_lane][h-1].z)
        mesh.Vertices[mid_lane][h] = CalcNextPosOnCenterLane(mesh.Vertices[mid_lane][h-1], mesh.Vertices[mid_lane][h])

    # Build left side
    for lane in range(mid_lane-1, -1, -1):
        # First build the bottom vertex
        mesh.Vertices[lane][0] = CalcLeftSideBottomPos(mesh.Vertices[lane+1][0], mesh.Vertices[lane][0])
        # Then calculate each point above it
        for h in range(1, height_vertices_count):
            mesh.Vertices[lane][h] = CalcNextPosOnLeftSide(mesh.Vertices[lane][h-1], mesh.Vertices[lane+1][h], mesh.Vertices[lane][h])

    # Build right side
    for lane in range(mid_lane+1, width_vertices_count):
        # First build the bottom vertex
        mesh.Vertices[lane][0] = CalcLeftSideBottomPos(mesh.Vertices[lane-1][0], mesh.Vertices[lane][0])
        # Then calculate each point above it
        for h in range(1, height_vertices_count):
            mesh.Vertices[lane][h] = CalcNextPosOnRightSide(mesh.Vertices[lane][h-1], mesh.Vertices[lane-1][h], mesh.Vertices[lane][h])

    return mesh
