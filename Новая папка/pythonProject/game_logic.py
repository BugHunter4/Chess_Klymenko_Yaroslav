import pickle
import random

def save_game(board, filename="saved_game.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(board, f)

def load_game(filename="saved_game.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)

def get_bot_move(board):
    moves = list(board.legal_moves)
    return random.choice(moves)
