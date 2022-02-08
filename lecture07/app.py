from flask import Flask, render_template
from my_forms import AliveForm, ToppingForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key" # this line is also for security purposes


@app.route('/alive', methods=['GET','POST'])
def alive():
    form = AliveForm()
    outcome=""
    if form.validate_on_submit():
        alive = form.alive.data
        if alive:
            outcome = "You are right! He is living on the moon."

        else: 
            outcome = "You are wrong. I saw him down the chipper."
    
    return render_template('alive_form.html', title='Elvis Lives?', form=form,outcome=outcome)

@app.route('/topping', methods=["GET","POST"])
def topping():
    form = ToppingForm()
    outcome = ""
    topping = ""
    if form.validate_on_submit():
        topping = form.topping.data
        if topping == 'anchovies':
            outcome = 'You are right.'
        else:
            outcome = 'You are wrong.'
    
    return render_template('topping_form.html', title="Elvis Eats?", form=form, topping=topping, outcome=outcome)

