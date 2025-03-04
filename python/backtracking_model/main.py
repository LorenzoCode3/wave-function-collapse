import pygame
import random
import sys
import copy

from tiles import load_images, tiles, DIM, WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT
from grid import grid, count_collapsed
from wfc import propagate_constraints, check_contradiction, choose_cell_with_lowest_entropy, collapse_cell

# Main entry point for the application.
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wave Function Collapse with Backtracking")
    clock = pygame.time.Clock()

    load_images()

    # List to store states for backtracking.
    backtrack_stack = []

    # Randomly collapse a cell to start the algorithm.
    rand_x = random.randint(0, DIM - 1)
    rand_y = random.randint(0, DIM - 1)
    initial_choice = random.choice(grid[rand_x][rand_y]["options"])
    grid[rand_x][rand_y]["options"] = [initial_choice]

    propagate_constraints()

    running = True
    solved = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Draw the grid: if a cell is collapsed, draw its image; otherwise, draw a black cell with a white border.
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

        # Check if the puzzle is solved.
        if count_collapsed() == DIM * DIM:
            print("All cells collapsed!")
            solved = True
            running = False
            continue

        propagate_constraints()

        # If a contradiction is found, perform backtracking.
        if check_contradiction():
            print("Contradiction found, performing backtracking...")
            if not backtrack_stack:
                print("No solution found.")
                running = False
                continue
            backtracked = False
            while backtrack_stack and check_contradiction():
                last_state = backtrack_stack.pop()
                grid[:] = copy.deepcopy(last_state["grid"])
                cell = last_state["cell"]
                i, j = cell
                # Determine options not yet attempted.
                remaining_options = [opt for opt in last_state["options"] if opt not in last_state["tried"]]
                if remaining_options:
                    new_choice = random.choice(remaining_options)
                    last_state["tried"].append(new_choice)
                    grid[i][j]["options"] = [new_choice]
                    backtrack_stack.append({
                        "grid": copy.deepcopy(grid),
                        "cell": cell,
                        "options": last_state["options"],
                        "tried": last_state["tried"][:]
                    })
                    propagate_constraints()
                    backtracked = True
                    break
            if not backtracked:
                print("Unable to solve the puzzle using backtracking.")
                running = False
                continue
        else:
            cell, options = choose_cell_with_lowest_entropy()
            if cell is None:
                continue
            backtrack_stack.append({
                "grid": copy.deepcopy(grid),
                "cell": cell,
                "options": options[:],
                "tried": []
            })
            choice = random.choice(options)
            collapse_cell(cell, choice)
            propagate_constraints()

        clock.tick(30)  # Limit to 30 FPS

    pygame.time.delay(3000)  # Wait for 3 seconds before closing.
    pygame.quit()
    if solved:
        sys.exit("Puzzle solved!")
    else:
        sys.exit("Puzzle unsolvable!")

if __name__ == "__main__":
    main()
