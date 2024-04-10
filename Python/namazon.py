from search import *
import time

#################
# Problem class #
#################

class NAmazonsProblem(Problem):
    """The problem of placing N amazons on an NxN board with none attacking
    each other. A state is represented as an N-element array, where
    a value of r in the c-th entry means there is an empress at column c,
    row r, and a value of -1 means that the c-th column has not been
    filled in yet. We fill in columns left to right.
    """
    def __init__(self, N):
        super().__init__(tuple([-1] * N))
        self.N = N

    def actions(self, state):
        if state[-1] != -1:
            return []  # All columns filled; no successors
        else:
            col = state.index(-1)
            return [row for row in range(self.N)
                    if not self.conflicted(state, row, col)]

    def result(self, state, row):
        col = state.index(-1)
        new = list(state[:])
        new[col] = row
        return tuple(new)

    def goal_test(self, state):
        if state[-1] == -1:
            return False
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

    def h(self, node):
        num_conflicts = 0
        for (r1, c1) in enumerate(node.state):
            for (r2, c2) in enumerate(node.state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)

        return num_conflicts

    def conflicted(self, state, row, col):
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        return (row1 == row2 or
                col1 == col2 or
                row1 - col1 == row2 - col2 or
                row1 + col1 == row2 + col2 or
                (row1 + 3 == row2 and col1 - 2 == col2) or
                (row1 - 3 == row2 and col1 - 2 == col2) or
                (row1 + 2 == row2 and col1 - 3 == col2) or
                (row1 - 2 == row2 and col1 - 3 == col2) or
                (row1 + 4 == row2 and col1 - 1 == col2) or
                (row1 - 4 == row2 and col1 - 1 == col2) or
                (row1 + 1 == row2 and col1 - 4 == col2) or
                (row1 - 1 == row2 and col1 - 4 == col2))

#####################
# Launch the search #
#####################

problem = NAmazonsProblem(int(sys.argv[1]))

start_timer = time.perf_counter()

node = astar_search(problem) # TODO: Launch the search

end_timer = time.perf_counter()


# example of print
path = node.path()

print('Number of moves: ', str(node.depth))

for n in path:
    state = n.state
    for row in range(len(state)):
        row_str = ''
        for col in range(len(state)):
            if state[col] == row:
                row_str += 'A'
            else:
                row_str += '#'
        print(row_str)
    print()

#print("Time: ", end_timer - start_timer)
