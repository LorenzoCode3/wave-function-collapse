import pygame
import random
import sys

# Tile definitions: each tile has an id, a name, an image path, and adjacency rules.
tile_definitions = [
    {
        "id": 0,
        "name": "Blank",
        "imagePath": "tiles\\blank.png",
        "rules": {
            "up": [0, 1],
            "right": [0, 2],
            "down": [0, 3],
            "left": [0, 4]
        }
    },
    {
        "id": 1,
        "name": "Up",
        "imagePath": "tiles\\up.png",
        "rules": {
            "up": [2, 4, 3],
            "right": [4, 1, 3],
            "down": [0, 3],
            "left": [2, 1, 3]
        }
    },
    {
        "id": 2,
        "name": "Right",
        "imagePath": "tiles\\right.png",
        "rules": {
            "up": [2, 4, 3],
            "right": [4, 1, 3],
            "down": [2, 4, 1],
            "left": [0, 4]
        }
    },
    {
        "id": 3,
        "name": "Down",
        "imagePath": "tiles\\down.png",
        "rules": {
            "up": [0, 1],
            "right": [4, 1, 3],
            "down": [2, 4, 1],
            "left": [2, 1, 3]
        }
    },
    {
        "id": 4,
        "name": "Left",
        "imagePath": "tiles\\left.png",
        "rules": {
            "up": [2, 4, 3],
            "right": [0, 2],
            "down": [2, 4, 1],
            "left": [1, 3, 2]
        }
    }
]

# Grid and window dimensions
DIM = 20
WIDTH, HEIGHT = 800, 800
CELL_WIDTH = WIDTH // DIM
CELL_HEIGHT = HEIGHT // DIM

# List to store loaded images for each tile
tiles = [None] * len(tile_definitions)

def load_images():
    # Load images for each tile and scale them to cell dimensions
    for tile in tile_definitions:
        try:
            image = pygame.image.load(tile["imagePath"])
            image = pygame.transform.scale(image, (CELL_WIDTH, CELL_HEIGHT))
            tiles[tile["id"]] = image
        except Exception as e:
            print(f"Error loading image {tile['imagePath']}: {e}")
            # If image fails to load, create a placeholder surface
            dummy = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
            dummy.fill((200, 200, 200))
            tiles[tile["id"]] = dummy

# Initialize grid: each cell starts with all possible tile options
grid = [[{"options": [tile["id"] for tile in tile_definitions]} for _ in range(DIM)] for _ in range(DIM)]

def count_collapsed():
    # Returns the number of collapsed cells (cells with a single option)
    count = 0
    for row in grid:
        for cell in row:
            if len(cell["options"]) == 1:
                count += 1
    return count

def update_grid(x, y, valid_options):
    # Updates the options of a cell by intersecting them with the valid options
    current_options = grid[x][y]["options"]
    grid[x][y]["options"] = [option for option in current_options if option in valid_options]

def get_allowed_neighbors(tile_id, direction):
    # Given a tile id and a direction, returns allowed tile ids for the neighbor
    tile = next((t for t in tile_definitions if t["id"] == tile_id), None)
    if tile:
        return tile["rules"][direction]
    return []

def propagate_constraints():
    # Propagates constraints from collapsed cells to neighbors until no further updates occur
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
                    # Update the cell above
                    if i > 0:
                        update_grid(i - 1, j, get_allowed_neighbors(state, "up"))
                    # Update the cell to the right
                    if j < DIM - 1:
                        update_grid(i, j + 1, get_allowed_neighbors(state, "right"))
                    # Update the cell below
                    if i < DIM - 1:
                        update_grid(i + 1, j, get_allowed_neighbors(state, "down"))
                    # Update the cell to the left
                    if j > 0:
                        update_grid(i, j - 1, get_allowed_neighbors(state, "left"))

def collapse_lowest_entropy():
    # Finds cells with the lowest entropy (fewest options, but more than one) and randomly collapses one of them.
    # Returns True if a collapse occurred, otherwise False.
    lowest_entropy_value = float('inf')
    for i in range(DIM):
        for j in range(DIM):
            options_length = len(grid[i][j]["options"])
            if 1 < options_length < lowest_entropy_value:
                lowest_entropy_value = options_length

    if lowest_entropy_value == float('inf'):
        return False

    # Collect all cells with the minimum entropy
    lowest_entropy_cells = [
        (i, j) for i in range(DIM) for j in range(DIM)
        if len(grid[i][j]["options"]) == lowest_entropy_value
    ]
    if lowest_entropy_cells:
        cell_x, cell_y = random.choice(lowest_entropy_cells)
        grid[cell_x][cell_y]["options"] = [random.choice(grid[cell_x][cell_y]["options"])]
        return True
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wave Function Collapse")
    clock = pygame.time.Clock()

    load_images()

    # Randomly collapse one cell to start the algorithm.
    rand_x = random.randint(0, DIM - 1)
    rand_y = random.randint(0, DIM - 1)
    grid[rand_x][rand_y]["options"] = [random.choice(grid[rand_x][rand_y]["options"])]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Draw the grid: if a cell is collapsed, draw its corresponding image;
        # otherwise, draw a black cell with a white border.
        for i in range(DIM):
            for j in range(DIM):
                cell = grid[i][j]
                rect = pygame.Rect(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                if len(cell["options"]) == 1:
                    tile_id = cell["options"][0]
                    screen.blit(tiles[tile_id], rect)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        pygame.display.flip()

        # If all cells are collapsed, the algorithm stops.
        if count_collapsed() == DIM * DIM:
            print("All cells are collapsed!")
            running = False
            pygame.time.delay(3000)  # Wait for 3000 milliseconds (3 seconds)
        else:
            propagate_constraints()
            collapse_lowest_entropy()

        clock.tick(30)  # Limit to 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
