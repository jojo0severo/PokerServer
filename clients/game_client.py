import json
import socketio


client = socketio.Client()


class Client:
    def __init__(self, address):
        self.socket = socketio.Client()
        self.socket.connect(f'http://{address}:8910')
        self.response = None
        self.define_endpoints()

    def define_endpoints(self):
        self.socket.on('game_started', self.play)
        self.socket.on('play_response', self.result)

    def start(self, name):
        self.socket.emit('connect_user', data=json.dumps({'name': name}), callback=self.save_response)

        while self.response is None:
            pass

        if not self.response['result']:
            exit(self.response['message'])

        else:
            self.format_response()

    def play(self, args):
        input('Faça sua jogada:\n')
        pass

    def result(self, args):
        pass

    def save_response(self, resp):
        self.response = json.loads(resp)

    def format_response(self):
        print('Nome:', self.response['json']['name'])
        print('Dinheiro:', self.response['json']['money'])
        print(self.response['json']['hand'])


if __name__ == '__main__':
    c = Client('10.132.241.146')
    c.start('pedro')
