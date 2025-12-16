import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    """Class untuk mengelola koneksi database MySQL"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'fuzzy_tsukamoto')
        self.port = os.getenv('DB_PORT', '3306')
        self.connection = None
    
    def connect(self):
        """Membuat koneksi ke database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def disconnect(self):
        """Menutup koneksi database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Eksekusi query INSERT, UPDATE, DELETE"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def fetch_all(self, query, params=None):
        """Mengambil semua data dari query SELECT"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            cursor.close()
    
    def fetch_one(self, query, params=None):
        """Mengambil satu baris data dari query SELECT"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            cursor.close()

# Fungsi helper untuk kemudahan penggunaan
def get_db_connection():
    """Mendapatkan instance koneksi database"""
    db = DatabaseConnection()
    conn = db.connect()
    if conn:
        return db
    return None

def test_connection():
    """Test koneksi database"""
    db = get_db_connection()
    if db:
        print("✓ Database connection successful!")
        db.disconnect()
        return True
    else:
        print("✗ Database connection failed!")
        return False

if __name__ == "__main__":
    # Test koneksi saat file dijalankan langsung
    test_connection()
