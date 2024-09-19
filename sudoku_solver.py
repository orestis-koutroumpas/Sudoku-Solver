import pulp as plp
from math import sqrt

# Converts letters A, B, C, ... to numbers 10, 11, 12, etc. (for 16x16 puzzles)
def convert_to_numeric(value):
    if isinstance(value, str) and value.isalpha():
        return ord(value.upper()) - 55  # Convert 'A' -> 10, 'B' -> 11, etc.
    return int(value)  # If it's already a number or 0, return as is

# Checks the validity of the Sudoku problem
def validate_sudoku_input(input_sudoku):
    n_rows = len(input_sudoku)
    n_cols = len(input_sudoku[0])

    # Check if all rows have the same length (rectangular check)
    for row_index, row in enumerate(input_sudoku):
        if len(row) != n_cols:
            raise ValueError(f"Row {row_index + 1} has a different length ({len(row)} columns) "
                             f"than the first row ({n_cols} columns). The grid is not rectangular.")

    # Check if the matrix is square (n_rows == n_cols)
    if n_rows != n_cols:
        raise ValueError(f"Sudoku grid is not square. Found {n_rows} rows and {n_cols} columns.")

    # Check if the number of rows/columns (n) is a perfect square (i.e., n = m^2)
    m = int(sqrt(n_rows))
    if m * m != n_rows:
        raise ValueError(f"Sudoku dimension {n_rows}x{n_cols} is invalid. "
                         f"The number of rows/columns must be a perfect square (e.g., 4x4, 9x9, 16x16).")

    # Check if all values are valid (between 1 and n or 0 for empty cells)
    for row in range(n_rows):
        for col in range(n_cols):
            value = input_sudoku[row][col]
            numeric_value = convert_to_numeric(value)
            if not (0 <= numeric_value <= n_rows):
                raise ValueError(f"Invalid value '{value}' at position ({row + 1}, {col + 1}). "
                                 f"Values must be between 1 and {n_rows}, or 0 for empty cells.")
    return n_rows, n_cols, m

# Sets up the Sudoku problem using PuLP
def setup_problem(n_rows, n_cols):
    prob = plp.LpProblem("Sudoku_Solver")
    rows = range(n_rows)
    cols = range(n_cols)
    values = range(1, 1 + n_rows)

    # Decision Variables: grid_value[row][col][value] is binary (either 0 or 1)
    grid_vars = plp.LpVariable.dicts("grid_value", (rows, cols, values), cat='Binary')

    # Objective function (we minimize zero as we are only concerned with satisfying constraints)
    prob.setObjective(plp.lpSum(0))

    return prob, rows, cols, values, grid_vars

# Adds the basic Sudoku constraints to the problem
def create_sudoku_constraints(prob, grid_vars, rows, cols, values, n, m, input_sudoku):
    # Each column contains exactly one integer number 1 to n:
    for col in cols:
        for value in values:
            prob.addConstraint(plp.lpSum([grid_vars[row][col][value] for row in rows]) == 1,
                               name=f"col_{col}_value_{value}")

    # Each row contains exactly one integer number 1 to n:
    for row in rows:
        for value in values:
            prob.addConstraint(plp.lpSum([grid_vars[row][col][value] for col in cols]) == 1,
                               name=f"row_{row}_value_{value}")

    # Each cell contains exactly one integer number 1 to n:
    for row in rows:
        for col in cols:
            prob.addConstraint(plp.lpSum([grid_vars[row][col][value] for value in values]) == 1,
                               name=f"cell_{row}_{col}")

    # Each sub-grid contains exactly one integer number 1 to n:
    for grid_row in range(m):
        for grid_col in range(m):
            for value in values:
                prob.addConstraint(plp.lpSum([grid_vars[grid_row*m+row][grid_col*m+col][value]
                                              for row in range(m)
                                              for col in range(m)]) == 1,
                                   name=f"subgrid_{grid_row}_{grid_col}_value_{value}")

    # Prefill known values (clues)
    for row in rows:
        for col in cols:
            if input_sudoku[row][col] != 0:
                value = convert_to_numeric(input_sudoku[row][col])
                prob.addConstraint(grid_vars[row][col][value] == 1,
                                   name=f"prefilled_{row}_{col}")

# Adds diagonal Sudoku constraints if needed (for Sudoku X)
def add_diagonal_sudoku_constraints(prob, grid_vars, rows, cols, values):
    # Top-left to bottom-right diagonal
    for value in values:
        prob.addConstraint(plp.lpSum([grid_vars[i][i][value] for i in rows]) == 1,
                           name=f"diagonal1_value_{value}")
    # Top-right to bottom-left diagonal
    for value in values:
        prob.addConstraint(plp.lpSum([grid_vars[i][len(rows)-i-1][value] for i in rows]) == 1,
                           name=f"diagonal2_value_{value}")

# Extracts the solution from the PuLP variables
def extract_solution(grid_vars, rows, cols, values):
    solution = [[0 for _ in cols] for _ in rows]
    for row in rows:
        for col in cols:
            for value in values:
                if plp.value(grid_vars[row][col][value]):
                    # Convert numbers > 9 to letters
                    solution[row][col] = chr(55 + value) if value > 9 else value  
    return solution

# Solver for Sudoku, including optional diagonal constraint
def solver(input_sudoku, diagonal=False):
    try:
        # Validate the input Sudoku
        n_rows, n_cols, m = validate_sudoku_input(input_sudoku)

        # Setup the PuLP problem
        prob, rows, cols, values, grid_vars = setup_problem(n_rows, n_cols)

        # Add constraints for a standard Sudoku
        create_sudoku_constraints(prob, grid_vars, rows, cols, values, n_rows, m, input_sudoku)

        # Add diagonal constraints if required
        if diagonal:
            add_diagonal_sudoku_constraints(prob, grid_vars, rows, cols, values)

        # Solve the problem
        prob.solve()

        # Check solution status
        solution_status = plp.LpStatus[prob.status]
        if solution_status == 'Optimal':
            solution = extract_solution(grid_vars, rows, cols, values)
        else:
            raise Exception(f"No optimal solution found. Status: {solution_status}")

    except Exception as e:
        print(f"Error: {e}")
        solution = None

    return solution

# Reads Sudoku puzzles from an input file, validates them, and returns them
def read_sudokus_from_file(filename):
    sudokus = []
    diagonal_flags = []

    try:
        with open(filename, 'r') as f:
            num_sudokus = int(f.readline().strip())
            for sudoku_index in range(num_sudokus):
                try:
                    dim, diagonal_flag = map(int, f.readline().strip().split())
                    diagonal = diagonal_flag == 1

                    # Validate if the dimension is a perfect square
                    m = int(sqrt(dim))
                    if m * m != dim:
                        raise ValueError(f"Sudoku {sudoku_index + 1}: Invalid dimension {dim}. Must be a perfect square.")

                    sudoku = []
                    for row_index in range(dim):
                        row = f.readline().strip().split()

                        if len(row) != dim:
                            raise ValueError(f"Sudoku {sudoku_index + 1}: Row {row_index + 1} has invalid length.")

                        numeric_row = [convert_to_numeric(value) for value in row]
                        for col_index, value in enumerate(numeric_row):
                            if not (0 <= value <= dim):
                                raise ValueError(f"Sudoku {sudoku_index + 1}: Invalid value '{value}' at position ({row_index + 1}, {col_index + 1}).")

                        sudoku.append(numeric_row)

                    sudokus.append(sudoku)
                    diagonal_flags.append(diagonal)

                    f.readline()

                except ValueError as e:
                    print(f"Error reading Sudoku {sudoku_index + 1}: {e}")
                    continue

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except ValueError as e:
        print(f"Error processing file '{filename}': {e}")

    return sudokus, diagonal_flags

# Writes the Sudoku solutions to an output file
def write_sudoku_solutions_to_file(solutions, filename):
    with open(filename, 'w') as file:
        for i, solution in enumerate(solutions):
            if solution:
                file.write(f"Solution for Sudoku {i + 1}:\n")
                for row in solution:
                    file.write(' '.join(map(str, row)) + '\n')
                file.write('\n')
            else:
                file.write(f"Solution for Sudoku {i + 1}: No solution found.\n\n")

# Main function to read Sudoku puzzles, solve them, and write the solutions
def main(input_file, output_file):
    sudokus, diagonal_flags = read_sudokus_from_file(input_file)
    solutions = []

    for sudoku, diagonal in zip(sudokus, diagonal_flags):
        solution = solver(sudoku, diagonal)
        solutions.append(solution)

    write_sudoku_solutions_to_file(solutions, output_file)

if __name__ == "__main__":
    input_filename = "input_sudokus.txt"
    output_filename = "output_solutions.txt"
    main(input_filename, output_filename)
