from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/form')
def send_form():
    return render_template('form.html')

@app.route('/response', methods=['post'])
def send_response():
    # to get data from the form use request.form["name assigned to data"]
    given_name = request.form['given_name']
    family_name = request.form['family_name']

    return render_template('response.html', given_name=given_name, family_name=family_name)

# --------------------------------------------------------------------------------------------------------
# Combine BOTH methods to ONE route
# --------------------------------------------------------------------------------------------------------
'''
With the below method, the server will run the send_greeting function twice, once after the initial GET request
and again after the form is filled and the results are POST-ed.

This method allows you to leave the action attribute of form blank.
'''
@app.route("/greet_me", methods=['GET','POST'])
def send_greeting():
    if request.method == 'GET':
        return render_template('form.html')

    else: # i.e. a POST request
        given_name = request.form['given_name']
        family_name = request.form['family_name']

        return render_template('response.html', given_name=given_name, family_name=family_name)
