from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



from boggle import Boggle

boggle_game = Boggle()
board = boggle_game.make_board()

@app.route('/')
def home_page():
    return render_template('index.html')