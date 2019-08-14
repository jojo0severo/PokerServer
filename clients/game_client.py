import json
import time
import socketio


client = socketio.Client()


class Client:
    def __init__(self, address):
        self.socket = socketio.Client()
        self.socket.connect(f'http://{address}:8910')
        self.response = None
        self.define_endpoints()

    def define_endpoints(self):
        self.socket.on('game_started', self.show_info)
        self.socket.on('round_finished', self.show_info)
        self.socket.on('play', self.ask_play)

    def start(self, name):
        self.socket.emit('connect_user', data=json.dumps({'name': name}), callback=self.save_response)

        while self.response is None:
            pass

        if not self.response['result']:
            exit(self.response['message'])

    def ask_play(self, _):
        time.sleep(.2)
        input('\n\nFaça sua jogada:\n')
        print('\n')
        self.socket.emit('make_play', data=json.dumps({'play': 'a', 'bet': 0}), callback=self.save_response)

    def show_info(self, msg):
        while self.response is None:
            pass

        if not self.response['result']:
            exit(self.response['message'])

        msg = json.loads(msg)
        print('Nome:', msg['user']['name'], '\n' + 'Dinheiro:',
              msg['user']['money'], '\n' + msg['user']['hand'], '\n\n', 'Mesa:\n' + ''.join(msg['table']))

        if msg['user']['small_blind']:
            print('You are the small blind')

        elif msg['user']['big_blind']:
            print('You are the big blind')

        self.response = None

    def save_response(self, resp):
        self.response = json.loads(resp)


if __name__ == '__main__':
    c = Client('10.132.241.146')
    c.start('pedro')
