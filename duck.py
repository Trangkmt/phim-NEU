from flask import Flask, render_template , jsonify
import requests
app=Flask(__name__)
app.secret_key='your_secret_key'
# ----------------- 🚀 ROUTES HIỂN THỊ TRANG -----------------

@app.route('/')
def home():
    url = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwYmY3YTAzOGNmNDU2YTVmZDFjMDZkNTQ3ZWI2M2JkMSIsIm5iZiI6MTc0MjEzMDQzOS4yNDYsInN1YiI6IjY3ZDZjZDA3MzE2NzhjYzNmODAxNmMzNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1S9ZgzNWjwQ5BcNIn25DeuQcfLv7lsfk_6xpLRnNqjM"
    }

    response = requests.get(url, headers=headers)
    if response.status_code ==200:
        response = response.json()
        results=response['results']
        for result in results:
            result['poster_path']=f"https://image.tmdb.org/t/p/w500/{result['poster_path']}"
        return render_template('homepage2.html',movies =results)
    else:
        return jsonify({"eror": "saime roi"}),response.status_code



if __name__ == '__main__':
    app.run(debug=True, port=5005)
