from flask import Flask, render_template
from database import get_db, close_db

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished
