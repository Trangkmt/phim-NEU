import os
from datetime import timedelta
from typing import Dict, Any

class Config:
    """Application configuration class with environment variables and defaults."""

    DEFAULT_CONFIG: Dict[str, Any] = {
        'SECRET_KEY': os.urandom(24).hex(),
        'SESSION_LIFETIME_DAYS': 1,
        'DB_TYPE': 'mssql',  # 'mssql' or 'mysql'
        'DB_DRIVER': '{ODBC Driver 17 for SQL Server}',
        'DB_SERVER': 'localhost',
        'DB_NAME': 'QLTAIKHOAN',
        'DB_TRUSTED': 'yes',
        'DB_USER': '',
        'DB_PASS': '',
        'DB_HOST': 'localhost',  # For MySQL
        'DB_PORT': '3306',       # For MySQL
        'LOG_FILE': 'app.log',
        'LOG_MAX_BYTES': 10000,
        'LOG_BACKUP_COUNT': 3,
        'DEFAULT_PORT': 5000,
        'DEBUG': False
    }

    def __init__(self):
        """Initialize configuration from environment variables with defaults."""
        # Security settings
        self.secret_key: str = os.environ.get('SECRET_KEY', self.DEFAULT_CONFIG['SECRET_KEY'])
        self.session_lifetime: timedelta = timedelta(
            days=int(os.environ.get('SESSION_LIFETIME_DAYS', self.DEFAULT_CONFIG['SESSION_LIFETIME_DAYS']))
        )

        # Database configuration
        db_type = os.environ.get('DB_TYPE', self.DEFAULT_CONFIG['DB_TYPE']).lower()
        
        self.db_config: Dict[str, Any] = {
            'type': db_type,
            # MSSQL specific
            'driver': os.environ.get('DB_DRIVER', self.DEFAULT_CONFIG['DB_DRIVER']),
            'server': os.environ.get('DB_SERVER', self.DEFAULT_CONFIG['DB_SERVER']),
            'database': os.environ.get('DB_NAME', self.DEFAULT_CONFIG['DB_NAME']),
            'trusted': os.environ.get('DB_TRUSTED', self.DEFAULT_CONFIG['DB_TRUSTED']),
            'username': os.environ.get('DB_USER', self.DEFAULT_CONFIG['DB_USER']),
            'password': os.environ.get('DB_PASS', self.DEFAULT_CONFIG['DB_PASS']),
            # MySQL specific
            'host': os.environ.get('DB_HOST', self.DEFAULT_CONFIG['DB_HOST']),
            'port': os.environ.get('DB_PORT', self.DEFAULT_CONFIG['DB_PORT']),
            'user': os.environ.get('DB_USER', self.DEFAULT_CONFIG['DB_USER']),
            'password': os.environ.get('DB_PASS', self.DEFAULT_CONFIG['DB_PASS'])
        }

        # Logging configuration
        self.log_config: Dict[str, Any] = {
            'file': os.environ.get('LOG_FILE', self.DEFAULT_CONFIG['LOG_FILE']),
            'max_bytes': int(os.environ.get('LOG_MAX_BYTES', self.DEFAULT_CONFIG['LOG_MAX_BYTES'])),
            'backup_count': int(os.environ.get('LOG_BACKUP_COUNT', self.DEFAULT_CONFIG['LOG_BACKUP_COUNT']))
        }

        # Server configuration
        self.port: int = int(os.environ.get('PORT', self.DEFAULT_CONFIG['DEFAULT_PORT']))
        self.debug: bool = os.environ.get('DEBUG', str(self.DEFAULT_CONFIG['DEBUG'])).lower() == 'true'

    @property
    def db_connection_string(self) -> str:
        """Generate database connection string based on type."""
        if self.db_config['type'] == 'mysql':
            return (
                f"mysql+pymysql://{self.db_config['user']}:{self.db_config['password']}@"
                f"{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            )
        else:  # Default to MSSQL
            if self.db_config['trusted'].lower() == 'yes':
                return (
                    f"mssql+pyodbc:///"
                    f"?driver={self.db_config['driver']}"
                    f"&server={self.db_config['server']}"
                    f"&database={self.db_config['database']}"
                    "&trusted_connection=yes"
                )
            return (
                f"mssql+pyodbc://{self.db_config['username']}:{self.db_config['password']}@"
                f"?driver={self.db_config['driver']}"
                f"&server={self.db_config['server']}"
                f"&database={self.db_config['database']}"
            )