from tiles import tile_definitions, DIM
import copy

# Initialize the grid: each cell starts with all possible options.
grid = [
    [{"options": [tile["id"] for tile in tile_definitions]} for _ in range(DIM)]
    for _ in range(DIM)
]

# Return the number of collapsed cells (cells with only one option).
def count_collapsed():
    count = 0
    for row in grid:
        for cell in row:
            if len(cell["options"]) == 1:
                count += 1
    return count

# Update the cell's options by keeping only those that are allowed.
def update_grid(x, y, valid_options):
    current_options = grid[x][y]["options"]
    grid[x][y]["options"] = [option for option in current_options if option in valid_options]
