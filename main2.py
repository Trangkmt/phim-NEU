from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import bcrypt
import pyodbc  # Kết nối SQL Server

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Để quản lý session

# 🔗 Cấu hình kết nối SQL Server
driver = "{ODBC Driver 17 for SQL Server}"
server = r'KiWi-HERE\KMT'
database = "QLTAIKHOAN"
username = "kiwi"
password = "1234"
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

def connect_db():
    """Kết nối SQL Server"""
    return pyodbc.connect(conn_str)

# ----------------- 🚀 ROUTES HIỂN THỊ TRANG -----------------

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

# ----------------- 🔐 XỬ LÝ ĐĂNG NHẬP, ĐĂNG KÝ, ĐĂNG XUẤT -----------------

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    if password != confirm_password:
        return jsonify({"success": False, "message": "Mật khẩu không khớp!"})

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM taikhoan1 WHERE username = ?", (username,))
    
    if cursor.fetchone()[0] > 0:
        return jsonify({"success": False, "message": "Tài khoản đã tồn tại!"})

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("INSERT INTO taikhoan1 (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Đăng ký thành công!", "username": username})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM taikhoan1 WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        session['username'] = username  # Lưu vào session
        return jsonify({"success": True, "message": "Đăng nhập thành công!", "username": username})

    return jsonify({"success": False, "message": "Sai tên đăng nhập hoặc mật khẩu!"})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# API lấy thông tin user từ session
@app.route('/user-info', methods=['GET'])
def user_info():
    return jsonify({"username": session.get('username', None)})

# ----------------- 🔥 CHẠY ỨNG DỤNG -----------------
if __name__ == '__main__':
    app.run(debug=True)
