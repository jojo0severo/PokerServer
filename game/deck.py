import pathlib
from random import choice


class Deck:

    def __init__(self):
        self.deck = {}
        self.table = []
        self.plays = []

    def load_deck(self, number_of_decks):
        suits = ['ouros', 'paus', 'copas', 'espadas'] * number_of_decks
        cards = ['As', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * number_of_decks

        for card in cards:
            self.deck[card] = []
            for suit in suits:
                self.deck[card].append(suit)

    def get_cards(self, number_of_cards):
        hand = []
        for i in range(number_of_cards):
            cards = list(self.deck.keys())
            value = choice(cards)
            suit = choice(list(self.deck[value]))

            hand.append({'value': value, 'suit': suit})
            self.deck[value].remove(suit)

            if len(self.deck[value]) == 0:
                del self.deck[value]

        return hand

    @staticmethod
    def hand_view_format(lines, amount_by_line=10):
        hand_image = []
        for i in range(int(len(lines)/amount_by_line) + 1):
            for j in range(len(lines[0])):
                current_line = ''
                for idx, line in enumerate(lines[i * amount_by_line: (i+1) * amount_by_line]):
                    current_line += line[j] + ' '
                    if j == 0:
                        current_line += ' '

                hand_image.append(current_line)

        return '\n'.join(hand_image)

    @staticmethod
    def get_card_image(card):
        file = pathlib.Path(__file__).parent / 'cards_images' / card['value']

        if card['suit'] == 'ouros':
            file /= 'diamonds.txt'

        elif card['suit'] == 'paus':
            file /= 'clubs.txt'

        elif card['suit'] == 'copas':
            file /= 'hearts.txt'

        elif card['suit'] == 'espadas':
            file /= 'spades.txt'

        with open(file, 'r', encoding='utf-8') as card_image:
            image = card_image.read()

        return image
