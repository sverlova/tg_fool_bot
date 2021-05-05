class Player:
    def __init__(self, uid):
        self.cards = []
        self.user_id = uid

class Card:
    symbols = ['♥️', '♦️', '♠️', '♣️']

    def create_from_val_suit(self, value, suit):
        self.value = value
        self.suit = suit

    def create_from_text(self, s):
        if len(s) == 4:
            self.value = 10
        elif s[0] in ['J', 'Q', 'K', 'A']:
            self.value = ['J', 'Q', 'K', 'A'].index(s[0]) + 11
        else:
            self.value = int(s[0])
        self.suit = Card.symbols.index(s[-2:])

    def __init__(self, value, suit=-1):
        if suit == -1:
            self.create_from_text(value)
        else:
            self.create_from_val_suit(value, suit)

    def get_deck(cards_count=36):
        deck = None
        if cards_count == 36:
            deck = [Card(i, j) for i in range(6, 15) for j in range(4)]
        elif cards_count == 52:
            deck = [Card(i, j) for i in range(2, 15) for j in range(4)]
        return deck

    def __str__(self):
        s = None
        if self.value <= 10:
            s = str(self.value)
        else:
            s = (['J', 'Q', 'K', 'A'])[self.value - 11]
        s += Card.symbols[self.suit]
        return s

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

class Move:
    def __init__(self):
        self.who = None
        self.is_end = False
        self.error = False
        self.replic = None
        self.defended = False
        self.attacked = False
        self.took = False
        self.bito = False
        self.card = None
