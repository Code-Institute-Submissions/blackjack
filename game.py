import random 
import itertools

class Deck:
    """ Deck of playing cards """


    def __init__(self, nop):
        
        self.suits = ["spade", "clubs", "hearts", "diamonds"]
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.nop = nop    # Number Of Players cgange to num_of_players
        self.deck = list(itertools.product(self.suits, self.ranks)) * self.nop
        random.shuffle(self.deck)
    

    def deal(self):
        """ deal a card and remove that card from the deck, 
            this will also serve as a HIT function """
        card = self.deck.pop() # since the deck is already shuffled we can just use pop 
        return card


    def __str__(self):
        return "test"
    
    
    # how to reset the deck when a player wins?

class Player:
    """ Simulate a player """
    
    def __init__(self,name, score):
        self.name = name
        self.score = score
        
    def __str__(self):
        return "Player" 
