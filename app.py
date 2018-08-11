import os
import copy
import sys
from flask import Flask, render_template, request, redirect, flash, url_for, render_template_string, session
from pickle_manage_data import *
from flask_wtf import Form, FlaskForm
from wtforms import StringField, IntegerField, IntegerField, SubmitField, SelectField   # http://wtforms.simplecodes.com/docs/0.6.2/fields.html
from wtforms.validators import DataRequired
from game import Deck

# from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)

# where the entire data is held
# game_state = dict()

house = Deck(2) # number of players going in
print(house.deck)
# print(len(house.deck))
# print(house.deal())
# print(house.deal())
# print(house.deal())
# print(house.deal())
# print(len(house.deck))

# game idea
# a bastardised version of blackjack, where players take turn to play against the house,
# every time each players wins agasint the house, they're awarded a point which can be tracked
# via the console (scoreboard).
# has to be tested: only the house is to hold a collection of (2-4) decks depending on the number 
# of players set. 2 decks by default
# how to add images of cards on the screen?



# TO ASK!

# why cant i install "flask_wtf"? - RESOLVED!
    # i am better off using flask_wtf - tutorials online are very helpful
# still not clear on sessions, users, how the data is held! does refresh gets rid of everything?
    # the difference between sessions and pickle:
        # dont we write to the disk using pickle? why do we have to use it at the first place?
        # does it load user data? if it does how does it pull it off? how do i do it?
# how do i pass arguments in with redirect using url_for? 
# how do i use SVG cards, it's only one file containing all the cards
        # how link the images to the format used to contruct the deck ("suit", "")
# player class needs to be added - player.deck() ...

#  ================= routes =====================
@app.route("/base")
def base():
    return render_template("base.html")


@app.route("/", methods=["POST","GET"])
def index():

    if request.method == "POST":
    
        # the data extracted from the form was coming in as an "ImmutableMultiDict", which made it absolutely impossible to
        # to use the same names (name = username) on the form inputs as it was only capable getting the first value out,
        # it simply fetched the first value with the key "username" and it ignored the rest. However, i wished to use the
        # same names for the inputs within my form however unconventional it might be. so with the use of ".getlist()" the 
        #"ImmutableMultiDict" was changed to a normal dictionary which stores the values for my username key (name input on the form) 
        # as a list containing all the given names as shown in the example below.
        # {'username': [u'damian', u'yoni', u'michael', u'james'] }
        # please refer to the readme.md for more information on this
        for key in request.form.keys():
            
            # game_state[key] = request.form.getlist(key)
            session[key] = request.form.getlist(key)
            
            if key == "username":
                # decided to go with a dictionary here with the usernames stored as keys which makes 
                # the data handling alot easier and the format easier to read.
                session["score"] = {username: 0 for username in session["username"]}
            
            if key == "rounds":
                # targeting the only value within the list and converting it to integer
                session["rounds"] = int(session["rounds"][0]) 
        
        # will be used in conjuction with the given usernames, allowing the 
        # usernames  to play their turns in the same order as they were submitted.     
        session["seq"] = 0 
        session["rounds_played"] = 0 # to keep track of the rounds played
        session["won"] = "TBC"  # winner to be declared

        print("session = ", session)

        return redirect( url_for('game') ) # targets the view(function)
        
    return render_template("index.html")
    

@app.route("/game", methods=["POST","GET"])
def game():

    scores = session["score"]
    usernames = session["username"]

    seq = session["seq"] # assigned to a variable only for readability purposes
    username = session["username"][seq]
    
    if request.method == "POST":
        
        print("request.form.keys() = ", request.form.keys())
        

        
        if "win" in request.form.keys():
            scores[username] += 1
            
        session["score"] = scores
        print("scores = ", scores)
        session["seq"] += 1
        
        # reseting mechanism - simulating a full cycle
        if session["seq"] >= len( session["username"] ):
            session["seq"] = 0            # reset the counter to cycle to the first player
            session["rounds_played"] += 1 # one cycle is complete meaning one round has been played!
            
            print("rounds played = ", session["rounds_played"])
            

            if session["rounds_played"] == session["rounds"]:
                session["won"] = max(scores, key= lambda x: scores[x])
                return redirect( url_for('winner') ) 

    # print("NO POST: username= {}, seq= {}".format(username, session["seq"]))
    return render_template("game.html", usernames=usernames, scores=scores, seq=session["seq"], round=session["rounds_played"]+1)
    


@app.route("/winner")
def winner():
    return render_template("winner.html", winner=session["won"])

if __name__ == "__main__":
    # host = os.getenv("IP", "0.0.0.0")
    # port = os.getenv("PORT", "8080")
    port = int( os.getenv("PORT") )
    host = os.getenv("IP")
    app.run(host=host, port=port)