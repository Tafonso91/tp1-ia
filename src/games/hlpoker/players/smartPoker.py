from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State


class SmartHLPokerPlayer(HLPokerPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        """
        Escolhe a ação do jogador com base nas cartas privadas.

        Retorna:
        - HLPokerAction.CALL se as cartas privadas formarem um par (dupla) com valor superior a 5.
        - HLPokerAction.FOLD em todos os outros casos.
        """
        # Obtenha as cartas privadas
        card1, card2 = private_cards

        # Verifique se as cartas formam um par (mesmo número) com valor superior a 5
        if card1.rank == card2.rank and card1.rank.value > 5:
            # Se a ação CALL for válida, retorne CALL
            if state.validate_action(HLPokerAction.CALL):
                return HLPokerAction.CALL
        # Caso contrário, retorne FOLD
        return HLPokerAction.FOLD

    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        pass

    def event_new_game(self):
        pass

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        pass

    def event_new_round(self, round: Round):
        pass

