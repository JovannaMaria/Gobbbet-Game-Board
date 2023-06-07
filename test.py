from collections import deque
import random

# Define the empty and blocked spots on the board
EMPTY_SPOT = '-'
BLOCKED_SPOT = 'X'
# create dictionary
d = {'A': 3, 'B': 2, 'C': 1, 'X': 3, 'Y': 2, 'Z': 1}
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
        
    def __repr__(self):
        return f"GobbletBoard([[[] for _ in range(3)] for _ in range(3)])"


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
            return True, 'Player 1'
        if self.board[0][2][-1] in y and self.board[1][1][-1] in y and self.board[2][0][-1] in y:
            return True, 'Player 1'

        return False, ''


class QLearningAgent:
    def __init__(self, alpha, gamma):
        self.q_values = {}  # Q-values table
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor

    def get_q_value(self, state, action):
        # Get the Q-value for a state-action pair
        if state not in self.q_values:
            return 0.0
        if action not in self.q_values[state]:
            return 0.0
        return self.q_values[state][action]

    def update_q_value(self, state, action, value):
        # Update the Q-value for a state-action pair
        if state not in self.q_values:
            self.q_values[state] = {}
        self.q_values[state][action] = value

    def get_best_action(self, state):
        # Get the best action for a given state
        max_q_value = float('-inf')
        best_action = None

        if state in self.q_values:
            actions = self.q_values[state]
            for action, q_value in actions.items():
                if q_value > max_q_value:
                    max_q_value = q_value
                    best_action = action

        return best_action

    '''def choose_action(self, state, epsilon):
        # Choose an action based on the epsilon-greedy policy
        if random.random() < epsilon:
            return random.choice(list(possible_actions(state)))
        else:
            return self.get_best_action(state)'''
    def choose_action(self, state, epsilon):
    # Choose an action based on the epsilon-greedy policy
        if random.random() < epsilon:
            available_actions = possible_actions(state)
            if not available_actions:
                return None  # No available actions, return None
            return random.choice(available_actions)
        else:
            return self.get_best_action(state)


    def update(self, state, action, reward, next_state):
        # Update the Q-value based on the observed reward and next state
        current_q_value = self.get_q_value(state, action)
        max_q_value = max(self.get_q_value(next_state, a) for a in possible_actions(next_state))
        new_q_value = (1 - self.alpha) * current_q_value + self.alpha * (reward + self.gamma * max_q_value)
        self.update_q_value(state, action, new_q_value)


def possible_actions(state):
    # Get the possible actions for a given state
    board = GobbletBoard()
    board.board = eval(state)  # Convert the string representation of the board to a list

    actions = []
    for from_row in range(6):
        for from_col in range(3):
            for to_row in range(3):
                for to_col in range(3):
                    if board.is_valid_move(from_row, from_col, to_row, to_col, 'Player 1') or \
                            board.is_valid_move(from_row, from_col, to_row, to_col, 'Player 2'):
                        actions.append((from_row, from_col, to_row, to_col))

    return actions



def play_game(agent):
    board = GobbletBoard()
    current_player = 'Player 1'
    print("Each player has 2 stacks with 3 pieces. Players 1 and 2 can access their stack using from_row 4 and 5.")
    print("This is a 3x3 game board where row and col numbers range between 0 and 2.")

    while True:
        # Print the current state of the board
        print(f"{current_player}'s turn:")
        board.print_board()

        if current_player == 'Player 1':
            # Human player's turn
            from_row, from_col, to_row, to_col = map(int, input("Enter your move (from_row, from_col, to_row, to_col): ").split())

            # Check if the move is valid
            if not board.is_valid_move(from_row, from_col, to_row, to_col, current_player):
                print('Invalid move. Try again.')
                continue
        else:
            # AI player's turn
            epsilon = 0.2  # Exploration rate
            action = agent.choose_action(str(board), epsilon)
            if action is None:
                print('No available actions for the AI. Enter your move:')
                from_row, from_col, to_row, to_col = map(int, input("(from_row, from_col, to_row, to_col): ").split())
            else:
                from_row, from_col, to_row, to_col = action

        # Move the piece on the board
        board.is_valid_move(from_row, from_col, to_row, to_col, current_player)

        # Check if the current player has won
        is_winner, winner = board.check_win_condition()
        if is_winner:
            print(f"{winner} wins!")
            break

        # Switch to the other player
        current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'

        if current_player == 'Player 1':
            # Update the Q-values based on the AI player's experience
            reward = 0.0  # No reward for the AI player
            next_state = str(board)
            agent.update(str(board), (from_row, from_col, to_row, to_col), reward, next_state)

def train_agent(agent, num_episodes, alpha, gamma, epsilon):
    for episode in range(1, num_episodes + 1):
        board = GobbletBoard()
        current_player = 'Player 1'

        while True:
            state = str(board)

            # Choose an action based on the epsilon-greedy policy
            if current_player == 'Player 1':
                available_actions = possible_actions(str(board))
                if not available_actions:
                    print('No available actions for Player 1. Skipping episode.')
                    break
                action = agent.choose_action(state, epsilon)
                if action is None:
                    print('No available actions for the AI. Skipping episode.')
                    break
            else:
                available_actions = possible_actions(str(board))
                if not available_actions:
                    print('No available actions for Player 2. Skipping episode.')
                    break
                action = random.choice(available_actions)

            # Execute the chosen action
            from_row, from_col, to_row, to_col = action
            board.is_valid_move(from_row, from_col, to_row, to_col, current_player)

            # Check if the current player has won
            is_winner, winner = board.check_win_condition()
            if is_winner:
                reward = 1.0 if winner == 'Player 1' else -1.0
                agent.update(state, action, reward, None)
                break

            # Switch to the other player
            current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'

        # Update Q-values based on the AI player's experience
        if current_player == 'Player 1':
            reward = 0.0  # No reward for the AI player
            agent.update(state, action, reward, None)

        # Decrease epsilon
        epsilon *= 0.99


# Create an instance of the QLearningAgent class
# Create an instance of the QLearningAgent class with alpha and gamma values
alpha = 0.5  # Learning rate
gamma = 0.9  # Discount factor
agent = QLearningAgent(alpha, gamma)
num_episodes = 1000  # Define the number of episodes for training
epsilon = 0.2  # Define the exploration rate

# Train the agent
train_agent(agent, num_episodes, alpha, gamma, epsilon)


# Play against the AI
play_game(agent)
