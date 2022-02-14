from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class BandForm(FlaskForm):
    band = StringField("Band:", validators=[InputRequired()])
    submit = SubmitField('Submit')