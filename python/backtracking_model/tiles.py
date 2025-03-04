import pygame

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

# Global settings for grid dimensions and window size.
DIM = 20
WIDTH, HEIGHT = 800, 800
CELL_WIDTH = WIDTH // DIM
CELL_HEIGHT = HEIGHT // DIM

# List to store loaded images for each tile.
tiles = [None] * len(tile_definitions)

# Load and scale images for each tile.
def load_images():
    for tile in tile_definitions:
        try:
            image = pygame.image.load(tile["imagePath"])
            image = pygame.transform.scale(image, (CELL_WIDTH, CELL_HEIGHT))
            tiles[tile["id"]] = image
        except Exception as e:
            print(f"Error loading image {tile['imagePath']}: {e}")
            # Create a fallback surface if the image fails to load.
            dummy = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
            dummy.fill((200, 200, 200))
            tiles[tile["id"]] = dummy
