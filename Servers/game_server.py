import time
import threading
from flask import Flask
from flask_socketio import SocketIO, emit
from Game.board import Board

app = Flask(__name__)
socketIO = SocketIO(app)

connected_users = []
admin = None
thread_connections = None
thread_plays = None


@socketIO.on('connect_user')
def connect_user(message):
    global connected_users, admin

    if len(connected_users) == 5:
        emit('response', 'Number of players already satisfied')
        return

    if message not in board.users:
        board.add_user(message)

        if admin == None:
            admin = board[message]

        emit('response', 'Connected motherfucker')
        emit('cards', board.get_hand(message))

    else:
        emit('response', 'Create another nickname motherfucker')
        return

    if message.__contains__('fucker'):
        emit('response', 'That´s the spirit motherfucker')


@socketIO.on('terminate/'+str(admin))
def quit_game():
    board.clear_round()
    thread_connections = None
    exit(0)


@socketIO.on('remove_player')
def remove_player(message):
    board.remove_user(message)


@socketIO.on('remove_money')
def remove_money(message):
    board[message].remove_money(300)


@socketIO.on('play')
def do_plays(message):
    board.do_play(message)


# ================= PARALLEL FUNCTIONS =====================
@socketIO.on('wait_connections')
def wait_connections(message='^'):
    global connected_users
    connected_users.append(message)
    print('entrou em connections')

    while len(connected_users) < 2 + 1:
        time.sleep(3)
        print('Waiting connections')

    with app.app_context():
        socketIO.emit('users_connected', 'All motherfuckers connected')


def wait_all_plays():
    while True:
        while not board.manage_match():
            time.sleep(3)
            print('waiting for other players to play')

        with app.app_context():
            socketIO.emit('plays_done', 'All motherfuckers played')
            low_bet_players, quit_players = board.verify_plays()

            if not low_bet_players:
                board.clear_round()
                continue

            board.count_plays -= len(low_bet_players)

            for bigger in low_bet_players:
                for player in low_bet_players[bigger]:
                    socketIO.emit('plays_done/' + player, 'You must increase your bet to: ' + bigger +
                                  '\nIn order to continue playing (you can still quit, pussy)')


if __name__ == "__main__":
    board = Board()

    thread_connections = threading.Thread(target=wait_connections)
    thread_connections.start()

    time.sleep(1)

    thread_plays = threading.Thread(target=wait_all_plays)
    thread_plays.start()

    socketIO.run(app, host='0.0.0.0', port='5000')

