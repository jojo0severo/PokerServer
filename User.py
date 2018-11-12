from socketIO_client import SocketIO, LoggingNamespace
import sys

sys.setrecursionlimit(10000)
connected = False
all_players_played = False


def on_receive_hand(message):
    [print(value) for value in message]
    print('\n')


def bet_received(message):
    global all_players_played
    all_players_played = True
    print(message + '\n\n')


def on_users_connected(message):
    global connected
    connected = True


def on_response(message):
    print('\nResponse: ' + message + '\n')

    if message.lower().__contains__('create another nickname'):
        exit(-1)


# connection
def connection():
    socketIO.on('response', on_response)
    socketIO.on('cards', on_receive_hand)
    socketIO.emit('connect_user', name)
    socketIO.wait(5)


def wait_users():
    socketIO.on('users_connected', on_users_connected)
    socketIO.emit('wait_connections', name)
    while not connected:
        socketIO.wait(5)


def wait_plays(bet):
    socketIO.on('plays_done', bet_received)
    socketIO.emit('play', {'play': 'bet', 'name': name, 'bet': bet})
    while not all_players_played:
        socketIO.wait(3)


def match():
    while True:
        option = input('	If you want to quit (pussy): 1\n'
                       '	If you want to bet (will lose anyway, just know it): 2\n'
                       '	If you are pissed with the game (extremaly pussy): 3\n')

        if option == '2':
            bet = input('Gimme your bet, motherfucker:\n')
            print('Waiting for other motherfucker players')
            wait_plays(bet)

        elif option == '1':
            print('Just know that you are a pussy, motherfucker')
            socketIO.emit('remove_player', name)
            socketIO.wait(2)
            print('Say the exit code slowly and out loud')
            print('Process finished with exit code 104')
            exit(0)

        elif option == '3':
            print('I don´t give a fuck')
            socketIO.emit('remove_money', name)
            print('Just removed 300 from your wallet, bitch')
            socketIO.wait(3)

        else:
            print('Are you stupid?\nI guess you are...\nChoose a valid option -_-')


if __name__ == '__main__':
    socketIO = SocketIO('localhost', 5000, LoggingNamespace)
    name = input('Informe seu nome:\n')

    connection()
    wait_users()
    match()
