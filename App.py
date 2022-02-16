
throw_distance = 5
hoop_height = 2
hoop_backboard_distance = 0.2

class Vec3:    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def Set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# Not finished
def CalcNextPosOnCenterLane(prev, current):
    current.Set(0,0,0)

# Not finished
def CalcLeftSideBottomPos(right, current):
    current.Set(0,0,0)

# Not finished
def CalcNextPosOnLeftSide(bottom, right, current):
    current.Set(0,0,0)

# Not finished
def CalcNextPosOnRightSide(bottom, left, current):
    current.Set(0,0,0)



def BuildBackboard(board_width, board_height, step_size):
    width_vertices_count = int(board_width / step_size) + 1 
    height_vertices_count = int(board_height / step_size) + 1

    # Vertices coordinates        size = [width_point_count][height_point_count]
    vertices = [[Vec3(0,0,0) for x in range(height_vertices_count)] for y in range(width_vertices_count)]

    # Build the middle line of vertices first
    mid_lane = width_vertices_count // 2
    vertices[mid_lane][0] = Vec3(0, hoop_height, 0)

    for h in range(1, height_vertices_count):
        # Use previous z value as begin value for binary search
        vertices[mid_lane][h] = Vec3(0, hoop_height + step_size * h, vertices[mid_lane][h-1].y)
        CalcNextPosOnCenterLane(vertices[mid_lane][h-1], vertices[mid_lane][h])

    
    # Build left side
    for lane in range(mid_lane-1, -1, -1):
        # First build the bottom vertex
        CalcLeftSideBottomPos(vertices[lane+1][0], vertices[lane][0])
        # Then calculate each point above it
        for h in range(1, height_vertices_count):
            CalcNextPosOnLeftSide(vertices[lane][h-1], vertices[lane+1][h], vertices[lane][h])


    # Build right side
    for lane in range(mid_lane+1, width_vertices_count):
        # First build the bottom vertex
        CalcLeftSideBottomPos(vertices[lane-1][0], vertices[lane][0])
        # Then calculate each point above it
        for h in range(1, height_vertices_count):
            CalcNextPosOnRightSide(vertices[lane][h-1], vertices[lane-1][h], vertices[lane][h])







BuildBackboard(1.4, 0.6, 0.1)