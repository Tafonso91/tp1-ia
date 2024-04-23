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
        # Primeiro, jogar nas quatro esquinas
        # Canto superior esquerdo
        corners = [
            MinesweeperAction(0, 0),  # Canto superior esquerdo
            MinesweeperAction(0, state.get_num_cols() - 1),  # Canto superior direito
            MinesweeperAction(state.get_num_rows() - 1, 0),  # Canto inferior esquerdo
            MinesweeperAction(state.get_num_rows() - 1, state.get_num_cols() - 1),  # Canto inferior direito
        ]

        for index, move in enumerate(corners):
            if state.validate_action(move) and not self.corners_played[index]:
                # Marcar este canto como jogado
                self.corners_played[index] = True
                return move
        
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
                            # Certificar-se de que os índices estão dentro dos limites
                            if 0 <= adj_row < state.get_num_rows() and 0 <= adj_col < state.get_num_cols():
                                move = MinesweeperAction(adj_row, adj_col)
                                if state.validate_action(move):
                                    return move

        # Se não houver uma jogada clara, faça uma escolha aleatória
        possible_actions = list(state.get_possible_actions())
        return choice(possible_actions)

    def event_action(self, pos: int, action, new_state: State):
        # Ignorar eventos de ação por enquanto
        pass

    def event_end_game(self, final_state: State):
        # Ignorar eventos de fim de jogo por enquanto
        pass


