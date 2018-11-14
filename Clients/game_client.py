from socketIO_client import SocketIO, LoggingNamespace


all_users_connected = False
all_players_played = False
name = ''


# ======= CONNECT WITH THE SERVER AND GET THE INFORMATION
def on_receive_hand(message):
    [print(value) for value in message]
    print('\n')


def on_response(message):
    print('\nResponse: ' + message + '\n')

    if message.lower().__contains__('create another nickname') or message.lower().__contains__('already satisfied'):
        exit(-1)


def connection():
    socketIO.on('response', on_response)
    socketIO.on('cards', on_receive_hand)
    socketIO.emit('connect_user', name)
    socketIO.wait(5)


#  ============ WAITS FOR ALL THE PLAYERS TO CONNECT =========
def on_users_connected(message):
    global all_users_connected
    all_users_connected = True

    print(message + '\n\n')


def wait_users():
    socketIO.on('users_connected', on_users_connected)
    socketIO.emit('wait_connections', name)

    while not all_users_connected:
        socketIO.wait(1)


# =========== WAITS FOR ALL THE PLAYERS TO PLAY ===============
def bet_received(message):
    global all_players_played
    all_players_played = True
    print(message + '\n\n')


def wait_plays(kind, bet):
    if kind == 'bet':
        socketIO.on('plays_done', bet_received)
        socketIO.emit('play', {'type': 'bet', 'name': name, 'data': bet})

    else:
        socketIO.on('plays_done', bet_received)
        socketIO.emit('play', {'type': 'quit', 'name': name, 'data': None})

    while not all_players_played:
        socketIO.wait(1)


# ============ SHOW THE OPTIONS OF EACH MATCH ================

def match():
    while True:
        option = input('	If you want to quit (pussy): 1\n'
                       '	If you want to bet (will lose anyway, just know it): 2\n'
                       '	If you are pissed with the game (extremaly pussy): 3\n')

        if option == '1':
            print('Just know that you are a pussy, motherfucker')
            socketIO.emit('remove_player', name)
            socketIO.wait(5)
            print('Say the exit code slowly and out loud')
            print('Process finished with exit code 104')
            exit(0)

        elif option == '2':
            bet = input('Gimme your bet, motherfucker:\n')
            print('Waiting for other motherfucker players')
            wait_plays('bet', bet)

        elif option == '3':
            print('I don´t give a fuck')
            socketIO.emit('remove_money', name)
            print('Just removed 300 from your wallet, bitch')
            socketIO.wait(5)

        else:
            print('Are you stupid?\nI guess you are...\nChoose a valid option -_-')


if __name__ == '__main__':
    socketIO = SocketIO('localhost', 5000, LoggingNamespace)
    name = input('Informe seu nome:\n')

    connection()
    wait_users()
    match()
