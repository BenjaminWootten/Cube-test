from designer import *
import numpy as np
import math as m

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



def main_loop():


    for point in points:
        # @ is the matrix multiplication operator
        # Use transpose to change point from 1x3 to 3x1 matrix to make multiplication with 2d matrix compatible

        # For each 3d coordinate, multiply by projection_matrix to convert to 2d coordinate
        projected2d = projection_matrix @ point.transpose()


        x = projected2d[0, 0] * scale + circle_pos[0]
        y = projected2d[1, 0] * scale + circle_pos[1]

        circle("black", 5, x, y)




when('updating', main_loop)
start()