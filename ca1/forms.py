from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, RadioField, TimeField, BooleanField, DecimalField, SelectField
from wtforms.validators import InputRequired, EqualTo, Optional
import datetime



class RegistrationForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password:", validators=[InputRequired(),EqualTo("password", "Passwords must match")])
    submit = SubmitField("Submit")

class DeletionForm(FlaskForm):
    user_id = StringField("User id:")
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password:", validators=[InputRequired(),EqualTo("password", "Passwords must match")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class ResetPasswordForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    current_password = PasswordField("Password:", validators=[InputRequired()])
    new_password = PasswordField("New password:", validators=[InputRequired()])
    new_password2 = PasswordField("Repeat your new password:", validators=[InputRequired(), EqualTo("new_password", "Passwords must match")])
    submit = SubmitField("Submit")
    

class CreateEventForm(FlaskForm):
    event_date = DateField("Event Date:", validators=[InputRequired()], default = datetime.date.today())
    event_name = StringField("Title:", validators=[InputRequired()])
    event_all_day = BooleanField("Is the event all day?", validators=[Optional()])
    event_start_time = TimeField("Start Time:", validators=[Optional()])
    event_end_time = TimeField("End Time:", validators=[Optional()])
    event_category = RadioField("Category:", choices=["Personal", "Work", "Family", "Other"], default = ["Personal"])
    event_description = StringField("Description (Optional):")
    recurring_field = BooleanField("Repeat Event:")
    recurring_period = RadioField("Repeat every:", choices = ["Day", "Week", "Month"], validators=[Optional()])
    end_repeat = DateField("End repeat on date:", validators=[Optional()])
    submit = SubmitField("Submit")

class CalendarViewForm(FlaskForm):
    view_calendar = RadioField("Choose a view type:", choices=["Events on date","All events", "By category"], validators=[InputRequired()])
    event_date = DateField("Show events on date", validators=[Optional()])
    submit= SubmitField("Submit")

class ToDoListForm(FlaskForm):
    item_details = StringField()
    submit = SubmitField("Add new item")

class ExpenseForm(FlaskForm):
    date = DateField("Date:", validators=[InputRequired()], default = datetime.date.today())
    title = StringField("Title:", validators=[InputRequired()])
    amount = DecimalField("Amount:", places=2, validators=[InputRequired()])
    category = SelectField("Category:", choices=[("Miscellaneous", "Miscellaneous"),("Work", "Work"), ("Health","Health"), ("Food","Food"), 
                                                ("Housing","Housing"), ("Entertainment","Entertainment")], validators=[InputRequired()], default=['Miscellaneous'])
    details = StringField("Details:")
    submit = SubmitField("Submit")