from collections import defaultdict
from Game.cards import Cards
from Game.users import User


class Board:

    def __init__(self):
        self.cards = Cards()
        self.users = defaultdict()

        self.players_plays = defaultdict()
        self.quit_players = []
        self.count_plays = 0

    def add_user(self, name):
        self.users[name] = User(name, self.cards.get_hand())

    def __getitem__(self, name):
        return self.users[name]

    def do_play(self, play):
        self.count_plays += 1

        if play['type'] == 'quit':
            self.quit_players.append(play['name'])
            del self.users[play['name']]

        else:
            self.players_plays[play['name']] = play['data']

    def manage_match(self):
        if self.count_plays < len(self.users):
            return False

        return True

    def get_hand(self, name):
        return self.users[name].get_hand()

    def verify_plays(self):
        increase_bet, bigger_bet = defaultdict(), 0

        for i in self.players_plays.keys():
            if self.players_plays[i] == 'bet':
                if bigger_bet < self.players_plays[i]['data']:
                    bigger_bet = float(self.players_plays[i]['data'])

        if bigger_bet == 0:
            return [], self.quit_players

        for i in self.players_plays:
            if self.players_plays[i]['data'] is None or self.players_plays[i]['data'] < bigger_bet:
                increase_bet[bigger_bet].append(i)

        return increase_bet, self.quit_players

    def remove_user(self, name):
        del self.users[name]

    def clear_round(self):
        self.players_plays.clear()
        self.quit_players.clear()
        self.count_plays = 0