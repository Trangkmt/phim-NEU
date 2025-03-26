from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pyodbc
import bcrypt
import requests  # 🔥 Thêm thư viện để gọi API TMDb

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Bảo mật session

# 🔗 Cấu hình kết nối SQL Server
driver = "{ODBC Driver 17 for SQL Server}"
server = r'KiWi-HERE\KMT'
database = "QLTAIKHOAN"
login = "kiwi"
password = "1234"
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def connect_db():
    """Kết nối SQL Server"""
    return pyodbc.connect(conn_str)

# ================== 🚀 ROUTES ==================

@app.route('/')
def home():
    return render_template('base.html')  # Trang chính

# 🔹 Xử lý Đăng ký
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    if password != confirm_password:
        return jsonify({"success": False, "message": "Mật khẩu nhập lại không khớp!"})

    conn = connect_db()
    cursor = conn.cursor()

    # Kiểm tra user đã tồn tại chưa
    cursor.execute("SELECT COUNT(*) FROM taikhoan1 WHERE username = ?", (username,))
    if cursor.fetchone()[0] > 0:
        return jsonify({"success": False, "message": "Tài khoản đã tồn tại!"})

    # Hash mật khẩu trước khi lưu vào database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Lưu user vào database
    cursor.execute("INSERT INTO taikhoan1 (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    # 🔥 Lưu username vào session
    session['username'] = username

    return jsonify({"success": True, "message": "Đăng ký thành công!", "username": username})

# 🔹 Xử lý Đăng nhập
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = connect_db()
    cursor = conn.cursor()

    # Lấy password từ database
    cursor.execute("SELECT password FROM taikhoan1 WHERE username = ?", (username,))
    taikhoan1 = cursor.fetchone()

    if taikhoan1 and taikhoan1[0]:  # Kiểm tra nếu user tồn tại và password không bị NULL
        hashed_password = taikhoan1[0]  # Dữ liệu đã là string
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            session['username'] = username
            return jsonify({"success": True, "message": "Đăng nhập thành công!", "username": username})
    return jsonify({"success": False, "message": "Sai tên đăng nhập hoặc mật khẩu!"})

# 🔹 API lấy thông tin user
@app.route('/user-info')
def user_info():
    if 'username' in session:
        return jsonify({"username": session['username']})
    return jsonify({"username": None})

# 🔹 Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# 🔥 *THÊM ROUTE MỚI ĐỂ LẤY DỮ LIỆU TỪ TMDb*
TMDB_API_KEY = "0bf7a038cf456a5fd1c06d547eb63bd1"
TMDB_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwYmY3YTAzOGNmNDU2YTVmZDFjMDZkNTQ3ZWI2M2JkMSIsIm5iZiI6MTc0MjEzMDQzOS4yNDYsInN1YiI6IjY3ZDZjZDA3MzE2NzhjYzNmODAxNmMzNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1S9ZgzNWjwQ5BcNIn25DeuQcfLv7lsfk_6xpLRnNqjM"

@app.route('/movies')
def get_movies():
    """Lấy danh sách thay đổi phim từ TMDb API"""
    url = "https://api.themoviedb.org/3/movie/changes?page=1"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())  # Trả dữ liệu về dưới dạng JSON
    else:
        return jsonify({"success": False, "message": "Lỗi khi lấy dữ liệu từ TMDb!"})

# ================== 🔥 CHẠY ỨNG DỤNG ==================
if __name__ == '__main__':
    app.run(debug=True)
