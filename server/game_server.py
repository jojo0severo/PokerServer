import sys
import time
import json
import socketio
import eventlet
import multiprocessing
from multiprocessing import Queue
from eventlet import wsgi
from game.board import Board


socket = socketio.Server()
app = socketio.WSGIApp(socket)
connected_players = 0
number_of_bets = 0


def control_first_round():
    while connected_players < number_of_players:
        time.sleep(.5)

    small_blind, big_blind = board.get_small_big_blind()


def control_bets():
    while number_of_bets < connected_players:
        time.sleep(.5)

    bets = board.get_bets()


@socket.event
def connect_user(sid, data):
    global connected_players

    if number_of_players == connected_players:
        return json.dumps({'result': False, 'status': 1, 'json': {}, 'message': 'All users already connected.'})

    try:
        data = json.loads(data)

        if 'name' not in data:
            return json.dumps({'result': False, 'status': 4, 'data': {}, 'message': 'Key not found.'})

        else:
            if board.connect(sid, data['name']):
                user = board.get_user(sid)
                if user is not None:
                    info = {
                        'name': user.name,
                        'hand': user.hand(),
                        'money': user.money
                    }

                    connected_players += 1

                    return json.dumps({'result': True, 'status': 2, 'json': info, 'message': 'User connected.'})

                else:
                    return json.dumps({'result': False, 'status': 5, 'json': {}, 'message': 'Possible internal error.'})

    except TypeError:
        return json.dumps({'result': False, 'status': 3, 'data': {}, 'message': 'Wrong format.'})

    except json.JSONDecodeError:
        return json.dumps({'result': False, 'status': 3, 'data': {}, 'message': 'Wrong format.'})


if __name__ == '__main__':
    params = sys.argv[1:]

    if len(params) == 1:
        number_of_players = 2
        board = Board(params[0])
    elif len(params) == 2:
        number_of_players = params[0]
        board = Board(params[1])
    else:
        number_of_players = 2
        board = Board(1)

    connected_players_queue = Queue()
    connect_players = multiprocessing.Process(target=control_first_round, args=(connected_players_queue,))
    wsgi.server(eventlet.listen(('', 8910)), app)
