from random import choice
from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State

class IntelligentMinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.corners_played = [False, False, False, False]  

    def get_action(self, state: MinesweeperState):
        # First play at the corners
        corners = [
            MinesweeperAction(0, 0),  # Top left corner
            MinesweeperAction(0, state.get_num_cols() - 1),  # Top right corner
            MinesweeperAction(state.get_num_rows() - 1, 0),  # Lower left corner
            MinesweeperAction(state.get_num_rows() - 1, state.get_num_cols() - 1),  # Lower right corner
        ]

        # Play at the corners
        for i, corner in enumerate(corners):
            if not self.corners_played[i] and state.validate_action(corner):
                self.corners_played[i] = True
                return corner
        
        # Create a list to avoid some actions
        avoid_moves = set()
        
        # Looking for number 0 and  fills adjacent cells
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                # Check actual cell
                cell_value = state.get_grid()[row][col]
                
                if cell_value == 0:  # Found number 0 cell
                    # Explores adjacent cells
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            # Check if the indexes are within limits
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                move = MinesweeperAction(adj_row, adj_col)
                                if state.validate_action(move):
                                    return move
                
                elif cell_value == 3:  # Found a cell with value 3
                    # Avoid adjacent cells
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            # Check if the indexes are within limits
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                avoid_moves.add(MinesweeperAction(adj_row, adj_col))
                
                elif isinstance(cell_value, int) and cell_value > 0:  # Verify cells with numbers
                    empty_cells_adjacent = []
                    # Verify adjacent cells
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                adj_value = state.get_grid()[adj_row][adj_col]
                                if adj_value == MinesweeperState.EMPTY_CELL:
                                    empty_cells_adjacent.append(MinesweeperAction(adj_row, adj_col))
                    # If the number of adjacent empty cells is equal to the value of the current cell
                    if len(empty_cells_adjacent) == cell_value:
                        avoid_moves.update(empty_cells_adjacent)
        
        # Filtrar ações possíveis para evitar adjacências a células com o número 3 e células vazias adjacentes
        possible_actions = list(state.get_possible_actions())
        possible_actions = [action for action in possible_actions if action not in avoid_moves]
        
        # Se houver alguma ação possível após filtrar, escolha uma aleatória
        if possible_actions:
            return choice(possible_actions)
        
        # Se não houver uma jogada clara, faça uma escolha aleatória
        return choice(list(state.get_possible_actions()))

    def event_action(self, pos: int, action, new_state: State):
    
        pass

    def event_end_game(self, final_state: State):
        
        pass