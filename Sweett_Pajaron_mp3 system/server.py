import os
import sqlite3

import requests
from flask import Flask, render_template, request, Response, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key')
DATABASE = os.path.join(app.root_path, 'users.db')


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db_connection() as connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')


init_db()

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            error = 'Username and password are required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        else:
            try:
                with get_db_connection() as connection:
                    cursor = connection.execute(
                        'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                        (username, generate_password_hash(password))
                    )
                    session['user_id'] = cursor.lastrowid
                    session['username'] = username
                return redirect(url_for('home'))
            except sqlite3.IntegrityError:
                error = 'That username is already registered.'

    return render_template('auth.html', mode='register', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        with get_db_connection() as connection:
            user = connection.execute(
                'SELECT id, username, password_hash FROM users WHERE username = ?',
                (username,)
            ).fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        error = 'Invalid username or password.'

    return render_template('auth.html', mode='login', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/stream')
def stream_audio():
    file_id = request.args.get('id')
    if not file_id:
        return "Missing file ID", 400
    
    drive_url = f"https://docs.google.com/uc?export=open&id={file_id}"
    
    # Forward Range headers from the browser to Google Drive for seeking support
    headers = {}
    range_header = request.headers.get('Range', None)
    if range_header:
        headers['Range'] = range_header

    try:
        # 10s connect timeout, 30s read timeout
        req = requests.get(drive_url, headers=headers, stream=True, timeout=(10, 30))
    except requests.exceptions.Timeout:
        return "Connection to Google Drive timed out.", 504
    except requests.exceptions.RequestException as e:
        return f"Failed to reach Google Drive: {e}", 502

    # Expose necessary response headers for browser seekbar controls
    response_headers = {
        'Content-Type': req.headers.get('Content-Type', 'audio/mpeg'),
        'Accept-Ranges': 'bytes',
    }
    if 'Content-Range' in req.headers:
        response_headers['Content-Range'] = req.headers['Content-Range']
    if 'Content-Length' in req.headers:
        response_headers['Content-Length'] = req.headers['Content-Length']

    def generate():
        try:
            for chunk in req.iter_content(chunk_size=1024 * 32):
                if chunk:
                    yield chunk
        finally:
            req.close()

    return Response(
        generate(),
        status=req.status_code,
        headers=response_headers
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)