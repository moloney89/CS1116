from flask import Flask, render_template
from database import get_db, close_db
from forms import WinnersForm, MinWinnersForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key" # this line is also for security purposes
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished

@app.route('/winners', methods=["POST","GET"])
def winners():
    form = WinnersForm()
    wins = None
    if form.validate_on_submit():
        country = form.country.data
        db = get_db()
        exists = db.execute("""SELECT COUNT(country) FROM winners WHERE country = ?""",(country,)).fetchone()[0]
        if exists > 0:
            wins = db.execute("""SELECT * FROM winners
                                 WHERE country == ?;""",(country,)).fetchall()
        else:
            form.country.errors.append('Country not found in the database.')
        
    return render_template('winners.html', form=form,wins=wins,
                    title='Eurovision Winners',caption='Eurovision Winners')


@app.route('/min_winners', methods=["POST","GET"])
def min_winners():
    form = MinWinnersForm()
    wins = None

    if form.validate_on_submit():
        country = form.country.data
    
        points = form.points.data
        if points =='':
            points = '0' # if teh user does not provide points data, it can be any amount of points -> greater than 0

        db = get_db()

        if country == '':   
            wins = db.execute("""SELECT * FROM winners
                                WHERE points >= ?;""",(points,)).fetchall()
        else:
            wins = db.execute("""SELECT * FROM winners
                             WHERE country == ? AND points >= ?;""",(country, points)).fetchall()


    return render_template('min_winners.html', form=form, wins=wins, title='Eurovision Winners',caption='Eurovision Winners')