import random 

class Cards:
    """ Create a deck of playing cards """


    def __init__(self):
        
        self.suits = ["c", "s", "h", "d"]
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    
    def pick_card(self):
        a = random.randint(0, 12) # random.choice  random.shuffle
        b = random.randint(0, 3)
        print("a={}, b={}".format(a, b))
        
        return self.ranks[a] + self.suits[b]
    
    def __str__(self):
        return "test"
        
    # deal()

class Deck:
    pass
        
        
class Player:
    """ Simulate a player """
    pass

"""
use the following when it comes to it
    `self.deck = ["2H", "QS", ...]` (edited)
    `random.shuffle(self.deck)` (edited)
    
    `return self.deck.pop()` (edited)
    https://docs.python.org/3.6/library/itertools.html#itertools.product
"""