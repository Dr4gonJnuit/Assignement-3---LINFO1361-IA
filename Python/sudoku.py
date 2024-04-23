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


def lock_check(board, locked_position):
    """Check if the board is locked and we can't add any new digit

    Args:
        board (List): The board to check
        empy_positions (List): The empty positions in the board

    Returns:
        bool : True if the board is locked, False otherwise
    """
    initial_board = [row[:] for row in board]
    
    for positions in locked_position:
        checker_board = generate_neighbor(board, position=positions, verify_lock=False)
        
        if checker_board != initial_board:
            return False
    
    return True


def missing_numbers(list, size=10):
    """Generate a list of missing numbers in the list

    Args:
        list (List): A list of numbers
        size (int, optional): The size of the list to generate. Defaults to 10.

    Returns:
        List : A list of missing numbers
    """
    return [x for x in range(1, size) if x not in list]
    

def generate_neighbor(board, locked_positions=None, forbiden_value=None, debug=False):
    neighbor = [row[:] for row in board]
    size = len(board)

    # Lock the position if it's not in the locked positions
    for pos_value in forbiden_value:
        if forbiden_value[pos_value][0] == size - 1 and not locked_positions[pos_value]:
            #locked_positions[pos_value] = True
            row, col = pos_value
            neighbor[row][col] = missing_numbers(forbiden_value[pos_value][1])[0]
            
            return neighbor, True
    
    # Generate a number for the locked position
    # that only him can have
    for pos_locked in locked_positions:
        if not locked_positions[pos_locked]:
            for possible_value in missing_numbers(forbiden_value[pos_locked][1]):
                only_value = True
                
                for other_pos in locked_positions:
                    if (not locked_positions[other_pos]) and (other_pos != pos_locked) and (possible_value not in forbiden_value[other_pos][1]):
                        only_value = False
                        break
                if only_value:
                    row, col = pos_locked
                    neighbor[row][col] = possible_value
                    
                    return neighbor, True

    
    # Generate a random POSSIBLE position 
    # That means we didn't find a position with 8 forbidden numbers
    for pos_locked in locked_positions:
        if not locked_positions[pos_locked]:
            row, col = pos_locked
            neighbor[row][col] = random.choice(missing_numbers(forbiden_value[pos_locked][1]))
    
    return neighbor, False


def initial_position_information(board):
    return {(i, j): True if board[i][j] != 0 else False for i in range(len(board)) for j in range(len(board))}


def forbiden_numbers_positions(board, locked_position, unique_position=None):
    """Generate a dictionary with the forbidden numbers for each empty position

    Args:
        board (List): The board to check
    
    Returns:
        Dict : A dictionary with the forbidden numbers for each empty position and the number of forbidden numbers
    """
    size = len(board)
    position = {pos: [0,[]] for pos in locked_position if locked_position[pos] == False}
    
    for pos in position:
        if locked_position[pos]:
            continue
        
        i, j = pos
        
        # Check the row
        position[pos][1].extend([board[i][k] for k in range(size) if (board[i][k] != 0 and board[k][j] not in position[pos][1])])
        
        # Check the column
        position[pos][1].extend([board[k][j] for k in range(size) if (board[k][j] != 0 and board[k][j] not in position[pos][1])])
        
        # Check the subgrid
        subgrid_size = int(math.sqrt(size))
        start_row = (i // subgrid_size) * subgrid_size
        start_col = (j // subgrid_size) * subgrid_size
        subgrid = [board[k][start_col:start_col + subgrid_size] for k in range(start_row, start_row + subgrid_size)]
        position[pos][1].extend([cell for row in subgrid for cell in row if (cell != 0 and cell not in position[pos][1])])
        
        position[pos][1].sort()
        
        position[pos][0] = len(position[pos][1])        
    
    return position


def simulated_annealing_solver(initial_board, debug=False):
    """
    Simulated annealing Sudoku solver.
    """
    current_solution = [row[:] for row in initial_board]
    best_solution = current_solution
        
    current_score = objective_score(current_solution)
    best_score = current_score

    temperature = 1.0
    cooling_rate = 0.9999  # Adjust this parameter to control the cooling rate
    
    locked = True
    
    while temperature > 0.0001:
        try:
            # TODO: Generate a neighbor (Don't forget to skip non-zeros tiles in the initial board ! It will be verified on Inginious.)
            
            ##############################
            
            #   / \    These functions need to be modified so they             / \
            #  / | \   wont generate a locked position after we begin         / | \
            # /  °  \  to attributes random numbers to the empty positions.  /  °  \
            
            if locked:
                locked_positions = initial_position_information(best_solution) # Dict with the locked positions and the initial empty positions
                forbiden_numbers_positions_dict = forbiden_numbers_positions(best_solution, locked_positions)
            
            ##############################
            
            neighbor, locked = generate_neighbor(best_solution, locked_positions, forbiden_numbers_positions_dict, debug=debug)
            
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