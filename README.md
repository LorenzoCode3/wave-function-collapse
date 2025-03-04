# Wave Function Collapse

## Description

This repository contains implementations of the wave function collapse algorithm in two languages: JavaScript (using p5.js) and Python. The project explores procedural pattern generation using the algorithm, featuring both a standard implementation and a version enhanced with backtracking (in Python).

## Features

- **p5js Folder**:  
    Contains two implementations:
  - `WaveFunctionCollapse.js`: Implements the standard wave function collapse algorithm using p5.js.
  - `WaveFunctionCollapseGeneralized.js`: Extends the standard model with a data structure to store tile information, allowing for an expandable tileset.

- **python Folder**:  
  Contains two implementations:
  - `base_model`: Uses the standard approach to perform wave function collapse.
  - `backtracking_model`: Uses a backtracking approach to handle conflicts during the collapse process.

## Getting Started

### Running the p5.js Versions

1. Open the [p5.js web editor](https://editor.p5js.org/).
2. Load the necessary tiles into the editor.
3. Copy and paste the code from `WaveFunctionCollapse.js` or `WaveFunctionCollapseGeneralized.js` into the editor.
4. Click the play button to run the code.

### Running the Python Versions

1. Ensure you have **Python 3.x** installed.
2. Install the required library:

    ```bash
    pip install pygame
    ```

3. Open a terminal and navigate to the `python` folder.
4. Choose either the `base_model` or `backtracking_model` folder:
    - For the base model, execute:

      ```bash
      python WaveFunctionCollapse.py
      ```

    - For the backtracking model, execute:

      ```bash
      python main.py
      ```

## License

This project is open source and available under the [MIT License](LICENSE).
