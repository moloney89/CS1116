from flask import Flask, render_template, redirect, url_for, session, make_response
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
from sqlite3 import IntegrityError
from random import randint

app = Flask(__name__)
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False # Covers distinction between persistent cookies/memory cookies, True = Persistent (expiry date)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/guess', methods = ["GET","POST"])
def guess():
    form = GuessForm()
    message = None

    if form.validate_on_submit():
        user_input = int(form.user_input.data)

        if "secret_number" not in session:
            secret_number = randint(1,100)
            session["secret_number"] = secret_number
        
        if user_input == session["secret_number"]: message = "Correct"
        elif user_input > session["secret_number"]: message = "Too High"
        else: message = "Too Low"

    return render_template('guess.html', message=message, form=form)