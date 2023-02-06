import os
import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def handler(signum, frame):
    raise Exception("end of time")


def update_axis(axis, legend_elements, GVD_grid, path, label):
    """ Update plot axis given the path data

    Args:
        ax (matplotlib axis): the subplot axis
        legend_elements (list of patches): the plot legends
        GVD_grid (numpy array): the gvd grid
        path (list[tuple]): the path computed.
        label (string): description for the title and legend
    """
    path_x, path_y = zip(*path)
    GVD_grid[path_x, path_y] = 40
    grid_path = GVD_grid.copy()
    grid_path = np.ma.masked_where(grid_path != 40.0, grid_path)
    img3 = axis.imshow(grid_path, cmap="cool_r", interpolation="nearest")
    axis.set_title(label)
    legend_elements.append(
        Patch(facecolor='#e741f6', label=f'{label} Test'))
    axis.legend(handles=legend_elements)


def plot_GVD_unit_tests(
        grid, GVD, start_path=None, bfs=None, dfs=None, end=None):
    """ Plot the Generalized Voronoi Diagram
    given a n x n numpy grid.
    Args:
        grid (numpy): _description_
        GVD (list, optional): _description_. Defaults to None.
        path (list, optional): _description_. Defaults to None.
    """

    _, axes = plt.subplots(2, 2, figsize=(10, 10))
    GVD_grid = np.copy(grid)
    if GVD:
        GVD_x, GVD_y = zip(*GVD)
        GVD_grid[GVD_x, GVD_y] = 20

    for axis in axes.flatten():
        axis.imshow(GVD_grid, cmap="RdBu", alpha=0.6)
        obstacles = GVD_grid.copy()
        obstacles[obstacles < 0] = -2.0
        masked_data = np.ma.masked_where(obstacles > 0, obstacles)
        axis.imshow(masked_data, cmap="bwr")
        legend_elements = [Patch(facecolor='blue', label='Obstacle')]
        legend_elements.append(Patch(facecolor='#83b1d3', label='GVD'))

    if start_path["path"]:
        start = start_path["start"]
        goal = start_path["path"][-1]
        axes[0, 0].plot([start[1], goal[1]], [
                        start[0], goal[0]], "k*", label="Start/Goal")
        update_axis(
            axes[0, 0], legend_elements.copy(), GVD_grid.copy(),
            start_path["path"], "Gradient Ascent Test")
    if bfs["path"]:
        start = bfs["start"]
        goal = bfs["goal"]
        axes[0, 1].plot([start[1], goal[1]], [
                        start[0], goal[0]], "k*", label="Start/Goal")
        update_axis(axes[0, 1], legend_elements.copy(),
                    GVD_grid.copy(), bfs["path"], "BFS Test")
    if dfs["path"]:
        start = dfs["start"]
        goal = dfs["goal"]
        axes[1, 0].plot([start[1], goal[1]], [
                        start[0], goal[0]], "k*", label="Start/Goal")
        update_axis(axes[1, 0], legend_elements.copy(),
                    GVD_grid.copy(), dfs["path"], "DFS Test")
    if end["path"]:
        start = end["start"]
        goal = end["goal"]
        axes[1, 1].plot([start[1], goal[1]], [start[0], goal[0]], "k-.")
        axes[1, 1].plot([start[1], goal[1]], [start[0], goal[0]], "k*")
        legend_elements.append(
            Patch(facecolor='#000000', label='Heuristic Line'))
        update_axis(axes[1, 1], legend_elements.copy(),
                    GVD_grid.copy(), end["path"], "A* Test")
    plt.show()


def check_directory():
    """ Check if the user is running script in the valid directory 

    Returns:
        boolean: true if the directory is valid. else false. 
    """
    files = os.listdir("./")
    if "hw1" in files:
        hw1_files = os.listdir("./hw1")
        if "path_finding.py" in hw1_files:
            return True
    print("we are unable to find the path_finding.py file. \
        Please see the README for how to use this unit test file")
    return False


def test_part1(grid, GVD, start=(83, 16), goal=(7, 8)):
    from hw1.path_finding import GVD_path
    from hw1.utils import PathPlanMode

    print("="*20)
    print("running 4.1 BFS and DFS...")

    path_bfs, _, _ = GVD_path(
        grid, GVD, start, goal, PathPlanMode.BFS)
    cost = len(path_bfs) if path_bfs else 0
    print(f"BFS Finished. Path length: {cost} steps")

    path_dfs, _, _ = GVD_path(
        grid, GVD, start, goal, PathPlanMode.DFS)
    cost = len(path_dfs) if path_bfs else 0
    print(f"DFS Finished: Path length: {cost} steps")

    return {"path": path_bfs, "start": start, "goal": goal}, \
        {"path": path_dfs, "start": start, "goal": goal}


def test_part2(grid, GVD, start=(50, 0), goal=(7, 8)):
    from hw1.path_finding import cell_to_GVD_gradient_ascent

    print("="*20)
    print("running 4.2 Gradient Ascent")

    start_path = cell_to_GVD_gradient_ascent(grid, GVD, start)
    return {"path": start_path, "start": start, "goal": goal}


def test_part3(grid, GVD, start=(95, 80), goal=(25, 8)):
    from hw1.path_finding import cell_to_GVD_a_star

    print("="*20)
    print("running 4.3 A*")

    end_path, _, _ = cell_to_GVD_a_star(grid, GVD, start, goal=goal)
    return {"path": end_path, "start": start, "goal": goal}


def visualize_testing_results(grid, GVD, start, end, bfs, dfs):

    print("="*20)
    print("Validating results...")

    if bfs["path"] is None or dfs["path"] is None:
        print("="*20)
        print("4.1 FAILED: function returned none. your 4.1 implementation might be empty")
    if start["path"] is None:
        print("="*20)
        print("4.2 FAILED: function returned none. your 4.2 implementation might be empty")
    if end["path"] is None:
        print("="*20)
        print("4.3 FAILED: function returned none. your 4.3 implementation might be empty")

    plot_GVD_unit_tests(grid, GVD, start, bfs, dfs, end)


def main():

    valid_directory = check_directory()
    if valid_directory is False:
        return

    bfs, dfs = None, None
    start_path = {"path": None}
    end_path = {"path": None}

    world_dir = "worlds"
    world_id = 1

    grid = np.load(f"{world_dir}/world_{world_id}.npy")
    GVD = set([tuple(cell) for cell in np.load(
        f"{world_dir}/world_{1}_gvd.npy")])

    # ==========================================================================
    # ==== comment / uncomment the following three tests to test your code =====
    bfs, dfs = test_part1(grid, GVD)
    start_path = test_part2(grid, GVD)
    end_path = test_part3(grid, GVD)
    # ==========================================================================
    # ==========================================================================

    visualize_testing_results(
        grid, GVD, start_path, end_path, bfs, dfs)


if __name__ == "__main__":
    main()
