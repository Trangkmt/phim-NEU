from flask import Flask, render_template, session
from app import initialize_database, User  # Import from app.py
from auth.routes import auth_bp  # Import authentication blueprint
from utils.logging import setup_logging
from utils.file_handlers import create_static_dirs
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key in production

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

# Setup logging
setup_logging()

# Create necessary directories
create_static_dirs()

# Database configuration
DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': r'localhost\KMT',
    'database': 'QLTAIKHOAN',
    'trusted': 'yes'
}

# Initialize database and get session factory
Session = initialize_database(DB_CONFIG)

@app.route('/')
def home():
    db_session = Session()
    try:
        # Get list of users from database
        users = db_session.query(User).limit(5).all()
        return render_template('homepage.html', users=users)
    except Exception as e:
        logging.error(f"Error in home route: {str(e)}", exc_info=True)
        return render_template('homepage.html', users=[], error="Unable to load users")
    finally:
        db_session.close()

@app.route('/film')
def film_details():
    return render_template('film_details.html')

@app.route('/film/play')
def play_film():
    return render_template('play_film.html')

@app.route('/search')
def search():
    return render_template('search_result.html')

@app.route('/genre')
def genre():
    return render_template('film_genres.html')

if __name__ == '__main__':
    app.run(debug=True)