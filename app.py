import os
import time # use with time.sleep(5) 5 sec delay
import sys
from flask import Flask, render_template, request, redirect, flash, url_for, render_template_string, session
from flask_wtf import Form, FlaskForm
from wtforms import StringField, IntegerField, IntegerField, SubmitField, SelectField   # http://wtforms.simplecodes.com/docs/0.6.2/fields.html
from wtforms.validators import DataRequired
from game import *

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)


def reset_table(restart=False, increment_seq=False, increment_score=False):
    """ if the game was reset during the game then clear session, 
        otherwise just re-set the table and deal new cards to
        both player and house """
        
    if restart:
        session.clear()     # gets rid of the lingering data by clearing the session
    
    if increment_score:
        session["score"][ session["current_player"] ] += 1
    
    if increment_seq:
        session["seq"] += 1
    
    session["house_plays"] = False
    deck.reset()    # restores a full deck of cards
    session["houseHand"]  = [] # deck.deal(2)  # deal 2 new cards to house
    session["playerHand"] = deck.deal(2)  # deal 2 new cards to player


    
def apply_verdict(verdict):
    """ APPLY points based on the passed verdict!
        bind to the next player button!
        """

    # collect the verdict and make changes accordingly
    if verdict == "PLAYER":
        # player has won - award a point, reset table and move to the next player
        reset_table(increment_seq=True, increment_score=True )
    else:
        # player has lost or PUSH has occured - reset table and move to the next player
        reset_table(increment_seq=True)
            


# defining globals
deck = Deck() # create deck initially with only 1 deck of cards

    # left to do:
    #   if player.hand value is greater than 18, the STAND button should pulsate
    #   unittests
    #   responsiveness
    #   theming and layout
    #   expanding on sass
    #   readme file
    #   leave more comments

# to ask
# couldnt deploy to heroku, app.py  could not be located --- RESOLVED!!!!!!!
# how do i start with the card faced down? --- RESOLVED!!!
# how do i address multiple winners, house win, no winners and a winner --- RESOLVED!!!
# what to do if the same name was entered repeatedly? should i switch to wtforms? jquery validate?
# create fall back for session if expired 

# the house div shoudl show all the cards played for the previous player

# MAIN ISSUE!
# unittesting?

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
        session["won"] = "TBC"             # winner(s) to be declared
        
        # by this point all the basic player data is now stored in the session.
        print("session = ", session)
        
        # if POST then redirect to the first player in game view
        return redirect( url_for('game') )
        
    return render_template("index.html")
    

# game page - add more comments - docstring
@app.route("/game", methods=["POST","GET"])
def game():
    
    scores = session["score"]               # holds all the scores
    seq = session["seq"]                    # assigned to a variable only for readability purposes
    username = session["username"][seq]     # player whose turn it is to play
    session["current_player"]= username     # current player
    test_verdict = "UNDECIDED" 
    
    if request.method == "POST":
        
        print("request.form.keys() = ", request.form.keys())
        
        if "reset" in request.form.keys():
            # reseting mechanism - triggered via the reset button
            reset_table(restart=True)   # clearing the session as well as resetting the table 
            return redirect( url_for("index")) 
        
        if "next" in request.form.keys(): 
            test_verdict = get_verdict(session["playerHand"], session["houseHand"])
            print("NEXT!!!!!!  test_verdict = ", test_verdict)
            apply_verdict(test_verdict)
                
            
            # pass
        
        
        if "hit" in request.form.keys():
            # deals one card to the player
            # session["playerHand"].append( ('clubs', 'K') )
            session["playerHand"].append(deck.deal())
        
        
        test_verdict = get_verdict(session["playerHand"], session["houseHand"])

        
        if "stand" in request.form.keys():
            # house gets cards until one of the below conditions is met.
            # BLACKJACK, BUST or hand value higher than player
            session["houseHand"] = deck.deal(2) # initialising house hand
            house_hand = house_plays(deck, session["playerHand"], session["houseHand"]) # simulate house play
            session["houseHand"] = house_hand
            
            test_verdict = get_verdict(session["playerHand"], session["houseHand"])
            print("test_verdict = ", test_verdict)
            

        print("scores = ", scores)

        # reseting mechanism - simulating a full cycle - each full cycle means 1 round
        if session["seq"] >= len( session["username"] ):
            session["seq"] = 0              # reset the sequence counter to cycle back to the first player
            session["rounds_played"] += 1   # when a cycle is complete, one found of game has been played by all the player!
            
            print("rounds played = ", session["rounds_played"])
            
            # game has eneded, declare the winner if there is one
            if session["rounds_played"] == session["rounds"]:
                

                # get maximum score attained by the players
                maxScore = max( scores.values()  )     
                
                # noone has won a single game - declare house as the winner
                if maxScore == 0:       
                    session["won"] = "house"
                
                # check to see if there is anybody else with the same max score
                elif list( scores.values() ).count(maxScore) > 1:     
                    winners_list     = [key for key, value in scores.items() if value == maxScore]      # save all the players with the same max score into a list
                    winners_list_str = ", ".join(str(winner).title() for winner in winners_list)    # convert the list into a string
                    lastComma        = winners_list_str.rfind(",")     # locate the character "," within the string
                    session["won"]   = winners_list_str[:lastComma] + " and" + winners_list_str[lastComma+1:]     # replace lace occurance of "," with "and"
                    
                else:   # only one person scored the max score!
                    session["won"] = max(scores, key= lambda x: scores[x]) # get the player with the highest score
                
                return redirect( url_for('winner') ) 


    player_dict = {"hand": convert_card_names( session["playerHand"] ), "value" : get_hand_value( session["playerHand"] ) }
    house_dict  = {"hand": convert_card_names( session["houseHand"] ), "value" : get_hand_value( session["houseHand"] ),
                    "folded": ["back.jpg","back.jpg"], "house_plays": session["house_plays"] }
    round_dict  = {"total": session["rounds"], "played": session["rounds_played"]+1}

    return render_template("game.html", usernames=session["username"], scores=scores, seq=session["seq"], 
        rounds=round_dict, player=player_dict, house=house_dict, verdict=test_verdict)
    

# show the winner if there is any - add more comments
@app.route("/winner", methods=["POST","GET"])
def winner():
    
    if request.method == "POST":
    
        if "reset" in request.form.keys():
            # reseting mechanism - triggered via the reset button
            reset_table(restart=True)   # clearing the session as well as resetting the table 
            return redirect( url_for("index")) 

    # being passed in for the completeness of the 
    round_dict = {"total": session["rounds"], "played": session["rounds_played"]}
    
    return render_template("winner.html", usernames=session["username"], winner=session["won"], 
        scores=session["score"], rounds=round_dict)

if __name__ == "__main__":
    # host = os.getenv("IP", "0.0.0.0")
    # port = os.getenv("PORT", "8080")
    port = int( os.getenv("PORT") )
    host = os.getenv("IP")
    app.run(host=host, port=port)