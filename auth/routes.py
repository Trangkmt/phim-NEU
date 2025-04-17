from flask import Blueprint, jsonify, session, send_from_directory, request
from auth.services import register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() if request.is_json else request.form
    return register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() if request.is_json else request.form
    return login_user(data)

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