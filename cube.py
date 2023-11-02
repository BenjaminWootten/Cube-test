from designer import *
import numpy as np
import math as m
from dataclasses import dataclass


@dataclass
class World:
    angle: float
    vertices: list[DesignerObject]

scale = 100
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


def create_World() -> World:
    vertices = []
    for point in points:
        # @ is the matrix multiplication operator
        # Use transpose to change point from 1x3 to 3x1 matrix to make multiplication with 2d matrix compatible
        projected2d = projection_matrix @ point.transpose()

        x = projected2d[0, 0] * scale + circle_pos[0]
        y = projected2d[1, 0] * scale + circle_pos[1]

        vertices.append(circle("black", 5, x, y))

    return World(0.0, vertices)


def main_loop(world: World):


    world.angle += 0.01

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, m.cos(world.angle), -m.sin(world.angle)],
        [0, m.sin(world.angle), m.cos(world.angle)]
    ])

    rotation_y = np.matrix([
        [m.cos(world.angle), 0, m.sin(world.angle)],
        [0, 1, 0],
        [-m.sin(world.angle), 0, m.cos(world.angle)]
    ])

    rotation_z = np.matrix([
        [m.cos(world.angle), -m.sin(world.angle), 0],
        [m.sin(world.angle), m.cos(world.angle), 0],
        [0, 0, 1]
    ])

    point1 = [0, 0]
    drawline = False

    for index, point in enumerate(points):

        # @ is the matrix multiplication operator
        # Use transpose to change point from 1x3 to 3x1 matrix to make multiplication with 2d matrix compatible

        # For each 3d coordinate, multiply by rotation_z to rotate points about the z axis
        rotated2d = rotation_x @ point.transpose()
        rotated2d = rotation_y @ rotated2d
        rotated2d = rotation_z @ rotated2d
        # For each 3d coordinate, multiply by projection_matrix to convert to 2d coordinate
        projected2d = projection_matrix @ rotated2d


        x = projected2d[0, 0] * scale + circle_pos[0]
        y = projected2d[1, 0] * scale + circle_pos[1]

        world.vertices[index].x = x
        world.vertices[index].y = y



when('starting', create_World)
when('updating', main_loop)
start()