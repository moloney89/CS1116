from flask import Flask, render_template
from my_forms import BMIForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key" # this line is also for security purposes

@app.route('/bmi', methods=["GET","POST"])
def bmi():
    form = BMIForm()

    if form.validate_on_submit(): # if the request is a POST request and if the data validates
        weight = form.weight.data
        height = form.height.data
        bmi = weight/(height**2)
        form.bmi.data = bmi

    return render_template('bmi_form.html', form=form)

