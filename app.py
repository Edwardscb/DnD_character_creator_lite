from flask import Flask, render_template



app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')

# @app.route('/login')

# @app.route('/signup')

# @app.route('/logout')

# @app.route('/users/<int:user_id>')

# @app.route('/users/<int:user_id>/new_character')

# @app.route('/user/<int:user_id>/characters')

# @app.route('/user/<int:user_id>/characters/<int:character_id>')

