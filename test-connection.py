import pyodbc

try:
    conn = pyodbc.connect(
        Driver='ODBC Driver 17 for SQL Server',
        Server='KiWi-HERE\\KMT',
        Database='QLTAIKHOAN',
        Trusted_Connection='yes'
    )
    print("Kết nối thành công!")
    conn.close()
except Exception as e:
    print("Lỗi kết nối:", str(e))