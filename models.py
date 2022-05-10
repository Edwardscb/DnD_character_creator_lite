from datetime import datetime


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, default='/static/assets/default_profile.png')
    character_id = db.ForeignKey('characters.id', ondelete='cascade')
    my_characters = db.relationship('Character', secondary='character_information', backref='curr_user')

    @classmethod
    def signup(cls, username, email, password, image_url):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url = image_url
)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False

class Character(db.Model):

    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    character_name = db.Column(db.String(30))
    gender = db.Column(db.Text)
    race = db.Column(db.Text)
    character_class = db.Column(db.Text)
    background = db.Column(db.Text)
    stats = db.ForeignKey('stats.id')
    equipment = db.ForeignKey('equipments.id')
    items = db.ForeignKey('items.id')
    character_stats = db.relationship('Stat', secondary='character_information', backref='curr_char')
    character_equipment = db.relationship('Equipment', secondary='character_information', backref='curr_char')
    character_items = db.relationship('Item', secondary='character_information', backref='curr_char')
    creator = db.ForeignKey('users.id')

class CharacterInfo(db.Model):

    __tablename__ = 'character_information'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    char_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='cascade'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id', ondelete='cascade'))
    stat_id = db.Column(db.Integer, db.ForeignKey('stats.id', ondelete='cascade'))
    equip_id = db.Column(db.Integer, db.ForeignKey('equipments.id', ondelete='cascade'))



class Stat(db.Model):

    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)

class Equipment(db.Model):

    __tablename__ = 'equipments'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    weapon1 = db.Column(db.Text)
    weapon2 = db.Column(db.Text)
    weapon3 = db.Column(db.Text)
    armor = db.Column(db.Text)

class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    item1 = db.Column(db.Text)
    item2 = db.Column(db.Text)
    item3 = db.Column(db.Text)
    item4 = db.Column(db.Text)
    item5 = db.Column(db.Text)
    item6 = db.Column(db.Text)



    



