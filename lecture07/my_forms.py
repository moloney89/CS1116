from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField,RadioField
from wtforms.validators import InputRequired

class AliveForm(FlaskForm):
    alive = BooleanField("Check the box if you think Elvis is still alive:")
    submit = SubmitField("Submit")

class ToppingForm(FlaskForm):
    topping = RadioField("",choices=["anchovies","chocolate","morphine","finger nails"],
        default = "morphine")
    submit = SubmitField("Submit")