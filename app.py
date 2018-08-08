import os
import copy
import sys
from flask import Flask, render_template, request, redirect, flash, url_for, render_template_string
import itertools
import random
import io
from game import Deck

# from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.debug = True


# where the entire data is held
game_state = dict()

house = Deck(2) # number of players going in
# print(house.deck)
# print(len(house.deck))
# print(house.deal())
# print(house.deal())
# print(house.deal())
# print(house.deal())
# print(len(house.deck))


# def trackScore(usernames):
#     score = io.StringIO()
#     score.write('First line.\n')
#     for username in usernames:
#         pass


# to ASK!
# how to stop it submiting when enter is pressed on text inputs on the index page
# the string on the console couldnt break lines so i had to resort to splitting them
# apparently heroku doesnt perform as well with files being editted? should i switch to "io.StringIO()" ?

# game idea
# a bastardised version of blackjack, where players take turn to play against the house,
# every time each players wins agasint the house, they're awarded a point which can be tracked
# via the console (scoreboard).
# has to be tested: only the house is to hold a collection of (2-4) decks depending on the number 
# of players set. 2 decks by default
# how to add images of cards on the screen?
# how link the images to the format used to contruct the deck ("suit", "")


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
            game_state[key] = request.form.getlist(key)
            if key == "username":
                # decided to go with a dictionary here with the usernames stored as keys which makes 
                # the data handling alot easier and the format easier to read.
                game_state["score"] = {username: 0 for username in game_state["username"]}
                
        game_state["seq"] = 0 # initialising user scores
        
        print("game_state = ", game_state)

        seq = game_state["seq"] # assigned to a variable only for readability purposes
        username = game_state["username"][seq]
        return redirect( url_for('game', username=username) ) # targets the view(function)
        
    return render_template("index.html")
    

@app.route("/game/<username>", methods=["POST","GET"])
def game(username):

    scores = game_state["score"]
    usernames = game_state["username"]
    seq = game_state["seq"]

    if request.method == "POST":
        

        for key in request.form.keys():
            if key == "win":
                scores[username] += 1

        # reseting mechanism - simulating a full cycle
        if game_state["seq"] >= len(game_state["username"]):
            game_state["seq"] = 0 
            
        k = game_state["seq"]
        username = game_state["username"][k]
        
        return redirect( url_for('game', username=username) )

    game_state["seq"] += 1

    
    print("NO POST: username, seq = ", username, game_state["seq"])
    return render_template("game.html", username=username, usernames=usernames, data=game_state, scores=scores, seq=game_state["seq"])
    

if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = os.getenv("PORT", "8080")
    app.run(host=host, port=port)