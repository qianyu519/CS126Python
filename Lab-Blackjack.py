# Qian Yu, Ying Zhang
# qy28, yz346
# CS126L-03
# Lab 10 - Blackjack

import random


class Card:
    '''
    Header for the class Card.
    Any new card objects which are created will use Card(card_number) method, which
    a suit, rank, and value will be used to create card objects. Cards start from
    facing down.
    '''
    # class member variables which is shared by all objects.
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    ranks = ["Jack", "Queen", "King"]

    def __init__(self, card_number):
        '''
            __init__ will be run whenever a new card object is created
            Takes in 2 parameters, card_number(any number which is between 0 and 51)
                                 , self(make object be able to call
                                 it's own methods)
        '''
        # Sets the Card's instance variables:
        # Cards start from facing down
        self._facing_up = False

        # Integer division of the initial card num determines the suit.
        # 1-13 spades, 14-26 hearts, 27-39 clubs, 40-52 diamonds
        self._suit = Card.suits[card_number // 13]

        # Use modules 13 to determine the card's "rank" (e.g., Ace, King,
        # Queen, Jack, 1, 2, ...)
        #  and point "value" (2-10,11)
        num = card_number % 13
        # If num%13 == 0, its an Ace.
        if num == 0:
            self._rank = "Ace"
            self._value = 11
        # King if 12, Queen if 11, Jack if 10
        elif num in [10, 11, 12]:
            self._rank = Card.ranks[num-10]
            # ranks of J, Q, and K
            self._value = 10
        # Else rank and value is it's number +1
        else:
            self._rank = str(num + 1)
            self._value = num + 1

    # a "getter" returns the string value of the suit
    def get_suit(self):
        return self._suit

    # a "getter" returns string of rank
    def get_rank(self):
        return self._rank

    # value getter, returns int value
    def get_value(self):
        return self._value

    # facing_up getter, return boolean
    def get_face_up(self):
    	return self._facing_up

    # two setters are implements for "facing up " attribute, face_down() and
    # face_up()

    # turns card face down
    def face_down(self):
        self._facing_up = False

    # turns card face_up
    def face_up(self):
        self._facing_up = True

    # Without it the print method would simply print the "memory address" of
    # the object
    # With it, if the card is facing up it prints its rank and suit, else it
    # prints "<facedown>"
    def __str__(self):
        if self._facing_up:
            return self._rank + " of " + self._suit
        else:
            return "<facedown>"


class ChipBank():
    '''
    Header for class ChipBank
    which is used to store a dollar amount
    '''
    # Initializes the chipbank with a dollar value
    def __init__(self, value):
        self._value = value

    # Tries to withdraw the amount from the current saved value.
    # Returns the total amount withdrawn
    def withdraw(self, amount):
        total = self._value
        self._value -= amount
        if self._value < 0:
            self._value = 0
            return total  # original balance
        return amount   # only return amount if they had enough to take it all

    # adds amount to total value and saves it
    def deposit(self, amount):
        self._value += amount

    # returns the total value of bank
    def get_balance(self):
        return self._value

    # Prints the amount and types of chips stored in bank
    def __str__(self):
        return "%d blacks, %d greens, %d reds, %d blues - totaling $%d" % \
        (self._value // 100,
         self._value % 100 // 25,
         self._value % 25 // 5,
         self._value % 5,
         self._value)


class BlackjackHand:
    '''
    allowing user to store information about each players' hand.
    '''
    def __init__(self):
        # This list is where the user's cards will be stored.
        self.hand = []

    def __str__(self):
        string_of_hand = ''
        for card in self.hand:
            # card = str(card.face_up)
            string_of_hand += str(card) + ", "
        string_of_hand = string_of_hand.strip(", ")
        return string_of_hand

    def add_card(self, new_card):
        self.hand.append(new_card)

    def get_value(self):
        total_value = 0
        for card in self.hand:
            total_value += card.get_value()
        return total_value


class Deck:
    '''A deck class.
    '''
    def __init__(self):
        # Creates deck and shuffles it
        self.deck = []
        for i in range(52):
            c = Card(i)
            self.deck.append(c)
        random.shuffle(self.deck)

    def draw(self):
        if len(self.deck) == 0:
            # Creates new deck and shuffles it if the deck is empty
            for i in range(52):
                c = Card(i)
                self.deck.append(c)
            random.shuffle(self.deck)
        # Draws a random card from a shuffled deck and removes the card from
        # the deck
        drawn_card = self.deck.pop()
        drawn_card.face_up()
        return drawn_card


class Blackjack:
    '''simulating gameplay, and gives an interface for
    user to deal with the ChipBank class
    '''
    def __init__(self, starting_dollars):
        self.game_in_play = False
        # Creates bank instance variable that stores the user's chipbank
        self.bank = ChipBank(starting_dollars)
        self.d = Deck()
        # Sets up hands
        self.player_hand = BlackjackHand()
        self.dealer_hand = BlackjackHand()

    def start_hand(self, wager):
        self.game_in_play = True

        # Starts game
        self.player_hand.add_card(self.d.draw())
        self.player_hand.add_card(self.d.draw())
        self.dealer_hand.add_card(self.d.draw())
        self.dealer_hand.hand[0].face_down()
        self.dealer_hand.add_card(self.d.draw())
        print(f"You: {self.player_hand}")
        print(f"Dealer: {self.dealer_hand}")

        # Deals with Wager
        self.wager_amount = self.bank.withdraw(wager)

        # Checks if player wins
        if self.player_hand.get_value() == 21:
            if self.dealer_hand.get_value() == self.player_hand.get_value:
                print("You tied with the dealer ")
                self.end_hand("TIE")
            print("You won with a BlackJack!")
            self.end_hand("WIN")

    def hit(self):
        # Adds card to user's Hand
        self.player_hand.add_card(self.d.draw())
        print(f"New Card: {self.player_hand.hand[-1]}")
        print(f"You: {self.player_hand}")

        # Checks if player wins
        if self.player_hand.get_value() == 21:
            self.stand()
        elif self.player_hand.get_value() > 21:
            self.end_hand("LOSE")

    def stand(self):
        # This function represents what happens when the player stands, and the
        # game continues without drawing a new card.

        # The dealer's first card is turned faceup
        self.dealer_hand.hand[0].face_up()
        print(f"Dealer: {self.dealer_hand}")
        # Checks whether the dealer needs to hit, according to
        # prescribed rules (Provided by the casino)
        while self.dealer_hand.get_value() <= 16:
            self.dealer_hand.add_card(self.d.draw())
            print(f"Dealer's new card: {self.dealer_hand.hand[-1]}")
            print(f"Dealer: {self.dealer_hand}")
        if self.dealer_hand.get_value() > 21:
            # The dealer busts
            self.end_hand("WIN")
        else:
            # compares user and dealer hands to determine a winner
            ps = self.player_hand.get_value()
            ds = self.dealer_hand.get_value()
            if ps < ds:
                self.end_hand("LOSE")
            elif ps > ds:
                self.end_hand("WIN")
            elif ps == ds:
                self.end_hand("TIE")

    def end_hand(self, outcome):
        # If anytime a winner is determined for a paricular
        # round, this function is triggered.
        self.game_in_play = False
        self.outcome = outcome
        if outcome == "WIN":
            print("You win.")
            reward = self.wager_amount * 2
            self.bank.deposit(reward)
        elif outcome == "LOSE":
            print("You lose")
        elif outcome == "TIE":
            print("TIE")
            self.bank.deposit(self.wager_amount)
        # Clears the hand new game starts
        while len(self.player_hand.hand) > 0:
            self.player_hand.hand.pop()
        while len(self.dealer_hand.hand) > 0:
            self.dealer_hand.hand.pop()

    def game_active(self):
        return self.game_in_play


# Test Code
def tests():
    # Tests add_card()
    my_hand = BlackjackHand()
    print("ADD CARD")
    print(f"Before: {my_hand}")
    my_hand.add_card(25)
    print(f"After: {my_hand}")
    # Tests __str__()
    my_hand.add_card(1)
    my_hand.add_card(2)
    print(f"STR: {str(my_hand)}")
    # Tests get_value()
    print(f"GET VALUE: {my_hand.get_value()}")
    
    # Blackjack Tests
    # Tests bank
    my_game = Blackjack(250)
    print(f"Bank: {my_game.bank}")
    # Tests deck
    d = Deck()
    print(f"Deck: {d.deck}")
    # Tests Hands
    blackjack = Blackjack(250)
    blackjack.start_hand(25)
    # print(str(player_hand))
    # print(str(dealer_hand))
    blackjack.hit()


def new_main():
    blackjack = BlackJack(startVal)
    while blackjack.bank.get_balance() > 0:
        wager = 5
        blackjack.starthand(wager)
        while blackjack.game_active():
            pass
            # Hit or stand logic
            # use record method
            # Maybe need a counter?
    # print number of games


if __name__ == "__main__":
    blackjack = Blackjack(250)
    while blackjack.bank.get_balance() > 0:
        print("Your remaining chips: " + str(blackjack.bank))
        wager = int(input("How much do you want to wager? "))
        blackjack.start_hand(wager)
        while blackjack.game_active():
            choice = input("STAND or HIT: ").upper().strip()
            if choice == "STAND":
                blackjack.stand()
            elif choice == "HIT":
                blackjack.hit()
    print("Out of money! The casino wins!")
