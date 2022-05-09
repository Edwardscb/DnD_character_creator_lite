import os
import requests
from flask import Flask, render_template, session, g, request, flash, redirect
from models import User, db, connect_db
from sqlalchemy.exc import IntegrityError
from forms import NewUserForm, LoginForm, CharacterCreationForm

app = Flask(__name__)

CURR_USER_KEY = "curr_user"

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///dnd_database'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "1234abcd")

connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():
    """if a user is logged in, it sets the global user variable to CURR_USER_KEY in session""" 
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    
    else:
        g.user = None


@app.route('/')
def home_page():
    """ landing page, renders home page"""

    
    return render_template('home.html')

def do_login(user):
    """puts the user.id into the session"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """if a user is logged in, it removes them from the session"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/login', methods=["GET", "POST"])
def login():
    """Allows a user to input username/password.  On submit, credentials are authenticated.  If correct, returns user, else returns False and re-renders the template
    with an error message"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(username = form.username.data, password = form.password.data)
        
        if user:
            do_login(user)
            return redirect('/')
        
        
        else:
            flash('Wrong username or password', 'error-message')
            return render_template('login.html', form=form)
        
    
    else:
        return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """Allows a user to input basic information to sign-up and if fields are valid, logs user in"""
    form = NewUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(

                image_url = form.image_url.data,                            
                username = form.username.data,
                password = form.password.data,
                email = form.email.data
                
            )

            db.session.commit()
        
        except IntegrityError:
            flash('Username already taken', 'error-message')
            return render_template('signup.html', form=form)
        
        do_login(user)

        return redirect('/')
    
    else:
        return render_template('signup.html', form=form)

# these serve as a place to store the data once requested from the dnd5e api        
dnd_classes = []
dnd_races = []
dnd_backgrounds = [('Acolyte', 'Acolyte'), ('Charlatan', 'Charlatan'), ('Criminal', 'Criminal'), ('Entertainer', 'Entertainer'), ('Folk Hero', 'Folk Hero'), 
('Guild Artisan', 'Guild Artisan'), ('Hermit', 'Hermit'), ('Noble', 'Noble'), ('Outlander', 'Outlander'), ('Sage', 'Sage'), ('Sailor', 'Sailor'), ('Soldier', 'Soldier'),
('Urchin', 'Urchin')]


def get_races(races):
    """function to get the races out of the results returned by the dnd api and puts them into tuple format so the WTForms select field can use them"""
    for race in races:
        new_race = race.get('name')
        dnd_races.append((new_race, new_race))

def get_classes(myClass):
    """function to get the classes out of the results returned by the dnd api and puts them into tuple format so the WTForms select field can use them"""
    for new_class in myClass:
        jobClass = new_class.get('name')
        dnd_classes.append((jobClass,jobClass))


@app.route('/new_character')
def create_new_character():

    form = CharacterCreationForm()

    gender = [('Male', 'Male'), ('Female', 'Female'), ('Yes', 'Yes'), ('No', 'No'), ('Maybe?', 'Maybe?'), ('None', 'None')]
    form.gender.choices = gender
    races = requests.get('https://www.dnd5eapi.co/api/races').json()
    results = races.get('results')    
    classes = requests.get('https://www.dnd5eapi.co/api/classes/').json()
    class_results = classes.get('results')    
    get_races(results)
    get_classes(class_results)
    form.race.choices = dnd_races
    form.character_class.choices = dnd_classes
    form.background.choices = dnd_backgrounds
    print(dnd_races)
    print(dnd_classes)  


    return render_template('character_creation.html', form=form)

# @app.route('/logout')

# @app.route('/users/<int:user_id>')

# @app.route('/users/<int:user_id>/new_character')

# @app.route('/user/<int:user_id>/characters')

# @app.route('/user/<int:user_id>/characters/<int:character_id>')

