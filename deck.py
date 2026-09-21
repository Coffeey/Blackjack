from random import choice
from data import CARD_VALUES

class Deck():
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        for card in CARD_VALUES:
            for i in range(4):
                self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def deal_one(self):
        card = choice(self.cards)
        self.remove(card)
        return card
    