from Mesh import *

def BuildBoard(throw_distance = 5, hoop_height = 2, hoop_backboard_distance = 0.2
              , board_width = 1, board_height = 0.7, step_size = 0.05):

    hoopPos = vec(0,hoop_height,hoop_backboard_distance)
    throwPos = vec(0,0,throw_distance)

    G = 9.81

    def CalcNormal(contactPos : vec):

        average_normal = vec(0,0,0)
        # Theta for elevation angle
        for angle in range(30, 60, 1):
            theta = radians(angle)
            # Throwing Part
            throw_dis = contactPos - throwPos
            tan_theta = tan(theta)
            disXZ = sqrt(throw_dis.x ** 2 + throw_dis.z ** 2)
            inital_speed = sqrt(G * disXZ * disXZ * (1 + tan_theta * tan_theta) * 0.5 / (disXZ * tan_theta - throw_dis.y))
            impact_velocity = vec(  inital_speed * cos(theta) * throw_dis.x / disXZ,
                                    inital_speed * sin(theta) - G  / (inital_speed * cos(theta) / disXZ), 
                                    inital_speed * cos(theta) * throw_dis.z / disXZ )

            # Bouncing Part
            bounce_dis = hoopPos - contactPos
            bounce_speed = inital_speed * 0.9 # Bounding Constant
            disXZ = sqrt(bounce_dis.x ** 2 + bounce_dis.z ** 2)
            sqrtEqu = bounce_speed ** 4 - 2 * G * bounce_dis.y * bounce_speed ** 2 - G ** 2 * disXZ ** 2
            if sqrtEqu < 0: # Impossible to bounce in
                continue
            tan_theta = (bounce_speed ** 2 - sqrt(sqrtEqu)) / G / disXZ
            bounce_theta = atan(tan_theta)
            bounce_velocity = vec( bounce_speed * cos(theta) * bounce_dis.x / disXZ,
                                   bounce_speed * sin(theta),
                                   bounce_speed * cos(theta) * bounce_dis.z / disXZ)


            normal = -impact_velocity.norm() + bounce_velocity.norm()
            normal = normal.norm()

            average_normal += normal

        return average_normal.norm()



    def CalcNextPosOnCenterLane(down):
        normal = CalcNormal(down)
        up_dir = normal.cross(vec(1,0,0))
        return down + up_dir * step_size / abs(up_dir.y)


    def CalcLeftSideBottomPos(right):
        normal = CalcNormal(right)
        left_dir = normal.cross(vec(0,1,0))
        return right + left_dir * step_size / abs(left_dir.x)


    def CalcRightSideBottomPos(left):
        normal = CalcNormal(left)
        right_dir = -normal.cross(vec(0,1,0))
        return left + right_dir * step_size / abs(right_dir.x)


    # Not finished
    def CalcNextPosOnLeftSide(bottom, right):
        avgPos = (bottom + right) * 0.5
        normal = CalcNormal(avgPos)
        # ax + by + cz = d
        d = avgPos.x * normal.x + avgPos.y * normal.y + avgPos.z * normal.z
        x, y = bottom.x, right.y
        z = (d - normal.x * x - normal.y * y) / normal.z if normal.z != 0 else 0
        return vec(x, y, z)
    
    # Not finished
    def CalcNextPosOnRightSide(bottom, left):
        avgPos = (bottom + left) * 0.5
        normal = CalcNormal(avgPos)
        # ax + by + cz = d
        d = avgPos.x * normal.x + avgPos.y * normal.y + avgPos.z * normal.z
        x, y = bottom.x, left.y
        z = (d - normal.x * x - normal.y * y) / normal.z if normal.z != 0 else 0
        return vec(x, y, z)



    width_vertices_count = int(board_width / step_size) + 1 
    height_vertices_count = int(board_height / step_size) + 1
    
    mesh = Mesh(vec(0,hoop_height,0), width_vertices_count, height_vertices_count)

    # Build the middle line of vertices first
    mid_lane = width_vertices_count // 2

    mesh.Vertices[mid_lane][0] = vec(0, 0, 0)

    for h in range(1, height_vertices_count):
        mesh.Vertices[mid_lane][h] = CalcNextPosOnCenterLane(mesh.Vertices[mid_lane][h-1])

    # Build left side
    for lane in range(mid_lane-1, -1, -1):
        # First build the bottom vertex
        mesh.Vertices[lane][0] = CalcLeftSideBottomPos(mesh.Vertices[lane+1][0])
        # Then calculate each point above it
        for h in range(1, height_vertices_count):
            mesh.Vertices[lane][h] = CalcNextPosOnLeftSide(mesh.Vertices[lane][h-1], mesh.Vertices[lane+1][h])

    # Build right side
    for lane in range(mid_lane+1, width_vertices_count):
        # First build the bottom vertex
        mesh.Vertices[lane][0] = CalcRightSideBottomPos(mesh.Vertices[lane-1][0])
        # Then calculate each point above it
        for h in range(1, height_vertices_count):
            mesh.Vertices[lane][h] = CalcNextPosOnRightSide(mesh.Vertices[lane][h-1], mesh.Vertices[lane-1][h])

    return mesh
