from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User, SessionLocal
import logging

def register_user(username: str, password: str):
    """
    Đăng ký người dùng mới.
    """
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            logging.warning("Tên người dùng đã tồn tại.")
            return {"status": "error", "message": "Tên người dùng đã tồn tại."}

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)

        db.add(new_user)
        db.commit()
        logging.info(f"Người dùng '{username}' đã được tạo.")
        return {"status": "success", "message": "Đăng ký thành công."}
    except Exception as e:
        logging.error(f"Lỗi khi đăng ký người dùng: {str(e)}", exc_info=True)
        return {"status": "error", "message": "Đã xảy ra lỗi khi đăng ký."}
    finally:
        db.close()

def login_user(username: str, password: str):
    """
    Đăng nhập người dùng.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and check_password_hash(user.password_hash, password):
            logging.info(f"Người dùng '{username}' đã đăng nhập.")
            return {"status": "success", "message": "Đăng nhập thành công."}
        else:
            logging.warning("Thông tin đăng nhập không hợp lệ.")
            return {"status": "error", "message": "Tên đăng nhập hoặc mật khẩu không đúng."}
    except Exception as e:
        logging.error(f"Lỗi khi đăng nhập: {str(e)}", exc_info=True)
        return {"status": "error", "message": "Đã xảy ra lỗi khi đăng nhập."}
    finally:
        db.close()
