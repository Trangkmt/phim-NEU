from functools import wraps
from flask import jsonify, redirect, url_for, request, session

def login_required(f):
    """Decorator xác thực yêu cầu đăng nhập"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            if request.accept_mimetypes.accept_json:
                return jsonify({"success": False, "message": "Vui lòng đăng nhập!"}), 401
            return redirect(url_for('home', next=request.url))
        return f(*args, **kwargs)
    return decorated_function