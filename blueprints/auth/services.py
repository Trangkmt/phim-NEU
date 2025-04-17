from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

class AuthError(Exception):
    """Custom exception for authentication errors"""
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        raise AuthError("Mật khẩu phải có ít nhất 6 ký tự", 400)
    
    # Additional password strength checks could be added here
    return True

def register_user(username, password, confirm_password):
    """Register a new user with validation"""
    try:
        # Check if fields are empty
        if not username or not password:
            raise AuthError("Vui lòng điền đầy đủ thông tin", 400)
            
        # Check if passwords match
        if password != confirm_password:
            raise AuthError("Mật khẩu nhập lại không khớp", 400)
        
        # Validate password strength
        validate_password(password)
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise AuthError("Tên đăng nhập đã được sử dụng", 409)
        
        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Set session data
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        
        return {"success": True, "username": new_user.username, "message": "Đăng ký thành công!"}
    
    except AuthError as e:
        return {"success": False, "message": e.message}, e.code
        
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return {"success": False, "message": "Có lỗi xảy ra. Vui lòng thử lại sau."}, 500

def login_user(username, password):
    """Authenticate user with detailed error messages"""
    try:
        # Check if fields are empty
        if not username:
            raise AuthError("Vui lòng nhập tên đăng nhập", 400)
            
        if not password:
            raise AuthError("Vui lòng nhập mật khẩu", 400)
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user:
            raise AuthError("Tên đăng nhập không tồn tại", 401)
            
        if not user.check_password(password):
            raise AuthError("Mật khẩu không đúng", 401)
        
        # Set session data
        session['user_id'] = user.id
        session['username'] = user.username
        
        # Update last login time
        user.last_login = db.func.now()
        db.session.commit()
        
        return {"success": True, "username": user.username, "message": "Đăng nhập thành công!"}
        
    except AuthError as e:
        return {"success": False, "message": e.message}, e.code
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return {"success": False, "message": "Có lỗi xảy ra. Vui lòng thử lại sau."}, 500

def logout_user():
    """Log out user and clear session data"""
    try:
        session.clear()
        return {"success": True, "message": "Đăng xuất thành công!"}
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return {"success": False, "message": "Có lỗi xảy ra khi đăng xuất."}, 500
