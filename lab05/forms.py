from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class GuessForm(FlaskForm):
    user_input = IntegerField("Guess a number:", validators=[InputRequired(), NumberRange(1,100)])
    submit = SubmitField("Submit")