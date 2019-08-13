class User:
    def __init__(self, sid, name, cards):
        self.sid = sid
        self.name = name
        self.money = 1000
        self.cards = cards
        self.small_blind = False
        self.big_blind = False
        self.played = False
        self.last_bet = -1

    def hand(self):
        return self.cards

    def receive_money(self, money):
        self.money += money

    def remove_money(self, money):
        if self.money - money > 0:
            self.money -= money
            return True

        else:
            self.money = 0
            return False
