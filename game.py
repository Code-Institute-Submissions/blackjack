import sys 
import random 
import itertools

class Deck:
    """ Deck of playing cards """


    def __init__(self):
        
        self.suits = ["spades", "clubs", "hearts", "diamonds"]
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = list(itertools.product(self.suits, self.ranks))
        random.shuffle(self.deck)
    

    def deal(self, num=1):
        """ deal a card and remove that card from the deck, 
            this will also serve as a HIT function 
            num:    number of cards being drawn
        """
            
        if num == 1:
            return self.deck.pop() # since the deck is already shuffled we can just use pop
        else:
            return list( self.deck.pop() for x in range(num) )


    def __str__(self):
        return "test"
    
    def reset(self):
        """ restore the deck to its original state "52" cards """        
        
        self.deck = list(itertools.product(self.suits, self.ranks))
        random.shuffle(self.deck)
        print("deck is now reset to {} cards".format( len(self.deck) ))


class Player:
    """ Simulate a player """
    
    def __init__(self,name, score, hand=None):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand
        self.name = name
        self.score = score
        
    def __str__(self):
        return "Player" 
    

def convertCardNames(cards):
    
    
    """ 
    convert the name of the cards in the deck to the names of 
    the individual PNGs.
    card names in deck: ('spades', 'Q') 
    target name: Q_of_spades.png
    """
    name = list(card[1] + "_of_" + card[0] + ".png" for card in cards)
        
    return name
    
    
    
def getHandValue(hand):
    
    # K,Q,J are worth 10 points each
    # A is worth either 1 or 11 depending on the hand
    # 2-10 = face value
    # format = ('spades', 'K')
    
    jdebug = 0
    if jdebug > 0:  print( "count_hand() called by: {}".format(sys._getframe(1).f_code.co_name) )
    
    val = 0
    aceCounter = 0
    aceCounterAddressed = 0
    for card in hand:
        if jdebug > 0:  print("card={} card[1]={}".format(card, card[1]))
        
        try:
            val += int(card[1])
            if jdebug > 0:  print("Number detected, {}".format(card[1]))
            
        except ValueError:
            
            if jdebug > 0:  print("Letter detected, {}".format(card[1]))
            
            if card[1] in ["K", "Q", "J"]:
                val += 10
            
            else:
                if jdebug > 0:  print("'A' detected, {}".format(card[1]))
                
                if val+11 > 21:
                    val += 1
                else:
                    aceCounter += 1
                    val += 11
                
        if aceCounter > 0 and val > 21 and (aceCounterAddressed != aceCounter):
            print("special! aceCounter, val = ", aceCounter, val)
            aceCounterAddressed += 1
            val -= 10
        
        if val == 21:
            status = "BLACKJACK"
        elif val > 21:
            status = "BUST"
        else:
            status = "active"
        
        
    return val, status


def getVerdict(*hands):
    
    """
    decides who wins
    hand[0] = player
    hand[1] = house
    """
    
    verdict = "undecided"
    
    # if player goes bust or house gets blackjack decale house as winner
    if hands[0] == "BUST" or hands[1] == "BLACKJACK":
        verdict = "house"
        
    # if house goes bust or player gets blackjack decale player as winner
    elif hands[1] == "BUST" or hands[0] == "BLACKJACK":
        verdict = "player"
    
    # if both player and house get black jack then PUSH
    if hands[0] == "BLACKJACK" and hands[1] == "BLACKJACK":
        verdict = "PUSH"
