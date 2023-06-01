from collections import deque

# Define the empty and blocked spots on the board
EMPTY_SPOT = '-'
BLOCKED_SPOT = 'X'
# create dictionary
d={'A':3,'B':2,'C':1,'X':3,'Y':2,'Z':1}
x=list('ABC')
y=list('XYZ')
# Create the stacks
s1 = deque(['C','B','A'])
s2 = deque(['C','B','A'])
s3 = deque(['Z','Y','X'])
s4 = deque(['Z','Y','X'])
px=[s1,s2]
py=[s3,s4]
class GobbletBoard:
    def __init__(self):
        # Initialize the empty board

        self.board = [[deque([EMPTY_SPOT])] * 3 for _ in range(3)]
        
        # Block the middle spot
        #self.board[1][1] = BLOCKED_SPOT
    
    def print_board(self):
        # Print the current state of the board
        for row in self.board:
            x=''
            for st in row:
                x=x +' '+ st[-1]
            print(x)
    
    def is_valid_move(self, from_row, from_col, to_row, to_col,curr):
        # Check if the move is within the bounds of the board
        if not (0 <= from_row < 5 and 0 <= from_col < 3 and
                0 <= to_row < 3 and 0 <= to_col < 3) :
            return False
        
        # Check if the source and destination spots are different
        if from_row == to_row and from_col == to_col:
            return False
        
        
        # Check if new piece is moved
        if (curr=='Player 1' and 4==from_row and 0<= from_col <2):
            x=px[from_col][0]
            if self.board[to_row][to_col][-1] == EMPTY_SPOT:
                print(self.board[to_row][to_col])
                self.board[to_row][to_col].append(px[from_col].pop())
            elif d[x] > d[self.board[to_row][to_col][-1]]:
                self.board[to_row][to_col].append(px[from_col].pop()) 
            return True
        elif (curr=='Player 2' and 5==from_row and 0<= from_col <2):
            y=py[from_col][0]
            if self.board[to_row][to_col][-1] == EMPTY_SPOT:
                self.board[to_row][to_col].pop()
                self.board[to_row][to_col].append(py[from_col].pop())
            if d[y] > d[self.board[to_row][to_col][-1]]:
                self.board[to_row][to_col].append(py[from_col].pop())
            return True 
        
        if not (0 <= from_row < 3 and 0 <= from_col < 3 and
                0 <= to_row < 3 and 0 <= to_col < 3) :
            return False
        # Check if the source spot is not empty
        if self.board[from_row][from_col][-1] == EMPTY_SPOT:
            return False
        # Check if the destination spot is empty or has a smaller piece on top
        if self.board[to_row][to_col][-1] == EMPTY_SPOT:
            self.board[to_row][to_col].pop()
            self.board[to_row][to_col].append(self.board[from_row][from_col].pop())  
            if len(self.board[from_row][from_col])==0:
                self.board[from_row][from_col].append(EMPTY_SPOT)
            return True
        
        elif d[self.board[from_row][from_col][-1]] > d[self.board[to_row][to_col][-1]]:
            self.board[to_row][to_col].append(self.board[from_row][from_col].pop())
            if len(self.board[from_row][from_col])==0:
                self.board[from_row][from_col].append(EMPTY_SPOT)
            return True
        
        return False
    
    '''def move_piece_new(self, from_row, from_col, to_row, to_col,curr):
        # Move the piece from the source spot to the destination spot
        if (curr=='Player 1' and 4==from_row and 0<= from_col <2):
            x=px[from_col][0]
            if self.board[to_row][to_col] == EMPTY_SPOT or x > self.board[to_row][to_col]:
                self.board[to_row][to_col]= px[from_col].pop()
                self.board[from_row][from_col] = EMPTY_SPOT
                return True
        elif (curr=='Player 2' and 5==from_row and 0<= from_col <2):
            y=py[from_col][0]
            if self.board[to_row][to_col] == EMPTY_SPOT or y > self.board[to_row][to_col]:
                self.board[to_row][to_col]= py[from_col].pop()
                self.board[from_row][from_col] = EMPTY_SPOT
                return True 
        else:
            self.board[to_row][to_col] = self.board[from_row][from_col]
            self.board[from_row][from_col] = EMPTY_SPOT
            return True
        
        return False'''
    
    '''def move_piece(self, from_row, from_col, to_row, to_col,curr):
        self.board[to_row][to_col].append(self.board[from_row][from_col].pop())  
        if len(self.board[from_row][from_col])==0:
            self.board[from_row][from_col].append(EMPTY_SPOT) 
    '''

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
        if not(board.is_valid_move(from_row, from_col, to_row, to_col,current_player)):
            print('Invalid move. Try again.')
        else:
            board.print_board()
            # Check if the current player has won
            t,winner= check_win_condition(board)
            if t:
                print(f"{winner} wins!")
                break
            
            # Switch to the other player
            current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'
            
            
        '''if board.is_valid_move(from_row, from_col, to_row, to_col,current_player):
            # Move the piece on the board
            if not(board.move_piece(from_row, from_col, to_row, to_col,current_player)):
                print('Invalid move. Try again.')
            
            # Check if the current player has won
            if check_win_condition(board, current_player):
                print(f"{current_player} wins!")
                break
            
            # Switch to the other player
            current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'
        else:
            print('Invalid move. Try again.')'''

# Function to check win condition
def check_win_condition(board):
    # Check rows
    for row in board.board:
        if row[0][-1] in x and row[1][-1] in x and row[2][-1] in x: 
            return True,'Player 1'
        if row[0][-1] in y and row[1][-1] in y and row[2][-1] in y: 
            return True,'Player 2'
    
    # Check columns
    for col in range(3):
        if board.board[0][col][-1] in x and board.board[1][col][-1] in x and board.board[2][col][-1] in x:
            return True,'Player 1'
        if board.board[0][col][-1] in y and board.board[1][col][-1] in y and board.board[2][col][-1] in y:
            return True,'Player 2'
    
    # Check diagonals
    if board.board[0][0][-1] in x and board.board[1][1][-1] in x and board.board[2][2][-1] in x:
        return True,'Player 1'
    if board.board[0][2][-1] in x and board.board[1][1][-1] in x and board.board[2][0][-1] in x:
        return True,'Player 1'
    if board.board[0][0][-1] in y and board.board[1][1][-1] in y and board.board[2][2][-1] in y:
        return True,'Player 1'
    if board.board[0][2][-1] in y and board.board[1][1][-1] in y and board.board[2][0][-1] in y:
        return True,'Player 1'
    
    return False,''

# Start the game
play_game()
