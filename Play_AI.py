import chess as ch
import numpy as np
import random as rd
#import tensorflow as tf
from AlphaBetaPruningMinimax import Engine #QLearning, or AlphaBetaPruningMinimax

class Main:

    def __init__(self, board=ch.Board()):
        self.board=board

    def playHumanMove(self):
        try:
            print(self.board.legal_moves)
            play = input("MOVE: ")
            self.board.push_san(play)
        except:
            self.playHumanMove()

    def playEngineMove(self, maxDepth, color):
        engine = Engine(self.board, maxDepth, color)
        Move = engine.getBestMove()
        self.board.push(Move)
        print(Move)

    def startGame(self):
        color = None
        while color not in ["b", "w"]:
            color = input("""Play as (type "b" or "w"): """)
        maxDepth = None
        while not isinstance(maxDepth, int):
            maxDepth = int(input("Choose depth: ")) #
        if color == "b":
            while not self.board.is_checkmate():
                self.playEngineMove(maxDepth, ch.WHITE)
                print(self.board)
                print("")
                self.playHumanMove()
                print(self.board)
            print(self.board)
            print(self.board.outcome())
        elif color == "w":
            while not self.board.is_checkmate():
                print(self.board)
                self.playHumanMove()
                print("")
                print(self.board)
                self.playEngineMove(maxDepth, ch.BLACK)
            print(self.board)
            print(self.board.outcome())
        self.board.reset()
        self.startGame()

# Create an instance and start a game
newBoard = ch.Board()
game = Main(newBoard)
game.startGame()