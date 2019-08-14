import sys
import json
import time
import socketio
import eventlet
from eventlet import wsgi
from game.board import Board


socket = socketio.Server()
app = socketio.WSGIApp(socket)

connected_players = 0
number_of_bets = 0


@socket.event
def connect_user(sid, data):
    global connected_players

    if number_of_players == connected_players:
        return json.dumps({'result': False, 'status': 1, 'message': 'All users already connected.'})

    try:
        data = json.loads(data)

        if 'name' not in data:
            return json.dumps({'result': False, 'status': 4, 'message': 'Key not found.'})

        else:
            if board.connect(sid, data['name']):
                user = board.get_player(sid)
                if user is not None:
                    connected_players += 1
                    if connected_players == number_of_players:
                        board.update_big_small()
                        board.update_table(3)
                        table_cards = board.get_table()
                        for sid in board.manager.players:
                            socket.emit('game_started',
                                        data=json.dumps({'user': board.get_player(sid).json(), 'table': table_cards}),
                                        room=sid)

                        socket.emit('play', room=board.current_player())

                    return json.dumps({'result': True, 'status': 2, 'message': 'User connected.'})

                else:
                    return json.dumps({'result': False, 'status': 5, 'message': 'Possible internal error.'})

    except TypeError:
        return json.dumps({'result': False, 'status': 3, 'message': 'Wrong format.'})

    except json.JSONDecodeError:
        return json.dumps({'result': False, 'status': 3, 'message': 'Wrong format.'})


@socket.event
def make_play(sid, data):
    try:
        data = json.loads(data)

        if board.get_player(sid) is None:
            return json.dumps({'result': False, 'status': 4, 'message': 'User not found.'})

        elif board.get_player(sid).played:
            return json.dumps({'result': False, 'status': 4, 'message': 'User already sent play.'})

        elif 'bet' not in data:
            return json.dumps({'result': False, 'status': 4, 'message': 'Key not found.'})

        elif 'play' not in data:
            return json.dumps({'result': False, 'status': 4, 'message': 'Key not found.'})

        if board.make_play(sid, data['play'], data['bet']):
            board.update_big_small()
            board.update_table()
            table_cards = board.get_table()
            for sid in board.manager.players:
                socket.emit('round_finished',
                            data=json.dumps({'user': board.get_player(sid).json(), 'table': table_cards}), room=sid)

        c = board.current_player()
        print(c)
        socket.emit('play', room=c)

        return json.dumps({'result': True, 'status': 2, 'message': ''})

    except TypeError:
        return json.dumps({'result': False, 'status': 3, 'message': 'Wrong format.'})

    except json.JSONDecodeError:
        return json.dumps({'result': False, 'status': 3, 'message': 'Wrong format.'})


if __name__ == '__main__':
    params = sys.argv[1:]

    if len(params) == 1:
        number_of_players = 2
        board = Board(int(params[0]), 2)
    elif len(params) == 2:
        number_of_players = int(params[0])
        board = Board(int(params[1]), 2)
    else:
        number_of_players = 2
        board = Board(1, 2)

    wsgi.server(eventlet.listen(('', 8910)), app)
