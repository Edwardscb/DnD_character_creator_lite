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

    character_name = TextField('Character Name', validators=[InputRequired(), Length(max=12)])
    gender = SelectField('Sex')
    race = SelectField('Race', validators=[DataRequired()])
    character_class = SelectField('Class', validators=[DataRequired()])
    background = SelectField('Background')

class BaseStatForm(FlaskForm):
    class Meta:
        csrf = False

    strength = SelectField('Strength', validators=[DataRequired()])
    dexterity = SelectField('Dexterity', validators=[DataRequired()])
    constitution = SelectField('Constitution', validators=[DataRequired()])
    intelligence = SelectField('Intelligence', validators=[DataRequired()])
    wisdom = SelectField('Wisdom', validators=[DataRequired()])
    charisma = SelectField('Charisma', validators=[DataRequired()])

class EquipmentForm(FlaskForm):

    weapon1 = SelectField('Main Hand')
    weapon2 = SelectField('Off Hand')
    weapon3 = SelectField('Back or Two-Hand')
    armor = SelectField('Armor', validators=[DataRequired()])

class ItemsForm(FlaskForm):

    item1 = SelectField('Item')
    item2 = SelectField('Item')
    item3 = SelectField('Item')
    item4 = SelectField('Item')
    item5 = SelectField('Item')
    item6 = SelectField('Item')

class EditProfileForm(FlaskForm):

    email = TextField('Update e-mail')
    password = PasswordField('Update password')
    image_url = TextField('Update profile image')
    
    