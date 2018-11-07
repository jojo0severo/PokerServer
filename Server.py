import time
from random import choice
from flask import Flask
from flask_socketio import SocketIO, emit
from collections import defaultdict
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketIO = SocketIO(app)

deck = defaultdict()
users = {}


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


@socketIO.on('connect_user')
def connect_user(message):
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


@socketIO.on('bet')
def manage_bets(message):
	data = message
	users[data['name']]['money'] -= data['bet']

	emit('bet_done', users[data['name']]['money'])


@socketIO.on('remove_player')
def remove_player(message):
	del users[message]


@socketIO.on('remove_money')
def remove_money(message):
	users[message]['money'] -= 300


def wait_connections():
	while len(users) < 1:
		time.sleep(4)
		print('Waiting connections')

	with app.app_context():
		socketIO.emit('users_connected', 'All motherfuckers connected')


if __name__ == "__main__":
	initialize_deck()
	eventlet.spawn(wait_connections)
	socketIO.run(app, host='0.0.0.0')
