// Tile definitions: each tile has an id, a name, an image path, and adjacency rules.
// The rules define, for each direction ("up", "right", "down", "left"), which tile ids are allowed.
const tileDefinitions = [
    {
        id: 0,
        name: "Blank",
        imagePath: "tiles\\blank.png",
        rules: {
            up: [0, 1],
            right: [0, 2],
            down: [0, 3],
            left: [0, 4]
        }
    },
    {
        id: 1,
        name: "Up",
        imagePath: "tiles\\up.png",
        rules: {
            up: [2, 4, 3],
            right: [4, 1, 3],
            down: [0, 3],
            left: [2, 1, 3]
        }
    },
    {
        id: 2,
        name: "Right",
        imagePath: "tiles\\right.png",
        rules: {
            up: [2, 4, 3],
            right: [4, 1, 3],
            down: [2, 4, 1],
            left: [0, 4]
        }
    },
    {
        id: 3,
        name: "Down",
        imagePath: "tiles\\down.png",
        rules: {
            up: [0, 1],
            right: [4, 1, 3],
            down: [2, 4, 1],
            left: [2, 1, 3]
        }
    },
    {
        id: 4,
        name: "Left",
        imagePath: "tiles\\left.png",
        rules: {
            up: [2, 4, 3],
            right: [0, 2],
            down: [2, 4, 1],
            left: [1, 3, 2]
        }
    }
];

const tiles = []; // Array for loaded tile images
const DIM = 20;   // Grid size

// Initialize an empty 2D grid
let grid = Array.from({ length: DIM }, () => []);
let collapsedCounter = 0;

// p5.js preload: loads the images for each tile based on tileDefinitions.
function preload() {
    tileDefinitions.forEach(tile => {
        tiles[tile.id] = loadImage(tile.imagePath);
    });
}

// p5.js setup: creates the canvas and initializes each grid cell with all possible tile options.
function setup() {
    createCanvas(800, 800);

    // For each grid cell, assign all tile ids as possible options.
    for (let i = 0; i < DIM; i++) {
        for (let j = 0; j < DIM; j++) {
            grid[i][j] = { options: tileDefinitions.map(t => t.id) };
        }
    }

    // Randomly collapse one cell to start the algorithm.
    const randX = round(random(0, DIM - 1));
    const randY = round(random(0, DIM - 1));
    grid[randX][randY].options = [random(grid[randX][randY].options)];
    collapsedCounter++;
}

// p5.js mousePressed: redraws the canvas when the mouse is clicked.
function mousePressed() {
    redraw();
}

// Updates a cell's possible options by reducing them to the intersection of its current options
// and the valid options provided (from an adjacent cell).
function updateGrid(x, y, validOptions) {
    const currentOptions = grid[x][y].options;
    grid[x][y].options = currentOptions.filter(option => validOptions.includes(option));
}

// Returns the number of collapsed cells (cells with only one option left).
function countCollapsed() {
    let count = 0;
    for (let i = 0; i < DIM; i++) {
        for (let j = 0; j < DIM; j++) {
            if (grid[i][j].options.length === 1) count++;
        }
    }
    return count;
}

// Given a tile id and a direction, returns the allowed neighboring tile ids.
function getAllowedNeighbors(tileId, direction) {
    const tile = tileDefinitions.find(t => t.id === tileId);
    return tile ? tile.rules[direction] : [];
}

// Propagates constraints from collapsed cells to their neighbors until no further changes occur.
function propagateConstraints() {
    let previousCount;
    do {
        previousCount = countCollapsed();
        for (let i = 0; i < DIM; i++) {
            for (let j = 0; j < DIM; j++) {
                if (grid[i][j].options.length === 1) {
                    const state = grid[i][j].options[0];
                    // Update the cell above, if it exists.
                    if (i > 0) updateGrid(i - 1, j, getAllowedNeighbors(state, "up"));
                    // Update the cell to the right, if it exists.
                    if (j < DIM - 1) updateGrid(i, j + 1, getAllowedNeighbors(state, "right"));
                    // Update the cell below, if it exists.
                    if (i < DIM - 1) updateGrid(i + 1, j, getAllowedNeighbors(state, "down"));
                    // Update the cell to the left, if it exists.
                    if (j > 0) updateGrid(i, j - 1, getAllowedNeighbors(state, "left"));
                }
            }
        }
    } while (countCollapsed() !== previousCount);
}

// p5.js draw: renders the grid and applies the wave function collapse algorithm.
function draw() {
    background(0);
    const cellWidth = width / DIM;
    const cellHeight = height / DIM;

    // Draw each cell: if collapsed, display the corresponding image;
    // otherwise, draw a black rectangle with a white border.
    for (let i = 0; i < DIM; i++) {
        for (let j = 0; j < DIM; j++) {
            const cell = grid[i][j];
            if (cell.options.length === 1) {
                image(tiles[cell.options[0]], j * cellWidth, i * cellHeight, cellWidth, cellHeight);
            } else {
                fill(0);
                stroke(255);
                rect(j * cellWidth, i * cellHeight, cellWidth, cellHeight);
            }
        }
    }

    // Stop the algorithm when all cells are collapsed.
    if (collapsedCounter === DIM * DIM) return;

    // Propagate constraints based on adjacency rules.
    propagateConstraints();
    collapsedCounter = countCollapsed();

    // Identify cells with the lowest entropy (fewest options left, but >1).
    let lowestEntropyValue = Infinity;
    const lowestEntropyCells = [];
    for (let i = 0; i < DIM; i++) {
        for (let j = 0; j < DIM; j++) {
            const optionsLength = grid[i][j].options.length;
            if (optionsLength > 1 && optionsLength < lowestEntropyValue) {
                lowestEntropyValue = optionsLength;
            }
        }
    }
    for (let i = 0; i < DIM; i++) {
        for (let j = 0; j < DIM; j++) {
            if (grid[i][j].options.length === lowestEntropyValue) {
                lowestEntropyCells.push([i, j]);
            }
        }
    }

    // Randomly collapse one cell among those with the lowest entropy.
    if (lowestEntropyCells.length > 0) {
        const [cellX, cellY] = random(lowestEntropyCells);
        grid[cellX][cellY].options = [random(grid[cellX][cellY].options)];
        collapsedCounter++;
    }

    // Debug: print the number of collapsed cells.
    console.log(collapsedCounter);
}
