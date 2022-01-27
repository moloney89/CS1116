from re import template
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/greeting/<name>')
def send_greeting_by_name(name):
    # return '''
    # <!DOCTYPE html>
    # <html lang='en'>
    #     <head>
    #         <meta charset="utf-8" />
    #         <title>Web Development</title>
    #     </head>
    #     <body>
    #         <p>Hello, %s</p>
    #     </body>
    # </html>
    # ''' % name

    ''' 
    This way of returning a webpage makes code too long,
    we will return a file instead.
    
    In order to this we must also import a function called: render_template
    
    The file must be stored in a folder called "templates".
    
    In order to return a web page, call render_template('filename') in your return line.

    Note: the filename on its own is sufficient, the function knows its in the folder 'templates'.

    To pass the parameter to the placeholder in the HTML template, assign the placeholder within the render_template function.

    NB: while 'name=name' seems obvious, we are actually letting the program know that the placeholder = variable/parameter

    Standard practice in flask is to have the placeholder and variable have the same name, thus leading to 'name=name'
    '''
    return render_template('greet01.html', name = name)


@app.route('/greeting_lang/<language>/<name>')
def send_greeting_in_language(language:str, name:str):
    hello_dict = {'en':'Hello', 'es':'Hola', 'fr':'Bonjour'}

    # dictionaryName.get(key, "default value") -> .get() allows you to set a default value for what will be returned if the key is not in the dicitonary
    greeting = hello_dict.get(language, 'Hi')

    return render_template('greet02.html', greeting=greeting, name=name)


@app.route('/ciao')
@app.route('/au_revoir/<name>')
@app.route('/adios/<name>')
def send_parting_by_name(name=None):
    return render_template('bye.html', name=name)