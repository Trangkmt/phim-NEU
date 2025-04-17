import pyodbc
import urllib.parse
import subprocess
import sys
import os
import platform

def check_system():
    """Check system information"""
    print("=== System Information ===")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if running with admin privileges
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    print(f"Running as admin: {is_admin}")

def check_sql_server():
    """Check SQL Server status"""
    print("\n=== SQL Server Status ===")
    try:
        # Check if SQL Server service is running on Windows
        if platform.system() == 'Windows':
            result = subprocess.run(
                ['sc', 'query', 'MSSQLSERVER'], 
                capture_output=True, 
                text=True
            )
            if 'RUNNING' in result.stdout:
                print("SQL Server service is running")
            else:
                print("SQL Server service might not be running. Full output:")
                print(result.stdout)
        else:
            print("Not on Windows, skipping service check")
    except Exception as e:
        print(f"Error checking SQL Server status: {e}")

def check_odbc_drivers():
    """Check available ODBC drivers"""
    print("\n=== ODBC Drivers ===")
    try:
        print("Available ODBC drivers:")
        drivers = pyodbc.drivers()
        if not drivers:
            print("No ODBC drivers found!")
        else:
            for i, driver in enumerate(drivers, 1):
                print(f"{i}. {driver}")
    except Exception as e:
        print(f"Error checking ODBC drivers: {e}")

def test_connections():
    """Test various connection strings"""
    print("\n=== Connection Tests ===")
    
    # List of connection configurations to try
    configs = [
        {
            'name': 'Basic SQL Server',
            'conn_str': "DRIVER={SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;"
        },
        {
            'name': 'SQL Server with instance',
            'conn_str': "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes;"
        }
    ]
    
    # Add tests for each ODBC driver found
    for driver in pyodbc.drivers():
        if 'sql' in driver.lower():
            configs.append({
                'name': f'Using {driver}',
                'conn_str': f"DRIVER={{{driver}}};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;"
            })
            configs.append({
                'name': f'Using {driver} with instance',
                'conn_str': f"DRIVER={{{driver}}};SERVER=localhost\\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes;"
            })
    
    # Try each connection
    success_count = 0
    for config in configs:
        try:
            print(f"\nTrying {config['name']}...")
            print(f"Connection string: {config['conn_str']}")
            conn = pyodbc.connect(config['conn_str'], timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"✓ SUCCESS! SQL Server version: {version[:50]}...")
            conn.close()
            success_count += 1
            
            # If successful, show SQLAlchemy connection too
            quoted = urllib.parse.quote_plus(config['conn_str'])
            sqlalchemy_str = f"mssql+pyodbc:///?odbc_connect={quoted}"
            print(f"SQLAlchemy connection string to use: {sqlalchemy_str}")
            
        except Exception as e:
            print(f"✗ Failed: {str(e)}")
    
    print(f"\n{success_count} of {len(configs)} connection tests succeeded.")
    
    if success_count > 0:
        print("\nCONNECTION SUCCESS! Use one of the successful connection strings in your application.")
    else:
        print("\nAll connection tests failed. Please check your SQL Server installation and configuration.")

if __name__ == "__main__":
    print("SQL Server Connection Diagnostic Tool")
    print("====================================")
    
    check_system()
    check_sql_server()
    check_odbc_drivers()
    test_connections()
    
    print("\n=== Troubleshooting Tips ===")
    print("1. Make sure SQL Server is installed and running")
    print("2. Check if you have ODBC drivers installed")
    print("3. Try using SQL Server Configuration Manager to verify instances")
    print("4. Make sure Windows Authentication is enabled if not using SQL auth")
    print("5. Check if your firewall is blocking connections")
    print("6. Try connecting with SQL Server Management Studio to verify server availability")
