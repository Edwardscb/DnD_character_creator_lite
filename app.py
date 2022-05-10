import os
import requests
from flask import Flask, render_template, session, g, request, flash, redirect
from models import User, db, connect_db, Stat, Character, Equipment, Item, Stat
from sqlalchemy.exc import IntegrityError
from forms import NewUserForm, LoginForm, CharacterCreationForm, BaseStatForm, ItemsForm, EquipmentForm

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
dnd_stats = []
dnd_weapons = []
dnd_items = []
dnd_armor = []
dnd_backgrounds = [('Acolyte', 'Acolyte'), ('Charlatan', 'Charlatan'), ('Criminal', 'Criminal'), ('Entertainer', 'Entertainer'), ('Folk Hero', 'Folk Hero'), 
('Guild Artisan', 'Guild Artisan'), ('Hermit', 'Hermit'), ('Noble', 'Noble'), ('Outlander', 'Outlander'), ('Sage', 'Sage'), ('Sailor', 'Sailor'), ('Soldier', 'Soldier'),
('Urchin', 'Urchin')]
gender = [('Male', 'Male'), ('Female', 'Female'), ('Yes', 'Yes'), ('No', 'No'), ('Maybe?', 'Maybe?'), ('None', 'None')]



def get_races():
    """function to get the races out of the results returned by the dnd api and puts them into tuple format so the WTForms select field can use them"""
    if len(dnd_races) < 2:
        races = requests.get('https://www.dnd5eapi.co/api/races').json()
        results = races.get('results')    
        for race in results:
            new_race = race.get('name')
            dnd_races.append((new_race, new_race))
    

def get_classes():
    """function to get the classes out of the results returned by the dnd api and puts them into tuple format so the WTForms select field can use them"""
    if len(dnd_classes) < 2:
        classes = requests.get('https://www.dnd5eapi.co/api/classes/').json()
        class_results = classes.get('results')    
        for new_class in class_results:
            jobClass = new_class.get('name')
            dnd_classes.append((jobClass,jobClass))

def get_stats(num=18):
    """function to populate the dnd_stats list, default is 1 to 18, however, option to do more or less depending on user input"""
    if len(dnd_stats) < 2:
        for n in range(num+1):
            dnd_stats.append((n,n))

def get_equipment():
    """calls the api, gets all weapons, and pushes them to the dnd_weapons list as the name of the weapon if the list isn't already populated"""
    if len(dnd_weapons) < 2:
        weapons = requests.get('https://www.dnd5eapi.co/api/equipment-categories/weapon').json()
        weapons_results = weapons.get('equipment')
        print(weapons_results)

        for weapon in weapons_results:
            new_weapon = weapon['name']
            dnd_weapons.append((new_weapon, new_weapon))

def get_armor():
    """calls the api, gets all armors, and pushes them to the dnd_weapons list as the name of the weapon if the list isn't already populated"""

    if len(dnd_armor) < 2:
        equipment = requests.get('https://www.dnd5eapi.co/api/equipment-categories/armor').json()
        equipment_results = equipment.get('equipment')
        print(equipment_results)

        for armor in equipment_results:
            new_armor = armor['name']
            dnd_armor.append((new_armor, new_armor))


def get_items():
    """calls the api, gets all items, and pushes them to the dnd_weapons list as the name of the weapon if the list isn't already populated"""
    if len(dnd_items) < 2:
        items = requests.get('https://www.dnd5eapi.co/api/equipment').json()
        items_results = items.get('results')
        for item in items_results:
            new_item = item.get('name')
            dnd_items.append((new_item, new_item))

@app.route('/new_character', methods=["GET", "POST"])
def create_new_character():

    form = CharacterCreationForm()
    stat_form = BaseStatForm()
    equipment_form = EquipmentForm()
    item_form = ItemsForm()

    form.gender.choices = gender
    get_races()
    get_classes()
    get_stats()
    get_equipment()
    get_armor()
    get_items()

    form.race.choices = dnd_races
    form.character_class.choices = dnd_classes
    form.background.choices = dnd_backgrounds

    stat_form.strength.choices = dnd_stats
    stat_form.dexterity.choices = dnd_stats
    stat_form.constitution.choices = dnd_stats
    stat_form.intelligence.choices = dnd_stats
    stat_form.wisdom.choices = dnd_stats
    stat_form.charisma.choices = dnd_stats

    equipment_form.weapon1.choices = dnd_weapons
    equipment_form.weapon2.choices = dnd_weapons
    equipment_form.weapon3.choices = dnd_weapons
    equipment_form.armor.choices = dnd_armor

    item_form.item1.choices = dnd_items
    item_form.item2.choices = dnd_items
    item_form.item3.choices = dnd_items
    item_form.item4.choices = dnd_items
    item_form.item5.choices = dnd_items
    item_form.item6.choices = dnd_items

    if form.validate_on_submit():
        new_char = Character(
            character_name = form.character_name.data,
            gender = form.gender.data,
            race = form.race.data,
            character_class = form.character_class.data
            )

        db.session.add(new_char)
        
        char_stats = Stat(
            strength = stat_form.strength.data,
            dexterity = stat_form.dexterity.data,
            constitution = stat_form.constitution.data,
            intelligence = stat_form.intelligence.data,
            wisdom = stat_form.wisdom.data,
            charisma = stat_form.charisma.data,
        )
        db.session.add(char_stats)

        char_equipment = Equipment(
            weapon1 = equipment_form.weapon1.data,
            weapon2 = equipment_form.weapon2.data,
            weapon3 = equipment_form.weapon3.data,
            armor = equipment_form.armor.data,
        )
        db.session.add(char_equipment)

        char_items = Item(
            item1 = item_form.item1.data,
            item2 = item_form.item2.data,
            item3 = item_form.item3.data,
            item4 = item_form.item4.data,
            item5 = item_form.item5.data,
            item6 = item_form.item6.data,
        )
        db.session.add(char_items)

        db.session.commit()
        

        return redirect('/')
    else: 


        return render_template('character_creation.html', form=form, stat_form=stat_form, equipment_form=equipment_form, item_form=item_form)

# @app.route('/logout')

# @app.route('/users/<int:user_id>')

# @app.route('/users/<int:user_id>/new_character')

# @app.route('/user/<int:user_id>/characters')

# @app.route('/user/<int:user_id>/characters/<int:character_id>')

