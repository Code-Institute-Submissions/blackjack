import sys 
import random 
import itertools


class Deck:
    """ Deck of playing cards """

    def __init__(self, number_of_decks=1):
        
        self.suits = ["spades", "clubs", "hearts", "diamonds"]
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.number_of_decks = number_of_decks
        self.deck = list(itertools.product(self.suits, self.ranks)) * self.number_of_decks
        random.shuffle(self.deck)
        print("len of deck =", len(self.deck))

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
        
        self.deck = list(itertools.product(self.suits, self.ranks)) * self.number_of_decks
        random.shuffle(self.deck)
        print("deck is now reset to {} cards".format( len(self.deck) ))



def convert_card_names(cards):
    
    """ 
    convert the name of the cards in the deck to match the names of 
    the individual PNGs.
    format of card names in deck =  ('spades', 'Q') 
                   target format =  Q_of_spades.png
    """
    print("cards = ", cards)
    if cards:
        conversions = list(card[1] + "_of_" + card[0] + ".png" for card in cards)
    else:
        conversions = ["back.png","back.png"]
    
    print("convert_card_names():    conversions = ", conversions)
    return conversions
    


def get_hand_value(hand):
    
    """
    # K,Q,J are worth 10 points each
    # A is worth either 1 or 11 depending on the hand
    # 2-10 = face value
    # format = ('spades', 'K')
    """
    jdebug = 0
    if jdebug > 0:  print( "count_hand() called by: {}".format(sys._getframe(1).f_code.co_name) )
    
    status = "empty"
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



def get_verdict(player_hand, house_hand):
    """ 
    when both player/house have played
    player ->  get_hand_value(player_hand) ->  player_hand_val, player_stat
    house  ->  get_hand_value(house_hand)  ->  house_val, house_stat
    
    possible scenarios:
        player BUST - game over
            verdict house
        player BJ - house BJ
            verdict push
        player BJ - house BUST
            verdict player


    if house_hand empty -> get_hand_value(player_hand) - > 0, 'undecided'
    """
    verdict = "undecided"
    
    
    # fetching house/player data from session
    player_hand_val , player_status = get_hand_value( player_hand )
    house_hand_val , house_status = get_hand_value( house_hand )
    print("get_verdict_new():   player_hand_val = ", player_hand_val)
    print("get_verdict_new():   house_hand_val  = ", house_hand_val)
    print("get_verdict_new():   player_status   = ", player_status)
    print("get_verdict_new():   house_status    = ", house_status)
    
    # player stands or no bust/blackjack occurs
    if player_status == "active" and house_status == "active":
        
        # house matches the player hand
        if player_hand_val == house_hand_val:
            verdict = "push"
            
        # player ends up with a higher hand value
        elif player_hand_val > house_hand_val:
            print('player_hand_val > house_hand_val')
            verdict = "player"
        
        # house ends up with a higher hand value
        elif player_hand_val < house_hand_val:
            verdict = "house"
        else:
            print("it shouldnt get here")
            assert False

    else:
        
                
        if player_status != "BUST" and house_status == "empty":
            # at this point house hasnt played its turn yet
            # if player goes BUST, house win period!
            verdict = "undecided" 
            
        # if player goes bust or house gets blackjack declare house as winner
        elif player_status == "BUST":
            verdict = "house"
            
        elif house_status == "BUST":
            verdict = "player"
            
        # if both player and house get black jack then PUSH
        elif player_status == "BLACKJACK" and house_status == "BLACKJACK":
            verdict = "push"
            
        # if house goes bust or player gets blackjack declare player as winner
        elif player_status == "BLACKJACK":
            
            verdict = "player" 
            
        # if house goes bust or player gets blackjack declare player as winner
        elif house_status == "BLACKJACK":
            verdict = "house"
 
            
        else:
            print("it shouldnt get here")
            assert False
    
    print("get_verdict_new():   verdict.upper() = ", verdict.upper())
    
    return verdict.upper()
    


def house_plays(deck, player_hand, house_hand):
    
    """ 
        Simulate house playing its turn
        the house will stop pulling cards if one of the 
        conditions given below is met:
        
        - house BUST
        - house gets BLACKJACK
        - house_hand_val is greater than player_hand_value
        - house_hand_val is greater than 18 and player_hand_val is less than 18
        
        house is smart enough to stop pulling when it gets a value higher than what the player 
        has achieved, However, if the player somehow ends up with a higher value than the house, 
        knowing that it has already lost the game, it will risk going bust in efforts of beating the player.
        lets assume the player ends up with "20" and the house with a high "18", now since the house
        has already lost the game, it will pull another card just for the sake of beating the player, 
        in the hopes of pulling a BLACKJACK or PUSH.
    """
    
    # fetch player hand value out to compare with house's
    player_hand_val , _ = get_hand_value( player_hand )

    while True:
        
        # fetch house data everytime a card is pulled - the first time it gets here, there are 
        # already two cards in house's deck
        house_hand_val , house_game_outcome = get_hand_value( house_hand)
        print("house_hand = {}, player_hand={}, house_game_outcome= {} ".format(house_hand_val, player_hand_val, house_game_outcome) )
        
        # break out of loop if the ny of these conditions are met
        if (house_game_outcome == "BUST" or 
            house_game_outcome == "BLACKJACK" or 
            house_hand_val >= player_hand_val or 
            (house_hand_val > 18 and player_hand_val < 18) ):
                        
            print("house_game_outcome = ", house_hand_val, house_game_outcome)
            
            break
        
        house_hand.append(deck.deal())  
        
    return house_hand  



def pick_winner(scores):
    """ at the end of the final rounds, pick the winner.
        if noone scores any points, house wins
        if a player scores the highest point, player wins
        if several players score the same highest point, no-one wins """

    # get maximum score attained by the players
    maxScore = max( scores.values()  )     
    winner = ""
    
    # noone has won a single game - declare house as the winner
    if maxScore == 0:       
        winner = "house"
    
    # check to see if there is anybody else with the same max score
    elif list( scores.values() ).count(maxScore) > 1:     
        winners_list     = [key for key, value in scores.items() if value == maxScore]      # save all the players with the same max score into a list
        winners_list_str = ", ".join(str(winner).title() for winner in winners_list)        # convert the list into a string
        lastComma        = winners_list_str.rfind(",")                                      # locate the character "," within the string
        winner   = winners_list_str[:lastComma] + " and" + winners_list_str[lastComma+1:]   # replace lace occurance of "," with "and"
        
    else:   # only one person scored the max score!
        winner = max(scores, key= lambda x: scores[x]) # get the player with the highest score
        
    return winner