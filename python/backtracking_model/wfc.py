import random
import copy
from grid import grid, count_collapsed, update_grid
from constraints import get_allowed_neighbors
from tiles import DIM

# Propagate constraints from collapsed cells to their neighbors.
def propagate_constraints():
    previous_count = -1
    while True:
        current_count = count_collapsed()
        if current_count == previous_count:
            break
        previous_count = current_count
        for i in range(DIM):
            for j in range(DIM):
                if len(grid[i][j]["options"]) == 1:
                    state = grid[i][j]["options"][0]
                    # Update the cell above.
                    if i > 0:
                        update_grid(i - 1, j, get_allowed_neighbors(state, "up"))
                    # Update the cell to the right.
                    if j < DIM - 1:
                        update_grid(i, j + 1, get_allowed_neighbors(state, "right"))
                    # Update the cell below.
                    if i < DIM - 1:
                        update_grid(i + 1, j, get_allowed_neighbors(state, "down"))
                    # Update the cell to the left.
                    if j > 0:
                        update_grid(i, j - 1, get_allowed_neighbors(state, "left"))

# Check if any cell has no available options.
def check_contradiction():
    for i in range(DIM):
        for j in range(DIM):
            if len(grid[i][j]["options"]) == 0:
                return True
    return False

# Find the cell with the lowest entropy (more than one option) and return its coordinates and available options.
def choose_cell_with_lowest_entropy():
    lowest_entropy = float('inf')
    best_cell = None
    for i in range(DIM):
        for j in range(DIM):
            n_options = len(grid[i][j]["options"])
            if 1 < n_options < lowest_entropy:
                lowest_entropy = n_options
                best_cell = (i, j)
    if best_cell is not None:
        i, j = best_cell
        return best_cell, grid[i][j]["options"][:]
    else:
        return None, []

# Collapse the given cell by selecting the specified option.
def collapse_cell(cell, option):
    i, j = cell
    grid[i][j]["options"] = [option]
