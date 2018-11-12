import time
import threading
from random import choice
from flask import Flask
from flask_socketio import SocketIO, emit
from collections import defaultdict
# import eventlet


app = Flask(__name__)
socketIO = SocketIO(app)

deck = defaultdict()
users = defaultdict()
connected = []
plays = []


def get_hand():
    hand = []
    for i in range(2):
        cards = list(deck.keys())
        value = choice(cards)
        suit_card = choice(list(deck[value]))

        hand.append('Value:' + value + '\nSuit:' + suit_card)
        deck[value].remove(suit_card)

        if len(deck[value]) == 0:
            del deck[value]

    return hand


def initialize_deck():
    naipes = ['Ouros', 'Paus', 'Copas', 'Espadas']
    cartas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    for card in cartas:
        deck[card] = []
        for naipe in naipes:
            deck[card].append(naipe)


def manage_bets(message):
    plays.append(message['name'])
    users[message['name']]['money'] -= int(message['bet'])


@socketIO.on('connect_user')
def connect_user(message):
    global connected
    print(str(connected) + 'lista no connect_user')
    if len(connected) == 5:
        emit('response', 'Number of players already satisfied')
        return
    if message not in users:
        cards = get_hand()
        users[message] = {'money': 1000, 'cards': cards}
        emit('response', 'Connected motherfucker')
        emit('cards', cards)

    else:
        emit('response', 'Create another nickname motherfucker')
        return

    if message.__contains__('fucker'):
        emit('response', 'That´s the spirit motherfucker')


@socketIO.on('remove_player')
def remove_player(message):
    del users[message]


@socketIO.on('remove_money')
def remove_money(message):
    users[message]['money'] -= 300


@socketIO.on('wait_connections')
def wait_connections(message='^'):
    global connected
    connected.append(message)
    print('entrou em connections e adicionou na lista')
    print(str(connected) + ' lista no wait_connections')

    while len(connected) < 2 + 1:
        time.sleep(4)
        print('Waiting connections')

    with app.app_context():
        socketIO.emit('users_connected', 'All motherfuckers connected')


@socketIO.on('play')
def handle_plays(message):
    if message['play'] == 'bet':
        manage_bets(message)

    pass


def manage_match(none=()):
    print('entrou no manage match')
    while len(plays) < len(connected):
        time.sleep(3)
        print('waiting players to play')

    with app.app_context():
        socketIO.emit('plays_done', 'All motherfuckers played')


def run_socket():
    socketIO.run(app, host='0.0.0.0', port='5000')


if __name__ == "__main__":
    initialize_deck()
    thread_connections = threading.Thread(target=wait_connections)
    thread_connections.start()

    time.sleep(1)

    thread_plays = threading.Thread(target=manage_match)
    thread_plays.start()

    aux = threading.Thread(target=run_socket)
    aux.start()
    print()

