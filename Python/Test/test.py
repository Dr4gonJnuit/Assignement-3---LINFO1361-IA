import sys
sys.path.append("./")
import sudoku

if __name__ == "__main__":
    # Reading Sudoku from file
    initial_board = sudoku.read_sudoku_from_file(sys.argv[1])
    
    print("Initial board:\n")
    sudoku.print_board(initial_board)
    
    locked_positions = sudoku.initial_position_information(initial_board) # Dict with the locked positions and the initial empty positions
    
    print("\nLocked positions:\n")
    print(locked_positions)
    
    forbiden_numbers_positions_dict = sudoku.forbiden_numbers_positions(initial_board, locked_positions)
    
    print("\nForbiden numbers positions:\n")
    print(forbiden_numbers_positions_dict)
    
    for pos in forbiden_numbers_positions_dict:
        if forbiden_numbers_positions_dict[pos][0] == 8:
            print(forbiden_numbers_positions_dict[pos][1])
            print(sudoku.missing_numbers(forbiden_numbers_positions_dict[pos][1]))
        
    # assert sudoku.objective_score(initial_board) == 43
    
    # solved_board, current_score = sudoku.simulated_annealing_solver(initial_board, debug=True)
    
    #sudoku.print_board(solved_board)
    #print("\nValue(C):", current_score)