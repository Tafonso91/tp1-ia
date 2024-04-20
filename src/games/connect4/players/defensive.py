from random import choice
from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State
from games.connect4.result import Connect4Result

class BotConnect4Player(Connect4Player):

    def __init__(self, name, depth=4):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: Connect4State):
        # Chama a função MiniMax para encontrar a melhor ação
        return self.minimax(state, self.depth, True)[1]

    def minimax(self, state: Connect4State, depth: int, is_maximizing: bool):
        if depth == 0 or state.is_finished():
            # Retorna a avaliação do estado
            return self.evaluate(state), None

        possible_actions = state.get_possible_actions()

        if is_maximizing:
            max_eval = float('-inf')
            best_action = None
            for action in possible_actions:
                # Clona o estado para simular a jogada
                new_state = state.clone()
                new_state.update(action)
                # Chama minimax recursivamente para alternar os jogadores
                eval, _ = self.minimax(new_state, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_action = action
            return max_eval, best_action
        else:
            min_eval = float('inf')
            worst_action = None
            for action in possible_actions:
                # Clona o estado para simular a jogada
                new_state = state.clone()
                new_state.update(action)
                # Chama minimax recursivamente para alternar os jogadores
                eval, _ = self.minimax(new_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    worst_action = action
            return min_eval, worst_action

    def evaluate(self, state: Connect4State):
        # Lógica de avaliação para verificar se o bot deve bloquear as peças verticais do adversário
        if state.get_result(self.get_current_pos()) == Connect4Result.WIN.value:
            return 1000  # Vitória é um valor alto
        elif state.get_result(self.get_current_pos()) == Connect4Result.LOOSE.value:
            return -1000  # Derrota é um valor baixo
        elif state.get_result(self.get_current_pos()) == Connect4Result.DRAW.value:
            return 0  # Empate é neutro
        
        # Verifica se há 3 peças verticais consecutivas do adversário em uma coluna
        grid = state.get_grid()
        score = 0
        
        for col in range(state.get_num_cols()):
            # Verifica as linhas com pelo menos 3 peças consecutivas do adversário
            for row in range(state.get_num_rows() - 2):
                if (grid[row][col] == 1 - self.get_current_pos() and
                    grid[row + 1][col] == 1 - self.get_current_pos() and
                    grid[row + 2][col] == 1 - self.get_current_pos()):
                    # Adiciona uma penalização ao score para a presença de 3 peças verticais consecutivas do adversário
                    score -= 100
                
        # Calcula um score com base nas peças do bot e do adversário
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if grid[row][col] == self.get_current_pos():
                    score += 1
                elif grid[row][col] == 1 - self.get_current_pos():
                    score -= 1
        
        return score

    def event_action(self, pos: int, action, new_state: State):
        # Ignora
        pass

    def event_end_game(self, final_state: State):
        # Ignora
        pass



