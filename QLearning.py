import chess as ch
import numpy as np
import random as rd
import tensorflow as tf

class Engine:

    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth
        self.replay_buffer = []
        self.q_network = self.build_q_network()
        self.target_network = self.build_q_network()
        self.target_network.set_weights(self.q_network.get_weights())
        self.epsilon = 1.0  
        self.epsilon_decay = 0.995  
        self.epsilon_min = 0.01  
        self.batch_size = 64  
        self.gamma = 0.99  

    def build_q_network(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(64,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def state_to_features(self, state):
        features = np.zeros((64,))
        for square in ch.SQUARES:
            piece = state.piece_at(square)
            if piece is not None:
                features[square] = piece.piece_type
        return features

    def select_action(self, state):
        if rd.random() < self.epsilon:
            return rd.choice(list(state.legal_moves))
        else:
            state_features = self.state_to_features(state)
            q_values = self.q_network.predict(np.array([state_features]))[0]
            legal_moves = list(state.legal_moves)
            move_indices = {move: idx for idx, move in enumerate(legal_moves)}
            best_move = max(legal_moves, key=lambda move: q_values[move_indices[move]])
            return best_move

    def update_replay_buffer(self, state, action, reward, next_state):
        self.replay_buffer.append((state, action, reward, next_state))

    def train_q_network(self):
        batch = rd.sample(self.replay_buffer, self.batch_size)
        states, actions, rewards, next_states = zip(*batch)

        next_q_values = self.target_network.predict(np.array([self.state_to_features(s) for s in next_states]))
        target_q_values = [r + self.gamma * np.max(q) for r, q in zip(rewards, next_q_values)]

        states = np.array([self.state_to_features(s) for s in states])
        actions = [ch.Move.from_uci(str(a)) for a in actions]
        target = self.q_network.predict(states)
        for i, action in enumerate(actions):
            target[i][action] = target_q_values[i]

        self.q_network.fit(states, target, epochs=1, verbose=0)

    def update_target_network(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def getBestMove(self):
        return self.select_action(self.board)

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
