from unittest import TestCase

from flask.wrappers import Response
from werkzeug.test import Client
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    
    # def test_root_board(self):
    #     with app.test_client() as client:
    #         self.assertEqual(len(session['board']),5)
    #         # self.assertEqual(len(board[4]),5)
    
    def test_root_Directory(self):
        with app.test_client() as client:
            "Test that root directory is working"
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("<td>",html)
            self.assertIn("board",session)
            
    def test_root_board(self):
        """Test if board is added to the flask session"""
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(len(session['board']),5)
            self.assertEqual(len(session['board'][4]),5)
            
    def test_valid_word(self):
        """Test if word is valid, both on the board, and in our dictionary"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['T', 'P', 'K', 'V', 'M'],
                 ['R', 'D', 'T', 'C', 'I'], 
                 ['A', 'J', 'O', 'A', 'B'], 
                 ['J', 'B', 'U', 'G', 'Y'], 
                 ['M', 'U', 'M', 'M', 'Y']]
        resp = client.get('/check-guess?guess=mummy')
        self.assertEqual(resp.json['result'], 'ok')
    
    def test_not_on_board_word(self):
        """Test if word is on the board"""
        with app.test_client() as client:
            client.get('/')
            resp = client.get('/check-guess?guess=impossible')
            self.assertEqual(resp.json['result'],'not-on-board')

    def test_not_in_dictionary_word(self):
        """Test if word is in our words.txt file """
        with app.test_client() as client:
            client.get('/')
            resp = client.get('/check-guess?guess=invalidword')
            self.assertEqual(resp.json['result'],'not-word')