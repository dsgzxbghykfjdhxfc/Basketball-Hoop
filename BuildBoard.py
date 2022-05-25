from vpython import *
import meshio
import os
import pathlib


class Mesh:

    def __init__(self, pos, width_cnt, height_cnt):
        self.Pos = pos
        self.Vertices = [[vec(0,0,0) for i in range(height_cnt)] for j in range(width_cnt)]

    def BuildVisual(self, level_of_simplicity = 1):
        for column in self.Vertices[::level_of_simplicity]:
            curve(pos = column)
        for row in range(0, len(self.Vertices[0]), level_of_simplicity):
            curve(pos = [column[row] for column in self.Vertices])

    def OutputToFile(self, filename, level_of_simplicity = 1, thickness = 0.03):
        columns = [c for c in range(0, len(self.Vertices), level_of_simplicity)]
        rows = [r for r in range(0, len(self.Vertices[0]), level_of_simplicity)]

        vertices = [[self.Vertices[c][r].x, self.Vertices[c][r].y, self.Vertices[c][r].z] for c in columns for r in rows]


        width_cnt, height_cnt = len(columns), len(rows)
        to_triangle_index = lambda x, y : x * height_cnt + y

        # The curve backboard side
        triangles = []
        for i in range(width_cnt - 1):
            for j in range(height_cnt - 1):
                triangles.append([to_triangle_index(i, j), to_triangle_index(i + 1, j), to_triangle_index(i, j + 1)])
                triangles.append([to_triangle_index(i, j + 1), to_triangle_index(i + 1, j), to_triangle_index(i + 1, j + 1)])


        back_vertices = []
        for v in vertices:
            back_vertices.append([v[0], v[1], v[2] - thickness])
        vertices.extend(back_vertices)

        offset = len(vertices) // 2
        back_triangles = []
        for tri in triangles:
            back_triangles.append([tri[0] + offset, tri[2] + offset, tri[1] + offset])
        triangles.extend(back_triangles)
        

        outer_indices = []
        for i in range(1, height_cnt - 1):
            outer_indices.append(i)
        for i in range(width_cnt):
            outer_indices.append((i + 1) * height_cnt - 1)
        for i in range(height_cnt - 2, 0, -1):
            outer_indices.append((width_cnt - 1) * height_cnt + i)
        for i in range(width_cnt - 1, -1, -1):
            outer_indices.append(i * height_cnt)


        for i in range(len(outer_indices) - 1):
            triangles.append([outer_indices[i], outer_indices[i + 1], outer_indices[i] + offset])
            triangles.append([outer_indices[i + 1], outer_indices[i + 1] + offset, outer_indices[i] + offset])
        
        triangles.append([outer_indices[-1], outer_indices[0], outer_indices[-1] + offset])
        triangles.append([outer_indices[0], outer_indices[0] + offset, outer_indices[-1] + offset])


        '''
        
        # The 3D box behind the backboard
        deepest_point = min(vertices, key=lambda p : p[2])
        backboard_z = deepest_point[2] - thickness

        top_left, bottom_left, top_right, bottom_right = self.Vertices[0][-1], self.Vertices[0][0],self.Vertices[-1][-1], self.Vertices[-1][0]

        top_left = [top_left.x, top_left.y, backboard_z]
        bottom_left = [bottom_left.x, bottom_left.y, backboard_z]
        top_right = [top_right.x, top_right.y, backboard_z]
        bottom_right = [bottom_right.x, bottom_right.y, backboard_z]
        
        vertices.extend([top_left, bottom_left, top_right, bottom_right])
        l = len(vertices)
        top_left_idx, bottom_left_idx, top_right_idx, bottom_right_idx = l - 4, l - 3, l - 2, l - 1
        triangles.append([top_left_idx, bottom_right_idx, bottom_left_idx])
        triangles.append([top_left_idx, top_right_idx, bottom_right_idx])


        width_mid, height_mid = width // 2, height // 2

        # Upper face
        for x in range(0, width_mid):
            triangles.append([to_triangle_index(x, height - 1), to_triangle_index(x + 1, height - 1), top_left_idx])
        for x in range(width_mid, width - 1):
            triangles.append([to_triangle_index(x, height - 1), to_triangle_index(x + 1, height - 1), top_right_idx])
        triangles.append([to_triangle_index(width_mid, height - 1), top_right_idx, top_left_idx])

        # Lower face
        for x in range(0, width_mid):
            triangles.append([to_triangle_index(x + 1, 0), to_triangle_index(x, 0), bottom_left_idx])
        for x in range(width_mid, width - 1):
            triangles.append([to_triangle_index(x + 1, 0), to_triangle_index(x, 0), bottom_right_idx])
        triangles.append([to_triangle_index(width_mid, 0), bottom_left_idx, bottom_right_idx])
        
        # Left face
        for y in range(0, height_mid):
            triangles.append([to_triangle_index(0, y), to_triangle_index(0, y + 1), bottom_left_idx])
        for y in range(height_mid, height - 1):
            triangles.append([to_triangle_index(0, y), to_triangle_index(0, y + 1), top_left_idx])
        triangles.append([to_triangle_index(0, height_mid), top_left_idx, bottom_left_idx])
        
        # Right face
        for y in range(0, height_mid):
            triangles.append([to_triangle_index(width - 1, y + 1), to_triangle_index(width - 1, y), bottom_right_idx])
        for y in range(height_mid, height - 1):
            triangles.append([to_triangle_index(width - 1, y + 1), to_triangle_index(width - 1, y), top_right_idx])
        triangles.append([to_triangle_index(width - 1, height_mid), bottom_right_idx, top_right_idx])
        '''

        mesh = meshio.Mesh(points = vertices, cells = {'triangle' : triangles})
        mesh.write(filename)


        print(f'Mesh data saved to {filename}')

    
    def SaveAsSlices(self, width : int, height : int, level_of_simplicity = 1, thickness = 0.03):
        
        width_cnt, height_cnt = len(self.Vertices), len(self.Vertices[0])
        x_cut_points = [i for i in range(0, width_cnt, (width_cnt - 1) // width)]    # length should be width+1
        y_cut_points = [i for i in range(0, height_cnt, (height_cnt - 1) // height)] # length should be height+1


        sub_meshes = [[Mesh(vec(0,0,0), 0, 0) for i in range(height)] for j in range(width)]
        for i in range(width):
            for j in range(height):
                for column in self.Vertices[x_cut_points[i] : x_cut_points[i + 1] + 1]:
                    sub_meshes[i][j].Vertices.append(column[y_cut_points[j] : y_cut_points[j + 1] + 1])

        os.makedirs('Models', exist_ok=True)

        for x in range(width):
            for y in range(height):
                sub_meshes[x][y].OutputToFile(f'Models/slice-{x + y * width}.obj', level_of_simplicity, thickness)


        self.OutputToFile('Models/backboard.obj', level_of_simplicity, thickness)
        



def BuildBoard(throw_distance = 5, hoop_height = 3, hoop_backboard_depth_distance = 0.3, hoop_backboard_height_distance = 0,  throw_height = 2
              , board_width = 1, board_height = 0.7, step_size = 0.05):

    hoopPos = vec(0, hoop_height - hoop_backboard_height_distance, hoop_backboard_depth_distance)
    throwPos = vec(0, throw_height, throw_distance)

    G = 9.81

    def CalcNormal(contactPos : vec):

        normal_sum = vec(0,0,0)
        # Theta for elevation angle
        for angle in range(30, 60, 1):
            theta = radians(angle)

            # Throwing Part
            throw_dis = contactPos - throwPos
            tan_theta = tan(theta)
            disXZ = sqrt(throw_dis.x ** 2 + throw_dis.z ** 2)
            inital_speed = sqrt(G * disXZ ** 2 * (1 + tan_theta ** 2) * 0.5 / (disXZ * tan_theta - throw_dis.y))
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
            bounce_velocity = vec( bounce_speed * cos(bounce_theta) * bounce_dis.x / disXZ,
                                   bounce_speed * sin(bounce_theta),
                                   bounce_speed * cos(bounce_theta) * bounce_dis.z / disXZ)


            normal = -impact_velocity.norm() + bounce_velocity.norm()
            normal = normal.norm()

            normal_sum += normal

        return normal_sum.norm()



    def CalcNextPosOnCenterLane(down):
        normal = CalcNormal(mesh.Pos + down)
        up_dir = normal.cross(vec(1,0,0))
        return down + up_dir * step_size / abs(up_dir.y)


    def CalcLeftSideBottomPos(right):
        normal = CalcNormal(mesh.Pos + right)
        left_dir = normal.cross(vec(0,1,0))
        return right + left_dir * step_size / abs(left_dir.x)


    def CalcRightSideBottomPos(left):
        normal = CalcNormal(mesh.Pos + left)
        right_dir = -normal.cross(vec(0,1,0))
        return left + right_dir * step_size / abs(right_dir.x)


    def CalcNextPosOnLeftSide(bottom, right):
        avgPos = (bottom + right) * 0.5
        normal = CalcNormal(avgPos + mesh.Pos)
        # ax + by + cz = d
        d = avgPos.x * normal.x + avgPos.y * normal.y + avgPos.z * normal.z
        z = (d - normal.x * bottom.x - normal.y * right.y) / normal.z if normal.z != 0 else 0
        return vec(bottom.x, right.y, z)
    

    def CalcNextPosOnRightSide(bottom, left):
        avgPos = (bottom + left) * 0.5
        normal = CalcNormal(avgPos + mesh.Pos)
        # ax + by + cz = d
        d = avgPos.x * normal.x + avgPos.y * normal.y + avgPos.z * normal.z
        z = (d - normal.x * bottom.x - normal.y * left.y) / normal.z if normal.z != 0 else 0
        return vec(bottom.x, left.y, z)



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



if __name__ == '__main__':

    scene = canvas(width=1500, height=650, x=0, y=0, center=vec(0, 0, 0), background=vec(0.1, 0.1, 0.1))

    mesh = BuildBoard(throw_distance=5, hoop_height=3, hoop_backboard_depth_distance=0.3, hoop_backboard_height_distance=0.05,
                      throw_height=2, board_width=0.9, board_height=0.5, step_size=0.005)
    mesh.BuildVisual(level_of_simplicity=5)
    
    
    button(text='Save mesh', pos = scene.title_anchor, bind = lambda btn: mesh.SaveAsSlices(4, 2, level_of_simplicity=5))

    # Display with vpython
    while 1:
        rate(100)


