from tokenize import Number
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class BMIForm(FlaskForm):
    weight = DecimalField("Weight (kg):", validators=[InputRequired(),NumberRange(10,200)])
    height = DecimalField("Height (m):", validators=[InputRequired(), NumberRange(0.5,3)])
    bmi = DecimalField("BMI:")
    submit = SubmitField("Submit:")