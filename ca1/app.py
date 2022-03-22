from flask import Flask, render_template, redirect, url_for, session, flash, g, request
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
from sqlite3 import IntegrityError
import datetime
from relativedelta import relativedelta # import to add a "monthdelta", see comments at top of relativedelta.py
from functools import wraps


'''

ITEMS TO DO:
> Add a feature that moves to do list items from current to a "completed" database.
> -> Link the checkboxes to items being completed

> Expenses tracker
> -> Add totaling of expenses to daily view on dashboard
> -> Add spending by month to expenses tracker page
'''

app = Flask(__name__)
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False # Covers distinction between persistent cookies/memory cookies, True = Persistent (expiry date)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# User Validation
@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("You must be logged in to go there.")
            return redirect(url_for('login', request.url))
        return view(**kwargs)
    return wrapped_view






        



# Helper Functions
def todays_events():
    if g.user:
        now = datetime.datetime.now()
        today_date = now.strftime("%Y-%m-%d")
        db = get_db()
        g.todays_events = db.execute("""SELECT * FROM events WHERE user_id = ? AND event_date = ? ORDER BY event_start_time;""", (g.user, today_date)).fetchall()

def get_to_do_list():
    if g.user:
        '''Query the database and retrieve a specific users To Do list for events that are less than 24 hours old'''
        db = get_db()

        # JULIANDAY SQLite function can be used in arithmetic to get the difference between to dates in terms of days
        g.to_do_list = db.execute("""SELECT item_id, user_id, item_details, JULIANDAY(?) - JULIANDAY(creation_date) AS age, completed
                                    FROM to_do_list WHERE age < 1 AND user_id = ?;""", (datetime.datetime.now(), g.user)).fetchall()


def todays_expenses():
    if g.user:
        now = datetime.datetime.now()
        today_date = now.strftime("%Y-%m-%d")
        db = get_db()
        g.todays_expenses = db.execute("""SELECT * FROM expenses WHERE user_id = ? AND date = ?;""", (g.user, today_date)).fetchall()
        
        g.daily_total = 0
        for item in g.todays_expenses:
            g.daily_total += item['amount']
        


def validPassword(password:str):
    '''Confirm if a password is longer than 8 characters, has a capital, lower case and a number'''
    validPass = False
    
    errorMessage = None
    if len(password) < 8:
        errorMessage = "Increase the length"
        return validPass, errorMessage
    else:
        i=0
        upper=0
        digit=0
        lower=0
        while i < len(password):
            if password[i].isupper():
                upper +=1
            elif password[i].islower():
                lower +=1
            elif password[i].isdigit():
                digit +=1
            i+=1
        
        if (upper > 0) and (digit > 0) and (lower > 0):
            validPass=True
            return validPass, errorMessage

        elif (upper > 0) and (digit > 0):
            errorMessage = "Password must contain a lower-case letter"
            return validPass, errorMessage

        elif (upper > 0) and (lower>0):
            errorMessage = "Password must contain a number"
            return validPass, errorMessage
        elif (digit > 0) and (lower > 0):
            errorMessage = "Password must contain an upper-case letter"
            return validPass, errorMessage
        else:
            errorMessage = "Password must contain an upper-case letter, lower-case letter and number"
            return validPass, errorMessage

# -----------------------------------

@app.route("/", methods=["GET","POST"])
def index():
    if g.user:
        todays_events()
        get_to_do_list()
        todays_expenses()

        todo = ToDoListForm()
        if todo.validate_on_submit():
            now = datetime.datetime.now()
            today_date = now.strftime("%Y-%m-%d %H:%M")

            item_details = todo.item_details.data
            creation_date = today_date
            db = get_db()
            db.execute("""INSERT INTO to_do_list (user_id, item_details, creation_date) 
                        VALUES (?, ?, ?);""",(g.user, item_details, creation_date))
            
            db.commit()

            return redirect(url_for('index')) # Use redirect to render empty version of form


        return render_template('dashboard.html', todo=todo)
    else:
        return render_template("index.html")

# Account Management Routes

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        user_id = form.user_id.data
        password = form.password.data

        if validPassword(password)[0]: # validPassword returns a tuple consisting of (Boolean, Error), it boolean = True password
                                       # is valid

            db = get_db()

            try:
                db.execute("""INSERT INTO users (user_id, password)
                            VALUES (?, ?)""", (user_id, generate_password_hash(password)))

                db.commit()

                return redirect(url_for('login'))

            except IntegrityError:
                form.user_id.errors.append("User ID is already taken")
        
        else:
            form.password.errors.append(validPassword(password)[1])


    return render_template('register.html', form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data

        db = get_db()

        matching_user = db.execute("""SELECT * FROM users
                                      WHERE user_id = ?""", (user_id,)).fetchone()
        
        if matching_user is None:
            form.user_id.errors.append("Unknown User!")
        elif not check_password_hash(matching_user["password"], password):
            form.password.errors.append("Incorrect Password")
        else:
            session["user_id"] = user_id
            flash("You have successfully logged in")
            
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")

            return redirect(next_page)
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/reset_password', methods=["GET","POST"])
@login_required
def reset_password():
    form = ResetPasswordForm()

    if form.validate_on_submit():

        user_id = form.user_id.data
        current_password = form.current_password.data
        new_password = form.new_password.data
        new_password2 = form.new_password2.data

        db = get_db()

        matching_user = db.execute("""SELECT * FROM users
                                      WHERE user_id = ?""", (user_id,)).fetchone()
        
        if matching_user is None:
            form.user_id.errors.append("Unknown User!")
        elif not check_password_hash(matching_user["password"], current_password):
            form.current_password.errors.append("Incorrect Password")

        else:
            db.execute("""UPDATE users SET password = ?;""", (generate_password_hash(new_password),))

            db.commit()

            flash("You have successfully changed your password, login below.")
            return redirect(url_for('login')) #pass messages cross function? "change successful"

    return render_template('reset_password_form.html', form=form)
        

@app.route('/account_management', methods=["GET", "POST"])
@login_required
def account_management():
    return render_template('account_management.html')

@app.route('/delete_user', methods=["GET","POST"])
@login_required
def delete_user():
    form = DeletionForm()
    form.user_id.data = g.user
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data

        db = get_db()

        matching_user = db.execute("""SELECT * FROM users
                                      WHERE user_id = ?""", (user_id,)).fetchone()
        
        if matching_user is None:
            form.user_id.errors.append("Unknown User!")
        elif not check_password_hash(matching_user["password"], password):
            form.password.errors.append("Incorrect Password")
        else:
            db.execute("""DELETE FROM users WHERE user_id = ?;""", (user_id,))
            db.execute("""DELETE FROM events WHERE user_id = ?;""", (user_id,))
            db.execute("""DELETE FROM to_do_list WHERE user_id = ?;""", (user_id,))
            db.execute("""DELETE FROM expenses WHERE user_id = ?;""", (user_id,))
            
            session.clear()
            db.commit()
            flash("Account successfully deleted.")
            return redirect(url_for('index'))

    return render_template('delete_user.html', form=form)


# Calendar Routes
@app.route("/view_calendar", methods=["GET", "POST"])
@login_required
def view_calendar():
    form = CalendarViewForm()
    events = None

    if form.validate_on_submit():
        view_calendar = form.view_calendar.data

        db = get_db()

        if view_calendar == "All events":

            events = db.execute(""" SELECT * FROM events 
                             WHERE user_id = ? ORDER BY event_date ;""", (g.user,)).fetchall()

        elif view_calendar == "Events on date":
            event_date = form.event_date.data

            events = db.execute(""" SELECT * FROM events 
                            WHERE user_id = ? AND event_date = ? ;""", (g.user, event_date)).fetchall()
        
        else:
            return redirect(url_for('view_calendar_category', category="All"))
            
    return render_template("view_calendar_form.html", form=form, events = events)

@app.route('/view_calendar_category/<category>', methods=["GET","POST"])
@login_required
def view_calendar_category(category):
    db = get_db()
    events_category = ': '+category
    if category=="All":
        
        events = db.execute(""" SELECT * FROM events 
                             WHERE user_id = ? ORDER BY event_date ;""", (g.user,)).fetchall()
    else:
        events = db.execute(""" SELECT * FROM events 
                             WHERE user_id = ? AND event_category = ? ORDER BY event_date ;""", (g.user, category)).fetchall()

    return render_template('view_calendar_category.html', events_category=events_category, events=events)

@app.route('/create_event', methods=["GET","POST"])
@login_required
def create_event():

    form = CreateEventForm()

    if form.validate_on_submit():
        event_date = form.event_date.data
        event_name = form.event_name.data
        event_all_day = form.event_all_day.data
        event_start_time = str(form.event_start_time.data)
        event_end_time = str(form.event_end_time.data)
        event_category = form.event_category.data
        event_description = form.event_description.data
        recurring_field = form.recurring_field.data

        user_id = g.user

        db = get_db()
        
        if event_all_day:
            event_start_time = "All Day"
            event_end_time = "All Day"

        if recurring_field:
            # If recurring field is true, add event every x amount of times where x = recurring_period
            recurring_period = form.recurring_period.data
            end_repeat = form.end_repeat.data

            date_to_add = event_date # Initialize starting date

            if recurring_period != "Month":
                if recurring_period == "Day": time_difference = 1
                else: time_difference = 7

                while date_to_add <= end_repeat:
                    db.execute(""" 
                            INSERT INTO events (user_id, event_date, event_name, event_start_time, event_end_time, 
                                                event_category, event_description)
                            VALUES (?, ?, ?, ?, ?, ?, ?);
                        """, (user_id ,date_to_add, event_name, event_start_time, event_end_time, event_category, event_description))
                    
                    date_to_add += datetime.timedelta(days = time_difference)

                db.commit()
            
            else: # Monthly
                while date_to_add <= end_repeat:
                    db.execute(""" 
                                INSERT INTO events (user_id, event_date, event_name, event_start_time, event_end_time, 
                                                    event_category, event_description)
                                VALUES (?, ?, ?, ?, ?, ?, ?);
                            """, (user_id ,date_to_add, event_name, event_start_time, event_end_time, event_category, event_description))
                        
                    date_to_add += relativedelta(months = 1)

                db.commit()



        else: # i.e. event not recurring
            
            # Insert event to db
            db.execute(""" 
                            INSERT INTO events (user_id, event_date, event_name, event_start_time, event_end_time, 
                                                event_category, event_description)
                            VALUES (?, ?, ?, ?, ?, ?, ?);
                        """, (user_id ,event_date, event_name, event_start_time, event_end_time, event_category, event_description))
            db.commit()
            

       
        # form.event_name.errors.append("Event already exists on this date!")
        flash("Event(s) added successfully.")
        return redirect( url_for('view_calendar') )

    return render_template("create_event_form.html", form=form)

@app.route("/remove_event/<event_id>")
@login_required
def remove_event(event_id):
    db = get_db()

    db.execute(""" DELETE FROM events WHERE event_id =? AND user_id = ?; """,(event_id, g.user))
    db.commit()
    return redirect(url_for('view_calendar'))

@app.route('/clear_calendar')
@login_required
def clear_calendar():
    db = get_db()
    db.execute(""" DELETE FROM events WHERE user_id = ?; """,(g.user,))
    db.commit()

    flash("Calendar successfully cleared.")
    return redirect(url_for('account_management'))


# To Do List Routes
@app.route('/mark_as_done/<item_id>', methods=["GET","POST"])
@login_required
def mark_as_done(item_id):
    db = get_db()
    db.execute("""UPDATE to_do_list SET completed = 'TRUE' WHERE item_id=?;""", (item_id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/mark_as_not_done/<item_id>', methods=["GET","POST"])
@login_required
def mark_as_not_done(item_id):
    db = get_db()
    db.execute("""UPDATE to_do_list SET completed = 'FALSE' WHERE item_id=?;""", (item_id,))
    db.commit()
    return redirect(url_for('index'))


@app.route('/clear_to_do')
@login_required
def clear_to_do():
    db = get_db()
    db.execute(""" DELETE FROM to_do_list WHERE user_id = ?; """,(g.user,))
    db.commit()

    flash("To Do List successfully cleared.")
    return redirect(url_for('account_management'))

@app.route('/expired_to_do')
@login_required
def expired_to_do():
    db = get_db()

    expired_to_do = db.execute("""SELECT item_id, user_id, item_details, creation_date, JULIANDAY(?) - JULIANDAY(creation_date) AS age
                                 FROM to_do_list WHERE age > 1 AND user_id = ?;""", (datetime.datetime.now(), g.user)).fetchall()

    return render_template('expired_to_do.html', expired_to_do=expired_to_do)


@app.route("/recover_item/<int:item_id>", methods=["GET","POST"])
@login_required
def recover_item(item_id):
    db = get_db()

    db.execute("""UPDATE to_do_list SET creation_date = ? 
                  WHERE item_id = ?;""", (datetime.datetime.now(), item_id)) # This sets the creation date to now, which extends the valid
                                                                             # time on the item by 24 hours.

    db.commit()

    return redirect(url_for('expired_to_do'))


# Expenses Tracker Routes
@app.route('/expenses_tracker', methods=["GET","POST"])
@login_required
def expenses_tracker():
    '''
    View all expenses the user has logged so far
    '''
    db = get_db()

    expenses = db.execute("""
                            SELECT * FROM expenses WHERE user_id = ?;""", (g.user,)).fetchall()
    


    return render_template('expenses_tracker.html', expenses=expenses, category_title=": All")

@app.route('/add_expense', methods=["GET","POST"])
@login_required
def add_expense():
    form = ExpenseForm()

    if form.validate_on_submit():
        date = form.date.data
        title = form.title.data
        amount = float(form.amount.data)
        category = form.category.data
        details = form.details.data


        db = get_db()

        db.execute("""
                      INSERT INTO expenses (user_id, date, title, amount, category, details)
                      VALUES (?, ?, ?, ?, ?, ?);""", (g.user, date, title, amount, category, details))
        
        db.commit()

        flash("Item entered successfully")
        return redirect(url_for('expenses_tracker'))

    return render_template('expenses_tracker_form.html', form=form)

@app.route('/remove_expense/<item_id>')
@login_required
def remove_expense(item_id):
    db = get_db()
    db.execute("""DELETE FROM expenses WHERE item_id = ? AND user_id = ?;""", (item_id,g.user))
    db.commit()
    flash("Item removed")

    return redirect(url_for('expenses_tracker'))

@app.route('/clear_expenses')
@login_required
def clear_expenses():
    db = get_db()
    db.execute("""DELETE FROM expenses WHERE user_id = ?;""", (g.user,))

    return redirect(url_for('account_management'))

@app.route('/expenses_tracker_category/<category>', methods=["GET","POST"])
@login_required
def expenses_tracker_category(category):
    '''
    View all expenses the user has logged so far
    '''
    db = get_db()

    expenses = db.execute("""
                            SELECT * FROM expenses WHERE user_id = ? AND category = ?;""", (g.user, category)).fetchall()
    
    category_title = ': '+category


    return render_template('expenses_tracker.html', expenses=expenses, category_title = category_title)
