from random import choice
from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State
import random

class ProbMinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.corners_played = [False, False, False, False]  # To track if each corner has been played

    def get_action(self, state: MinesweeperState):
        # First, play in the four corners if not already played
        corners = [
            MinesweeperAction(0, 0),  # Top left corner
            MinesweeperAction(0, state.get_num_cols() - 1),  # Top right corner
            MinesweeperAction(state.get_num_rows() - 1, 0),  # Bottom left corner
            MinesweeperAction(state.get_num_rows() - 1, state.get_num_cols() - 1),  # Bottom right corner
        ]

        # Play in the corners if not already done
        for i, corner in enumerate(corners):
            if not self.corners_played[i] and state.validate_action(corner):
                self.corners_played[i] = True
                return corner

        # List of moves to avoid
        avoid_moves = set()

        # Now, look for cells with value 0 and explore their adjacencies
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                # Check the current cell
                cell_value = state.get_grid()[row][col]

                if cell_value == 0:  
                    
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                move = MinesweeperAction(adj_row, adj_col)
                                if state.validate_action(move):
                                    return move

                # Avoid adjacencies to cells with values greater than 3
                elif cell_value > 3:  
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                avoid_moves.add(MinesweeperAction(adj_row, adj_col))

                # If the cell has a number greater than 0, check if adjacent cells are filled with mines
                elif isinstance(cell_value, int) and cell_value > 0:
                    empty_cells_adjacent = []
                    num_mines_adjacent = 0

                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                move = MinesweeperAction(adj_row, adj_col)
                                adj_value = state.get_grid()[adj_row][adj_col]

                                # Check if the adjacent cell is a mine
                                if adj_value == MinesweeperState.MINE_CELL:
                                    num_mines_adjacent += 1
                                # If the adjacent cell is not revealed
                                elif adj_value == MinesweeperState.EMPTY_CELL:
                                    empty_cells_adjacent.append(move)

                    # If the number of adjacent mines equals the cell value, fill the adjacent empty cells
                    if num_mines_adjacent == cell_value:
                        if empty_cells_adjacent:
                            return empty_cells_adjacent[0]

        # Filter possible actions to avoid adjacencies to cells with values greater than 3 and adjacent empty cells
        possible_actions = list(state.get_possible_actions())
        possible_actions = [action for action in possible_actions if action not in avoid_moves]
        
        # Check if the current cell has the number of adjacent empty cells equal to its value
        for action in possible_actions:
            row, col = action.get_row(), action.get_col()
            cell_value = state.get_grid()[row][col]
            num_empty_adjacent = 0
            for d_row in [-1, 0, 1]:
                for d_col in [-1, 0, 1]:
                    adj_row = row + d_row
                    adj_col = col + d_col
                    if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                        if state.get_grid()[adj_row][adj_col] == MinesweeperState.EMPTY_CELL:
                            num_empty_adjacent += 1
            if num_empty_adjacent == cell_value:
                avoid_moves.add(action)

        # If there are possible actions after filtering, choose one based on probability
        if possible_actions:
            return self.choose_action_with_probability(possible_actions, state)

        # If no possible actions, choose randomly among remaining actions
        return choice(list(state.get_possible_actions()))


    def choose_action_with_probability(self, possible_actions, state: MinesweeperState):
        # Calculate probabilities for each action
        probabilities = [self.calculate_action_probability(action, possible_actions, state) for action in possible_actions]

        # Choose an action based on probabilities
        cum_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
        rand = random.random()
        for i, cum_prob in enumerate(cum_probabilities):
            if rand < cum_prob:
                return possible_actions[i]

        # If for some reason unable to choose based on probabilities,
        # choose randomly among available actions
        return random.choice(possible_actions)


    def calculate_action_probability(self, action, possible_actions, state: MinesweeperState):
        
        base_probability = 1 / len(possible_actions)
        
        # Factors to adjust probability based on certain criteria
        empty_cell_bonus = 1.5  # Bonus for actions adjacent to empty cells
        mine_penalty = 0.5  # Penalty for actions adjacent to mines
        revealed_cell_penalty = 0.2  # Penalty for actions adjacent to already revealed cells
        
        # Get the coordinates of the action
        row, col = action.get_row(), action.get_col()
        
        # Check adjacent cells
        adjacent_cells = [(row + dr, col + dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if (dr != 0 or dc != 0)]
        
        # Calculate probability based on factors
        probability = base_probability
        for adj_row, adj_col in adjacent_cells:
            if (0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols() and
                MinesweeperAction(adj_row, adj_col) in possible_actions):
                
                adj_cell_value = state.get_grid()[adj_row][adj_col]
                if adj_cell_value == MinesweeperState.EMPTY_CELL:
                    probability *= empty_cell_bonus
                elif adj_cell_value == MinesweeperState.MINE_CELL:
                    probability *= mine_penalty
                elif isinstance(adj_cell_value, int) and adj_cell_value > 0:
                    probability *= revealed_cell_penalty
        
        return probability


    def event_action(self, pos: int, action, new_state: State):
        pass

    def event_end_game(self, final_state: State):
        pass


