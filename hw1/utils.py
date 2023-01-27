from typing import List, Tuple, Optional, Union
from enum import IntEnum
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import numpy.typing as npt


class PathPlanMode(IntEnum):
    DFS = 1
    BFS = 2
    GRAD = 3
    A_STAR = 4


def distance(
    point_a: List[Tuple[int, int]], point_b: List[Tuple[int, int]]
) -> Union[npt.ArrayLike, float]:
    return np.linalg.norm(np.array(point_b) - np.array(point_a))


def neighbors(grid: npt.ArrayLike, i: int, j: int):

    """Find all of the adjacent cells
    in a grid given coordinate [i, j].

    Args:
        grid (numpy): n x n numpy grid.
        i (int): row coordinate
        j (int): column coordinate

    Returns:
        _type_: _description_
    """
    n = []

    if i - 1 >= 0:
        n.append((i - 1, j))
        if j - 1 >= 0:
            n.append((i - 1, j - 1))
        if j + 1 < grid.shape[1]:
            n.append((i - 1, j + 1))
    if i + 1 < grid.shape[0]:
        n.append((i + 1, j))
        if j - 1 >= 0:
            n.append((i + 1, j - 1))
        if j + 1 < grid.shape[1]:
            n.append((i + 1, j + 1))
    if j - 1 >= 0:
        n.append((i, j - 1))
    if j + 1 < grid.shape[1]:
        n.append((i, j + 1))
    return n


def plot_GVD(
    grid: npt.ArrayLike,
    world_id: int,
    GVD: Optional[List[Tuple[int, int]]] = None,
    path: Optional[Path] = None,
):
    """Plot the Generalized Voronoi Diagram
    given a n x n numpy grid.

    Args:
        grid (numpy): _description_
        GVD (list, optional): _description_. Defaults to None.
        path (list, optional): _description_. Defaults to None.
    """

    fig, ax = plt.subplots()
    GVD_grid = np.copy(grid)
    if GVD:
        GVD_x, GVD_y = zip(*GVD)
        GVD_grid[GVD_x, GVD_y] = 20

    img1 = ax.imshow(GVD_grid, cmap="RdBu", alpha=0.6)
    obstacles = GVD_grid.copy()
    obstacles[obstacles < 0] = -2.0
    masked_data = np.ma.masked_where(obstacles > 0, obstacles)
    img2 = ax.imshow(masked_data, cmap="bwr")
    legend_elements = [Patch(facecolor="blue", label="Obstacle")]
    if GVD:
        legend_elements.append(Patch(facecolor="#83b1d3", label="GVD"))

    if path:
        path_x, path_y = zip(*path)
        GVD_grid[path_x, path_y] = 40.0
        grid_path = GVD_grid.copy()
        grid_path = np.ma.masked_where(grid_path != 40.0, grid_path)
        img3 = ax.imshow(grid_path, cmap="cool_r", interpolation="nearest")
        legend_elements.append(Patch(facecolor="#e741f6", label="path"))

    ax.set_title(f"Grid World {world_id} Path Planning Result")
    ax.legend(handles=legend_elements)
    plt.show()


def create_circle_obstacle(
    grid_world: npt.ArrayLike, center_x: int, center_y: int, radius: int, obst_id: int
) -> npt.ArrayLike:
    c_x, c_y, r_2 = center_x, center_y, radius
    for x in range(grid_world.shape[0]):
        for y in range(grid_world.shape[1]):
            if np.sqrt((x - c_x) ** 2 + (y - c_y) ** 2) < r_2:
                grid_world[int(x), int(y)] = obst_id
    return grid_world


def create_rectangle_obstacle(
    grid_world: npt.ArrayLike,
    lower_x: int,
    upper_x: int,
    lower_y: int,
    upper_y: int,
    obst_id: int,
) -> npt.ArrayLike:
    grid_world[lower_x:upper_x, lower_y:upper_y] = obst_id
    return grid_world


def generate_world_1(width: int = 100, height: int = 100):
    x_list = np.linspace(0, width - 1, width)
    y_list = np.linspace(0, height - 1, height)

    grid_world = np.zeros((width, height))

    grid_world = create_rectangle_obstacle(grid_world, 30, 70, 40, 60, -1)
    return grid_world, x_list, y_list


def generate_world_2(width: int = 100, height: int = 100):
    x_list = np.linspace(0, width - 1, width)
    y_list = np.linspace(0, height - 1, height)

    grid_world = np.zeros((width, height))

    grid_world = create_rectangle_obstacle(grid_world, 20, 40, 45, 85, -1)

    for x in range(60, 91):
        for y in range(20, 91 - x + 21):
            grid_world[int(x), int(y)] = -2

    return grid_world, x_list, y_list


def generate_world_3(width: int = 100, height: int = 100):
    x_list = np.linspace(0, width - 1, width)
    y_list = np.linspace(0, height - 1, height)

    grid_world = np.zeros((width, height))

    grid_world = create_rectangle_obstacle(grid_world, 15, 45, 20, 50, -1)
    grid_world = create_circle_obstacle(grid_world, 75.0, 30.0, 12, -2)
    grid_world = create_circle_obstacle(grid_world, 50.0, 75.0, 16, -3)

    return grid_world, x_list, y_list


def generate_world_4(width: int = 100, height: int = 100):
    x_list = np.linspace(0, width - 1, width)
    y_list = np.linspace(0, height - 1, height)

    grid_world = np.zeros((width, height))

    # triangle
    for x in range(50, 81):
        for y in range(20, 21 + x - 50):
            grid_world[int(x), int(y)] = -1

    grid_world = create_rectangle_obstacle(grid_world, 30, 60, 55, 85, -2)
    grid_world = create_circle_obstacle(grid_world, 25.0, 30.0, 12, -3)

    return grid_world, x_list, y_list
