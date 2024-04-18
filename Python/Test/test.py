import sys
sys.path.append("./")
import sudoku

if __name__ == "__main__":
    # Reading Sudoku from file
    initial_board = sudoku.read_sudoku_from_file(sys.argv[1])
    
    print("Initial board:\n")
    sudoku.print_board(initial_board)
    
    assert sudoku.objective_score(initial_board) == 43
    
    solved_board, current_score = sudoku.simulated_annealing_solver(initial_board, debug=True)
    
    sudoku.print_board(solved_board)
    print("\nValue(C):", current_score)