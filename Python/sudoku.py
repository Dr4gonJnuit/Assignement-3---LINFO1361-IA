import random
import time
import math
import sys


def count_conflicts(board):
    conflicts = 0
    size = len(board)

    # Check conflicts in rows and columns
    for i in range(size):
        row_values = set()
        col_values = set()
        for j in range(size):
            if board[i][j] != 0 and board[i][j] in row_values:
                conflicts += 1
            if board[j][i] != 0 and board[j][i] in col_values:
                conflicts += 1
            row_values.add(board[i][j])
            col_values.add(board[j][i])

    # Check conflicts in subgrids
    subgrid_size = int(math.sqrt(size))
    for i in range(0, size, subgrid_size):
        for j in range(0, size, subgrid_size):
            subgrid_values = set()
            for x in range(i, i + subgrid_size):
                for y in range(j, j + subgrid_size):
                    if board[x][y] != 0 and board[x][y] in subgrid_values:
                        conflicts += 1
                    subgrid_values.add(board[x][y])

    return conflicts


def count_empty_tiles(board):
    return sum(1 for row in board for cell in row if cell == 0)


def objective_score(board):
    conflicts = count_conflicts(board)
    empty_tiles = count_empty_tiles(board)
    return conflicts + empty_tiles


def has_conflicts(board, row, col):
    digit = board[row][col]

    if board[row].count(digit) > 1:
        return True

    if [board[i][col] for i in range(len(board))].count(digit) > 1:
        return True

    # Check conflicts in the same subgrid
    subgrid_size = int(math.sqrt(len(board)))
    start_row = (row // subgrid_size) * subgrid_size
    start_col = (col // subgrid_size) * subgrid_size
    subgrid = [board[i][start_col:start_col + subgrid_size] for i in range(start_row, start_row + subgrid_size)]
    if sum(row.count(digit) for row in subgrid) > 1:
        return True

    return False


def lock_check(board, empty_positions):
    """Check if the board is locked and we can't add any new digit

    Args:
        board (List): The board to check
        empy_positions (List): The empty positions in the board

    Returns:
        bool : True if the board is locked, False otherwise
    """
    initial_board = [row[:] for row in board]
    
    for positions in empty_positions:
        checker_board = generate_neighbor(board, position=positions, verify_lock=False)
        
        if checker_board != initial_board:
            return False
    
    return True


def generate_neighbor(board, initial_empty_positions=None, position=None, verify_lock=True, debug=False):
    neighbor = [row[:] for row in board]
    size = len(board)

    if position is None:
        empty_positions = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]
        try:
            row, col = random.choice(empty_positions)
        except IndexError:
            return board
    else:
        row, col = position

    digits = list(range(1, 10))
    random.shuffle(digits)

    for digit in digits:
        neighbor[row][col] = digit

        if not has_conflicts(neighbor, row, col):
            return neighbor
    
    if verify_lock and lock_check(board, empty_positions=empty_positions):
        # TODO: remove numbers present in the board with the positions in the
        # ‘initial_empty_positions’ until we can add a different one
        old_empty_positions = initial_empty_positions.copy()
        random.shuffle(old_empty_positions)
        
        old_empty_positions_and_values = {pos: [] for pos in old_empty_positions}
        
        while old_empty_positions:
            if debug: print("Empty position :\n", old_empty_positions) # Debug
            i, j = old_empty_positions.pop()
            
            old_empty_positions_and_values[(i, j)].append(neighbor[i][j])
            
            digits = list(range(1, 10))
            random.shuffle(digits)
            
            for digit in digits:
                if digit in old_empty_positions_and_values[(i, j)]:
                    continue
                neighbor[i][j] = digit

                if not has_conflicts(neighbor, i, j):
                    return neighbor
    
    return board


def initial_position_empty(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == 0]


def simulated_annealing_solver(initial_board, debug=False):
    """
    Simulated annealing Sudoku solver.
    """
    current_solution = [row[:] for row in initial_board]
    best_solution = current_solution
    
    initial_empty_positions = initial_position_empty(initial_board)

    current_score = objective_score(current_solution)
    best_score = current_score

    temperature = 1.0
    cooling_rate = 0.9999  # Adjust this parameter to control the cooling rate

    while temperature > 0.0001:
        try:
            # TODO: Generate a neighbor (Don't forget to skip non-zeros tiles in the initial board ! It will be verified on Inginious.)
            neighbor = generate_neighbor(current_solution, initial_empty_positions, debug=debug)

            # Evaluate the neighbor
            neighbor_score = objective_score(neighbor)

            # Calculate acceptance probability
            delta = float(current_score - neighbor_score)

            # Accept the neighbor with a probability based on the acceptance probability
            if neighbor_score < current_score or (
                    neighbor_score > 0 and math.exp((delta / temperature)) > random.random()):
                current_solution = neighbor
                current_score = neighbor_score

                if current_score == 0:
                    return current_solution, current_score

                if current_score < best_score:
                    best_solution = current_solution
                    best_score = current_score

            # Cool down the temperature
            temperature *= cooling_rate
        except KeyboardInterrupt:
            print("Break asked")
            break

    return best_solution, best_score
 
def print_board(board):

    """Print the Sudoku board."""

    for row in board:
        print("".join(map(str, row)))

 

def read_sudoku_from_file(file_path):
    """Read Sudoku puzzle from a text file."""
    
    with open(file_path, 'r') as file:
        sudoku = [[int(num) for num in line.strip()] for line in file]

    return sudoku
 

if __name__ == "__main__":

    # Reading Sudoku from file
    initial_board = read_sudoku_from_file(sys.argv[1])
    """
    print_board(initial_board)
    print("\n\n")
    print_board(generate_neighbor(initial_board))
    """
        
    # Solving Sudoku using simulated annealing
    start_timer = time.perf_counter()

    solved_board, current_score = simulated_annealing_solver(initial_board)

    end_timer = time.perf_counter()

    print_board(solved_board)
    print("\nValue(C):", current_score)

    # print("\nTime taken:", end_timer - start_timer, "seconds")