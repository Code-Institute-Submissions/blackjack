import os
import time # use with time.sleep(5) 5 sec delay
import sys
from flask import Flask, render_template, request, redirect, flash, url_for, render_template_string, session
from flask_wtf import Form, FlaskForm
from wtforms import StringField, IntegerField, IntegerField, SubmitField, SelectField   # http://wtforms.simplecodes.com/docs/0.6.2/fields.html
from wtforms.validators import DataRequired
from game import *

# from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)



def reset_table(restart=False, increment_seq=False, increment_core=False):
    """ if the game was reset during the game then clear session, 
        otherwise just re-set the table and deal new cards to
        both player and house """
        
    if restart:
        session.clear()     # gets rid of the lingering data by clearing the session
    
    if increment_core:
        session["score"][session["current_player"]] += 1
    
    if increment_seq:
        session["seq"] += 1
    
    deck.reset()    # restores a full deck of cards
    session["houseHand"]  = deck.deal(2)  # deal 2 new cards to house
    session["playerHand"] = deck.deal(2)  # deal 2 new cards to player




def get_verdict(player_only=False):
    """
    Analyse both player and house states, then pass final verdict as to which side has won. 
    
    After both player and house play their turns, this function uses the "status" of 
    the "get_hand_value()" function to select the winner of the played sequence
    (player or house). 
    
    Additionally, it awards points and changes players accordingly, using the reset_table()
    function!

    player_only: 
    if the this parameter is set true, function analyses player ONLY!
    in doing so, the fucntion will:
    
    - check to see if the player has gone BUST
        - there's no need for the house to play. the table is then reset using reset_table()
          function and sequence incremented to move to the next player
          
    - check to see if the player has achieved BLACKJACK
        - house has to play its turn and the results will be assessed by
        the get_verdict() function 
    
    """
    
    # fetching house/player data from session
    player_Val , player = get_hand_value( session["playerHand"] )
    house_Val , house = get_hand_value( session["houseHand"] )
    verdict = "undecided"  
    
    # only check player - skip house
    if player_only:
        if player == "BUST":
            # player has lost - BUST occured
            #   - reset table and move to the next player
            reset_table(increment_seq=True)
            print("Player went BUST with {}".format(player_Val))
            
        if player == "BLACKJACK":
            
            print("Player gets BLACKJACK")
            # player scores blackjack
            #   - now house has to play its turn 
            house_plays() # simulate house play
            get_verdict()  # decide who won!
            
    else:
        # check both player and house
        
        # player stands or no bust/blackjack occurs
        if player == "active" and house == "active":
            
            # house matches the player hand
            if player_Val == house_Val:
                verdict = "PUSH"
                
            # player ends up with a higher hand value
            elif player_Val > house_Val:
                verdict = "player"
            
            # house ends up with a higher hand value
            elif player_Val < house_Val:
                verdict = "house"
        else:
            # if both player and house get black jack then PUSH
            if player == "BLACKJACK" and house == "BLACKJACK":
                verdict = "PUSH"
                
            # if player goes bust or house gets blackjack declare house as winner
            elif player == "BUST" or house == "BLACKJACK":
                verdict = "house"
                
            # if house goes bust or player gets blackjack declare player as winner
            elif house == "BUST" or player == "BLACKJACK":
                verdict = "player"
        
            else:
                print("Shouldnt get here")
        
        # collect the verdict and make changes accordingly
        if verdict == "player":
            # player has won
            #   - award a point, reset table and move to the next player
            reset_table(increment_seq=True, increment_core=True )
        else:
            # player has lost or PUSH has occured
            #   - reset table and move to the next player
            reset_table(increment_seq=True)
        
        print("verdict = {}".format(verdict.title()))
        


def house_plays():
    
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
    player_hand_val , _ = get_hand_value( session["playerHand"])
    
    while True:
        
        # fetch house data everytime a card is pulled - the first time it gets here, there are 
        # already two cards in house's deck
        house_hand_val , house_game_outcome = get_hand_value( session["houseHand"])
        print("house_hand = {}, player_hand={}, house_game_outcome= {} ".format(house_hand_val, player_hand_val, house_game_outcome) )
        
        # break out of loop if the ny of these conditions are met
        if ( house_game_outcome == "BUST" or 
            house_game_outcome == "BLACKJACK" or 
                house_hand_val >= player_hand_val or 
                    (house_hand_val > 18 and player_hand_val < 18) ):
                        
            print("house_game_outcome = ", house_hand_val, house_game_outcome)
            break
        
        # pull the next card
        session["houseHand"].append(deck.deal())


# defining globals
deck = Deck() # create deck initially with only 1 deck of cards

    # players
    # if player.hand value is greater than 18, the STAND button should pulsate
# to ask
# couldnt deploy to heroku, i mean i did but it cant find app.py
# it's all happening too fast, cant see the player going BUST or getting blackjack
# the house plays all its cards in one go and we're not able to see what's happening 
# how do we get it pull its card one by one?
# unittesting?

# how do i start with the card faced down?

#  ================= routes =====================
@app.route("/base")
def base():
    return render_template("base.html")


# Welcome view - add more comments
@app.route("/", methods=["POST","GET"])
def index():
    
    reset_table() # start fresh by clearing the session, resetting the deck
    
    if request.method == "POST":
        
        # with the use of a ".getlist()", the "ImmutableMultiDict" object is changed to a normal normal dictionary, allowing 
        # me to use the same input names (name = "John", name="Logan", ...) on my the form, which was impossible to do with an
        # "ImmutableMultiDict" object since it simply fetched the last value with the key "name" and ignored the rest.
        # all the values of the key "name" is stored as a list within the dictionary which was then stored in the session
        # using a key "username", {'username': [u'damian', u'yoni', u'michael', u'james'] }.
        for key in request.form.keys():
            
            # fetching the initital user data out of the from and putting it in a normal dictionary
            session[key] = request.form.getlist(key)
            
            if key == "decks":
                # comes in as a list with only ONE value
                # set how many how many decks to use
                global deck
                deck = Deck(int(session[key][0]))
            
            if key == "username":
                # with the usernames stored as keys in a dictionary, it makes 
                # the data handling alot easier and the format easier to read.
                session["score"] = {username: 0 for username in session["username"]}
            
            if key == "rounds":
                # sets how many rounds a single session would last.
                # will be used as an integer from this point onwards
                session["rounds"] = int(session["rounds"][0]) 
        
        # expanding on the uses data held in session
        session["seq"] = 0              # player turn tracker
        session["rounds_played"] = 0    # round tacker
        session["won"] = "TBC"          # winner to be declared
        session["status"] = "TBC"       # bust, push, blackjack - need two? for player and house
        
        # by this point all the basic player data is now stored in the session.
        print("session = ", session)
        
        # if POST then redirect to the first player in game view
        return redirect( url_for('game') )
        
    return render_template("index.html")
    

# game page - add more comments
@app.route("/game", methods=["POST","GET"])
def game():
    
    scores = session["score"]               # holds all the scores
    usernames = session["username"]         # holds all the usernames 
    seq = session["seq"]                    # assigned to a variable only for readability purposes
    username = session["username"][seq]     # player whose turn it is to play
    session["current_player"]= username     # current player

    if request.method == "POST":
        
        print("request.form.keys() = ", request.form.keys())
        
        if "reset" in request.form.keys():
            # reseting mechanism - triggered if reset button is pressed during an action session of the game
            reset_table(restart=True)   # clearing the session as well as resetting the table 
            return redirect( url_for("index")) 
        
        if "hit" in request.form.keys():
            # deals one card to the player
            session["status"] = "hit"
            session["playerHand"].append(deck.deal())
        
        # check the progress of the player ONLY.
        #   - if the player goes BUST, then there is no need for the house to play.
        #   - if the players gets BLACKJACK, then house has to player.
        get_verdict(player_only=True)
        
        
        # if results pending then session["seq"] -+ 1 
        # if the player has finished playing, BlackJack or hand value must be shown on the player side
        # once the house starts to play - for every card drawn the page needs to reload. until it goes BUST
        # gets BLACKJACK or ends with a higher hand value than the player. once the game has finished playing
        # another 2-3 seconds pause is needed before it moves on to the next player.
        
        
        if "stand" in request.form.keys():
            # house gets cards until one of the below conditions is met.
            # BLACKJACK, BUST or hand value higher than player
            session["status"] = "stand"
            house_plays() # simulate house play
            get_verdict()  # decide who won!

        # session["score"] = scores   # Aliased since session resets the content of the list to zero
        print("scores = ", scores)

        # reseting mechanism - simulating a full cycle - each full cycle means 1 round
        if session["seq"] >= len( session["username"] ):
            session["seq"] = 0              # reset the sequence counter to cycle back to the first player
            session["rounds_played"] += 1   # when a cycle is complete, one found of game has been played by all the player!
            
            print("rounds played = ", session["rounds_played"])
            
            # declare the winner
            if session["rounds_played"] == session["rounds"]:
                
                # select the player with the heighest score at the end of the final "pre-defined" round.
                session["won"] = max(scores, key= lambda x: scores[x])
                return redirect( url_for('winner') ) 


    player_dict = {"hand": convert_card_names( session["playerHand"] ), "value" : get_hand_value( session["playerHand"] ) }
    house_dict = {"hand": convert_card_names( session["houseHand"] ), "value" : get_hand_value( session["houseHand"] ),"folded": ["back.jpg","back.jpg"] }
    round_dict = {"total": session["rounds"], "played": session["rounds_played"]+1}

    return render_template("game.html", usernames=usernames, scores=scores, seq=session["seq"], 
        rounds=round_dict, player=player_dict, house=house_dict)
    

# show the winner if there is any - add more comments
@app.route("/winner", methods=["POST","GET"])
def winner():
    
    # note:
    # the scenario at which two players have the same score at the end 
    # of the final round needs to be address
    #   decalre both as winners? raise the the rounds by 3?
    
    
    if request.method == "POST":
        if "reset" in request.form.keys():
            # reseting mechanism - triggered if reset button is pressed during an action session of the game
            reset_table(restart=True)   # clearing the session as well as resetting the table 
            return redirect( url_for("index")) 
    
    
    
    # being passed in for the completeness of the 
    round_dict = {"total": session["rounds"], "played": session["rounds_played"]}
    
    return render_template("winner.html", winner=session["won"], scores=session["score"], rounds=round_dict)

if __name__ == "__main__":
    # host = os.getenv("IP", "0.0.0.0")
    # port = os.getenv("PORT", "8080")
    port = int( os.getenv("PORT") )
    host = os.getenv("IP")
    app.run(host=host, port=port)