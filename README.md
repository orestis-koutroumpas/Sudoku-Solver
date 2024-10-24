# Sudoku Solver using Linear Programming (Python and PuLP)

This is a Python program that solves Sudoku puzzles of various sizes (e.g. 9×9, 16×16, etc) using linear programming techniques via the PuLP library. The solver can handle standard Sudoku puzzles as well as the Sudoku X variant (which includes diagonal constraints).

## Features

- Solves standard Sudoku puzzles where the grid size is n×n,  with n being a perfect square (e.g., 4, 9, 16).
- Supports Sudoku X puzzles with diagonal constraints.
- Handles puzzles with numbers and letters for larger grids (greater than 9×9).
- Validates puzzle inputs for correctness before attempting to solve.
  
## Requirements

- **Python 3.x**
- **PuLP Library**

## Installation

1. **Install Python 3**: Make sure Python 3 is installed on your system. You can download it [here](https://www.python.org/downloads/).
2. **Install PuLP**: You can install the required PuLP library via `pip`:

    ```bash
    pip install pulp
    ```

## Usage

### Prepare the Input File

The program expects an input file (`input_sudokus.txt` by default) containing Sudoku puzzles in a specific format:

1. **First line**: Number of Sudoku puzzles in the file.
2. **For each puzzle**:
    - **Puzzle Header Line**: Two integers:
      - The size of the puzzle grid (e.g., `9` for a 9×9 puzzle).
      - A flag indicating whether it's a standard Sudoku (`0`) or Sudoku X (`1`).
    - **Puzzle Grid**: The puzzle grid with one row per line. Cells are separated by spaces. Use `0` for empty cells. For grids larger than 9×9, letters (A, B, C, etc.) represent numbers greater than 9.
    - **Empty Line**: A blank line separates different puzzles.

#### Example Input File
```plaintext
1
9 0
0 0 0 2 4 0 0 0 1
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 5 7 4
0 0 3 0 8 0 0 1 0
5 0 4 0 0 0 0 0 8
0 0 0 7 0 0 0 0 0
0 0 0 6 0 9 0 0 0
0 0 8 0 0 0 6 0 0 
0 7 0 0 0 4 0 9 2
```

### Running the Program

1. Clone or download the project to your local machine.
2. Ensure that the `input_sudokus.txt` file is in the same directory as the script.
3. Run the program using the following command:

```bash
python sudoku_solver.py
```
## Output

The solutions will be written to an output file (output_solutions.txt by default). If no solution is found for a puzzle, a message will indicate that.
