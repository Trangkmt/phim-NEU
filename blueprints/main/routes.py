from flask import render_template, request, redirect, url_for
from models import get_genres, search_movies
from . import main_bp
from blueprints.movies.services import get_api_movies

@main_bp.route('/')
def home():
    try:
        # Keep it simple, just render the existing template
        return render_template('homepage.html')
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        return render_template('homepage.html', error="Unable to load data")

@main_bp.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        # API integration point for search
        results = search_movies(query)
        suggested_movies = get_api_movies(endpoint='suggested', params={'query': query})
    else:
        results = []
        suggested_movies = get_api_movies(endpoint='trending')
        
    return render_template('search_result.html', query=query, results=results, suggested_movies=suggested_movies)

@main_bp.route('/genre/<genre_name>')
def genre(genre_name=None):
    # Keep this simple to ensure it works
    display_genre = genre_name.replace('-', ' ') if genre_name else ''
    
    # Filter movies by genre from API
    genre_movies = get_api_movies(endpoint='genre', params={'genre': genre_name})
    
    return render_template('film_genres.html', genre=display_genre, genre_movies=genre_movies)

# Fallback route for any other static pages
@main_bp.route('/<path:path>')
def catch_all(path):
    try:
        return render_template(f"{path}.html")
    except:
        return redirect(url_for('main.home'))
