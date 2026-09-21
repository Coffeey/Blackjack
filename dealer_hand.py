from hand import Hand

class DealerHand(Hand):
    def __init__(self):
        super().__init__("dealer")
        self.revealed=False

    def reset(self):
        self.revealed = False
        return super().reset()