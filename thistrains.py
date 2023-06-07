from collections import deque
import random

EMPTY_SPOT = '-'
d = {'A': 3, 'B': 2, 'C': 1, 'X': 3, 'Y': 2, 'Z': 1, '-': 0}
x = list('ABC')
y = list('XYZ')
s1 = deque(['C', 'B', 'A'])
s2 = deque(['C', 'B', 'A'])
s3 = deque(['Z', 'Y', 'X'])
s4 = deque(['Z', 'Y', 'X'])
px = [s1, s2]
py = [s3, s4]


class GobbletBoard:
    def __init__(self):
        self.board = [[deque([EMPTY_SPOT]) for _ in range(3)] for _ in range(3)]

    def print_board(self):
        for row in self.board:
            x = ''
            for st in row:
                x = x + ' ' + st[-1]
            print(x)
        print("player1:", px)
        print("player2:", py)

    def is_valid_move(self, from_row, from_col, to_row, to_col, curr):
        if not (0 <= from_row <= 5 and 0 <= from_col < 3 and
                0 <= to_row < 3 and 0 <= to_col < 3):
            return False

        if from_row == to_row and from_col == to_col:
            return False

        if (curr == 'Player 1' and 4 == from_row and 0 <= from_col < 2):
            if not px[from_col]:
                return False
            x1 = px[from_col][0]
            if self.board[to_row][to_col][-1] == EMPTY_SPOT:
                self.board[to_row][to_col].appendleft(px[from_col].popleft())
            elif d[x1] > d[self.board[to_row][to_col][-1]]:
                self.board[to_row][to_col].appendleft(px[from_col].popleft())
            return True

        elif (curr == 'Player 2' and 5 == from_row and 0 <= from_col < 2):
            if not py[from_col]:
                return False
            y1 = py[from_col][0]
            if self.board[to_row][to_col][-1] == EMPTY_SPOT:
                self.board[to_row][to_col].appendleft(py[from_col].popleft())
            elif d[y1] > d[self.board[to_row][to_col][-1]]:
                self.board[to_row][to_col].appendleft(py[from_col].popleft())
            return True

        if not (0 <= from_row < 3 and 0 <= from_col < 3 and
                0 <= to_row < 3 and 0 <= to_col < 3):
            return False

        if self.board[from_row][from_col][-1] == EMPTY_SPOT:
            return False

        if self.board[to_row][to_col][-1] == EMPTY_SPOT:
            if curr == 'Player 1' and self.board[from_row][from_col][-1] in x:
                self.board[to_row][to_col].appendleft(self.board[from_row][from_col].pop())
            elif curr == 'Player 2' and self.board[from_row][from_col][-1] in y:
                self.board[to_row][to_col].appendleft(self.board[from_row][from_col].pop())
            else:
                return False
            return True

        elif d[self.board[from_row][from_col][-1]] < d[self.board[to_row][to_col][-1]]:
            if curr == 'Player 1' and self.board[from_row][from_col][-1] in x:
                self.board[to_row][to_col].appendleft(self.board[from_row][from_col].pop())
            elif curr == 'Player 2' and self.board[from_row][from_col][-1] in y:
                self.board[to_row][to_col].appendleft(self.board[from_row][from_col].pop())
            else:
                return False
            return True

        return False

    def check_win_condition(self, curr):
        for row in range(3):
            if self.board[row][0][-1] == self.board[row][1][-1] == self.board[row][2][-1] != EMPTY_SPOT:
                return True
            if self.board[0][row][-1] == self.board[1][row][-1] == self.board[2][row][-1] != EMPTY_SPOT:
                return True
        if self.board[0][0][-1] == self.board[1][1][-1] == self.board[2][2][-1] != EMPTY_SPOT:
            return True
        if self.board[0][2][-1] == self.board[1][1][-1] == self.board[2][0][-1] != EMPTY_SPOT:
            return True
        return False


class QLearningAgent:
    def __init__(self, alpha, epsilon, discount, actions):
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount
        self.actions = actions
        self.q_values = {}

    def get_q_value(self, state, action):
        if (state, action) not in self.q_values:
            self.q_values[(state, action)] = 0.0
        return self.q_values[(state, action)]

    def compute_value_from_q_values(self, state):
        max_value = float('-inf')
        for action in self.actions:
            q_value = self.get_q_value(state, action)
            if q_value > max_value:
                max_value = q_value
        return max_value

    def compute_action_from_q_values(self, state):
        best_actions = []
        max_value = float('-inf')
        for action in self.actions:
            q_value = self.get_q_value(state, action)
            if q_value > max_value:
                best_actions = [action]
                max_value = q_value
            elif q_value == max_value:
                best_actions.append(action)
        return random.choice(best_actions)

    def get_best_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            return self.compute_action_from_q_values(state)

    def update(self, state, action, next_state, reward):
        old_q_value = self.get_q_value(state, action)
        max_q_value = self.compute_value_from_q_values(next_state)
        new_q_value = (1 - self.alpha) * old_q_value + self.alpha * (reward + self.discount * max_q_value)
        self.q_values[(state, action)] = new_q_value


def train_agent(agent, iterations):
    board = GobbletBoard()
    actions = []
    for i in range(iterations):
        curr = 'Player 1' if i % 2 == 0 else 'Player 2'
        state = str(board.board)
        action = agent.get_best_action(state)
        actions.append((state, action))
        from_row, from_col, to_row, to_col = action
        valid_move = board.is_valid_move(from_row, from_col, to_row, to_col, curr)
        if valid_move:
            next_state = str(board.board)
            reward = 1 if board.check_win_condition(curr) else 0
            agent.update(state, action, next_state, reward)
            if reward == 1:
                print("Player 1 wins!" if curr == 'Player 1' else "Player 2 wins!")
                print("Actions:", actions)
                return
    print("Game ended in a draw.")
    print("Actions:", actions)
    
def play_game(agent):
    board = GobbletBoard()
    curr = 'Player 1'
    
    while not board.check_win_condition(curr):
        board.print_board()

        if curr == 'Player 1':
            print("Player 1's turn:")
            from_row, from_col, to_row, to_col = map(int, input("Enter your move (from_row, from_col, to_row, to_col): ").split())

            action = (from_row, from_col, to_row, to_col)
        else:
            state = str(board.board)
            action = agent.get_best_action(state)
            print("Player 2's turn:")
            print("Agent chooses action:", action)

        from_row, from_col, to_row, to_col = action
        valid_move = board.is_valid_move(from_row, from_col, to_row, to_col, curr)

        if valid_move:
            if curr == 'Player 1':
                if board.board[from_row][from_col][-1] in x:
                    px[from_col].appendleft(board.board[from_row][from_col].pop())
                else:
                    print("Invalid move. Please try again.")
                    continue
            else:
                if board.board[from_row][from_col][-1] in y:
                    py[from_col].appendleft(board.board[from_row][from_col].pop())
                else:
                    print("Invalid move. Please try again.")
                    continue

            next_state = str(board.board)
            reward = 1 if board.check_win_condition(curr) else 0
            agent.update(state, action, next_state, reward)

            if reward == 1:
                print("Player 1 wins!" if curr == 'Player 1' else "Player 2 wins!")
                break

            curr = 'Player 2' if curr == 'Player 1' else 'Player 1'
        else:
            print("Invalid move. Please try again.")

    board.print_board()



if __name__ == "__main__":
    alpha = 0.5
    epsilon = 0.1
    discount = 0.8
    actions = [(row, col, new_row, new_col) for row in range(6) for col in range(3) for new_row in range(3)
               for new_col in range(3)]
    agent = QLearningAgent(alpha, epsilon, discount, actions)
    train_agent(agent, 1000)

    play_game(agent)