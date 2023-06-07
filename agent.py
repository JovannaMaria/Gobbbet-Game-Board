import random
from board_final import GobbletBoard
from math import sqrt, log

class MCTSTreeNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_valid_moves())

    def select_child(self, exploration_factor=1.4):
        total_visits = sum(child.visits for child in self.children)
        log_total = log(total_visits)

        best_child = None
        best_score = float('-inf')

        for child in self.children:
            exploitation_score = child.wins / child.visits
            exploration_score = sqrt(log_total / child.visits)

            uct_score = exploitation_score + exploration_factor * exploration_score

            if uct_score > best_score:
                best_score = uct_score
                best_child = child

        return best_child

    def expand(self):
        valid_moves = self.state.get_valid_moves()
        for move in valid_moves:
            new_state = self.state.clone()
            new_state.is_valid_move(move)
            new_node = MCTSTreeNode(new_state, self, move)
            self.children.append(new_node)

        return random.choice(self.children)

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result

        if self.parent:
            self.parent.backpropagate(result)


class MCTSPlayer:
    def __init__(self, iterations=1000, exploration_factor=1.4):
        self.iterations = iterations
        self.exploration_factor = exploration_factor

    def get_action(self, state):
        root = MCTSTreeNode(state)

        for _ in range(self.iterations):
            node = self.tree_policy(root)
            result = self.simulate(node.state)
            node.backpropagate(result)

        best_child = root.select_child(exploration_factor=self.exploration_factor)
        return best_child.action

    def tree_policy(self, node):
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            else:
                node = node.select_child(exploration_factor=self.exploration_factor)

        return node

    def simulate(self, state):
        while not state.is_terminal():
            valid_moves = state.get_valid_moves()
            random_move = random.choice(valid_moves)
            state.is_valid_move(random_move)

        return state.get_result()


# Game implementation and training
class GobbletGame:
    def __init__(self):
        # Initialize the game board and other variables
        self.board = GobbletBoard()
        self.current_player = 'Player 1'
        self.human_player = 'Player 1'
        self.agent_player = 'Player 2'

        self.agent = MCTSPlayer(iterations=1000, exploration_factor=1.4)

    def play_game(self):
        while True:
            # Print the current state of the board
            print(f"{self.current_player}'s turn:")
            self.board.print_board()

            if self.current_player == self.human_player:
                # Ask the human player for a move
                from_row, from_col, to_row, to_col = self.get_human_move()

                # Make the move on the board
                self.board.is_valid_move(from_row, from_col, to_row, to_col,self.current_player)

                # Check if the game is over
                if self.board.check_win_condition():
                    print("Game Over!")
                    self.board.print_board()
                    break
            else:
                # Let the agent player select a move
                action = self.agent.get_action(self.board)
                self.board.is_valid_move(action[0], action[1], action[2], action[3],self.current_player)

                # Check if the game is over
                if self.board.check_win_condition():
                    print("Game Over!")
                    self.board.print_board()
                    break

            # Switch the current player
            self.current_player = self.agent_player if self.current_player == self.human_player else self.human_player

    def get_human_move(self):
        # TODO: Implement the logic to get a move from the human player
        # You can prompt the user for input and parse it to obtain the move coordinates
        # Return the move coordinates as from_row, from_col, to_row, to_col
        from_row, from_col, to_row, to_col = map(int, input("Enter your move (from_row, from_col, to_row, to_col): ").split())

        return from_row, from_col, to_row, to_col


# Example usage
game = GobbletGame()
game.play_game()
