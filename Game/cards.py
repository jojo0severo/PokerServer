from collections import defaultdict
from random import choice


class Cards:

    def __init__(self):
        self.deck = defaultdict()
        self.plays = []
        self.initialize_deck()

    def initialize_deck(self):
        naipes = ['Ouros', 'Paus', 'Copas', 'Espadas']
        cartas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        for card in cartas:
            self.deck[card] = []
            for naipe in naipes:
                self.deck[card].append(naipe)

    def get_hand(self):
        hand = []
        for i in range(2):
            cards = list(self.deck.keys())
            value = choice(cards)
            suit_card = choice(list(self.deck[value]))

            hand.append('Value:' + value + '\nSuit:' + suit_card)
            self.deck[value].remove(suit_card)

            if len(self.deck[value]) == 0:
                del self.deck[value]

        return hand

