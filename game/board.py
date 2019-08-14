from game.player_manager import Manager


class Board:

    def __init__(self, number_of_decks, min_bet):
        self.manager = Manager(number_of_decks, min_bet)

    def connect(self, sid, name):
        return self.manager.connect(sid, name)

    def disconnect(self, sid):
        return self.manager.disconnect(sid)

    def get_player(self, sid):
        return self.manager.players.get(sid)

    def update_big_small(self):
        if self.manager.small_blind is None:
            return self.manager.start_small_big_blind()

        return self.manager.update_small_big_blind()

    def current_player(self):
        return self.manager.get_current_player()

    def make_play(self, sid, play_name, bet=0):
        self.manager.make_play(sid, play_name, bet)

        return self.manager.check_plays()

    def get_table(self):
        return self.manager.get_table()

    def update_table(self, number_of_cards=1):
        self.manager.update_table(number_of_cards)
