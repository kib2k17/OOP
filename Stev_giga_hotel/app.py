from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key_123'

# --- DOMAIN MODELS ---

class Room:
    def __init__(self, room_id, room_type, price, status="Available"):
        self.id = str(room_id)
        self.type = room_type
        self.price = float(price)
        self.status = status

    def to_dict(self):
        return {"id": self.id, "type": self.type, "price": self.price, "status": self.status}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["type"], data["price"], data.get("status", "Available"))


class Guest:
    def __init__(self, guest_id, name, email, room="N/A", status="Checked In"):
        self.id = str(guest_id)
        self.name = name
        self.email = email
        self.room = str(room)
        self.status = status

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "room": self.room, "status": self.status}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["email"], data.get("room", "N/A"), data.get("status", "Checked In"))


class Food:
    def __init__(self, food_id, name, price, category, status="Available"):
        self.id = str(food_id)
        self.name = name
        self.price = float(price)
        self.category = category
        self.status = status

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "category": self.category, "status": self.status}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["category"], data.get("status", "Available"))


class Event:
    def __init__(self, event_id, title, date, location, time="09:00 AM", status="Upcoming"):
        self.id = str(event_id)
        self.title = title
        self.date = date
        self.location = location
        self.time = time
        self.status = status

    def to_dict(self):
        return {"id": self.id, "title": self.title, "date": self.date, "location": self.location, "time": self.time, "status": self.status}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["title"], data["date"], data["location"], data.get("time", "09:00 AM"), data.get("status", "Upcoming"))


# --- HOTEL MANAGER CLASS ---

class HotelManager:
    def __init__(self, data_file='data.json', archive_file='archive.json'):
        self.data_file = data_file
        self.archive_file = archive_file
        self.rooms = []
        self.guests = []
        self.foods = []
        self.events = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            return

        with open(self.data_file, 'r') as f:
            data = json.load(f)
            self.rooms = [Room.from_dict(r) for r in data.get('rooms', [])]
            self.guests = [Guest.from_dict(g) for g in data.get('guests', [])]
            self.foods = [Food.from_dict(f_item) for f_item in data.get('foods', [])]
            self.events = [Event.from_dict(e) for e in data.get('events', [])]

    def save_data(self):
        data = {
            "rooms": [r.to_dict() for r in self.rooms],
            "guests": [g.to_dict() for g in self.guests],
            "foods": [f.to_dict() for f in self.foods],
            "events": [e.to_dict() for e in self.events]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def archive_item(self, item_type, item_obj):
        archive_data = {"deleted_rooms": [], "deleted_guests": [], "deleted_foods": [], "deleted_events": []}
        if os.path.exists(self.archive_file):
            with open(self.archive_file, 'r') as f:
                try:
                    archive_data = json.load(f)
                except json.JSONDecodeError:
                    pass

        key = f"deleted_{item_type}s"
        archive_data.setdefault(key, []).append(item_obj.to_dict())

        with open(self.archive_file, 'w') as f:
            json.dump(archive_data, f, indent=4)

    # --- ROOM OPERATIONS ---
    def add_room(self, room_id, room_type, price, status):
        self.rooms.append(Room(room_id, room_type, price, status))
        self.save_data()

    def delete_room(self, room_id):
        for room in self.rooms:
            if room.id == room_id:
                self.archive_item('room', room)
                break
        self.rooms = [r for r in self.rooms if r.id != room_id]
        self.save_data()

    def update_room_status(self, room_id, status):
        for room in self.rooms:
            if room.id == room_id:
                room.status = status
                break
        self.save_data()

    # --- GUEST OPERATIONS ---
    def add_guest(self, name, email, room_id, status):
        existing_ids = [int(g.id.split('-')[1]) for g in self.guests if g.id.startswith('G-')]
        new_id = f"G-{max(existing_ids, default=1000) + 1}"
        
        self.guests.append(Guest(new_id, name, email, room_id, status))
        if room_id and room_id != "N/A":
            self.update_room_status(room_id, "Occupied")
        self.save_data()

    def delete_guest(self, guest_id):
        for guest in self.guests:
            if guest.id == guest_id:
                if guest.room and guest.room != "N/A":
                    self.update_room_status(guest.room, "Available")
                self.archive_item('guest', guest)
                break
        self.guests = [g for g in self.guests if g.id != guest_id]
        self.save_data()

    # --- FOOD & EVENT OPERATIONS ---
    def add_food(self, food_id, name, price, category):
        self.foods.append(Food(food_id, name, price, category))
        self.save_data()

    def delete_food(self, food_id):
        for food in self.foods:
            if food.id == food_id:
                self.archive_item('food', food)
                break
        self.foods = [f for f in self.foods if f.id != food_id]
        self.save_data()

    def add_event(self, event_id, title, date, location):
        self.events.append(Event(event_id, title, date, location))
        self.save_data()

    def delete_event(self, event_id):
        for event in self.events:
            if event.id == event_id:
                self.archive_item('event', event)
                break
        self.events = [e for e in self.events if e.id != event_id]
        self.save_data()

    # --- REPORTS ---
    def get_stats(self):
        occupied = [r for r in self.rooms if r.status == 'Occupied']
        return {
            "total_rooms": len(self.rooms),
            "occupied": len(occupied),
            "total_guests": len(self.guests),
            "total_profit": sum(r.price for r in occupied)
        }


manager = HotelManager()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin123':
            session['logged_in'] = True
            session['user'] = 'System Administrator'
            return redirect(url_for('dashboard'))
        flash("Invalid username/password", "error")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    manager.load_data()
    stats = manager.get_stats()
    return render_template('dashboard.html', total_rooms=stats['total_rooms'], occupied=stats['occupied'], guests_count=stats['total_guests'])

@app.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
    manager.load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            manager.add_room(request.form.get('id'), request.form.get('type'), request.form.get('price', 0), request.form.get('status'))
        elif action == 'delete':
            manager.delete_room(request.form.get('id'))
        elif action == 'update_status':
            manager.update_room_status(request.form.get('id'), request.form.get('status'))
        return redirect(url_for('rooms'))

    query = request.args.get('search', '').lower()
    filtered = [r for r in manager.rooms if query in r.id.lower() or query in r.type.lower()] if query else manager.rooms
    return render_template('rooms.html', rooms=[r.to_dict() for r in filtered])

@app.route('/guests', methods=['GET', 'POST'])
@login_required
def guests():
    manager.load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            manager.add_guest(request.form.get('name'), request.form.get('email'), request.form.get('room'), request.form.get('status'))
        elif action == 'delete':
            manager.delete_guest(request.form.get('id'))
        return redirect(url_for('guests'))

    query = request.args.get('search', '').lower()
    filtered = [g for g in manager.guests if query in g.id.lower() or query in g.name.lower()] if query else manager.guests
    available_rooms = [r for r in manager.rooms if r.status == 'Available']
    return render_template('guests.html', guests=[g.to_dict() for g in filtered], available_rooms=[r.to_dict() for r in available_rooms])

@app.route('/foods', methods=['GET', 'POST'])
@login_required
def foods():
    manager.load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            manager.add_food(request.form.get('id'), request.form.get('name'), request.form.get('price', 0), request.form.get('category'))
        elif action == 'delete':
            manager.delete_food(request.form.get('id'))
        return redirect(url_for('foods'))

    query = request.args.get('search', '').lower()
    filtered = [f for f in manager.foods if query in f.id.lower() or query in f.name.lower()] if query else manager.foods
    return render_template('foods.html', foods=[f.to_dict() for f in filtered])

@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    manager.load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            manager.add_event(request.form.get('id'), request.form.get('title'), request.form.get('date'), request.form.get('location'))
        elif action == 'delete':
            manager.delete_event(request.form.get('id'))
        return redirect(url_for('events'))

    query = request.args.get('search', '').lower()
    filtered = [e for e in manager.events if query in e.id.lower() or query in e.title.lower()] if query else manager.events
    return render_template('events.html', events=[e.to_dict() for e in filtered])

@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    manager.load_data()
    return render_template('bookings.html', bookings=[g.to_dict() for g in manager.guests])

@app.route('/reports')
@login_required
def reports():
    manager.load_data()
    return render_template('reports.html', **manager.get_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)