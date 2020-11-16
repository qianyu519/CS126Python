import random


#header for the class Card.
class Card:
    def __init__(self, card_number):
        self.card_number = card_number

    def get_suit(self):
        #return the suit of a selected card
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        return suits[self.card_number % 4]

    def get_rank(self):
        #return the rank of a selected card
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8',
                        '9', '10', 'Jack', 'Queen', 'King']
        return ranks[self.card_number % 13]

    def get_value(self):
        #return the value of cards according to their ranks
        card_numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
        face_cards = ['Jack', 'Queen', 'King']
        if self.get_rank() in card_numbers:
            return int(self.get_rank())
        elif self.get_rank() in face_cards:
            return 10
        elif self.get_rank() == 'Ace':
            return 11

    def face_down(self):
        #Hide the information on the card
        self.face_down = True

    def face_up(self):
        #show the information on the card
        self.face_down = False

    def __str__(self):
        #use the facedown or faceup methods
        if self.face_down:
            return "<facedown>"
        if not self.face_down:
            return (str(self.get_rank) + 'of' + str(self.get_suit))

#header for the class Chip Bank
class ChipBank:
    def __init__(self, value):
        self.balance = value

    def withdraw(self, amount):
        #allow users remove money
        balance = self.balance
        balance -= amount
        if balance >= 0:
            return amount
        elif balance <= 0:
            return (amount + balance)

    def deposit(self, amount):
        #allow users add money
        self.balance += amount

    def get_balance(self):
        #show how much money the user has in their chip bank
        print(self.balance)

    def __str__(self):
        #show how many chips that users have in their bank
        balance = self.balance
        original_balance = balance
        black_chips = balance // 100
        balance = balance - (black_chips * 100)
        green_chips = balance // 25
        balance = balance - (green_chips * 25)
        red_chips = balance // 5
        blue_chips = balance - (red_chips * 5)
        xinxi = (str(black_chips) + "blacks," + str(green_chips) +
                 "greens," + str(red_chips) + "reds" + str(blue_chips) +
                 "blues - totalling $" + str(original_balance))
        return xinxi

if __name__ == '__main__':
#making a deck of cards
    deck = []
    for i in range(52):
        my_card = Card(i)
        deck.append(my_card)
        my_card.face_up()
        print(my_card)
#print random crads from deck

    print(random.choice(deck))

    card = Card(37)
    print(card)
        #queen of clubs
    print(card.get_value())
        #10
    print(card.get_suit())
        #Clubs
    print(card.get_rank())
        #queen
    card.face_down()
    print(card)
        #facedown
    card.face_up()
    print(card)
        #queen of clubs

    jisuanji = ChipBank(149)
    print(jisuanji)
    jisuanji.deposit(7)
        #1 black, 1 green, 4 red, 4 blue
    print(jisuanji.get_balance())
    print(jisuanji)
        #1 black, 2 green, 1 red, 1 blue
    print(jisuanji.withdraw(84))
    print(jisuanji)
        #0 black, 2 green, 4 red, 2 blue,
    jisuanji.deposit(120)
    print(jisuanji)
        #1 black, 3 green, 3 red, 2 blue
    print(jisuanji.withdraw(300))
