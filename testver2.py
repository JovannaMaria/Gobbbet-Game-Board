from collections import deque
import random

# Define the empty and blocked spots on the board
EMPTY_SPOT = '-'
BLOCKED_SPOT = 'X'
# create dictionary
d = {'A': 3, 'B': 2, 'C': 1, 'X': 3, 'Y': 2, 'Z': 1,'-':0}
x = list('ABC')
y = list('XYZ')
# Create the stacks
s1 = deque(['C', 'B', 'A'])
s2 = deque(['C', 'B', 'A'])
s3 = deque(['Z', 'Y', 'X'])
s4 = deque(['Z', 'Y', 'X'])
px = [s1, s2]
py = [s3, s4]


class GobbletBoard:
    def __init__(self):
        # Initialize the empty board
        self.board = [[deque([EMPTY_SPOT]) for _ in range(3)] for _ in range(3)]
        
        
    #def __repr__(self):
    #   return f"GobbletBoard([[[] for _ in range(3)] for _ in range(3)])"


    def print_board(self):
        # Print the current state of the board
        for row in self.board:
            x = ''
            for st in row:
                x = x + ' ' + st[-1]
            print(x)
        print("player1:", px)
        print("player2:", py)

    def is_valid_move(self, from_row, from_col, to_row, to_col, curr):
        # Check if the move is within the bounds of the board
        if not (0 <= from_row <= 5 and 0 <= from_col < 3 and
                0 <= to_row < 3 and 0 <= to_col < 3):
            return False

        # Check if the source and destination spots are different
        if from_row == to_row and from_col == to_col:
            return False

        # Check if new piece is moved
        if (curr == 'Player 1' and 4 == from_row and 0 <= from_col < 2):
            if not px[from_col]:
                return False
            x1 = px[from_col][0]
            if self.board[to_row][to_col][-1] == EMPTY_SPOT:
                self.board[to_row][to_col].append(px[from_col].pop())
            elif d[x1] > d[self.board[to_row][to_col][-1]]:
                self.board[to_row][to_col].append(px[from_col].pop())
            return True

        elif (curr == 'Player 2' and 5 == from_row and 0 <= from_col < 2):
            if not py[from_col]:
                return False
            y1 = py[from_col][0]
            if self.board[to_row][to_col][-1] == EMPTY_SPOT:
                self.board[to_row][to_col].append(py[from_col].pop())
            if d[y1] > d[self.board[to_row][to_col][-1]]:
                self.board[to_row][to_col].append(py[from_col].pop())
            return True

        if not (0 <= from_row < 3 and 0 <= from_col < 3 and
                0 <= to_row < 3 and 0 <= to_col < 3):
            return False
        # Check if the source spot is not empty
        if self.board[from_row][from_col][-1] == EMPTY_SPOT:
            return False
        # Check if the destination spot is empty or has a smaller piece on top
        if self.board[to_row][to_col][-1] == EMPTY_SPOT:
            if curr == 'Player 1' and self.board[from_row][from_col][-1] in x:
                self.board[to_row][to_col].append(self.board[from_row][from_col].pop())
            elif curr == 'Player 2' and self.board[from_row][from_col][-1] in y:
                self.board[to_row][to_col].append(self.board[from_row][from_col].pop())
            else:
                return False
            return True

        elif d[self.board[from_row][from_col][-1]] > d[self.board[to_row][to_col][-1]]:
            if curr == 'Player 1' and self.board[from_row][from_col][-1] in x:
                self.board[to_row][to_col].append(self.board[from_row][from_col].pop())
            elif curr == 'Player 2' and self.board[from_row][from_col][-1] in y:
                self.board[to_row][to_col].append(self.board[from_row][from_col].pop())
            else:
                return False
            return True

        return False, ''

    def check_win_condition(self):
        # Check rows
        for row in self.board:
            if row[0][-1] in x and row[1][-1] in x and row[2][-1] in x:
                return True, 'Player 1'
            if row[0][-1] in y and row[1][-1] in y and row[2][-1] in y:
                return True, 'Player 2'

        # Check columns
        for col in range(3):
            if self.board[0][col][-1] in x and self.board[1][col][-1] in x and self.board[2][col][-1] in x:
                return True, 'Player 1'
            if self.board[0][col][-1] in y and self.board[1][col][-1] in y and self.board[2][col][-1] in y:
                return True, 'Player 2'

        # Check diagonals
        if self.board[0][0][-1] in x and self.board[1][1][-1] in x and self.board[2][2][-1] in x:
            return True, 'Player 1'
        if self.board[0][2][-1] in x and self.board[1][1][-1] in x and self.board[2][0][-1] in x:
            return True, 'Player 1'
        if self.board[0][0][-1] in y and self.board[1][1][-1] in y and self.board[2][2][-1] in y:
            return True, 'Player 2'
        if self.board[0][2][-1] in y and self.board[1][1][-1] in y and self.board[2][0][-1] in y:
            return True, 'Player 2'

        return False, ''

class QLearningAgent:
    def __init__(self, alpha, gamma):
        self.Q = {}  # Dictionary to store Q-values
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor

    def get_best_action(self, state):
        # Retrieve the Q-values for the given state
        actions = self.Q.get(state)
        if actions is None:
            return None

        # Find the action with the highest Q-value
        best_action = max(actions, key=actions.get)
        return best_action

    def update_Q(self, state, action, reward, next_state):
        # Update the Q-value for the given state-action pair
        current_q = self.Q.get(state, {})
        next_q = self.Q.get(next_state, {})
        next_best_action = self.get_best_action(next_state)
        current_q[action] = current_q.get(action, 0) + self.alpha * (
            reward + self.gamma * next_q.get(next_best_action, 0) - current_q.get(action, 0)
        )
        self.Q[state] = current_q

    def choose_action(self, state, epsilon):
        # Choose an action based on the epsilon-greedy policy
        if random.random() < epsilon:
            available_actions = self.possible_actions(state)
            if not available_actions:
                return None  # No available actions, return None
            return random.choice(available_actions)
        else:
            return self.get_best_action(state)

    def possible_actions(self, state):
        # Generate all possible actions for the given state
        actions = []
        for from_row in range(3):
            for from_col in range(3):
                for to_row in range(3):
                    for to_col in range(3):
                        actions.append((from_row, from_col, to_row, to_col))
        return actions


def train_agent(agent, episodes, epsilon):
    for episode in range(episodes):
        # Initialize the game
        board = GobbletBoard()
        current_player = 'Player 1'

        while True:
            # Get the current state of the board
            state = str(board.board)

            # Choose an action for the current player
            action = agent.choose_action(state, epsilon)

            if action is None:
                break  # No available actions, end the game

            # Execute the action and get the next state
            from_row, from_col, to_row, to_col = action
            is_valid = board.is_valid_move(from_row, from_col, to_row, to_col, current_player)

            if not is_valid:
                break  # Invalid move, end the game

            next_state = str(board.board)

            # Update the Q-value for the current state-action pair
            if current_player == 'Player 1':
                reward = 1 if board.check_win_condition(current_player) else 0
            else:
                reward = -1 if board.check_win_condition(current_player) else 0

            agent.update_Q(state, action, reward, next_state)

            # Switch to the next player
            current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'

    return agent


def play_game(agent):
    # Initialize the game
    board = GobbletBoard()
    current_player = 'Player 1'

    while True:
        # Print the current state of the board
        board.print_board()

        # Get the current state of the board
        state = str(board.board)

        # Choose an action for the current player
        action = agent.get_best_action(state)

        if action is None:
            print("No available actions, the game ends in a draw.")
            break

        # Execute the action and get the next state
        from_row, from_col, to_row, to_col = action
        is_valid = board.is_valid_move(from_row, from_col, to_row, to_col, current_player)

        if not is_valid:
            print("Invalid move, the game ends in a draw.")
            break

        next_state = str(board.board)

        # Switch to the next player
        current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'

        # Check if the current player wins
        if board.check_win_condition(current_player):
            print(current_player, "wins!")
            break

        print("\n")

# Create an instance of the Q-learning agent
agent = QLearningAgent(alpha=0.5, gamma=0.9)

# Train the agent
agent = train_agent(agent, episodes=10000, epsilon=0.1)

# Play the game using the trained agent
play_game(agent)
