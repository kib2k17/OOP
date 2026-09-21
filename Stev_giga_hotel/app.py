from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'gigahotel_secret_key_123'

# --- model classes ---
class Room:
    VALID_STATUSES = {"Available", "Occupied", "Maintenance"}

    def __init__(self, room_id, room_type, price, status="Available"):
        self.id = str(room_id)
        self.type = str(room_type)
        self.price = price
        self.status = status

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        try:
            val = float(value)
            self._price = val if val >= 0 else 0.0
        except (ValueError, TypeError):
            self._price = 0.0

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        val = str(value).title()
        self._status = val if val in self.VALID_STATUSES else "Available"

    def to_dict(self):
        return {"id": self.id, "type": self.type, "price": self.price, "status": self.status}

# --- OOP guest ---
class Guest:
    VALID_STATUSES = {"Reserved", "Checked In", "Checked Out"}

    def __init__(self, guest_id, name, email, room="N/A", status="Checked In", time_in="N/A", time_out="N/A"):
        self.id = str(guest_id)
        self.name = str(name)
        self.email = str(email)
        self.room = str(room)
        self.status = status
        self.time_in = str(time_in) if time_in else "N/A"
        self.time_out = str(time_out) if time_out else "N/A"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        val = str(value).title()
        self._status = val if val in self.VALID_STATUSES else "Checked In"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "room": self.room,
            "status": self.status,
            "time_in": self.time_in,
            "time_out": self.time_out,
        }


# --- OOP food ---
class Food:
    VALID_MEAL_TIMES = {"Breakfast", "Lunch", "Dinner", "Snacks", "All Day"}

    def __init__(self, food_id, name, price, category, status="Available", meal_time="All Day"):
        self.id = str(food_id)
        self.name = str(name)
        self.price = price
        self.category = str(category)
        self.status = str(status)
        self.meal_time = meal_time

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        try:
            val = float(value)
            self._price = val if val >= 0 else 0.0
        except (ValueError, TypeError):
            self._price = 0.0

    @property
    def meal_time(self):
        return self._meal_time

    @meal_time.setter
    def meal_time(self, value):
        val = str(value).title() if value else "All Day"
        self._meal_time = val if val in self.VALID_MEAL_TIMES else "All Day"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "status": self.status,
            "meal_time": self.meal_time
        }


class HotelManager:
    def __init__(self):
        self.rooms = []
        self.guests = []
        self.foods = []
        self.archived_items = []

# --- room operation ---
    def add_room(self, room_id, room_type, price, status):
        self.rooms.append(Room(room_id, room_type, price, status))

    def delete_room(self, room_id):
        for room in self.rooms:
            if room.id == str(room_id):
                self.archived_items.append(room.to_dict())
                break
        self.rooms = [r for r in self.rooms if r.id != str(room_id)]

    def update_room_status(self, room_id, status):
        for room in self.rooms:
            if room.id == str(room_id):
                room.status = status
                break

# --- guest operation ---
    def add_guest(self, name, email, room="N/A", room_number=None, status="Checked In", time_in="N/A", time_out="N/A"):
        assigned_room = room_number or room or "N/A"
        
        existing_ids = [int(g.id.split('-')[1]) for g in self.guests if g.id.startswith('G-') and '-' in g.id]
        new_id = f"G-{max(existing_ids, default=1000) + 1}"
        
        guest = Guest(new_id, name, email, assigned_room, status, time_in, time_out)
        self.guests.append(guest)

        if assigned_room and assigned_room != "N/A":
            self.update_room_status(assigned_room, "Occupied")

    def delete_guest(self, guest_id):
        for guest in self.guests:
            if guest.id == str(guest_id):
                if guest.room and guest.room != "N/A":
                    self.update_room_status(guest.room, "Available")
                self.archived_items.append(guest.to_dict())
                break
        self.guests = [g for g in self.guests if g.id != str(guest_id)]

# --- food operation ---
    def add_food(self, food_id, name, price, category, status="Available", meal_time="All Day"):
        self.foods.append(Food(food_id, name, price, category, status, meal_time))

    def delete_food(self, food_id):
        for food in self.foods:
            if food.id == str(food_id):
                self.archived_items.append(food.to_dict())
                break
        self.foods = [f for f in self.foods if f.id != str(food_id)]

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

@app.context_processor
def inject_global_stats():
    stats = manager.get_stats()
    return dict(total_profit=stats['total_profit'])


# --- login routes ---

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

# --- logout routes ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- dashboard routes ---
@app.route('/dashboard')
@login_required
def dashboard():
    stats = manager.get_stats()
    return render_template(
        'dashboard.html',
        total_rooms=stats['total_rooms'],
        occupied=stats['occupied'],
        guests_count=stats['total_guests'],
        total_profit=stats['total_profit']
    )

# --- room routes ---
@app.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
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

# --- guests routes ---
@app.route('/guests', methods=['GET', 'POST'])
@login_required
def guests():
    if request.method == 'POST':
        action, form = request.form.get('action'), request.form.get
        
        if action == 'add':
            
            now = datetime.now().strftime('%Y-%m-%dT%H:%M')
            manager.add_guest(
                name=form('name'), email=form('email'), room=form('room'),
                status=form('status', 'Checked In'),
                time_in=form('time_in') or now, time_out=form('time_out') or now,
            )
        elif action == 'checkout' and form('id'):
            manager.delete_guest(form('id'))
            
        return redirect(url_for('guests'))

    occupied = {str(g.room) for g in manager.guests if g.status == 'Checked In'}
    available_rooms = [r for r in manager.rooms if r.status == 'Available' and str(r.id) not in occupied]

    return render_template('guests.html', guests=manager.guests, available_rooms=available_rooms, available_foods=manager.foods)

# --- foods routes ---
@app.route('/foods', methods=['GET', 'POST'])
@login_required
def foods():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            manager.add_food(
                request.form.get('id'),
                request.form.get('name'),
                request.form.get('price', 0),
                request.form.get('category'),
                request.form.get('status', 'Available'),
                request.form.get('meal_time', 'All Day')
            )
        elif action == 'delete':
            manager.delete_food(request.form.get('id'))
        return redirect(url_for('foods'))

    query = request.args.get('search', '').lower()
    filtered = [f for f in manager.foods if query in f.id.lower() or query in f.name.lower()] if query else manager.foods
    return render_template('foods.html', foods=[f.to_dict() for f in filtered])

# --- bookings routes ---
@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    return render_template('bookings.html', bookings=[g.to_dict() for g in manager.guests])

# --- reports routes ---
@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html', **manager.get_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)