import pyodbc
import logging
import time
from typing import Dict, Any

def get_db_connection(config: Dict[str, Any], max_retries: int = 3, retry_delay: int = 2) -> pyodbc.Connection:
    """Kết nối SQL Server với retry logic"""
    for attempt in range(max_retries):
        try:
            if config['trusted'] == 'yes':
                conn_str = (
                    f"DRIVER={config['driver']};"
                    f"SERVER={config['server']};"
                    f"DATABASE={config['database']};"
                    "Trusted_Connection=yes;"
                    "Connection Timeout=30;"
                )
            else:
                conn_str = (
                    f"DRIVER={config['driver']};"
                    f"SERVER={config['server']};"
                    f"DATABASE={config['database']};"
                    f"UID={config['username']};"
                    f"PWD={config['password']};"
                    "Connection Timeout=30;"
                )
            
            logging.debug(f"Attempt {attempt + 1}: Đang kết nối database")
            conn = pyodbc.connect(conn_str)
            logging.info("Kết nối database thành công!")
            return conn
            
        except pyodbc.Error as e:
            logging.error(f"Lỗi kết nối database (attempt {attempt + 1}): {str(e)}")
            if attempt == max_retries - 1:
                raise
            time.sleep(retry_delay)
    
    raise pyodbc.Error("Không thể kết nối database sau nhiều lần thử")