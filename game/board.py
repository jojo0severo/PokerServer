from game.player_manager import Manager


class Board:

    def __init__(self, number_of_decks, min_bet):
        self.manager = Manager(number_of_decks, min_bet)

    def connect(self, sid, name):
        return self.manager.connect(sid, name)

    def disconnect(self, sid):
        return self.manager.disconnect(sid)

    def update_big_small(self):
        if self.manager.small_blind is None:
            return self.manager.start_small_big_blind()

        return self.manager.update_small_big_blind()

    def current_player(self):
        return self.manager.get_current_player()

    def make_play(self, sid, play_name):
        self.manager.make_play(sid, play_name)

        return self.manager.check_plays()
