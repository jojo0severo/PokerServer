class User:
    def __init__(self, name, cards):
        self.name = name
        self.money = 1000
        self.cards = cards

    def remove_money(self, decrease):
        self.money -= decrease

        if self.money > 0:
            return True

        else:
            return False

    def receive_money(self, increase):
        self.money += increase

    def get_hand(self):
        return self.cards