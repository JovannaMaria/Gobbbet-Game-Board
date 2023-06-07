# Define the empty and blocked spots on the board
EMPTY_SPOT = '-'
BLOCKED_SPOT = 'X'

class GobbletBoard:
    def __init__(self):
        # Initialize the empty board
        self.board = [[EMPTY_SPOT] * 3 for _ in range(3)]
        
        # Block the middle spot
        self.board[1][1] = BLOCKED_SPOT
    
    def print_board(self):
        # Print the current state of the board
        for row in self.board:
            print(' '.join(row))
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        # Check if the move is within the bounds of the board
        if not (0 <= from_row < 3 and 0 <= from_col < 3 and
                0 <= to_row < 3 and 0 <= to_col < 3):
            return False
        
        # Check if the source and destination spots are different
        if from_row == to_row and from_col == to_col:
            return False
        
        # Check if the source spot is not empty
        if self.board[from_row][from_col] == EMPTY_SPOT:
            return False
        
        # Check if the destination spot is empty or has a smaller piece on top
        if self.board[to_row][to_col] == EMPTY_SPOT or self.board[from_row][from_col] < self.board[to_row][to_col]:
            return True
        
        return False
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        # Move the piece from the source spot to the destination spot
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = EMPTY_SPOT

# Main game loop
def play_game():
    board = GobbletBoard()
    current_player = 'Player 1'

    while True:
        # Print the current state of the board
        print(f"{current_player}'s turn:")
        board.print_board()
        
        # Ask the player for a move
        from_row, from_col, to_row, to_col = map(int, input("Enter your move (from_row, from_col, to_row, to_col): ").split())
        
        # Check if the move is valid
        if board.is_valid_move(from_row, from_col, to_row, to_col):
            # Move the piece on the board
            board.move_piece(from_row, from_col, to_row, to_col)
            
            # Check if the current player has won
            if check_win_condition(board, current_player):
                print(f"{current_player} wins!")
                break
            
            # Switch to the other player
            current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'
        else:
            print('Invalid move. Try again.')

# Function to check win condition
def check_win_condition(board, player):
    # Check rows
    for row in board.board:
        if row[0] == row[1] == row[2] == player:
            return True
    
    # Check columns
    for col in range(3):
        if board.board[0][col] == board.board[1][col] == board.board[2][col] == player:
            return True
    
    # Check diagonals
    if board.board[0][0] == board.board[1][1] == board.board[2][2] == player:
        return True
    if board.board[0][2] == board.board[1][1] == board.board[2][0] == player:
        return True
    
    return False

# Start the game
play_game()
