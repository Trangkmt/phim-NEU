from flask import request, jsonify, redirect, url_for, session
from . import auth_bp
from .services import register_user, login_user, logout_user

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    
    result = register_user(username, password, confirm_password)
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    
    return jsonify(result), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    result = login_user(username, password)
    
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    
    return jsonify(result), 200

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@auth_bp.route('/user-info')
def user_info():
    if 'username' in session:
        return jsonify({
            'username': session['username'],
            'avatar': '/static/images/avatar_user.png',
            'isLoggedIn': True
        })
    return jsonify({
        'isLoggedIn': False
    })
