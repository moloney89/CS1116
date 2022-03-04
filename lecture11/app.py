from flask import Flask, render_template, redirect, url_for, session
from database import get_db, close_db
from flask_session import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished
app.config["SESSION_PERMANENT"] = False # Covers distinction between persistent cookies/memory cookies, True = Persistent (expiry date)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/wines', methods=["GET"])
def wines():
    db = get_db()
    wines = db.execute("""SELECT * FROM wines;""").fetchall()
    return render_template("wines.html", wines=wines, title='Our Wine Catalog')

@app.route('/wine/<int:wine_id>')
def wine(wine_id):
    db = get_db()
    wine = db.execute("""SELECT * FROM wines
                         WHERE wine_id = ?;""", (wine_id,)).fetchone()
    return render_template("wine.html", wine=wine)

@app.route('/cart')
def cart():
    # Show the cart
    if "cart" not in session:
        session["cart"] = {}

    
    names = {}
    db = get_db()
    for wine_id in session["cart"]:
        wine = db.execute("""SELECT * FROM wines
                             WHERE wine_id = ?;""", (wine_id,)).fetchone()
        
        name = wine["name"]
        names[wine_id] = name

    return render_template("cart.html", cart=session["cart"], names=names)

@app.route('/add_to_cart/<int:wine_id>')
def add_to_cart(wine_id):
    # Add one bottle of wine_id to the cart
    if "cart" not in session:
        # session behaves like a dictionary that we can add cookies to
        session["cart"] = {}
    
    if wine_id not in session["cart"]:
        # If you haven't ordered the wine_id before, add it to the "cart" dictionary with a value of 0
        session["cart"][wine_id] = 0

    # +1 to the value of session['cart'][wine_id]
    session["cart"][wine_id] = session["cart"][wine_id] + 1
    return redirect( url_for("cart") )