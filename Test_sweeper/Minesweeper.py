import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

class Minesweeper: # creates the board
    def generate_board(self, grid_size, num_mines):
        board = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        mines_placed = 0
        
        # Prevent infinite loop if mines exceed total grid space
        num_mines = min(num_mines, (grid_size * grid_size) - 1)
                
        while mines_placed < num_mines:
            r = random.randint(0, grid_size - 1)
            c = random.randint(0, grid_size - 1)
            if board[r][c] != -1:
                board[r][c] = -1
                mines_placed += 1

        for r in range(grid_size):
            for c in range(grid_size):
                if board[r][c] == -1:
                    continue
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < grid_size and 0 <= nc < grid_size:
                            if board[nr][nc] == -1:
                                board[r][c] += 1
        return board

game_engine = Minesweeper() 

@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/new-game") # returns back to new game
def new_game():
    # Dynamic grid configuration sent from the user interface
    size = int(request.args.get("size", 9))
    mines = int(request.args.get("mines", 10))
    return jsonify(game_engine.generate_board(size, mines))

if __name__ == "__main__":
    app.run(debug=True)
