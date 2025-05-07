BOARD_SIZE = 3

# Function for checking if a state is terminal
def check_state(state):
    # Check per row 
    for row in state:
        if all(tile != ' ' and tile == row[0] for tile in row): return row[0]
    
    # Check per column
    for column in range(BOARD_SIZE):
        col = []
        for row in range(BOARD_SIZE):
            col.append(state[row][column])
        if all(tile != ' ' and tile == col[0] for tile in col): return col[0]
    
    # Check diagonal
    diagonal = [state[i][i] for i in range(BOARD_SIZE)]
    if all(tile != ' ' and tile == diagonal[0] for tile in diagonal): return diagonal[0]

    # Check reverse diagonal
    diagonal = [state[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)]
    if all(tile != ' ' and tile == diagonal[0] for tile in diagonal): return diagonal[0]

# Check if game is already a draw
def check_draw(state): 
    for row in state:
        if ' ' in row: return False
    return True

def value(state, ai, user):
    if check_state(state) == user: return -1  # Player wins
    elif check_state(state) == ai: return 1  # Computer wins
    else: return 0  # Draw

# Maximization/Minimization
def min_max(depth, is_max, state, alpha, beta, ai, user):
    terminal = value(state, ai, user)

    if terminal == 1 or terminal == -1: return terminal
    if check_draw(state): return 0

    # MAXIMIZATION
    if is_max:
        best_score = float('-inf')
        # Results
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if state[row][column] == ' ':
                    state[row][column] = ai
                    terminal = min_max(depth + 1, False, state, alpha, beta, ai, user)
                    state[row][column] = ' '
                    best_score = max(terminal, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  # Beta cutoff
        return best_score
    # MINIMIZATION
    else:
        best_score = float('inf')
        # Results
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if state[row][column] == ' ':
                    state[row][column] = user
                    terminal = min_max(depth + 1, True, state, alpha, beta, ai, user)
                    state[row][column] = ' '
                    best_score = min(terminal, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  # Alpha cutoff
        return best_score

# Reference: https://uyennguyen16900.medium.com/minimax-with-alpha-beta-pruning-7e2091ae7d95