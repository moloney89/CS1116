from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField

class VoteForm(FlaskForm):
    vote = RadioField('What is you favourite binary number?', choices=['0','1'], default=['0'])
    submit = SubmitField('Submit')