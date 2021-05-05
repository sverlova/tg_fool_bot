from fool_bot.entities import *
from fool_bot import replics
import random

class Game:
    def __init__(self, key, creator, cards_count=36):
        self.key = key
        self.started = False
        self.creator = creator
        self.players = []
        self.deactivated_players = []
        self.deck = Card.get_deck(cards_count)
        self.trump = None
        self.turn = None
        self.table = []
        self.result = None

    def add_player(self, uid):
        self.players.append(Player(uid))

    def give_cards(self, player):
        while len(self.players[player].cards) < 6 and len(self.deck) > 0:
            self.players[player].cards.append(self.deck.pop())

    def get_card_key(self, card):
        return (card.suit == self.trump, card.value)

    def sort_cards(self, player):
        self.players[player].cards.sort(key=self.get_card_key, reverse=True)

    def prepare(self):
        for i in range(len(self.players)):
            self.give_cards(i)
            self.sort_cards(i)
        self.table = []
        self.move_end = False
        if type(self.turn) == int:
            self.turn = (self.turn + 1) % len(self.players)

    def initialise(self):
        random.shuffle(self.deck)
        self.trump = self.deck[0].suit

        self.prepare()
        num = len(self.players)
        self.turn = 0
        for i in range(num):
            if self.players[i].cards[0].suit == self.trump and (self.players[i].cards[self.turn].suit
                != self.trump or self.players[self.turn].cards[0].value < self.players[i].cards[0].value):
                self.turn = i

    def can_attack(self, card):
        were = list(map(lambda c: c.value, self.table))
        return len(were) == 0 or card.value in were

    def can_defend(self, card):
        c = self.table[-1]
        return card.suit == self.trump and (c.suit != self.trump or
            card.value > c.value) or card.suit == c.suit and card.value > c.value

    def attack(self, text):
        result = Move()
        num = self.turn
        if text.lower() == replics.finish:
            self.move_end = True
            result.finish = True
        else:
            card = None

            try:
                card = Card(text)
            except:
                result.replic = replics.not_known_action
                result.error = True
                return result

            if not(card in self.players[num].cards):
                result.replic = replics.have_not_card
                result.error = True
            elif not self.can_attack(card):
                result.replic = replics.cant_use_card
                result.error = True
            else:
                self.table.append(card)
                self.players[num].cards.remove(card)
                result.attacked = True
                result.card = card

        return result

    def defend(self, text):
        result = Move()
        num = (self.turn + 1) % len(self.players)

        if text.lower() == replics.take:
            self.move_end = True
            result.took = True
            for c in self.table:
                self.players[num].cards.append(c)
            self.turn += 1
        else:
            card = None

            try:
                card = Card(text)
            except:
                result.replic = replics.not_known_action
                result.error = True
                return result

            if not(card in self.players[num].cards):
                result.replic = replics.have_not_card
                result.error = True
            elif not self.can_defend(card):
                result.replic = replics.cant_use_card
                result.error = True
            else:
                self.table.append(card)
                self.players[num].cards.remove(card)
                result.defended = True
                result.card = card

        return result

    def is_end_of_move(self):
        attacker = self.turn
        defender = (self.turn + 1)  % len(self.players)
        return self.move_end or len(self.players[attacker].cards) == 0 or len(self.players[defender].cards) == 0

    def next_player(self):
        next_p = self.players[self.turn].user_id
        if len(self.table) % 2 == 1:
            next_p = self.players[(self.turn + 1) % len(self.players)].user_id
        return next_p

    def move(self, uid, text):
        attacker = self.turn
        defender = (self.turn + 1) % len(self.players)
        cnt = len(self.table)

        result = Move()
        result.replic = replics.not_your_move
        result.error = True
        if self.players[attacker].user_id == uid and cnt % 2 == 0:
            result = self.attack(text)
        elif self.players[defender].user_id == uid and cnt % 2 == 1:
            result = self.defend(text)

        if self.is_end_of_move():
            self.prepare()

        result.who = uid

        return result
