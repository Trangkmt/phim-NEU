from flask import Flask
import os

# Import blueprints
from blueprints.auth import auth_bp
from blueprints.movies import movies_bp
from blueprints.main import main_bp

# Import database
from models import db

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.secret_key = 'your_secret_key_here'  # Replace with a real secret key in production
    
    # Setup SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movie_app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(movies_bp)
    app.register_blueprint(main_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting Flask server...")
    print("Visit http://127.0.0.1:5000/ in your browser")
    app.run(debug=True)