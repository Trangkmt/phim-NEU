# app.py
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Table
import datetime

# Use updated import for SQLAlchemy 2.0 compatibility
Base = declarative_base()

# User-Role many-to-many relationship
user_roles = Table('user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    full_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    roles = relationship("Role", secondary=user_roles, backref="users")
    sessions = relationship("UserSession", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"

class Role(Base):
    """Role model for user permissions"""
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    
    def __repr__(self):
        return f"<Role {self.name}>"

class UserSession(Base):
    """Store user sessions for tracking login status"""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_id = Column(String(64), unique=True, nullable=False)
    ip_address = Column(String(39))  # IPv6 compatible
    user_agent = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession {self.session_id}>"

def initialize_database(db_config):
    """Initialize database connection and create tables if they don't exist"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import logging
    
    try:
        # Create connection string based on config
        if db_config.get('trusted', 'yes').lower() == 'yes':
            connection_string = (
                f"mssql+pyodbc://{db_config.get('server', 'localhost')}/"
                f"{db_config.get('database', 'QLTAIKHOAN')}?"
                f"driver={db_config.get('driver', '{ODBC Driver 17 for SQL Server}')}"
                "&trusted_connection=yes"
            )
        else:
            connection_string = (
                f"mssql+pyodbc://{db_config.get('username', '')}:{db_config.get('password', '')}"
                f"@{db_config.get('server', 'localhost')}/"
                f"{db_config.get('database', 'QLTAIKHOAN')}?"
                f"driver={db_config.get('driver', '{ODBC Driver 17 for SQL Server}')}"
            )
        
        # Create engine and session factory
        engine = create_engine(
            connection_string,
            echo=False,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_pre_ping=True
        )
        
        # Create tables
        Base.metadata.create_all(engine)
        
        # Create session factory
        Session = sessionmaker(bind=engine)
        
        logging.info("Database initialized successfully")
        return Session
        
    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}", exc_info=True)
        raise