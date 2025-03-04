// Array for tile images and grid size
const tiles = [];
const DIM = 20;

// Initialize an empty 2D grid
let grid = Array.from({ length: DIM }, () => []);
let collapsedCounter = 0;

// Constants representing tile states
const BLANK = 0;
const UP = 1;
const RIGHT = 2;
const DOWN = 3;
const LEFT = 4;

// Tile adjacency rules.
// Each element in "rules" contains 4 arrays corresponding to:
// [above, right, below, left] based on the current state.
const rules = [
  // BLANK
  [
    [BLANK, UP],    // The cell above must be BLANK or UP
    [BLANK, RIGHT], // The cell to the right must be BLANK or RIGHT
    [BLANK, DOWN],  // The cell below must be BLANK or DOWN
    [BLANK, LEFT]   // The cell to the left must be BLANK or LEFT
  ],
  // UP
  [
    [RIGHT, LEFT, DOWN],
    [LEFT, UP, DOWN],
    [BLANK, DOWN],
    [RIGHT, UP, DOWN]
  ],
  // RIGHT
  [
    [RIGHT, LEFT, DOWN],
    [LEFT, UP, DOWN],
    [RIGHT, LEFT, UP],
    [BLANK, LEFT]
  ],
  // DOWN
  [
    [BLANK, UP],
    [LEFT, UP, DOWN],
    [RIGHT, LEFT, UP],
    [RIGHT, UP, DOWN]
  ],
  // LEFT
  [
    [RIGHT, LEFT, DOWN],
    [BLANK, RIGHT],
    [RIGHT, LEFT, UP],
    [UP, DOWN, RIGHT]
  ]
];

// p5.js preload: loads the images for each tile
function preload() {
  tiles[BLANK] = loadImage("tiles\\blank.png");
  tiles[UP] = loadImage("tiles\\up.png");
  tiles[RIGHT] = loadImage("tiles\\right.png");
  tiles[DOWN] = loadImage("tiles\\down.png");
  tiles[LEFT] = loadImage("tiles\\left.png");
}

// p5.js setup: creates the canvas and initializes each grid cell
// with all possible tile states.
function setup() {
  createCanvas(800, 800);
  
  for (let i = 0; i < DIM; i++) {
    for (let j = 0; j < DIM; j++) {
      grid[i][j] = { options: [BLANK, UP, RIGHT, DOWN, LEFT] };
    }
  }
  
  // Randomly collapse one cell to start the algorithm
  const randX = round(random(0, DIM - 1));
  const randY = round(random(0, DIM - 1));
  grid[randX][randY].options = [random(grid[randX][randY].options)];
  collapsedCounter++;
}

// p5.js mousePressed: redraws the canvas when the mouse is clicked
function mousePressed() {
  redraw();
}

// Updates a cell's possible options by reducing them to the intersection
// of its current options and the valid options from a neighbor.
function updateGrid(x, y, validOptions) {
  const currentOptions = grid[x][y].options;
  grid[x][y].options = currentOptions.filter(option => validOptions.includes(option));
}

// Returns the number of collapsed cells (cells with only one option left)
function countCollapsed() {
  let count = 0;
  for (let i = 0; i < DIM; i++) {
    for (let j = 0; j < DIM; j++) {
      if (grid[i][j].options.length === 1) count++;
    }
  }
  return count;
}

// Propagates constraints from collapsed cells to their neighbors
// until no further changes occur.
function propagateConstraints() {
  let previousCount;
  do {
    previousCount = countCollapsed();
    for (let i = 0; i < DIM; i++) {
      for (let j = 0; j < DIM; j++) {
        if (grid[i][j].options.length === 1) {
          const state = grid[i][j].options[0];
          // Update the cell above, if it exists
          if (i > 0) updateGrid(i - 1, j, rules[state][0]);
          // Update the cell to the right, if it exists
          if (j < DIM - 1) updateGrid(i, j + 1, rules[state][1]);
          // Update the cell below, if it exists
          if (i < DIM - 1) updateGrid(i + 1, j, rules[state][2]);
          // Update the cell to the left, if it exists
          if (j > 0) updateGrid(i, j - 1, rules[state][3]);
        }
      }
    }
  } while (countCollapsed() !== previousCount);
}

// p5.js draw: renders the grid and applies the wave function collapse algorithm
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

  // Stop the algorithm when all cells are collapsed
  if (collapsedCounter === DIM * DIM) return;

  // Propagate constraints based on adjacency rules
  propagateConstraints();
  collapsedCounter = countCollapsed();

  // Identify cells with the lowest entropy (fewest options left, but >1)
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

  // Randomly collapse one cell among those with the lowest entropy
  if (lowestEntropyCells.length > 0) {
    const [cellX, cellY] = random(lowestEntropyCells);
    grid[cellX][cellY].options = [random(grid[cellX][cellY].options)];
    collapsedCounter++;
  }

  // Debug: print the number of collapsed cells
  console.log(collapsedCounter);
}
