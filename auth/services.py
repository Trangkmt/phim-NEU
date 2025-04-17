from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, request
from database.models import User, UserSession
import logging
import datetime
import secrets
import uuid

def register_user(data):
    """
    Register a new user.
    """
    from database.models import SessionLocal
    
    db = SessionLocal()
    try:
        # Extract required fields
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        # Validate inputs
        if not username or not password or not email:
            return {"status": "error", "message": "Missing required fields."}, 400
        
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            field = "Username" if existing_user.username == username else "Email"
            logging.warning(f"{field} already exists: {username if field == 'Username' else email}")
            return {"status": "error", "message": f"{field} already exists."}, 409

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username, 
            email=email,
            password_hash=hashed_password
        )

        db.add(new_user)
        db.commit()
        logging.info(f"User '{username}' has been created.")
        return {"status": "success", "message": "Registration successful."}, 201
    except Exception as e:
        db.rollback()
        logging.error(f"Error during user registration: {str(e)}", exc_info=True)
        return {"status": "error", "message": "An error occurred during registration."}, 500
    finally:
        db.close()

def login_user(data):
    """
    Authenticate user and create session.
    """
    from database.models import SessionLocal
    
    db = SessionLocal()
    try:
        # Extract credentials
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return {"status": "error", "message": "Username and password required."}, 400
            
        # Find user
        user = db.query(User).filter(User.username == username).first()
        
        if user and check_password_hash(user.password_hash, password):
            # Create session
            session_id = secrets.token_hex(32)
            session_expires = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            
            # Create session record
            user_session = UserSession(
                user_id=user.id,
                session_id=session_id,
                ip_address=str(request.remote_addr) if request else None,
                user_agent=request.headers.get('User-Agent', 'Unknown') if request else None,
                expires_at=session_expires
            )
            
            db.add(user_session)
            
            # Update user's last login
            user.last_login = datetime.datetime.utcnow()
            db.commit()
            
            # Set session in Flask
            session['user_id'] = user.id
            session['username'] = user.username
            session['session_id'] = session_id
            
            logging.info(f"User '{username}' has logged in.")
            return {"status": "success", "message": "Login successful."}, 200
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            return {"status": "error", "message": "Invalid username or password."}, 401
    except Exception as e:
        db.rollback()
        logging.error(f"Error during login: {str(e)}", exc_info=True)
        return {"status": "error", "message": "An error occurred during login."}, 500
    finally:
        db.close()