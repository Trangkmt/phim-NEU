from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, User, sample_movies, get_movie_by_id, search_movies

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key in production

# Setup SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movie_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables before the first request is processed
# This replaces the deprecated before_first_request decorator
with app.app_context():
    db.create_all()
    print("Database tables created successfully")

@app.route('/')
def home():
    try:
        return render_template('homepage.html', movies=sample_movies)
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        return render_template('homepage.html', error="Unable to load data")

@app.route('/film/<int:movie_id>')
def film_details(movie_id):
    movie = get_movie_by_id(movie_id)
    if movie:
        return render_template('film_details.html', movie=movie)
    return render_template('film_details.html')

@app.route('/film/play/<int:movie_id>')
def play_film(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template('play_film.html', movie=movie)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        results = search_movies(query)
    else:
        results = []
    return render_template('search_result.html', query=query, results=results)

@app.route('/genre/<genre_name>')
def genre(genre_name=None):
    # Filter movies by genre in a real app
    return render_template('film_genres.html', genre=genre_name)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template('film_details.html', movie=movie)

@app.route('/watch/<int:movie_id>')
def watch_movie(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template('play_film.html', movie=movie)

# Authentication routes
@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        
        # Check if passwords match
        if password != confirm_password:
            return jsonify({"success": False, "message": "Passwords don't match"}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"success": False, "message": "Username already exists"}), 400
        
        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        
        return jsonify({"success": True, "username": new_user.username, "message": "Registration successful"}), 200
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred during registration"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({"success": True, "username": user.username, "message": "Login successful"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid username or password"}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred during login"}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/user-info')
def user_info():
    if 'username' in session:
        return jsonify({
            'username': session['username'],
            'avatar': '/static/images/avatar_user.png',
            'isLoggedIn': True
        })
    return jsonify({
        'isLoggedIn': False
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Visit http://127.0.0.1:5000/ in your browser")
    app.run(debug=True)