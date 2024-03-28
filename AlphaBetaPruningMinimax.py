import chess as ch
import numpy as np
import random as rd

class Engine:

    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth

    def evaluate_board(self, board):
        return rd.random() * 10

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board(self.board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def getBestMove(self):
        best_move = None
        best_eval = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = self.minimax(self.maxDepth, float('-inf'), float('inf'), False)
            self.board.pop()
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

if __name__ == "__main__":
    class Main:
        def __init__(self, board=ch.Board()):
            self.board=board
            self.engine = Engine(board, 3, ch.WHITE)

        def playHumanMove(self):
            try:
                print(self.board.legal_moves)
                print("""To undo your last move, type "undo".""")
                play = input("Your move: ")
                if play == "undo":
                    self.board.pop()
                    self.board.pop()
                    self.playHumanMove()
                    return
                self.board.push_san(play)
            except:
                self.playHumanMove()

        def playEngineMove(self):
            self.board.push(self.engine.getBestMove()) 

        def startGame(self):
            color = None
            while color not in ["b", "w"]:
                color = input("""Play as (type "b" or "w"): """)
            if color == "b":
                while not self.board.is_checkmate():
                    print("The engine is thinking...")
                    self.playEngineMove()
                    print(self.board)
                    self.playHumanMove()
                    print(self.board)
                print(self.board)
                print(self.board.outcome())
            elif color == "w":
                while not self.board.is_checkmate():
                    print(self.board)
                    self.playHumanMove()
                    print(self.board)
                    self.playEngineMove()
                print(self.board)
                print(self.board.outcome())
            self.board.reset()
            self.startGame()

    newBoard = ch.Board()
    game = Main(newBoard)
    game.startGame()
