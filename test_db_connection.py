import pyodbc
import urllib.parse
from sqlalchemy import create_engine
import sys

# Use the same configuration as in main.py
DB_CONFIG = {
    'server': 'localhost\\SQLEXPRESS',  # Change to your SQL Server instance
    'database': 'your_database_name',   # Change to your database name
    'driver': 'ODBC Driver 17 for SQL Server',
    # For Windows Authentication (remove username/password)
    # For SQL Authentication (uncomment and fill):
    # 'username': 'your_username',
    # 'password': 'your_password',
}

def test_pyodbc_connection():
    """Test direct connection via pyodbc"""
    try:
        # Format the connection string for direct pyodbc connection
        conn_str = f"DRIVER={{{DB_CONFIG['driver']}}};"
        conn_str += f"SERVER={DB_CONFIG['server']};"
        conn_str += f"DATABASE={DB_CONFIG['database']};"
        
        if DB_CONFIG.get('username') and DB_CONFIG.get('password'):
            conn_str += f"UID={DB_CONFIG['username']};"
            conn_str += f"PWD={DB_CONFIG['password']};"
        else:
            conn_str += "Trusted_Connection=yes;"
        
        print(f"Testing direct ODBC connection with:\n{conn_str}")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        print(f"PYODBC Connection successful!\nSQL Server version: {row[0]}")
        conn.close()
        return True
    except Exception as e:
        print(f"PYODBC Connection failed: {str(e)}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        server = DB_CONFIG.get('server')
        database = DB_CONFIG.get('database')
        username = DB_CONFIG.get('username', '')
        password = DB_CONFIG.get('password', '')
        driver = DB_CONFIG.get('driver')
        
        # URL encode the driver name
        driver_param = urllib.parse.quote_plus(driver)
        
        # Build the connection string
        if username and password:
            # SQL Server authentication
            connection_string = f"mssql+pyodbc://{username}:{urllib.parse.quote_plus(password)}@{server}/{database}?driver={driver_param}"
        else:
            # Windows authentication
            connection_string = f"mssql+pyodbc://{server}/{database}?driver={driver_param}&trusted_connection=yes"
        
        print(f"Testing SQLAlchemy connection with:\n{connection_string}")
        
        # Create engine and test connection
        engine = create_engine(connection_string)
        connection = engine.connect()
        result = connection.execute("SELECT @@VERSION").fetchone()
        print(f"SQLAlchemy connection successful!\nSQL Server version: {result[0]}")
        connection.close()
        return True
    except Exception as e:
        print(f"SQLAlchemy Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing database connections...")
    print("\n=== PYODBC Direct Test ===")
    pyodbc_success = test_pyodbc_connection()
    
    print("\n=== SQLAlchemy Test ===")
    sqlalchemy_success = test_sqlalchemy_connection()
    
    if not (pyodbc_success and sqlalchemy_success):
        print("\n=== Troubleshooting Tips ===")
        print("1. Make sure SQL Server is running")
        print("2. Verify ODBC driver is installed:")
        print("   - Open 'ODBC Data Sources (64-bit)' from Windows search")
        print("   - Check the 'Drivers' tab for 'ODBC Driver 17 for SQL Server'")
        print("3. If driver not found, download from:")
        print("   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
        print("4. Check your server name and instance (localhost\\SQLEXPRESS)")
        print("5. Make sure the database exists")
        print("6. Verify your authentication method is correct")
        sys.exit(1)
    else:
        print("\nAll connection tests passed! Your configuration is correct.")
