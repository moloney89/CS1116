from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, DecimalField
from wtforms.validators import InputRequired, NumberRange

class ShiftForm(FlaskForm):
    plaintext = StringField("Plaintext:", validators=[InputRequired()])
    shift = IntegerField("Shift:", validators=[NumberRange(1,25,'Number must be between %(min)s and %(max)s.'),InputRequired()])
    ciphertext = StringField("Ciphertext:")
    submit = SubmitField("Submit")

class ConversionForm(FlaskForm):
    input_scale = RadioField('',choices=['Fahrenheit:','Celsius:','Kelvin:'], default='Celsius:')
    input = IntegerField('',validators=[InputRequired()])
    output_scale = RadioField('',choices=['Fahrenheit:','Celsius:','Kelvin:'], default='Fahrenheit:')
    output = DecimalField('')
    submit = SubmitField()

