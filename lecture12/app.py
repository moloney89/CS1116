from flask import Flask, render_template, redirect, url_for, session, g
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False # Covers distinction between persistent cookies/memory cookies, True = Persistent (expiry date)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request # Automatically called before each route
def load_logged_in_user():
    g.user = session.get("user_id", None)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
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
                return redirect(session["url"])
            
            else:
                return redirect(url_for("index")) # Is there a way to redirect to the URL the user was sent from, i.e. auto send back to cart
    

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index") )

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data

        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users
                                               WHERE user_id = ?""",(user_id,))
        if possible_clashing_user is not None: 
            form.user_id.errors.append("User ID is already taken!")
        else:                                     
            db.execute("""INSERT INTO users (user_id, password)
                            VALUES (?, ?)""", (user_id, generate_password_hash(password)))

            db.commit()

        return redirect( url_for("login") )

    return render_template('register.html', form=form)


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
    # Check if logged in
    if "user_id" not in session:
        return "Go away, you're not logged in!"

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