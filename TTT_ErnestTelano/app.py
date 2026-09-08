from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import random


app = Flask(__name__)

app.config["SECRET_KEY"] = "tic-tac-toe-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# user database
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    # pvp stats
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)

    # bot stats
    bot_wins = db.Column(db.Integer, default=0)
    bot_losses = db.Column(db.Integer, default=0)
    bot_draws = db.Column(db.Integer, default=0)


@login_manager.user_loader
def load_user(user_id):

    user = db.session.get(User, int(user_id))

    return user


# multiplayer games
class Game(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    game_code = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    player_x_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    player_o_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    board = db.Column(
        db.String(20),
        default=",,,,,,,,"
    )

    current_player = db.Column(
        db.String(1),
        default="X"
    )

    winner = db.Column(
        db.String(1),
        nullable=True
    )

    finished = db.Column(
        db.Boolean,
        default=False
    )


# bot games
class BotGame(db.Model):

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

    difficulty = db.Column(
        db.String(20),
        nullable=False
    )

    board = db.Column(
        db.String(20),
        default=",,,,,,,,"
    )

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


# check if a game code is a proper 6 digit code
def valid_game_code(code):

    if not code:
        return False

    if len(code) != 6:
        return False

    if not code.isdigit():
        return False

    return True


# update database
def update_database():

    db.create_all()

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


    # old UUID games are no longer used
    # finish them so matchmaking does not keep opening them

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


# create a unique 6 digit game code
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


# get board from database
def get_board(game):

    board = game.board.split(",")

    return board


# save board to database
def save_board(game, board):

    game.board = ",".join(board)


# check winner
def check_winner(board):

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

    if "" not in board:

        return "D"

    return None


# get X or O for current user
def get_player_symbol(game):

    if game.player_x_id == current_user.id:

        return "X"

    if game.player_o_id == current_user.id:

        return "O"

    return None


# get empty spaces
def get_empty_spaces(board):

    spaces = []

    for i in range(9):

        if board[i] == "":

            spaces.append(i)

    return spaces


# easy bot
def easy_bot_move(board):

    spaces = get_empty_spaces(board)

    if len(spaces) > 0:

        move = random.choice(spaces)

        return move

    return None


# check winning move
def find_winning_move(board, symbol):

    spaces = get_empty_spaces(board)

    for position in spaces:

        test_board = board.copy()

        test_board[position] = symbol

        result = check_winner(test_board)

        if result == symbol:

            return position

    return None


# medium bot
def medium_bot_move(board):

    move = find_winning_move(board, "O")

    if move is not None:

        return move

    move = find_winning_move(board, "X")

    if move is not None:

        return move

    return easy_bot_move(board)


# minimax hard bot
def minimax(board, bot_turn):

    result = check_winner(board)

    if result == "O":

        return 10

    if result == "X":

        return -10

    if result == "D":

        return 0

    spaces = get_empty_spaces(board)

    if bot_turn:

        best_score = -1000

        for position in spaces:

            board[position] = "O"

            score = minimax(board, False)

            board[position] = ""

            if score > best_score:

                best_score = score

        return best_score

    else:

        best_score = 1000

        for position in spaces:

            board[position] = "X"

            score = minimax(board, True)

            board[position] = ""

            if score < best_score:

                best_score = score

        return best_score


# hard bot
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


# choose bot difficulty
def get_bot_move(board, difficulty):

    if difficulty == "easy":

        return easy_bot_move(board)

    elif difficulty == "medium":

        return medium_bot_move(board)

    elif difficulty == "hard":

        return hard_bot_move(board)

    else:

        return easy_bot_move(board)


# home
@app.route("/")
def home():

    if current_user.is_authenticated:

        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# register
@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:

        return redirect(url_for("dashboard"))

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

        db.session.add(new_user)

        db.session.commit()

        return redirect(
            url_for("login")
        )

    return render_template("register.html")


# login
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

            correct_password = check_password_hash(
                user.password,
                password
            )

            if correct_password:

                login_user(user)

                return redirect(
                    url_for("dashboard")
                )

        return render_template(
            "login.html",
            error="Incorrect username or password."
        )

    return render_template("login.html")


# dashboard
@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        user=current_user
    )


# leaderboard
@app.route("/leaderboard")
@login_required
def leaderboard():

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


# matchmaking page
@app.route("/matchmaking")
@login_required
def matchmaking():

    return render_template(
        "matchmaking.html"
    )


# find another player
@app.route("/find_match", methods=["POST"])
@login_required
def find_match():

    existing_game = Game.query.filter(
        (
            (Game.player_x_id == current_user.id)
            |
            (Game.player_o_id == current_user.id)
        ),
        Game.finished == False
    ).first()


    # only continue an old game if it has a proper 6 digit code
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


    # find waiting player
    waiting_game = Game.query.filter(
        Game.player_o_id == None,
        Game.player_x_id != current_user.id,
        Game.finished == False
    ).first()


    if waiting_game:

        # make sure old invalid codes are not used
        if not valid_game_code(waiting_game.game_code):

            waiting_game.finished = True

            db.session.commit()

        else:

            waiting_game.player_o_id = current_user.id

            db.session.commit()

            return redirect(
                url_for(
                    "play_game",
                    game_code=waiting_game.game_code
                )
            )


    # create new game
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


# matchmaking status
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


# pvp game page
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


# current game state
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


# make pvp move
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


    board[position] = symbol

    result = check_winner(board)


    if result:

        game.finished = True

        game.winner = result


        # draw
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


# bot difficulty page
@app.route("/bot")
@login_required
def bot():

    return render_template(
        "bot_select.html"
    )


# create bot game
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


# bot game page
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


    if game.player_id != current_user.id:

        return redirect(
            url_for("bot")
        )


    return render_template(
        "bot_game.html",
        game_code=game_code,
        difficulty=game.difficulty
    )


# bot game state
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


# player move vs bot
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


    # player is X
    board[position] = "X"

    result = check_winner(board)


    # player wins
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


    # draw before bot moves
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


    # bot turn
    game.current_player = "bot"

    bot_position = get_bot_move(
        board,
        game.difficulty
    )


    if bot_position is not None:

        board[bot_position] = "O"


    result = check_winner(board)


    # bot wins
    if result == "O":

        game.finished = True

        game.winner = "O"

        current_user.bot_losses += 1


    # draw
    elif result == "D":

        game.finished = True

        game.winner = "D"

        current_user.bot_draws += 1


    else:

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


# logout
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# start server
if __name__ == "__main__":

    with app.app_context():

        update_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )