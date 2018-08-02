import os
from flask import Flask, render_template, request, redirect, flash


app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/base")
def base():
    return render_template("base.html")

if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = os.getenv("PORT", "8080")
    app.run(host=host, port=port)