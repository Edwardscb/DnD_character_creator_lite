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

class BaseStatForm(FlaskForm):
    class Meta:
        csrf = False

    strength = SelectField('Strength')
    dexterity = SelectField('Dexterity')
    constitution = SelectField('Constitution')
    intelligence = SelectField('Intelligence')
    wisdom = SelectField('Wisdom')
    charisma = SelectField('Charisma')

class EquipmentForm(FlaskForm):

    weapon1 = SelectField('Weapon')
    weapon2 = SelectField('Weapon')
    weapon3 = SelectField('Weapon')
    armor = SelectField('Armor')

class ItemsForm(FlaskForm):

    item1 = SelectField('Item')
    item2 = SelectField('Item')
    item3 = SelectField('Item')
    item4 = SelectField('Item')
    item5 = SelectField('Item')
    item6 = SelectField('Item')
    