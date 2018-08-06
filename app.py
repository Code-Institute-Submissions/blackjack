import os
import copy
import sys
from flask import Flask, render_template, request, redirect, flash, url_for, render_template_string
import itertools
import random
import io

# from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.debug = True

#     # ============= functions ===================
#     def create_deck(num=1):
#         """ ready deck(s) where num is number of decks """
#         
#         jdebug = 0
#         if jdebug > 0:  print('>> create_deck() : called by',sys._getframe(1).f_code.co_name)
#         
#         suits = ["spade", "clubs", "hearts", "diamonds"]
#         ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
#         deck = list(itertools.product(suits,ranks)) * num
#         
#         if jdebug > 0:
#             if num == 1:
#                 print("\tdeck = ", deck)
#         
#         return deck
#     
#     
#     def shuffle(deck):
#         """ get rid of function, just use random.shuffle(deck) """
#         
#         jdebug = 0
#         if jdebug > 0:  print('>> shuffle() : called by',sys._getframe(1).f_code.co_name)
#         
#         random.shuffle(deck)
#         
#         if jdebug > 0:  print("\tdeck = ", deck)
#         
#         return deck
#     
#     
#     def draw_card(deck):
#         """ draw a card """
#         
#         jdebug = 1
#         if jdebug > 0:  print('>> draw_card() : called by',sys._getframe(1).f_code.co_name)
#         
#         # card = sorted(random.choice(deck), reverse=True)
#         card = random.choice(deck)
#         if jdebug > 0:  print("\tcard = ", card)
#         
#         return card
#     
#     
#     def burn_card(deck, card):
#         """ remove played card from the deck, remove parameter and use self.deck """
#         
#         jdebug = 0
#         if jdebug > 0:  print('>> burn_card() : called by',sys._getframe(1).f_code.co_name)
#     
#         indexNum = deck.index(tuple(card))
#         deck.pop(indexNum)
#         
#         return deck


raw_data = dict()


def cyclePlayer(data):

  # reseting mechanism - simulating a full cycle
  if data["seq"] >= len(data["username"]):
    data["seq"] = 0  
  k = data["seq"]
  print("k, seq, usernames[k] = ", k, data["seq"], data["username"][k])

  return data["seq"], data["username"][k]

# def trackScore(usernames):
#     score = io.StringIO()
#     score.write('First line.\n')
#     for username in usernames:
#         pass

#  ================= routes =====================

@app.route("/base")
def base():
    return render_template("base.html")


@app.route("/", methods=["POST","GET"])
def index():

    if request.method == "POST":

        # data = dict((key, request.form.getlist(key)) for key in request.form.keys())
        for key in request.form.keys():
            # print("key = ", key, request.form.getlist(key))
            raw_data[key] = request.form.getlist(key)
            if key == "username":
                temp = {}
                for username in raw_data["username"]:
                    temp[username] = 0
                raw_data["score"] = temp
        raw_data["seq"] = 0
        
        print("raw_data = ", raw_data)
        # print("raw_data = ", raw_data["score"]["damian"])
        seq = raw_data["seq"] 
        username = raw_data["username"][seq]
        return redirect( url_for('game', username=username) ) # targets the view(function)
        
    return render_template("index.html")
    

@app.route("/game/<username>", methods=["POST","GET"])
def game(username):

    scores = raw_data["score"]
    usernames = raw_data["username"]
    seq = raw_data["seq"]

    StrScore = ""
    for user in usernames:
        StrScore += " {}:    {} -".format(user.title(), scores[user])
        # StrScore += render_template_string(" {{userG}}:  {{scoreG}} \n", userG=user.title(), scoreG=scores[user])
    StrScore = StrScore.split("-") # cant seem to be able to add \n to the strings so splitting instead

    if request.method == "POST":
        scores[username] += 1
        
        # reseting mechanism - simulating a full cycle
        if raw_data["seq"] >= len(raw_data["username"]):
            raw_data["seq"] = 0 
            
        k = raw_data["seq"]
        username = raw_data["username"][k]
        
        return redirect( url_for('game', username=username) )
    
    raw_data["seq"] += 1

    
    print("NO POST: username, seq = ", username, raw_data["seq"])
    return render_template("game.html", username=username, usernames=usernames, data=raw_data, scores=scores, StrScore=StrScore, seq=raw_data["seq"])
    

if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = os.getenv("PORT", "8080")
    app.run(host=host, port=port)