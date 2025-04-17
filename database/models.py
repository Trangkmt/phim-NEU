from sqlalchemy import Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use `MetaData` with schema if needed
metadata = MetaData(schema="dbo")
Base = declarative_base(metadata=metadata)

# Global session factory (better to use dependency injection in production)
SessionLocal: Optional[sessionmaker] = None

class User(Base):
    """User model representing the 'taikhoan' table."""
    __tablename__ = "taikhoan"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}')>"

def initialize_database(db_config: Dict[str, Any]) -> None:
    """Initialize the database connection and create tables if they don't exist.
    
    Args:
        db_config: Dictionary containing database configuration
            - driver: ODBC driver name
            - server: Server address
            - database: Database name
            - trusted: Boolean for trusted connection
            - username: Database username (if not trusted)
            - password: Database password (if not trusted)
    """
    global SessionLocal
    
    try:
        # Validate required configuration
        required_keys = {'driver', 'server', 'database', 'trusted'}
        if not required_keys.issubset(db_config.keys()):
            missing = required_keys - db_config.keys()
            raise ValueError(f"Missing required database config keys: {missing}")

        # Generate the connection URL
        if db_config['trusted']:
            db_url = (
                f"mssql+pyodbc://{db_config['server']}/{db_config['database']}"
                f"?driver={db_config['driver']}"
                "&trusted_connection=yes"
            )
        else:
            if not all(k in db_config for k in ['username', 'password']):
                raise ValueError("Username and password required for non-trusted connection")
                
            db_url = (
                f"mssql+pyodbc://{db_config['username']}:{db_config['password']}"
                f"@{db_config['server']}/{db_config['database']}"
                f"?driver={db_config['driver']}"
            )

        # Create the engine with connection pooling and timeout settings
        engine = create_engine(
            db_url,
            echo=False,
            future=True,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_pre_ping=True  # Test connections before use
        )
        
        # Configure session factory
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False  # Better for web applications
        )

        # Create tables if they don't exist (consider migrations for production)
        Base.metadata.create_all(bind=engine)

        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.critical(f"Database initialization failed: {str(e)}", exc_info=True)
        raise