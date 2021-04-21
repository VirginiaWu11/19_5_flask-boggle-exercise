from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



from boggle import Boggle

boggle_game = Boggle()


@app.route('/')
def homepage():
    """Show board on Homepage"""
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

@app.route("/post-score", methods = ["POST"])
def post_score():
    """Update number of times played and highscore if necessary. Send json back to frontend to relay whether the most recent game broke the record"""
    score = request.json['score']
    highscore = session.get("highscore", 0)
    n_plays = session.get("n_plays",0)


    session["n_plays"]=n_plays +1
    session["highscore"] = max(score,highscore)

    return jsonify(brokeRecord=score>highscore)
    # returns {brokeRecord:true} or {brokeRecord:false} as response.data