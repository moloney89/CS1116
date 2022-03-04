from flask import Flask, render_template, redirect, url_for, session, make_response, flash
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
from sqlite3 import IntegrityError
import datetime


app = Flask(__name__)
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False # Covers distinction between persistent cookies/memory cookies, True = Persistent (expiry date)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Helper Functions
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

@app.route("/")
def index():
    return render_template("index.html")

# Account Management Routes

@app.route('/register', methods=["GET","POST"])
def register():
    if "user_id" in session:
        return redirect( url_for('index' )) # cross page error message, you must log out first
    form = RegistrationForm()

    if form.validate_on_submit():

        user_id = form.user_id.data
        password = form.password.data

        if validPassword(password)[0]:

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
    if "user_id" in session:
        return redirect(url_for('index')) # cross page message to say already logged in 
    
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

            if "url" in session:
                flash("You have successfully logged in")
                return redirect(session["url"])
            
            else:
                flash("You have successfully logged in")
                return redirect(url_for("index")) # Is there a way to redirect to the URL the user was sent from, i.e. auto send back to cart
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/reset_password', methods=["GET","POST"])
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

            return redirect(url_for('login')) #pass messages cross function? "change successful"

    return render_template('reset_password_form.html', form=form)
        




# Calendar Routes

@app.route("/view_calendar", methods=["GET", "POST"])
def view_calendar():
    session["url"] = 'view_calendar'
    if "user_id" not in session:
        return redirect( url_for('login') )

    searchForm = SearchForm()
    form = CalendarViewForm()
    events = None

    if form.validate_on_submit():
        view_calendar = form.view_calendar.data

        db = get_db()

        if view_calendar == "All events":
            searchForm = SearchForm
            events = db.execute(""" SELECT * FROM events 
                             WHERE user_id = ? ;""", (session["user_id"],)).fetchall()

        else:
            event_date = form.event_date.data

            events = db.execute(""" SELECT * FROM events 
                            WHERE user_id = ? AND event_date = ? ;""", (session["user_id"], event_date)).fetchall()
            
            
            
    return render_template("view_calendar_form.html", searchForm=searchForm, form=form, events = events)

@app.route('/create_event', methods=["GET","POST"])
def create_event():
    session["url"] = 'create_event'

    if "user_id" not in session:
        return redirect( url_for('login') )

    form = CreateEventForm()

    if form.validate_on_submit():
        event_date = form.event_date.data
        event_name = form.event_name.data
        event_all_day = form.event_all_day.data
        event_start_time = str(form.event_start_time.data)
        event_end_time = str(form.event_end_time.data)
        event_category = form.event_category.data
        event_description = form.event_description.data
        # recurring_field = form.recurring_field.data
        # recurring_period = form.recurring_period.data
        # end_repeat = form.end_repeat.data

        user_id = session["user_id"]

        db = get_db()
        
        if event_all_day:
            event_start_time = "All Day"
            event_end_time = "All Day"
            
        
        # Insert event to db
        db.execute(""" 
                        INSERT INTO events (user_id, event_date, event_name, event_start_time, event_end_time, 
                                            event_category, event_description)
                        VALUES (?, ?, ?, ?, ?, ?, ?);
                    """, (user_id ,event_date, event_name, event_start_time, event_end_time, event_category, event_description))
        db.commit()
            

       
        # form.event_name.errors.append("Event already exists on this date!")

        return redirect( url_for('view_calendar') )

    return render_template("create_event_form.html", form=form)

@app.route("/remove_event/<event_id>")
def remove_event(event_id):
    db = get_db()

    db.execute(""" DELETE FROM events WHERE event_id =? AND user_id = ?; """,(event_id, session["user_id"]))
    db.commit()
    return redirect(url_for('view_calendar'))


# To Do List Routes
@app.route("/todo", methods=["GET","POST"])
def todo():
    session["url"] = 'todo'
    if "user_id" not in session:
        return redirect(url_for('login'))

    form = ToDoListForm()
    if "toDoList" not in session:
        to_do_list = []
    else:
        to_do_list = session["toDoList"]

    if form.validate_on_submit():
        
        new_item = form.new_item.data

        to_do_list.append(new_item)

        session["toDoList"] = to_do_list

        
    # response = make_response(render_template("to_do_list_form.html", form=form, to_do_list=to_do_list))

    # response.set_cookie("to_do_list", to_do_list, expires=datetime.datetime.now() + datetime.timedelta(days=1))

    return render_template("to_do_list_form.html", form=form)

