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



def reset_table(restart=False):
    
    """ if the game was reset during the game then clear cash, 
        otherwise just re-set the table and deal new cards to
        both player and house """
        
    if restart:
        session.clear()     # gets rid of the lingering data but clearing the session
        
    deck.reset()       # restores a full deck of cards
    session["houseHand"] = deck.deal(2) # list( deck.deal() for x in range(2) )
    session["playerHand"] = deck.deal(2) # list( deck.deal() for x in range(2) )

# defining globals
deck = Deck() # number of players going in



# houseHand = list( house.deal() for x in range(2) )
# houseHandValue = 0
# print(house.deck)
# print(len(house.deck))
# test_card = house.deal()
# print(test_card)
# print(convertCardNames(test_card))

# game idea
# a bastardised version of blackjack, where players take turn to play against the house,
# every time each players wins agasint the house, they're awarded a point which can be tracked
# via the console (scoreboard).
# has to be tested: only the house is to hold a collection of (2-4) decks depending on the number 
# of players set. 2 decks by default
# how to add images of cards on the screen?

    
    # game logic before player decides on hit or stand
    # the house must show 2 cards
    # possible variables
        # house_hand = house cards shown or to be shown
        # player_hand = player cards 

    
    
    # if HIT pressed append another card 
    
    # if STAND hit:
        # calculate player hand
        # house.deal()
    
    # players
    # if player.hand value is greater than 18, the STAND button should pulsate


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
    

    if request.method == "POST":
        
        print("request.form.keys() = ", request.form.keys())
        
        if "reset" in request.form.keys():
            # reseting mechanism - triggered if reset button is pressed during an action session of the game
            reset_table(restart=True)   # clearing the session as well as resetting the table 
            return redirect( url_for("index")) 
        
        if "hit" in request.form.keys():
            # deals one card to the player
            # session["houseHand"].append(house.deal())
            session["playerHand"].append(deck.deal())
        
        # if player goes "BUST" - increment seq key to move on the next player
        if getHandValue( session["playerHand"] )[1] == "BUST":
            print("BUUUUUUUUUUSSSSSTTT")
            session["seq"] += 1
            reset_table()
        
        # if the player gets "blackjack"
        if getHandValue( session["playerHand"] )[1] == "BLACKJACK":
            print("BLACKJACKKKKKKKKKKKKKKKKKKKK")
            
            # house has to play after the player so this bit of code needs to move!
                # if house goes bust:       Decalre "BLACKJACK" - increment score and seq
                # if house get blackjack:   declare "PUSH" - increment seq ONLY!  
            
            scores[username] += 1
            session["seq"] += 1
            reset_table()
            
            
        # if the player wins its turn, award one point 
        # if "win" in request.form.keys():
        #     scores[username] += 1
        
        session["score"] = scores   # Aliased since session resets the content of the list to zero
        print("scores = ", scores)
        
        # if "hit" not in request.form.keys():
        #     session["seq"] += 1         # win or lose, increment the sequence counter for the next player to start its turn
        
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
    house_dict = {"hand": convertCardNames( session["houseHand"] ), "value" : getHandValue( session["playerHand"] ) }
    round_dict = {"total": session["rounds"], "played": session["rounds_played"]+1}

    return render_template("game.html", usernames=usernames, scores=scores, seq=session["seq"], 
        rounds=round_dict, player=player_dict, house=house_dict)
    


@app.route("/winner")
def winner():
    
    # note:
    # the scenario at which two players have the same score at the end 
    # of the final round needs to be address
    #   decalre both as winners? raise the the rounds by 3?
    # session.pop(key)
    return render_template("winner.html", winner=session["won"])

if __name__ == "__main__":
    # host = os.getenv("IP", "0.0.0.0")
    # port = os.getenv("PORT", "8080")
    port = int( os.getenv("PORT") )
    host = os.getenv("IP")
    app.run(host=host, port=port)