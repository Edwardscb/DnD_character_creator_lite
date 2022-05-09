from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, SelectField
from wtforms.validators import DataRequired, Email, Length, InputRequired


class NewUserForm(FlaskForm):

    username = TextField('Username', validators=[InputRequired()])
    email = TextField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = TextField('(Optional) Image URL')

class LoginForm(FlaskForm):

    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class CharacterCreationForm(FlaskForm):

    character_name = TextField('Character Name')
    gender = SelectField('Sex')
    race = SelectField('Race')
    character_class = SelectField('Class')
    background = SelectField('Background')
    


