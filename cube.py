from designer import *
import numpy as np
import math as m
from dataclasses import dataclass


@dataclass
class World:
    angle_x: float
    angle_y: float
    angle_z: float
    scale: int
    vertices: list[DesignerObject]
    lines: list[DesignerObject]
    faces: list[DesignerObject]
    click_pos: list[int]
    is_clicking: bool

circle_pos = [get_width()/2, get_height()/2]



projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])


points = []
# Create list of 3d coordinates
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1, 1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

# sets number of projected points to equal regular 3d points
projected_points = [
    [n, n] for n in range(len(points))
]


def connect_points(i: int, j: int, points) -> DesignerObject:
    # Returns a line connecting points at indexes i and j in list points
    return line("black", points[i][0], points[i][1], points[j][0], points[j][1])

def create_face(color: str, i: int, j: int, k: int, l: int, points) -> DesignerObject:
    # Returns a shape of chosen color connecting points at indexes i, j, k, and l in list points
    return shape(color, [points[i][0], points[i][1], points[j][0], points[j][1], points[k][0], points[k][1], points[l][0], points[l][1]], absolute=True, anchor='topleft')






def pan_start(world: World, x, y):
    world.click_pos = [x, y]
    world.is_clicking = True

def pan_end(world: World):
    world.is_clicking = False

def scale(world: World, key):
    if key == 'up':
        world.scale += 25
    if key == 'down':
        world.scale -= 25

def main_loop(world: World):




    rotation_x = np.matrix([
        [1, 0, 0],
        [0, m.cos(world.angle_x), -m.sin(world.angle_x)],
        [0, m.sin(world.angle_x), m.cos(world.angle_x)]
    ])

    rotation_y = np.matrix([
        [m.cos(world.angle_y), 0, m.sin(world.angle_y)],
        [0, 1, 0],
        [-m.sin(world.angle_y), 0, m.cos(world.angle_y)]
    ])

    rotation_z = np.matrix([
        [m.cos(world.angle_z), -m.sin(world.angle_z), 0],
        [m.sin(world.angle_z), m.cos(world.angle_z), 0],
        [0, 0, 1]
    ])


    for index, point in enumerate(points):

        # @ is the matrix multiplication operator
        # Use transpose to change point from 1x3 to 3x1 matrix to make multiplication with 2d matrix compatible

        # For each 3d coordinate, multiply by rotation_z to rotate points about the z axis
        rotated2d = rotation_x @ point.transpose()
        rotated2d = rotation_y @ rotated2d
        rotated2d = rotation_z @ rotated2d
        # For each 3d coordinate, multiply by projection_matrix to convert to 2d coordinate
        projected2d = projection_matrix @ rotated2d

        # Set projected x and y values for each coordinate
        x = projected2d[0, 0] * world.scale + circle_pos[0]
        y = projected2d[1, 0] * world.scale + circle_pos[1]

        # Add x and y values to list of projected points
        projected_points[index] = [x, y]

        # Move corresponding vertices to newly calculated positions
        world.vertices[index].x = x
        world.vertices[index].y = y

    #Destroys current faces
    for face in world.faces:
        destroy(face)

    # Generates 6 new faces
    world.faces[0] = create_face("red", 0, 1, 2, 3, projected_points)
    world.faces[1] = create_face("red", 4, 5, 6, 7, projected_points)
    for p in range(4):
        world.faces[p+2] = create_face("red", p, (p+1)%4, (p+1)%4+4, p+4, projected_points)

    # Destroys current lines
    for line in world.lines:
        destroy(line)

    # Generates 12 new lines
    for p in range(4):
        world.lines[p] = connect_points(p, (p+1) % 4, projected_points)
        world.lines[p+4] = connect_points(p+4, (p + 1) % 4 + 4, projected_points)
        world.lines[p+8] = connect_points(p, p+4, projected_points)

    for vertex in world.vertices:
        destroy(vertex)
    for index, projected_point in enumerate(projected_points):
        world.vertices[index] = circle("black", 5, projected_point[0], projected_point[1])


    # Code for rotating cube with mouse pan
    if world.is_clicking:
        world.angle_y += -(get_mouse_x() - world.click_pos[0])/500
        world.angle_x += (get_mouse_y() - world.click_pos[1])/500
        world.click_pos[0] = get_mouse_x()
        world.click_pos[1] = get_mouse_y()






def create_World() -> World:
    vertices = []
    lines = []
    faces = []
    starting_scale = 100.0
    for index, point in enumerate(points):
        # @ is the matrix multiplication operator
        # Use transpose to change point from 1x3 to 3x1 matrix to make multiplication with 2d matrix compatible
        projected2d = projection_matrix @ point.transpose()

        x = projected2d[0, 0] * starting_scale + circle_pos[0]
        y = projected2d[1, 0] * starting_scale + circle_pos[1]

        vertices.append(circle("black", 5, x, y))

        projected_points[index] = [x, y]


    for p in range(4):
        lines.append(connect_points(p, (p+1) % 4, projected_points))
        lines.append(connect_points(p+4, (p + 1) % 4 + 4, projected_points))
        lines.append(connect_points(p, p+4, projected_points))

    faces.append(create_face("red", 0, 1, 2, 3, projected_points))
    faces.append(create_face("red", 4, 5, 6, 7, projected_points))
    for p in range(4):
        faces.append(create_face("red", p, (p + 1) % 4, (p + 1) % 4 + 4, p + 4, projected_points))

    return World(0.0, 0.0, 0.0, starting_scale, vertices, lines, faces, [0,0], False)









when('starting', create_World)
when('input.mouse.down', pan_start)
when('input.mouse.up', pan_end)
when('typing', scale)
when('updating', main_loop)
start()