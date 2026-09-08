from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import json
import os

app = Flask(__name__)
app.secret_key = 'gigahotel_secret_key_123'

DATA_FILE = 'data.json'
ARCHIVE_FILE = 'archive.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    
    default_data = {
        "rooms": [
            {"id": "101", "type": "Deluxe Suite", "price": 150.0, "status": "Available"},
            {"id": "102", "type": "Standard Double", "price": 90.0, "status": "Occupied"},
            {"id": "103", "type": "Single Room", "price": 60.0, "status": "Available"},
            {"id": "104", "type": "Presidential Suite", "price": 350.0, "status": "Maintenance"}
        ],
        "guests": [
            {"id": "G-1001", "name": "Castillo, Kim", "email": "kcastillo@example.com", "room": "102", "status": "Checked In"},
            {"id": "G-1002", "name": "Dela Cruz, Juan", "email": "jdelacruz@example.com", "room": "101", "status": "Reserved"},
            {"id": "G-1003", "name": "stev", "email": "henrymaratas046@gmail.com", "room": "N/A", "status": "Checked In"}
        ],
        "foods": [
            {"id": "F-1001", "name": "Club Sandwich", "category": "Snacks", "price": 12.0, "status": "Available"},
            {"id": "F-1002", "name": "Seafood Pasta", "category": "Main Course", "price": 24.0, "status": "Available"},
            {"id": "F-1003", "name": "Grilled Wagyu Steak", "category": "Main Course", "price": 45.0, "status": "Available"},
            {"id": "F-1004", "name": "Iced Americano", "category": "Beverages", "price": 5.0, "status": "Available"},
            {"id": "F-1005", "name": "Chocolate Lava Cake", "category": "Desserts", "price": 8.5, "status": "Out of Stock"}
        ],
        "events": [
            {"id": "E-1001", "title": "Corporate Tech Summit", "date": "2026-10-15", "location": "Grand Ballroom", "status": "Upcoming"},
            {"id": "E-1002", "title": "Wedding Reception", "date": "2026-11-02", "location": "Garden Pavilion", "status": "Confirmed"},
            {"id": "E-1003", "title": "Annual Executive Meeting", "date": "2026-12-05", "location": "Conference Room A", "status": "Upcoming"}
        ]
    }
    save_data(default_data)
    return default_data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def archive_deleted_item(item_type, item_data):
    archive_data = {"deleted_rooms": [], "deleted_guests": [], "deleted_foods": [], "deleted_events": []}
    
    if os.path.exists(ARCHIVE_FILE):
        with open(ARCHIVE_FILE, 'r') as f:
            try:
                archive_data = json.load(f)
            except json.JSONDecodeError:
                pass

    key = f"deleted_{item_type}s"
    archive_data.setdefault(key, []).append(item_data)

    with open(ARCHIVE_FILE, 'w') as f:
        json.dump(archive_data, f, indent=4)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- login MANAGEMENT ---
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['user'] = 'System Administrator'
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username/password", "error")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    data = load_data()
    rooms_db = data.get('rooms', [])
    guests_db = data.get('guests', [])

    total_rooms = len(rooms_db)
    occupied_rooms = sum(1 for r in rooms_db if r['status'] == 'Occupied')
    total_guests = len(guests_db)
    
    return render_template('dashboard.html', total_rooms=total_rooms, occupied=occupied_rooms, guests_count=total_guests)

# --- rooms MANAGEMENT ---
@app.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
    data = load_data()
    rooms_db = data.get('rooms', [])

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            rooms_db.append({
                "id": request.form.get('id'),
                "type": request.form.get('type'),
                "price": float(request.form.get('price', 0)),
                "status": request.form.get('status'),
                "is_deleted": False
            })
        elif action == 'delete':
            room_id = request.form.get('id')
            for room in rooms_db:
                if room['id'] == room_id:
                    room['is_deleted'] = True
                    archive_deleted_item('room', room)
                    break
        elif action == 'update_status':
            room_id = request.form.get('id')
            new_status = request.form.get('status')
            for room in rooms_db:
                if room['id'] == room_id:
                    room['status'] = new_status
                    break

        data['rooms'] = rooms_db
        save_data(data)
        return redirect(url_for('rooms'))

    active_rooms = [r for r in rooms_db if not r.get('is_deleted', False)]
    
    query = request.args.get('search', '').lower()
    filtered_rooms = [
        r for r in active_rooms 
        if query in str(r['id']).lower() or query in r['type'].lower()
    ] if query else active_rooms

    return render_template('rooms.html', rooms=filtered_rooms)


# --- guests MANAGEMENT ---
@app.route('/guests', methods=['GET', 'POST'])
@login_required
def guests():
    data = load_data()
    guests_db = data.get('guests', [])
    rooms_db = data.get('rooms', [])
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            guests_db.append({
                "id": f"G-{len(guests_db) + 1001}",
                "name": request.form.get('name'),
                "email": request.form.get('email'),
                "room": request.form.get('room'),
                "status": request.form.get('status')
            })
        elif action == 'delete':
            guest_id = request.form.get('id')
            for guest in guests_db:
                if guest['id'] == guest_id:
                    archive_deleted_item('guest', guest)
                    break
            guests_db = [g for g in guests_db if g['id'] != guest_id]

        data['guests'] = guests_db
        save_data(data)
        return redirect(url_for('guests'))

    query = request.args.get('search', '').lower()
    filtered_guests = [g for g in guests_db if query in g['name'].lower() or query in g['email'].lower()] if query else guests_db
    available_rooms = [r for r in rooms_db if r['status'] == 'Available']
    
    return render_template('guests.html', guests=filtered_guests, available_rooms=available_rooms)


# --- foods MANAGEMENT ---
@app.route('/foods', methods=['GET', 'POST'])
@login_required
def foods():
    data = load_data()
    foods_db = data.get('foods', [])

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            foods_db.append({
                "id": request.form.get('id'),
                "name": request.form.get('name'),
                "price": float(request.form.get('price', 0)),
                "category": request.form.get('category')
            })
        elif action == 'delete':
            food_id = request.form.get('id')
            for food in foods_db:
                if str(food['id']) == str(food_id):
                    archive_deleted_item('food', food)
                    break
            foods_db = [f for f in foods_db if str(f['id']) != str(food_id)]

        data['foods'] = foods_db
        save_data(data)
        return redirect(url_for('foods'))

    query = request.args.get('search', '').lower()
    filtered_foods = [
        f for f in foods_db 
        if query in str(f['id']).lower() or query in f['name'].lower()
    ] if query else foods_db

    return render_template('foods.html', foods=filtered_foods)

# --- events & REPORTS ---
@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    data = load_data()
    events_db = data.get('events', [])

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            events_db.append({
                "id": request.form.get('id'),
                "title": request.form.get('title'),
                "date": request.form.get('date'),
                "location": request.form.get('location')
            })
        elif action == 'delete':
            event_id = request.form.get('id')
            for event in events_db:
                if str(event['id']) == str(event_id):
                    archive_deleted_item('event', event) 
                    break
            events_db = [e for e in events_db if str(e['id']) != str(event_id)]

        data['events'] = events_db
        save_data(data)
        return redirect(url_for('events'))

    query = request.args.get('search', '').lower()
    filtered_events = [
        e for e in events_db 
        if query in str(e['id']).lower() or query in e['title'].lower()
    ] if query else events_db

    return render_template('events.html', events=filtered_events)


# --- bookings & REPORTS ---
@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    data = load_data()
    return render_template('bookings.html', bookings=data.get('guests', []))


@app.route('/reports')
@login_required
def reports():
    data = load_data()
    rooms_db = data.get('rooms', [])
    guests_db = data.get('guests', [])

    total_rooms = len(rooms_db)
    occupied_rooms = sum(1 for r in rooms_db if r['status'] == 'Occupied')
    total_guests = len(guests_db)
    total_profit = sum(r['price'] for r in rooms_db if r['status'] == 'Occupied')

    return render_template(
        'reports.html', 
        total_rooms=total_rooms, 
        occupied=occupied_rooms, 
        total_guests=total_guests,
        total_profit=total_profit
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)