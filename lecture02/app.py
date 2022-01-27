from random import choice
from flask import Flask
from datetime import datetime
# Flask is a class definition

# This is creating an object from the class definition
# almost every server-side program we write will begin with this
app = Flask(__name__)

# You will use a decorator -> a line with an "@" before a function name

'''
This decorator defines a route
The route specifies the view function for this endpoint
'''

@app.route('/')
def send_greeting():
    return 'Hello world!'

@app.route('/tell_time')
def send_current_date_time():
    return datetime.now().strftime('%H:%M:%S %d:%m:%y')

@app.route('/greet_me')
def send_random_greeting():
    phrases = ['my friend', 'bad ass', 'you sad sap', 'you failure', 'L', 'W']
    return 'Hello ' + choice(phrases)


# parameters/arguments are passed in via the URL
# this is done with the app route
@app.route('/greet_by_name/<name>')
def send_greeting_by_name(name):
    return 'Hello, ' + name


# you can have multiple routes with one view function
@app.route('/adios/<name>')
@app.route('/au_revoir/<name>')
def send_parting_by_name(name):
    return 'Goodbye, ' + name


# error page handling with flask

@app.errorhandler(404)
def page_not_found(error):
    return 'Wrong URL entered', 404