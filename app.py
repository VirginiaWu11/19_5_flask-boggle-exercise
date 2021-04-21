from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



from boggle import Boggle

boggle_game = Boggle()


@app.route('/')
def homepage():

    board = boggle_game.make_board()
    session['board']=board
    return render_template('index.html',board=board)

@app.route("/check-guess")
def check_guess():
    """Check if guessed word is both on the board and in our dictionary, return json to frontend AJAX call"""
    guess = request.args["guess"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, guess)

    return jsonify({'result':response})
    # {'result': "ok", "not-on-board", or "not-word}"
