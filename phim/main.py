from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

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