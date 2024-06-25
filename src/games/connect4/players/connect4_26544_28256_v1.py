from random import choice
from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State
from games.connect4.result import Connect4Result

class connect4_26544_28256_v1(Connect4Player):

    def __init__(self, name, depth=4):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: Connect4State):
        # Call Minimax to find the best solution
        return self.minimax(state, self.depth, True)[1]

    def minimax(self, state: Connect4State, depth: int, is_maximizing: bool):
        if depth == 0 or state.is_finished():
            # Return the state evaluation
            return self.evaluate(state), None

        possible_actions = state.get_possible_actions()

        if is_maximizing:
            max_eval = float('-inf')
            best_action = None
            for action in possible_actions:
                # Clone the state to simulate the play
                new_state = state.clone()
                new_state.update(action)
                # Call minimax recursively to alternate players
                eval, _ = self.minimax(new_state, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_action = action
            return max_eval, best_action
        else:
            min_eval = float('inf')
            worst_action = None
            for action in possible_actions:
                # Clone the state to simulate the play
                new_state = state.clone()
                new_state.update(action)
                # Call minimax recursively to alternate players
                eval, _ = self.minimax(new_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    worst_action = action
            return min_eval, worst_action

    def evaluate(self, state: Connect4State):
        # Evaluation logic to check if the bot should block the opponent's potential four in a line
        if state.get_result(self.get_current_pos()) == Connect4Result.WIN.value:
            return 1000  # Win is a high value
        elif state.get_result(self.get_current_pos()) == Connect4Result.LOOSE.value:
            return -1000  # Loss is a low value
        elif state.get_result(self.get_current_pos()) == Connect4Result.DRAW.value:
            return 0  # Draw is neutral
        
        # Check if there are potential four in a line (horizontal, vertical, diagonal)
        grid = state.get_grid()
        score = 0
        
        # Check horizontal lines for possible four in a line from the opponent
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols() - 3):
                # Check for three opponent pieces in a row
                if all(grid[row][col + i] == 1 - self.get_current_pos() for i in range(3)):
                    # Deduct score for potential four in a line
                    score -= 100

        # Check vertical lines for potential four in a line from the opponent
        for col in range(state.get_num_cols()):
            for row in range(state.get_num_rows() - 2):
                if all(grid[row + i][col] == 1 - self.get_current_pos() for i in range(3)):
                    score -= 100

        # Check diagonal lines (top-left to bottom-right) for potential four in a line from the opponent
        for row in range(state.get_num_rows() - 2):
            for col in range(state.get_num_cols() - 2):
                if all(grid[row + i][col + i] == 1 - self.get_current_pos() for i in range(3)):
                    score -= 100

        # Check diagonal lines (bottom-left to top-right) for potential four in a line from the opponent
        for row in range(2, state.get_num_rows()):
            for col in range(state.get_num_cols() - 2):
                if all(grid[row - i][col + i] == 1 - self.get_current_pos() for i in range(3)):
                    score -= 100
        
        # Calculate score based on bot and opponent pieces
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if grid[row][col] == self.get_current_pos():
                    score += 1
                elif grid[row][col] == 1 - self.get_current_pos():
                    score -= 1

        return score


    def event_action(self, pos: int, action, new_state: State):
        # Ignore
        pass

    def event_end_game(self, final_state: State):
        # Ignore
        pass



