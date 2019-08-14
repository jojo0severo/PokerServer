import random
from game.user import User
from game.deck import Deck


class Manager:
    def __init__(self, number_of_decks, min_bet):
        self.small_blind = None
        self.big_blind = None
        self.current_player = None
        self.small_blind_bet = min_bet
        self.players = {}
        self.table_cards = []
        self.cards = Deck()
        self.cards.load_deck(number_of_decks)

    def connect(self, sid, name):
        if sid in self.players:
            return False

        self.players[sid] = User(sid, name, self.cards.hand_view_format([self.cards.get_card_image(card).split('\n') for card in self.cards.get_cards(2)]))
        return True

    def disconnect(self, sid):
        if sid in self.players:
            del self.players[sid]
            return True

        return False

    def start_small_big_blind(self):
        self.small_blind = random.choice(list(self.players.keys()))
        for idx, user in enumerate(self.players.keys()):
            if user == self.small_blind:
                if idx + 1 == len(self.players.keys()):
                    self.big_blind = list(self.players.keys())[0]
                else:
                    self.big_blind = list(self.players.keys())[idx + 1]
                break

        self.players[self.small_blind].small_blind = True
        self.players[self.big_blind].big_blind = True
        self.set_current_player()

        return self.small_blind, self.big_blind

    def update_small_big_blind(self):
        self.players[self.big_blind].big_blind = False
        self.players[self.small_blind].small_blind = False

        for idx, user in enumerate(self.players.keys()):
            if user == self.big_blind:
                self.small_blind = user
                if idx + 1 == len(self.players.keys()):
                    self.big_blind = list(self.players.keys())[0]
                else:
                    self.big_blind = list(self.players.keys())[idx + 1]

                break

        self.players[self.small_blind].small_blind = True
        self.players[self.big_blind].big_blind = True
        self.set_current_player()

        return self.small_blind, self.big_blind

    def set_current_player(self):
        for idx, user in enumerate(self.players.keys()):
            if user == self.big_blind:
                if idx == len(self.players.keys()):
                    self.current_player = list(self.players.keys())[0]
                else:
                    self.current_player = list(self.players.keys())[idx]

                break

    def get_current_player(self):
        for idx, user in enumerate(self.players.keys()):
            if user == self.current_player:
                if idx + 1 == len(self.players.keys()):
                    self.current_player = list(self.players.keys())[0]
                else:
                    self.current_player = list(self.players.keys())[idx + 1]

                break

        return self.current_player

    def make_play(self, sid, play_name, bet):
        self.players[sid].last_bet = bet
        self.players[sid].played = True

    def check_plays(self):
        max_bet = -1
        for sid in self.players:
            if not self.players[sid].played:
                return False

            if max_bet == -1:
                max_bet = self.players[sid].last_bet

            elif self.players[sid].last_bet < max_bet:
                return False

        for sid in self.players:
            self.players[sid].played = False
            self.players[sid].last_bet = -1

        return True

    def get_table(self):
        return self.cards.hand_view_format([self.cards.get_card_image(card).split('\n') for card in self.table_cards])

    def update_table(self, number_of_cards):
        self.table_cards.extend(self.cards.get_cards(number_of_cards))

