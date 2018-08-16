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



def reset_table(restart=False, increment_seq=False, incrementScore=False):
    
    """ if the game was reset during the game then clear cash, 
        otherwise just re-set the table and deal new cards to
        both player and house """
        
    if restart:
        session.clear()     # gets rid of the lingering data but clearing the session
    
    if incrementScore:
        session["score"][session["current_player"]] += 1
    
    if increment_seq:
        session["seq"] += 1
    
    deck.reset()                                    # restores a full deck of cards (52)
    session["houseHand"] = deck.deal(2)             # deal 2 new cards to house
    session["playerHand"] = deck.deal(2)            # deal 2 new cards to player




def getVerdict():
    
    """
    decides who wins
    hand[0] = player
    hand[1] = house
    """
    
    player_Val , player = getHandValue( session["playerHand"] )
    house_Val , house = getHandValue( session["houseHand"] )

    verdict = "undecided"
    if player == "active" and house == "active":
                    
        if player_Val == house_Val:
            verdict = "PUSH"
            reset_table(increment_seq=True )  
            
        elif player_Val > house_Val:
            verdict = "player"
            reset_table(increment_seq=True, incrementScore=True ) 
            
        elif player_Val < house_Val:
            verdict = "house"
            reset_table(increment_seq=True )
    else:
        # if player goes bust or house gets blackjack decale house as winner
        if player == "BUST" or house == "BLACKJACK":
            verdict = "house"
            reset_table(increment_seq=True )
            
        # if house goes bust or player gets blackjack decale player as winner
        elif house == "BUST" or player == "BLACKJACK":
            verdict = "player"
            reset_table(increment_seq=True, incrementScore=True )
    
        # if both player and house get black jack then PUSH
        elif player == "BLACKJACK" and house == "BLACKJACK":
            verdict = "PUSH"
            reset_table(increment_seq=True )
        else:
            print("Shouldnt get here")
        
    print("{} wins".format(verdict.title()))
    
    return verdict


def house_plays():
    player_hand_val , _ = getHandValue( session["playerHand"])
    while True:
        house_hand_val , house_game_outcome = getHandValue( session["houseHand"])
        print("house_hand = {}, player_hand={}, house_game_outcome= {} ".format(house_hand_val, player_hand_val, house_game_outcome) )
        if house_game_outcome == "BUST" or house_game_outcome == "BLACKJACK" or house_hand_val >= player_hand_val or (house_hand_val > 18 and player_hand_val < 18):
            print("house_game_outcome = ", house_hand_val, house_game_outcome)
            break
        session["houseHand"].append(deck.deal())

# defining globals
deck = Deck() # number of players going in

    # players
    # if player.hand value is greater than 18, the STAND button should pulsate
# to ask

# the house plays all its cards in one go and we're not able to see what's happening 
# how do we get it pull its card one by one?

# how do i start with the card faced down?

#  ================= routes =====================
@app.route("/base")
def base():
    return render_template("base.html")


# Welcome view
@app.route("/", methods=["POST","GET"])
def index():
    
    reset_table() # start fresh by clearing the session, resetting the deck
    
    if request.method == "POST":
    
        # the data extracted from the form was coming in as an "ImmutableMultiDict", which made it absolutely impossible to
        # to use the same names (name = username) on the form inputs, as it was only capable getting the first value out,
        # it simply fetched the first value with the key "username" and it ignored the rest. However, i wished to use the
        # same names for the inputs within my form however unconventional it might be. so with the use of ".getlist()" the 
        #"ImmutableMultiDict" was changed to a normal dictionary which stores the values for my username key (name input on the form) 
        # as a list containing all the given names as shown in the example below.
        # {'username': [u'damian', u'yoni', u'michael', u'james'] }
        # please refer to the readme.md for more information on this
        for key in request.form.keys():
            
            # fetching the initital user data out of the from and putting it in a normal dictionary
            session[key] = request.form.getlist(key)
            
            if key == "username":
                # decided to go with a dictionary here with the usernames stored as keys which makes 
                # the data handling alot easier and the format easier to read.
                session["score"] = {username: 0 for username in session["username"]}
            
            if key == "rounds":
                # sets how many rounds a single game would last.
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
    

# game page
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
            session["playerHand"].append(deck.deal())
        
        # if player goes "BUST" - increment seq key to move on the next player
        if getHandValue( session["playerHand"] )[1] == "BUST":
            print("BUUUUUUUUUUSSSSSTTT = ", getHandValue(session["playerHand"] )[0] )
            reset_table(increment_seq=True)
            
        # if the player gets "blackjack"
        if getHandValue( session["playerHand"] )[1] == "BLACKJACK":
            print("BLACKJACKKKKKKKKKKKKKKKKKKKK")
            
            # house has to play after the player so this bit of code needs to move!
                # if house goes bust:       Decalre "BLACKJACK" - increment score and seq
                # if house get blackjack:   declare "PUSH" - increment seq ONLY!  
                
            house_plays()
            verdict = getVerdict()
            
        
        # if player stands or gets blackjack it's house's turn to play
        if "stand" in request.form.keys():
            # house gets cards until it has blackjack or goes bust or has value higher than player
            house_plays()
            verdict = getVerdict()

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
    

    player_dict = {"hand": convertCardNames( session["playerHand"] ), "value" : getHandValue( session["playerHand"] ) }
    house_dict = {"hand": convertCardNames( session["houseHand"] ), "value" : getHandValue( session["houseHand"] ),"folded": ["back.jpg","back.jpg"] }
    round_dict = {"total": session["rounds"], "played": session["rounds_played"]+1}

    return render_template("game.html", usernames=usernames, scores=scores, seq=session["seq"], 
        rounds=round_dict, player=player_dict, house=house_dict)
    


@app.route("/winner")
def winner():
    
    # note:
    # the scenario at which two players have the same score at the end 
    # of the final round needs to be address
    #   decalre both as winners? raise the the rounds by 3?
    
    # being passed in for the completeness of the 
    round_dict = {"total": session["rounds"], "played": session["rounds_played"]+1}
    
    return render_template("winner.html", winner=session["won"], scores=session["score"], rounds=round_dict)

if __name__ == "__main__":
    # host = os.getenv("IP", "0.0.0.0")
    # port = os.getenv("PORT", "8080")
    port = int( os.getenv("PORT") )
    host = os.getenv("IP")
    app.run(host=host, port=port)