from flask import Flask, render_template
from database import get_db, close_db
from forms import BandForm, GigForm, RegistrationForm
from datetime import date, datetime
from sqlite3 import IntegrityError
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished

@app.route("/all_gigs")
def all_gigs():
    db = get_db() 
    gigs = db.execute("""SELECT * FROM gigs;""").fetchall() # Execute the SQL, fetch all the results and store in 'gigs'

    return render_template('gigs.html', caption="All Gigs", gigs=gigs)


@app.route("/future_gigs")
def future_gigs():
    db = get_db() 
    gigs = db.execute("""
                        SELECT * FROM gigs
                        WHERE gig_date >= DATE('now');
                    """).fetchall()

    return render_template('gigs.html', caption="Future Gigs", gigs=gigs)

@app.route("/future_gigs_by_band", methods=["GET", "POST"])
def future_gigs_by_band():
    form = BandForm()
    gigs = None

    if form.validate_on_submit():
        band = form.band.data
        db = get_db()
        gigs = db.execute("""SELECT * FROM gigs
                             WHERE gig_date >= DATE('now')
                             AND band = ?;""", (band,)).fetchall() # even if there is only one placeholder, it must be in a tuple with a ","

    return render_template('gigs_by_band.html', form=form, caption = "Future Gigs", gigs=gigs)

@app.route('/insert_gig', methods=["GET","POST"])
def insert_gig():
    form = GigForm()
    message=""

    if form.validate_on_submit():
        band = form.band.data
        gig_date = form.gig_date.data
        if gig_date <= datetime.now().date():
            form.gig_date.errors.append("Date must be in the future.")
        else:
            db = get_db()
            confliciting_gig = db.execute("""SELECT * FROM gigs WHERE gig_date = ?""", (gig_date,)).fetchone()

            if confliciting_gig is not None:
                form.gig_date.errors.append('Gig clashes with another.')
            else:
                db.execute("""INSERT INTO gigs (band, gig_date)
                            VALUES (?, ?)""", (band, gig_date))
                db.commit() # The insertion will not happen unless the changes are 'commited'

                message = "New gig successfully inserted"

    return render_template('insert_gig.html', form=form, message=message)

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data

        db = get_db()
        try:
            db.execute("""INSERT INTO users (user_id, password)
                          VALUES (?, ?)""", (user_id, generate_password_hash(password)))

            db.commit()

            return 'Redirect to login UNFINISHED'
        except IntegrityError:
            form.user_id.errors.append("User ID is already taken")

    return render_template('register.html', form=form)
