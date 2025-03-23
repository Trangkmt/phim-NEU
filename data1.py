import pyodbc

# 🔗 Cấu hình kết nối SQL Server
driver = "{ODBC Driver 17 for SQL Server}"
server = r'KiWi-HERE\KMT'  # 🔥 Cập nhật thông tin server của bạn
database = "QLTAIKHOAN"
login = "kiwi"
password = "1234"
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def connect_db():
    """Kết nối SQL Server"""
    return pyodbc.connect(conn_str)