from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class WinnersForm(FlaskForm):
    country = StringField('Country:', validators=[InputRequired()])
    submit = SubmitField('Submit')

class MinWinnersForm(FlaskForm):
    country = StringField('Country:')
    points = StringField('Points:')
    submit = SubmitField('Submit')