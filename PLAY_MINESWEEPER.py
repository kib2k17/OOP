import random
from flask import Flask, jsonify, render_template

app = Flask(__name__)

class Minesweeper:
    def __init__(self, grid_size=9, num_mines=20):
        self.grid_size = grid_size
        self.num_mines = num_mines

    def generate_board(self):
        board = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        mines_placed = 0
                
        while mines_placed < self.num_mines:
            r = random.randint(0, self.grid_size - 1)
            c = random.randint(0, self.grid_size - 1)
            if board[r][c] != -1:
                board[r][c] = -1
                mines_placed += 1

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if board[r][c] == -1:
                    continue
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                            if board[nr][nc] == -1:
                                board[r][c] += 1
        return board

game_engine = Minesweeper(grid_size=9, num_mines=20)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/new-game")
def new_game():
    return jsonify(game_engine.generate_board())


if __name__ == "__main__":
    app.run(debug=True)
