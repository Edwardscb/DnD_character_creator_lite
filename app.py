import os
import requests
from flask import Flask, render_template, session, g, request, flash, redirect
from models import User, db, connect_db, Stat, Character, Equipment, Item, Stat
from sqlalchemy.exc import IntegrityError
from forms import NewUserForm, LoginForm, CharacterCreationForm, BaseStatForm, ItemsForm, EquipmentForm, EditProfileForm

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
            return redirect(f'/users/{user.id}')
        
        
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
                                               
                username = form.username.data.lower(),
                password = form.password.data,
                email = form.email.data,
                image_url = form.image_url.data or User.image_url.default.arg,
                
            )



            db.session.commit()
        
        except IntegrityError:
            flash('Username already taken', 'error-message')
            return render_template('signup.html', form=form)
        
        do_login(user)

        return redirect(f'/users/{user.id}')
    
    else:
        return render_template('signup.html', form=form)

# these serve as a place to store the data once requested from the dnd5e api        
dnd_classes = [('', '')]
dnd_races = [('', '')]
dnd_stats = []
dnd_weapons = [('', ''), ('shields', 'Shield')]
dnd_items = [('', '')]
dnd_armor = [('', '')]
dnd_backgrounds = [('', ''), ('Acolyte', 'Acolyte'), ('Charlatan', 'Charlatan'), ('Criminal', 'Criminal'), ('Entertainer', 'Entertainer'), ('Folk Hero', 'Folk Hero'), 
('Guild Artisan', 'Guild Artisan'), ('Hermit', 'Hermit'), ('Noble', 'Noble'), ('Outlander', 'Outlander'), ('Sage', 'Sage'), ('Sailor', 'Sailor'), ('Soldier', 'Soldier'),
('Urchin', 'Urchin')]
gender = [("", ""), ('Male', 'Male'), ('Female', 'Female')]

def get_races():
    """function to get the races out of the results returned by the dnd api and puts them into tuple format so the WTForms select field can use them"""
    if len(dnd_races) < 5:
        races = requests.get('https://www.dnd5eapi.co/api/races').json()
        results = races.get('results')    
        for race in results:
            new_race = race.get('name')
            dnd_races.append((new_race, new_race))
    

def get_classes():
    """function to get the classes out of the results returned by the dnd api and puts them into tuple format so the WTForms select field can use them"""
    if len(dnd_classes) < 5:
        classes = requests.get('https://www.dnd5eapi.co/api/classes/').json()
        class_results = classes.get('results')    
        for new_class in class_results:
            jobClass = new_class.get('name')
            dnd_classes.append((jobClass,jobClass))

def get_stats(num=40):
    """function to populate the dnd_stats list, default is 1 to 18, however, option to do more or less depending on user input"""
    if len(dnd_stats) < 5:
        for n in range(num+1):
            dnd_stats.append((n,n))

def get_equipment():
    """calls the api, gets all weapons, and pushes them to the dnd_weapons list as the name of the weapon if the list isn't already populated"""
    if len(dnd_weapons) < 5:
        weapons = requests.get('https://www.dnd5eapi.co/api/equipment-categories/weapon').json()
        weapons_results = weapons.get('equipment')

        for weapon in weapons_results:
            new_weapon = weapon['name']
            dnd_weapons.append((weapon['index'], new_weapon))

def get_armor():
    """calls the api, gets all armors, and pushes them to the dnd_weapons list as the name of the weapon if the list isn't already populated"""

    if len(dnd_armor) < 5:
        equipment = requests.get('https://www.dnd5eapi.co/api/equipment-categories/armor').json()
        equipment_results = equipment.get('equipment')
        print(equipment_results)

        for armor in equipment_results:
            new_armor = armor['name']
            dnd_armor.append((armor['index'], new_armor))


def get_items():
    """calls the api, gets all items, and pushes them to the dnd_weapons list as the name of the weapon if the list isn't already populated"""
    if len(dnd_items) < 5:
        items = requests.get('https://www.dnd5eapi.co/api/equipment').json()
        items_results = items.get('results')
        for item in items_results:
            new_item = item.get('name')
            dnd_items.append((new_item, new_item))

@app.route('/new_character', methods=["GET", "POST"])
def create_new_character():

    if g.user: 
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
                character_name = form.character_name.data.lower(),
                gender = form.gender.data,
                race = form.race.data,
                character_class = form.character_class.data,
                background = form.background.data
                )

            db.session.add(new_char)
            
            char_stats = Stat(
                strength = int(stat_form.strength.data),
                dexterity = int(stat_form.dexterity.data),
                constitution = int(stat_form.constitution.data),
                intelligence = int(stat_form.intelligence.data),
                wisdom = int(stat_form.wisdom.data),
                charisma = int(stat_form.charisma.data),
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

                    
            g.user.my_characters.append(new_char)
            new_char.character_stats.append(char_stats)
            new_char.character_equipment.append(char_equipment)
            new_char.character_items.append(char_items)
            db.session.commit()

            return redirect(f'/characters/{new_char.id}')
        else: 
            return render_template('character_creation.html', form=form, stat_form=stat_form, equipment_form=equipment_form, item_form=item_form)
    else: 
        flash('Please log-in to create a new character')
        return redirect('/')

@app.route('/logout')
def logout():
    """calls the do_logout function that checks if a user is logged in, and if so, logs them out"""
    do_logout()
    flash('Logout successful! We look forward to your next visit!')
    return redirect('/')
        
@app.route('/users/<int:user_id>', methods=["GET", "POST"])
def profile_page(user_id):
    """shows a user their profile page if they are logged in"""
    user = User.query.get(user_id)
    user_chars = user.my_characters
    try:
        if g.user.id == user_id:
            form = EditProfileForm(obj=g.user)
            if form.validate_on_submit():            
                user.password = form.email.data,
                user.email = form.email.data,
                user.image_url = form.image_url.data,
                db.session.commit()
                return redirect(f"/users/{g.user.id}")
            else:
                return render_template('profile.html', user=user, form=form, user_chars=user_chars)
        else:
            flash("Please login to view the user profile page")
            return render_template('/login')
    except AttributeError:
        flash("Please login to view the user profile page")
        return redirect('/login')

@app.route('/search')
def search_function():
    """User can search for other users by username OR search for characters by character name"""

    search = request.args.get('q').lower()

    if not search:
        users = User.query.all()
        characters = Character.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()
        characters = Character.query.filter(Character.character_name.like(f"%{search}%")).all()
    
    return render_template('search_results.html', users=users, characters=characters)



@app.route('/characters/<int:character_id>', methods=["GET", "POST"])
def character_profile(character_id):
    """this is the route for users to view characters"""
    character = Character.query.get_or_404(character_id)
    character_stats = character.character_stats[0]
    character_equipment = character.character_equipment[0]
    character_items = character.character_items[0]
    # char_armor = character_equipment.armor

    form = CharacterCreationForm(obj=character)
    stat_form = BaseStatForm(obj=character_stats)
    equipment_form = EquipmentForm(obj=character_equipment)
    item_form = ItemsForm(obj=character_items)

    form.gender.choices = gender
    get_races()
    get_classes()
    get_stats()
    get_equipment()
    get_armor()
    get_items()
    
    # char_armor_index = [item[0] for item in dnd_armor if char_armor in item]


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

    # if form.validate_on_submit():
    #     new_char = Character(
    #         character_name = form.character_name.data.lower(),
    #         gender = form.gender.data,
    #         race = form.race.data,
    #         character_class = form.character_class.data,
    #         background = form.background.data
    #         )

    #     db.session.add(new_char)
            
    #     char_stats = Stat(
    #         strength = stat_form.strength.data,
    #         dexterity = stat_form.dexterity.data,
    #         constitution = stat_form.constitution.data,
    #         intelligence = stat_form.intelligence.data,
    #         wisdom = stat_form.wisdom.data,
    #         charisma = stat_form.charisma.data,
    #     )
    #     db.session.add(char_stats)

    #     char_equipment = Equipment(
    #         weapon1 = equipment_form.weapon1.data,
    #         weapon2 = equipment_form.weapon2.data,
    #         weapon3 = equipment_form.weapon3.data,
    #         armor = equipment_form.armor.data,
    #     )
    #     db.session.add(char_equipment)

    #     char_items = Item(
    #         item1 = item_form.item1.data,
    #         item2 = item_form.item2.data,
    #         item3 = item_form.item3.data,
    #         item4 = item_form.item4.data,
    #         item5 = item_form.item5.data,
    #         item6 = item_form.item6.data,
    #     )
    #     db.session.add(char_items)
    #     db.session.commit()

                    
    #     g.user.my_characters.append(new_char)
    #     new_char.character_stats.append(char_stats)
    #     new_char.character_equipment.append(char_equipment)
    #     new_char.character_items.append(char_items)
    #     db.session.commit()

    #     return redirect('/')
    # else: 
    
    return render_template('character_profile.html', form=form, stat_form=stat_form, equipment_form=equipment_form, item_form=item_form)


@app.route('/user/<int:user_id>/characters/<int:character_id>')
def character_edit(user_id, char_id):
    """this is the route for a user to make adjustments to their character"""
    
    return redirect('/')

