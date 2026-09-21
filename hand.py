from data import CARD_VALUES

class Hand:
    def __init__(self, owner):
        self.owner = owner
        self.cards = []

    @property
    def value(self):
        return self.compute_value()
    
    def add(self, card):
        self.cards.append(card)

    def compute_value(self):
        total = sum(CARD_VALUES[c] for c in self.cards)
        aces = self.cards.count("A")
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total

    def is_bust(self):
        return self.value > 21

    def hit(self, deck):
        card = deck.deal_one()
        self.add(card)
        return card

    def reset(self):
        self.cards = []

    def natural(self):
        return len(self.cards) == 2 and self.value == 21