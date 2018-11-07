from socketIO_client import SocketIO, LoggingNamespace
import time
import sys


def wait():
	if not connected:
		time.sleep(3)
		try:
			wait()
		except:
			print('Users didn´t connect n time')
			exit(-1)
	else:
		return


def on_receive_hand(message):
	[print(value) for value in message]
	print('\n')


def bet_received(message):
	print(message + '\n\n')


def on_users_connected(message):
	connected = True


def on_response(message):
	print('\nResponse: ' + message + '\n')

	if message.lower().__contains__('create another nickname'):
		exit(-1)


sys.setrecursionlimit(10000)

socketIO = SocketIO('localhost', 5000, LoggingNamespace)
name = input('Informe seu nome:\n')
connected = False

# connection
socketIO.on('response', on_response)
socketIO.on('users_connected', on_users_connected)
socketIO.on('cards', on_receive_hand)
socketIO.emit('connect_user', name)
socketIO.wait(5)

wait()

print('Game started')
while True:
	option = input('	If you want to quit (pussy): 1\n'
				   '	If you want to bet (will lose anyway, just know it): 2\n'
				   '	If you are pissed with the game (extremaly pussy): 3\n')

	if option == '2':
		bet = input('Gimme your bet, motherfucker:\n')
		socketIO.on('bet_done', bet_received)
		socketIO.emit('bet', bet)
		socketIO.wait(3)

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
