from games.hlpoker.card import Card

def is_straight(cards):
    """ Verifica se as cartas formam uma sequência (straight). """
    ranks = sorted(card.rank.value for card in cards)
    return ranks == list(range(min(ranks), min(ranks) + 5))

def is_flush(cards):
    """ Verifica se as cartas formam um flush (todas as cartas são do mesmo naipe). """
    suits = [card.suit for card in cards]
    return len(set(suits)) == 1

def count_ranks(cards):
    """ Conta quantas vezes cada rank aparece nas cartas. """
    rank_count = {}
    for card in cards:
        if card.rank not in rank_count:
            rank_count[card.rank] = 0
        rank_count[card.rank] += 1
    return rank_count

def is_three_of_a_kind(cards):
    """ Verifica se as cartas formam um trio (three of a kind). """
    rank_count = count_ranks(cards)
    return 3 in rank_count.values()

def is_two_pairs(cards):
    """ Verifica se as cartas formam dois pares (two pairs). """
    rank_count = count_ranks(cards)
    return list(rank_count.values()).count(2) == 2

def is_full_house(cards):
    """ Verifica se as cartas formam um full house (três cartas iguais + um par). """
    rank_count = count_ranks(cards)
    return 3 in rank_count.values() and 2 in rank_count.values()

def is_four_of_a_kind(cards):
    """ Verifica se as cartas formam um poker (four of a kind). """
    rank_count = count_ranks(cards)
    return 4 in rank_count.values()
