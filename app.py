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
app.secret_key = os.urandom(24) # generate secret key randomly and safely


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
    
    deck.reset()    # restores a full deck of cards
    session["houseHand"]  = [] # deck.deal(2)  # deal 2 new cards to house
    session["playerHand"] = deck.deal(2)  # deal 2 new cards to player


def apply_verdict(verdict):
    """ APPLY points based on the passed verdict """

    if verdict == "PLAYER":
        # player has won - award a point, reset table and move to the next player
        reset_table(increment_seq=True, increment_score=True )
    else:
        # player has lost or PUSH has occured - reset table and move to the next player
        reset_table(increment_seq=True)
            

# defining globals
deck = Deck() # create deck initially with only 1 deck of cards

    # left to do:
    #   if player.hand value is greater than 18, the STAND button should pulsate --DONE!
    #   unittests
    #   responsiveness 
    #   theming and layout  -- DONE! still needs cleaning up
    #   expanding on sass   -- DONE!
    #   readme file
    #   leave more comments -- DONE!

# to ask/DO
# couldnt deploy to heroku, app.py  could not be located --- DONE!!!!!!!
# how do i start with the card faced down? --- DONE!!!!
# how do i address multiple winners, house win, no winners and a winner --- DONE!!
# what to do if the same name was entered repeatedly? should i switch to wtforms? jquery validate?
# create fall back for session if expired ???
# index:    
#           stop submission when enter is pressed or at least check to see if everything was entered --- DONE!
#           center the main input area on the index -- DONE!
#           add more content if they scrol down 
#           make it responsive -- DONE!
#           animate scroll effects on all links https://www.w3schools.com/jquery/tryit.asp?filename=tryjquery_eff_animate_smoothscroll
#                   Add hash (#) to URL when done scrolling (default click behavior) WHY??????
#           make the navbar collapse with the hamburger-- DONE!!

# unittesting?

#  ================= routes =====================
@app.route("/base")
def base():
    return render_template("base.html")


@app.route("/", methods=["POST","GET"])
def index():
    """ welcome view where players data is initially gathered """
    
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
        session["won"] = "TBC"          # winner(s) to be declared
        
        # by this point all the basic player data is now stored in the session.
        # print("session = ", session) # uncomment to check session data
        
        # if POST then redirect to the first player in game view
        return redirect( url_for('game') )
        
    return render_template("index.html")
    


@app.route("/game", methods=["POST","GET"])
def game():

    scores = session["score"]               # holds all the scores
    seq = session["seq"]                    # assigned to a variable only for readability purposes
    username = session["username"][seq]     # player whose turn it is to play
    session["current_player"]= username     # current player
    verdict = "UNDECIDED"                   # is this really needed now? YES, if nothing's been posted we want UNDECIDED to be passed through to the template

    if request.method == "POST":
        
        if "reset" in request.form.keys():
            # reseting mechanism - triggered via the reset button
            reset_table(restart=True)   # clearing the session as well as resetting the table 
            return redirect( url_for("index")) 
        
        if "next" in request.form.keys(): 
            verdict = get_verdict(session["playerHand"], session["houseHand"])
            apply_verdict(verdict)

        if "hit" in request.form.keys():
            # deals one card to the player
            session["playerHand"].append(deck.deal())
        
        verdict = get_verdict(session["playerHand"], session["houseHand"])
        
        if "stand" in request.form.keys():
            # house gets cards until one of the below conditions is met.
            # BLACKJACK, BUST or hand value higher than player
            session["houseHand"] = deck.deal(2) # initialising house hand
            house_hand = house_plays(deck, session["playerHand"], session["houseHand"]) # simulate house play
            session["houseHand"] = house_hand
            
            verdict = get_verdict(session["playerHand"], session["houseHand"])

        # reseting mechanism - simulating a full cycle - each full cycle means 1 round
        if session["seq"] >= len( session["username"] ):
            session["seq"] = 0              # reset the sequence counter to cycle back to the first player
            session["rounds_played"] += 1   # when a cycle is complete, one found of game has been played by all the player!

            # game has eneded, declare the winner if there is one
            if session["rounds_played"] == session["rounds"]:
                
                # pick the winner
                session["won"] = pick_winner(scores)

                return redirect( url_for('winner') ) 

    # dictionaries will be easier to handle on the template and less variables are needed to be passed.
    player_dict = {"hand": convert_card_names( session["playerHand"] ), "value" : get_hand_value( session["playerHand"] ) }
    house_dict  = {"hand": convert_card_names( session["houseHand"] ), "value" : get_hand_value( session["houseHand"] ) }
    round_dict  = {"total": session["rounds"], "played": session["rounds_played"]+1}

    return render_template("game.html", usernames=session["username"], scores=scores, seq=session["seq"], 
        rounds=round_dict, player=player_dict, house=house_dict, verdict=verdict)
    

@app.route("/winner", methods=["POST","GET"])
def winner():
    """ select the winner if there is any """
    
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