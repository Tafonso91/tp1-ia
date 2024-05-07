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
        Escolhe a ação do jogador com base nas cartas privadas e nas cartas do board.

        Parâmetros:
        - state: O estado atual do jogo.
        - private_cards: As cartas privadas do jogador.
        - board_cards: As cartas do board (comunitárias).

        Retorna:
        - A ação escolhida com base nas cartas privadas e no board.
        """
        # Verifica se há um Royal Flush
        if self._has_royal_flush(private_cards, board_cards):
            if state.validate_action(HLPokerAction.RAISE):
                return HLPokerAction.RAISE
        
        # Verifica se há um Straight Flush
        if self._has_straight_flush(private_cards, board_cards):
            if state.validate_action(HLPokerAction.RAISE):
                return HLPokerAction.RAISE

        # Verifica se há quatro cartas iguais (Four of a Kind)
        if self._has_four_of_a_kind(private_cards, board_cards):
            if state.validate_action(HLPokerAction.RAISE):
                return HLPokerAction.RAISE

        # Verifica se há um Full House
        if self._has_full_house(private_cards, board_cards):
            if state.validate_action(HLPokerAction.RAISE):
                return HLPokerAction.RAISE

        # Verifica se há uma sequência de cinco cartas seguidas (Straight)
        if self._has_straight(private_cards, board_cards):
            if state.validate_action(HLPokerAction.RAISE):
                return HLPokerAction.RAISE

        # Verifica se há uma Flush
        if self._has_flush(private_cards, board_cards):
            if state.validate_action(HLPokerAction.RAISE):
                return HLPokerAction.RAISE

        # Verifica se há três cartas iguais (Three of a Kind)
        if self._has_trips(private_cards, board_cards):
            if state.validate_action(HLPokerAction.RAISE):
                return HLPokerAction.RAISE

        # Caso as cartas privadas formem um par
        if private_cards[0].rank == private_cards[1].rank:
            if state.validate_action(HLPokerAction.CALL):
                return HLPokerAction.CALL

        # Considera a força das cartas privadas e outras estratégias para CALL ou FOLD
        card_strength = max(private_cards[0].rank.value, private_cards[1].rank.value)
        strength_threshold = 8  # Ajuste o valor conforme necessário

        if card_strength > strength_threshold:
            # Se a força das cartas for alta, retorna CALL
            if state.validate_action(HLPokerAction.CALL):
                return HLPokerAction.CALL
        else:
            # Caso contrário, retorna FOLD
            if state.validate_action(HLPokerAction.FOLD):
                return HLPokerAction.FOLD

        # Por padrão, retorna FOLD caso nenhum critério seja atendido
        return HLPokerAction.FOLD


    def event_my_action(self, action, new_state):
        # Implementação para eventos após a ação do jogador (se necessário)
        pass

    def event_opponent_action(self, action, new_state):
        # Implementação para eventos após a ação do oponente (se necessário)
        pass

    def event_new_game(self):
        # Implementações para o início de um novo jogo (se necessário)
        pass

    def event_new_round(self, round):
        # Implementações para uma nova rodada (se necessário)
        pass

    def event_end_game(self, final_state: State):
        # Implementação para o evento de fim de jogo (se necessário)
        pass

    def _has_trips(self, private_cards, board_cards):
        """
        Verifica se há três cartas iguais considerando as cartas privadas e as cartas do board.

        Parâmetros:
        - private_cards: As cartas privadas do jogador.
        - board_cards: As cartas do board.

        Retorna:
        - True se há três cartas iguais nas cartas privadas e no board; False caso contrário.
        """
        # Combina as cartas privadas e as cartas do board em uma lista
        all_cards = private_cards + board_cards

        # Conta as ocorrências de cada rank
        rank_counts = {}
        for card in all_cards:
            rank = card.rank.value
            if rank in rank_counts:
                rank_counts[rank] += 1
            else:
                rank_counts[rank] = 1

        # Verifica se há algum rank com três ocorrências (trinca)
        for count in rank_counts.values():
            if count == 3:
                return True

        # Se não encontrar trinca, retorna False
        return False

    def _has_straight(self, private_cards, board_cards):
        """
        Verifica se há uma sequência de cinco cartas seguidas considerando as cartas privadas e as cartas do board.

        Parâmetros:
        - private_cards: As cartas privadas do jogador.
        - board_cards: As cartas do board.

        Retorna:
        - True se houver uma sequência de cinco cartas seguidas nas cartas privadas e no board; False caso contrário.
        """
        # Combina as cartas privadas e as cartas do board em uma lista
        all_cards = private_cards + board_cards

        # Ordena as cartas por rank
        all_cards.sort(key=lambda card: card.rank.value)

        # Verifica se há uma sequência de cinco cartas seguidas
        for i in range(len(all_cards) - 4):
            # Verifica se as cartas são consecutivas
            if (all_cards[i + 4].rank.value - all_cards[i].rank.value == 4 and
                len(set(card.rank.value for card in all_cards[i:i + 5])) == 5):
                return True

        # Se não encontrar uma sequência, retorna False
        return False
    
    def _has_flush(self, private_cards, board_cards):
    # Combina as cartas privadas e as cartas do board
        all_cards = private_cards + board_cards

        # Conta as ocorrências de cada naipe
        suit_counts = {}
        for card in all_cards:
            suit = card.suit
            if suit in suit_counts:
                suit_counts[suit] = suit_counts[suit] + 1
            else:
                suit_counts[suit] = 1

        # Verifica se algum naipe tem pelo menos cinco cartas
        for count in suit_counts.values():
            if count >= 5:
                return True
        return False

    def _has_full_house(self, private_cards, board_cards):
        all_cards = private_cards + board_cards

        # Conta as ocorrências de cada rank
        rank_counts = {}
        for card in all_cards:
            rank = card.rank.value
            if rank in rank_counts:
                rank_counts[rank] += 1
            else:
                rank_counts[rank] = 1

        # Verifica se há um três de um tipo e um par
        has_three = False
        has_pair = False
        for count in rank_counts.values():
            if count >= 3:
                if not has_three:
                    has_three = True
                else:
                    has_pair = True
            elif count == 2:
                has_pair = True

        return has_three and has_pair

    def _has_four_of_a_kind(self, private_cards, board_cards):
        all_cards = private_cards + board_cards

        # Conta as ocorrências de cada rank
        rank_counts = {}
        for card in all_cards:
            rank = card.rank.value
            if rank in rank_counts:
                rank_counts[rank] += 1

        # Verifica se há quatro de um tipo
        for count in rank_counts.values():
            if count >= 4:
                return True
        return False

    def _has_straight_flush(self, private_cards, board_cards):
        all_cards = private_cards + board_cards

        # Agrupa as cartas por naipe e verifica a sequência em cada grupo
        suit_groups = {}
        for card in all_cards:
            suit = card.suit
            if suit not in suit_groups:
                suit_groups[suit] = []
            suit_groups[suit].append(card)

        # Verifica cada grupo de naipe para uma sequência
        for group in suit_groups.values():
            if len(group) >= 5:
                group.sort(key=lambda card: card.rank.value)
                for i in range(len(group) - 4):
                    if (group[i + 4].rank.value - group[i].rank.value == 4):
                        return True
        return False

    def _has_royal_flush(self, private_cards, board_cards):
        all_cards = private_cards + board_cards

        # Agrupa as cartas por naipe e verifica a sequência específica em cada grupo
        suit_groups = {}
        for card in all_cards:
            suit = card.suit
            if suit not in suit_groups:
                suit_groups[suit] = []
            suit_groups[suit].append(card)

        # Verifica cada grupo de naipe para a sequência específica
        royal_flush_rank_set = {10, 11, 12, 13, 14}  # 10, J, Q, K, A
        for group in suit_groups.values():
            if len(group) >= 5:
                rank_set = {card.rank.value for card in group}
                if royal_flush_rank_set <= rank_set:
                    return True
        return False

