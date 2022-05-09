from datetime import datetime


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, default='/static/assets/default_profile.jpg')

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

    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    character_name = (db.String(30))
    gender = (db.Text)
    race = (db.Text)
    character_class = (db.Text)

    



