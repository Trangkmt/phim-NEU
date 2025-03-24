from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép frontend truy cập API

API_KEY = "your_api_key_here"  # Thay bằng API Key từ TMDb
BASE_URL = "https://api.themoviedb.org/3"

@app.route('/api/movies', methods=['GET'])
def get_movies():
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=vi-VN&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        return jsonify(response.json()["results"])  # Trả về danh sách phim
    else:
        return jsonify({"error": "Không thể lấy dữ liệu"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Chạy trên localhost:5000