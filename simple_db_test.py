import pyodbc

def test_simple_connection():
    """Test the most basic ODBC connection to SQL Server"""
    
    # List all available ODBC drivers to help identify correct driver name
    print("Available ODBC drivers:")
    for driver in pyodbc.drivers():
        print(f"  - {driver}")
    
    # Try connection with the simplest possible connection string
    try:
        # Use Windows Authentication - simplest case
        conn_str = (
            "Driver={SQL Server};"   # Try with the basic SQL Server driver first
            "Server=localhost;"      # Try without instance name first
            "Database=master;"       # Connect to master database which always exists
            "Trusted_Connection=yes;"
        )
        
        print(f"\nTrying simple connection with: {conn_str}")
        conn = pyodbc.connect(conn_str)
        print("Simple connection succeeded!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@SERVERNAME, @@VERSION")
        row = cursor.fetchone()
        print(f"Server name: {row[0]}")
        print(f"SQL Server version: {row[1]}")
        conn.close()
    except Exception as e:
        print(f"Simple connection failed: {str(e)}")

if __name__ == "__main__":
    test_simple_connection()
