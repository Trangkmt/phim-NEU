from flask import render_template, redirect, url_for, request
from models import get_movie_by_id, sample_movies
from . import movies_bp
from .services import get_api_movies

@movies_bp.route('/film/<int:movie_id>')
def film_details(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template('film_details.html', movie=movie)

@movies_bp.route('/film/play/<int:movie_id>')
def play_film(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template('play_film.html', movie=movie)

@movies_bp.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template('film_details.html', movie=movie)

@movies_bp.route('/movie/new/<int:movie_id>')
def new_movie_details(movie_id):
    # Show the movie details with the original URL format
    movie = get_movie_by_id(movie_id)
    return render_template('film_details.html', movie=movie)

@movies_bp.route('/movie/collection/<int:movie_id>')
def collection_movie_details(movie_id):
    # Show the movie details with the original URL format
    movie = get_movie_by_id(movie_id)
    return render_template('film_details.html', movie=movie)

@movies_bp.route('/watch/<int:movie_id>')
def watch_movie(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template('play_film.html', movie=movie)
