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
2
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

16 0
0 0 0 A 0 F 0 0 0 0 E 0 6 0 0 0
0 0 C 0 1 6 2 0 0 3 7 8 0 5 0 0
0 3 0 0 0 0 0 5 9 0 0 0 0 0 F 0
0 6 B E 9 0 0 0 0 0 0 F 1 D 8 0
0 0 5 F 0 2 0 9 4 0 A 0 E B 0 0
0 0 E 7 4 0 1 G 6 8 0 9 F 2 0 0
0 0 D 0 0 0 0 B E 0 0 0 0 9 0 0
0 0 0 0 6 C 0 0 0 0 D 5 0 0 0 0
F 8 A 0 7 0 D 0 0 9 0 E 0 6 1 C
0 7 0 G F E 0 0 0 0 6 C 2 0 B 0
0 4 0 0 0 1 9 C 7 F 8 0 0 0 5 0
0 2 0 3 A B 0 8 D 0 4 1 G 0 7 0
0 G 7 0 2 4 3 0 0 C 9 B 0 1 E 0
0 0 0 9 0 0 0 0 0 0 0 0 5 0 0 0
1 D 3 0 0 5 7 0 0 E G 0 0 F 2 4
B 0 2 0 0 9 0 6 1 0 F 0 0 3 0 7
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

#### Example Output File
```plaintext
Solution for Sudoku 1:
6 5 9 2 4 7 3 8 1
4 1 7 5 3 8 2 6 9
8 3 2 9 6 1 5 7 4
7 6 3 4 8 2 9 1 5
5 9 4 3 1 6 7 2 8
2 8 1 7 9 5 4 3 6
1 2 5 6 7 9 8 4 3
9 4 8 1 2 3 6 5 7
3 7 6 8 5 4 1 9 2

Solution for Sudoku 2:
5 9 8 A 3 F 4 D B 1 E G 6 7 C 2
4 F C D 1 6 2 E A 3 7 8 B 5 9 G
7 3 G 1 C 8 B 5 9 6 2 D A 4 F E
2 6 B E 9 G A 7 C 4 5 F 1 D 8 3
6 C 5 F D 2 8 9 4 G A 7 E B 3 1
3 B E 7 4 A 1 G 6 8 C 9 F 2 D 5
G A D 8 5 7 F B E 2 1 3 C 9 4 6
9 1 4 2 6 C E 3 F B D 5 7 G A 8
F 8 A 5 7 3 D 2 G 9 B E 4 6 1 C
D 7 1 G F E 5 4 3 A 6 C 2 8 B 9
E 4 6 B G 1 9 C 7 F 8 2 3 A 5 D
C 2 9 3 A B 6 8 D 5 4 1 G E 7 F
8 G 7 6 2 4 3 F 5 C 9 B D 1 E A
A E F 9 8 D G 1 2 7 3 4 5 C 6 B
1 D 3 C B 5 7 A 8 E G 6 9 F 2 4
B 5 2 4 E 9 C 6 1 D F A 8 3 G 7
```
