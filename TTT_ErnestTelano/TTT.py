from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import random

# Initialize the Flask application and configure the database settings.
app = Flask(__name__)

app.config["SECRET_KEY"] = "tic-tac-toe-secret-key"

# use SQLite to store the game data
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Configure Flask-Login to manage user authentication and sessions. 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect users to login when required.

class User(UserMixin, db.Model):  # OOP - Inheritance: gets login methods from UserMixin and DB behavior from db.Model.
    # OOP - Encapsulation: this class stores username, password, wins, losses, draws, etc. for each user object.

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # password is saved as a hash for security

    # stats for player vs player games
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)

    # stats for player vs bot games
    bot_wins = db.Column(db.Integer, default=0)
    bot_losses = db.Column(db.Integer, default=0)
    bot_draws = db.Column(db.Integer, default=0)

# get the user that is currently logged in

@login_manager.user_loader
def load_user(user_id):

    user = db.session.get(User, int(user_id))

    return user

class Game(db.Model):  # OOP - Encapsulation: stores one match's full state in one object.
    # OOP - Association: player_x_id and player_o_id link the game to User records.

    id = db.Column(db.Integer, primary_key=True)

    # short code used to join the game
    game_code = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    # connect the game players to the User table
    player_x_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    player_o_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True  # stays empty until another player joins
    )

    # the board is stored as text in the database
    board = db.Column(
        db.String(20),
        default=",,,,,,,,"
    )

    current_player = db.Column(
        db.String(1),
        default="X"
    )

    # stores X, O, D for a finished game, or nothing
    winner = db.Column(
        db.String(1),
        nullable=True
    )

    finished = db.Column(
        db.Boolean,
        default=False
    )

class BotGame(db.Model):  # OOP - Encapsulation: stores bot game data in one object.
    # OOP - Association: player_id links the bot game to a specific User.

    id = db.Column(db.Integer, primary_key=True)

    game_code = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    player_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    # stores the selected bot difficulty
    difficulty = db.Column(
        db.String(20),
        nullable=False
    )

    board = db.Column(
        db.String(20),
        default=",,,,,,,,"
    )

    # shows whose turn it is
    current_player = db.Column(
        db.String(10),
        default="player"
    )

    winner = db.Column(
        db.String(10),
        nullable=True
    )

    finished = db.Column(
        db.Boolean,
        default=False
    )

# Helper functions manage data validation, board conversion, and win detection.

# Validate the game code before allowing a player to join or continue a match.
def valid_game_code(code):

    if not code:
        return False

    if len(code) != 6:
        return False

    if not code.isdigit():
        return False

    return True

# create and update the database when the server starts
def update_database():

    # create tables if they do not exist
    db.create_all()

    # add bot stats if an older database does not have them

    connection = db.engine.raw_connection()
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(user)")

    rows = cursor.fetchall()

    columns = []

    for row in rows:

        columns.append(row[1])

    if "bot_wins" not in columns:

        cursor.execute(
            "ALTER TABLE user ADD COLUMN bot_wins INTEGER DEFAULT 0"
        )

    if "bot_losses" not in columns:

        cursor.execute(
            "ALTER TABLE user ADD COLUMN bot_losses INTEGER DEFAULT 0"
        )

    if "bot_draws" not in columns:

        cursor.execute(
            "ALTER TABLE user ADD COLUMN bot_draws INTEGER DEFAULT 0"
        )

    connection.commit()

    cursor.close()
    connection.close()

    # finish old games that still use an invalid code

    old_pvp_games = Game.query.filter_by(
        finished=False
    ).all()

    for game in old_pvp_games:

        if not valid_game_code(game.game_code):

            game.finished = True

    old_bot_games = BotGame.query.filter_by(
        finished=False
    ).all()

    for game in old_bot_games:

        if not valid_game_code(game.game_code):

            game.finished = True

    db.session.commit()

# create a new 6 digit code that is not already used
def create_game_code():

    while True:

        game_code = str(
            random.randint(100000, 999999)
        )

        pvp_game = Game.query.filter_by(
            game_code=game_code
        ).first()

        bot_game = BotGame.query.filter_by(
            game_code=game_code
        ).first()

        if not pvp_game and not bot_game:

            return game_code

# change the saved board text back into a list

def get_board(game):

    board = game.board.split(",")

    return board

# save the board list as text in the database
def save_board(game, board):

    game.board = ",".join(board)

# check all possible winning lines

def check_winner(board):

    # these are the 8 possible winning lines
    combos = [

        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],

        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],

        [0, 4, 8],
        [2, 4, 6]

    ]

    for combo in combos:

        a = combo[0]
        b = combo[1]
        c = combo[2]

        if board[a] != "":

            if board[a] == board[b] and board[b] == board[c]:

                return board[a]

    # if every space is filled, the game is a draw
    if "" not in board:

        return "D"

    return None

# find out if the logged in player is X or O
def get_player_symbol(game):

    if game.player_x_id == current_user.id:

        return "X"

    if game.player_o_id == current_user.id:

        return "O"

    return None

# find all board positions that are still empty
def get_empty_spaces(board):

    spaces = []

    for i in range(9):

        if board[i] == "":

            spaces.append(i)

    return spaces

# Bot logic controls the different computer difficulty levels.
# The player uses X and the bot uses O.

# Easy mode selects a random empty square.
def easy_bot_move(board):

    spaces = get_empty_spaces(board)

    if len(spaces) > 0:

        move = random.choice(spaces)

        return move

    return None

# test the board to find a move that can win
def find_winning_move(board, symbol):

    spaces = get_empty_spaces(board)

    for position in spaces:

        # use a copy so the real board is not changed
        test_board = board.copy()

        test_board[position] = symbol

        result = check_winner(test_board)

        if result == symbol:

            return position

    return None

# medium bot tries to win first, then block

def medium_bot_move(board):

    move = find_winning_move(board, "O")

    if move is not None:

        return move

    move = find_winning_move(board, "X")

    if move is not None:

        return move

    return easy_bot_move(board)

# hard bot checks possible moves with minimax

def minimax(board, bot_turn):

    result = check_winner(board)

    # stop checking when the game already has a result
    if result == "O":

        return 10   # positive score means the bot wins

    if result == "X":

        return -10  # negative score means the player wins

    if result == "D":

        return 0    # zero means the game is a draw

    spaces = get_empty_spaces(board)

    if bot_turn:

        # the bot chooses the highest score
        best_score = -1000

        for position in spaces:

            board[position] = "O"

            score = minimax(board, False)

            board[position] = ""  # remove the test move before checking another one

            if score > best_score:

                best_score = score

        return best_score

    else:

        # the player side chooses the lowest score
        best_score = 1000

        for position in spaces:

            board[position] = "X"

            score = minimax(board, True)

            board[position] = ""

            if score < best_score:

                best_score = score

        return best_score

# choose the move with the best score
def hard_bot_move(board):

    best_score = -1000

    best_move = None

    spaces = get_empty_spaces(board)

    for position in spaces:

        board[position] = "O"

        score = minimax(board, False)

        board[position] = ""

        if score > best_score:

            best_score = score
            best_move = position

    return best_move

# choose the bot strategy based on difficulty
def get_bot_move(board, difficulty):

    if difficulty == "easy":

        return easy_bot_move(board)

    elif difficulty == "medium":

        return medium_bot_move(board)

    elif difficulty == "hard":

        return hard_bot_move(board)

    else:

        return easy_bot_move(board)

# Routes connect URLs to specific functions that handle requests.
# Each route manages a page, action, or data response for the application.

# Home route redirects users to the correct starting page.
@app.route("/")
def home():

    if current_user.is_authenticated:

        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))

# create a new user account
@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:

        return redirect(url_for("dashboard"))

    # show the form or process the submitted form
    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not username or not password or not confirm_password:

            return render_template(
                "register.html",
                error="Please fill in all fields."
            )

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return render_template(
                "register.html",
                error="Username already exists."
            )

        # create the user and hash the password before saving it
        new_user = User(

            username=username,

            password=generate_password_hash(password),

            wins=0,
            losses=0,
            draws=0,

            bot_wins=0,
            bot_losses=0,
            bot_draws=0

        )

        # add the new account to the database
        db.session.add(new_user)

        # save the new account
        db.session.commit()

        return redirect(
            url_for("login")
        )

    return render_template("register.html")

# log an existing user into the system
@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            username=username
        ).first()

        if user:

            # compare the entered password with the saved hash
            correct_password = check_password_hash(
                user.password,
                password
            )

            if correct_password:

                # start the user's login session
                login_user(user)

                return redirect(
                    url_for("dashboard")
                )

        return render_template(
            "login.html",
            error="Incorrect username or password."
        )

    return render_template("login.html")

# main page after logging in
# only logged in users can open this page
@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        user=current_user
    )

# show player rankings and PvP statistics
@app.route("/leaderboard")
@login_required
def leaderboard():

    # sort players by wins, losses, and draws
    users = User.query.order_by(
        User.wins.desc(),
        User.losses.asc(),
        User.draws.desc()
    ).all()

    leaderboard_data = []

    rank = 1

    for user in users:

        total_games = (
            user.wins +
            user.losses +
            user.draws
        )

        if total_games > 0:

            win_rate = (
                user.wins / total_games
            ) * 100

        else:

            win_rate = 0

        player_data = {

            "rank": rank,

            "username": user.username,

            "wins": user.wins,

            "losses": user.losses,

            "draws": user.draws,

            "total_games": total_games,

            "win_rate": round(win_rate, 1)

        }

        leaderboard_data.append(
            player_data
        )

        rank += 1

    return render_template(
        "leaderboard.html",
        leaderboard=leaderboard_data
    )

# page where players can find a match
@app.route("/matchmaking")
@login_required
def matchmaking():

    return render_template(
        "matchmaking.html"
    )

# find a waiting game or create a new one
@app.route("/find_match", methods=["POST"])
@login_required
def find_match():

    # check if the user is already in an unfinished game
    existing_game = Game.query.filter(
        (
            (Game.player_x_id == current_user.id)
            |
            (Game.player_o_id == current_user.id)
        ),
        Game.finished == False
    ).first()

    # only continue if the saved code is valid
    if existing_game:

        if valid_game_code(existing_game.game_code):

            return redirect(
                url_for(
                    "play_game",
                    game_code=existing_game.game_code
                )
            )

        else:

            existing_game.finished = True

            db.session.commit()

    # look for another player waiting for an opponent
    waiting_game = Game.query.filter(
        Game.player_o_id == None,
        Game.player_x_id != current_user.id,
        Game.finished == False
    ).first()

    if waiting_game:

        if not valid_game_code(waiting_game.game_code):

            waiting_game.finished = True

            db.session.commit()

        else:

            # join the waiting game as player O
            waiting_game.player_o_id = current_user.id

            db.session.commit()

            return redirect(
                url_for(
                    "play_game",
                    game_code=waiting_game.game_code
                )
            )

    # create a new game with the current user as X
    game_code = create_game_code()

    new_game = Game(

        game_code=game_code,

        player_x_id=current_user.id,

        player_o_id=None,

        board=",,,,,,,,",

        current_player="X",

        winner=None,

        finished=False

    )

    db.session.add(new_game)

    db.session.commit()

    return redirect(
        url_for(
            "play_game",
            game_code=game_code
        )
    )

# check whether the second player has joined
@app.route("/match_status/<game_code>")
@login_required
def match_status(game_code):

    game = Game.query.filter_by(
        game_code=game_code
    ).first()

    if not game:

        return jsonify({
            "success": False,
            "message": "Game not found."
        })

    # make sure the user belongs to this game
    if (
        game.player_x_id != current_user.id
        and
        game.player_o_id != current_user.id
    ):

        return jsonify({
            "success": False,
            "message": "You are not part of this game."
        })

    opponent = None

    if game.player_x_id == current_user.id:

        symbol = "X"

        if game.player_o_id:

            opponent_user = db.session.get(
                User,
                game.player_o_id
            )

            opponent = opponent_user.username

    else:

        symbol = "O"

        opponent_user = db.session.get(
            User,
            game.player_x_id
        )

        opponent = opponent_user.username

    return jsonify({

        "success": True,

        "ready": game.player_o_id is not None,

        "game_code": game.game_code,

        "symbol": symbol,

        "opponent": opponent

    })

# page for the actual player vs player game
@app.route("/play/<game_code>")
@login_required
def play_game(game_code):

    game = Game.query.filter_by(
        game_code=game_code
    ).first()

    if not game:

        return redirect(
            url_for("matchmaking")
        )

    if (
        game.player_x_id != current_user.id
        and
        game.player_o_id != current_user.id
    ):

        return redirect(
            url_for("matchmaking")
        )

    return render_template(
        "game.html",
        game_code=game_code
    )

# send the current PvP board to the webpage
@app.route("/game_state/<game_code>")
@login_required
def game_state(game_code):

    game = Game.query.filter_by(
        game_code=game_code
    ).first()

    if not game:

        return jsonify({
            "success": False
        })

    board = get_board(game)

    symbol = get_player_symbol(game)

    opponent = None

    if symbol == "X":

        if game.player_o_id:

            opponent_user = db.session.get(
                User,
                game.player_o_id
            )

            opponent = opponent_user.username

    elif symbol == "O":

        opponent_user = db.session.get(
            User,
            game.player_x_id
        )

        opponent = opponent_user.username

    return jsonify({

        "success": True,

        "board": board,

        "current_player": game.current_player,

        "your_symbol": symbol,

        "opponent": opponent,

        "winner": game.winner,

        "finished": game.finished,

        "ready": game.player_o_id is not None

    })

# receive and process a PvP move
@app.route("/game_move/<game_code>", methods=["POST"])
@login_required
def game_move(game_code):

    game = Game.query.filter_by(
        game_code=game_code
    ).first()

    if not game:

        return jsonify({
            "success": False,
            "message": "Game not found."
        })

    if game.player_o_id is None:

        return jsonify({
            "success": False,
            "message": "Waiting for another player."
        })

    if game.finished:

        return jsonify({
            "success": False,
            "message": "Game is already finished."
        })

    symbol = get_player_symbol(game)

    # make sure the player is moving on their turn
    if symbol != game.current_player:

        return jsonify({
            "success": False,
            "message": "It is not your turn."
        })

    data = request.get_json()

    position = data.get("position")

    if position is None or position < 0 or position > 8:

        return jsonify({
            "success": False,
            "message": "Invalid position."
        })

    board = get_board(game)

    if board[position] != "":

        return jsonify({
            "success": False,
            "message": "That space is already taken."
        })

    # put the player symbol in the selected space
    board[position] = symbol

    # check if the move ended the game
    result = check_winner(board)

    if result:

        game.finished = True

        game.winner = result

        # add one draw to both players
        if result == "D":

            player_x = db.session.get(
                User,
                game.player_x_id
            )

            player_o = db.session.get(
                User,
                game.player_o_id
            )

            player_x.draws += 1

            player_o.draws += 1

        else:

            # add a win to the winner and a loss to the loser
            if result == "X":

                winner_user = db.session.get(
                    User,
                    game.player_x_id
                )

                loser_user = db.session.get(
                    User,
                    game.player_o_id
                )

            else:

                winner_user = db.session.get(
                    User,
                    game.player_o_id
                )

                loser_user = db.session.get(
                    User,
                    game.player_x_id
                )

            winner_user.wins += 1

            loser_user.losses += 1

    else:

        # change the turn to the other player
        if game.current_player == "X":

            game.current_player = "O"

        else:

            game.current_player = "X"

    save_board(game, board)

    db.session.commit()

    return jsonify({

        "success": True,

        "board": board,

        "current_player": game.current_player,

        "winner": game.winner,

        "finished": game.finished

    })

# page where the player chooses a bot difficulty
@app.route("/bot")
@login_required
def bot():

    return render_template(
        "bot_select.html"
    )

# create a new player vs bot game
@app.route("/start_bot_game/<difficulty>")
@login_required
def start_bot_game(difficulty):

    if difficulty not in [
        "easy",
        "medium",
        "hard"
    ]:

        return redirect(
            url_for("bot")
        )

    game_code = create_game_code()

    new_game = BotGame(

        game_code=game_code,

        player_id=current_user.id,

        difficulty=difficulty,

        board=",,,,,,,,",

        current_player="player",

        winner=None,

        finished=False

    )

    db.session.add(new_game)

    db.session.commit()

    return redirect(
        url_for(
            "play_bot_game",
            game_code=game_code
        )
    )

# page for the player vs bot game
@app.route("/bot_game/<game_code>")
@login_required
def play_bot_game(game_code):

    game = BotGame.query.filter_by(
        game_code=game_code
    ).first()

    if not game:

        return redirect(
            url_for("bot")
        )

    # make sure the logged in user owns this game
    if game.player_id != current_user.id:

        return redirect(
            url_for("bot")
        )

    return render_template(
        "bot_game.html",
        game_code=game_code,
        difficulty=game.difficulty
    )

# send the current bot game board to the webpage
@app.route("/bot_game_state/<game_code>")
@login_required
def bot_game_state(game_code):

    game = BotGame.query.filter_by(
        game_code=game_code
    ).first()

    if not game:

        return jsonify({
            "success": False
        })

    if game.player_id != current_user.id:

        return jsonify({
            "success": False
        })

    board = get_board(game)

    return jsonify({

        "success": True,

        "board": board,

        "difficulty": game.difficulty,

        "current_player": game.current_player,

        "winner": game.winner,

        "finished": game.finished

    })

# receive the player's move and make the bot move
@app.route("/bot_move/<game_code>", methods=["POST"])
@login_required
def bot_move(game_code):

    game = BotGame.query.filter_by(
        game_code=game_code
    ).first()

    if not game:

        return jsonify({
            "success": False,
            "message": "Game not found."
        })

    if game.player_id != current_user.id:

        return jsonify({
            "success": False,
            "message": "You do not own this game."
        })

    if game.finished:

        return jsonify({
            "success": False,
            "message": "Game is finished."
        })

    if game.current_player != "player":

        return jsonify({
            "success": False,
            "message": "Wait for the bot."
        })

    data = request.get_json()

    position = data.get("position")

    board = get_board(game)

    if position is None or position < 0 or position > 8:

        return jsonify({
            "success": False,
            "message": "Invalid move."
        })

    if board[position] != "":

        return jsonify({
            "success": False,
            "message": "That space is taken."
        })

    # the player always uses X
    # player always uses X
    board[position] = "X"

    # check the result before letting the bot move
    result = check_winner(board)

    # the player won the game
    if result == "X":

        game.finished = True

        game.winner = "X"

        current_user.bot_wins += 1

        save_board(game, board)

        db.session.commit()

        return jsonify({

            "success": True,

            "board": board,

            "winner": "X",

            "finished": True

        })

    # zero means the game is a draw before bot moves
    if result == "D":

        game.finished = True

        game.winner = "D"

        current_user.bot_draws += 1

        save_board(game, board)

        db.session.commit()

        return jsonify({

            "success": True,

            "board": board,

            "winner": "D",

            "finished": True

        })

    # the bot makes its move using O
    game.current_player = "bot"

    # choose a bot move based on the difficulty
    bot_position = get_bot_move(
        board,
        game.difficulty
    )

    if bot_position is not None:

        board[bot_position] = "O"

    result = check_winner(board)

    # the bot won the game
    if result == "O":

        game.finished = True

        game.winner = "O"

        current_user.bot_losses += 1

    # zero means the game is a draw after bot moves
    elif result == "D":

        game.finished = True

        game.winner = "D"

        current_user.bot_draws += 1

    else:

        # let the player make the next move
        game.current_player = "player"

    save_board(game, board)

    db.session.commit()

    return jsonify({

        "success": True,

        "board": board,

        "winner": game.winner,

        "finished": game.finished,

        "current_player": game.current_player

    })

# log the user out of the account
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )

# Run the Flask application when this file is executed directly.
if __name__ == "__main__":

    # use the Flask app context for database setup
    with app.app_context():

        update_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )