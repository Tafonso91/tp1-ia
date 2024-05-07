from random import choice
from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State

class IntelligentMinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.corners_played = [False, False, False, False]  # Para rastrear se cada canto foi jogado

    def get_action(self, state: MinesweeperState):
        # Primeiro, jogar nas quatro esquinas, se ainda não jogadas
        corners = [
            MinesweeperAction(0, 0),  # Canto superior esquerdo
            MinesweeperAction(0, state.get_num_cols() - 1),  # Canto superior direito
            MinesweeperAction(state.get_num_rows() - 1, 0),  # Canto inferior esquerdo
            MinesweeperAction(state.get_num_rows() - 1, state.get_num_cols() - 1),  # Canto inferior direito
        ]

        # Jogue nos cantos, se ainda não o fez
        for i, corner in enumerate(corners):
            if not self.corners_played[i] and state.validate_action(corner):
                self.corners_played[i] = True
                return corner
        
        # Lista de ações a evitar
        avoid_moves = set()
        
        # Agora, procurar por células com o número 0 e explorar suas adjacências
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                # Verificar a célula atual
                cell_value = state.get_grid()[row][col]
                
                if cell_value == 0:  # Encontrou uma célula com valor 0
                    # Explorar adjacências
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            # Verificar se os índices estão dentro dos limites
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                move = MinesweeperAction(adj_row, adj_col)
                                if state.validate_action(move):
                                    return move

                
                # Evitar adjacências a células com valor 3
                elif cell_value == 3:  # Encontrou uma célula com valor 3
                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            # Verificar se os índices estão dentro dos limites
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                avoid_moves.add(MinesweeperAction(adj_row, adj_col))

                # Se a célula tem um número maior que 0, verifique se a adjacência está preenchida com minas
                elif isinstance(cell_value, int) and cell_value > 0:
                    empty_cells_adjacent = []
                    num_mines_adjacent = 0

                    for d_row in [-1, 0, 1]:
                        for d_col in [-1, 0, 1]:
                            adj_row = row + d_row
                            adj_col = col + d_col
                            # Verificar se os índices estão dentro dos limites
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                move = MinesweeperAction(adj_row, adj_col)
                                adj_value = state.get_grid()[adj_row][adj_col]
                                
                                # Verificar se a célula adjacente é uma mina
                                if adj_value == MinesweeperState.MINE_CELL:
                                    num_mines_adjacent += 1
                                # Se a célula adjacente ainda não foi revelada
                                elif adj_value == MinesweeperState.EMPTY_CELL:
                                    empty_cells_adjacent.append(move)

                    # Se o número de minas adjacentes for igual ao valor da célula, preencha as células adjacentes vazias
                    if num_mines_adjacent == cell_value:
                        if empty_cells_adjacent:
                            return empty_cells_adjacent[0]
        
        # Filtrar ações possíveis para evitar adjacências a células com o número 3 e células vazias adjacentes
        possible_actions = list(state.get_possible_actions())
        possible_actions = [action for action in possible_actions if action not in avoid_moves]
        
        # Se houver alguma ação possível após filtrar, escolha uma aleatória
        if possible_actions:
            return choice(possible_actions)
        
        # Se não houver uma jogada clara, faça uma escolha aleatória
        return choice(list(state.get_possible_actions()))

    def event_action(self, pos: int, action, new_state: State):
        # Ignorar eventos de ação por enquanto
        pass

    def event_end_game(self, final_state: State):
        # Ignorar eventos de fim de jogo por enquanto
        pass
