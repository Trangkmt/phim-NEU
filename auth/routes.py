from flask import Blueprint, jsonify, session, request, redirect, url_for
from auth.services import register_user, login_user
from auth.decorators import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() if request.is_json else request.form
    response, status_code = register_user(data)
    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() if request.is_json else request.form
    response, status_code = login_user(data)
    return jsonify(response), status_code

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear session
    session.clear()
    if request.method == 'POST' and request.is_json:
        return jsonify({"status": "success", "message": "Logged out successfully"})
    return redirect(url_for('home'))

@auth_bp.route('/user-info')
def user_info():
    if 'username' in session:
        return jsonify({
            'username': session['username'],
            'avatar': '/static/images/avatar_user.png',
            'isLoggedIn': True
        })
    return jsonify({
        'username': 'guest',
        'avatar': '/static/images/avatar_user.png',
        'isLoggedIn': False
    })