"""
Script untuk setup user admin
Jalankan script ini jika login gagal atau untuk reset password admin
"""

import bcrypt
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def setup_admin_user():
    """Setup atau reset user admin"""
    try:
        # Koneksi ke MySQL
        print("🔌 Menghubungkan ke MySQL...")
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'fuzzy_tsukamoto'),
            port=os.getenv('DB_PORT', '3306')
        )
        
        if connection.is_connected():
            print("✅ Koneksi database berhasil!")
            
            cursor = connection.cursor()
            
            # Cek apakah tabel users ada
            cursor.execute("SHOW TABLES LIKE 'users'")
            if not cursor.fetchone():
                print("\n⚠️  Tabel 'users' belum ada!")
                print("💡 Silakan jalankan database_setup.sql terlebih dahulu:")
                print("   Get-Content database_setup.sql | mysql -u root -p fuzzy_tsukamoto")
                return
            
            # Generate password hash untuk 'admin123'
            password = "admin123"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_str = hashed.decode('utf-8')
            
            print(f"\n🔐 Password hash generated: {hashed_str[:50]}...")
            
            # Cek apakah user admin sudah ada
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Update password yang sudah ada
                print("\n📝 User 'admin' sudah ada, mengupdate password...")
                update_query = "UPDATE users SET password = %s WHERE username = 'admin'"
                cursor.execute(update_query, (hashed_str,))
                connection.commit()
                print("✅ Password admin berhasil diupdate!")
            else:
                # Insert user baru
                print("\n➕ Membuat user admin baru...")
                insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(insert_query, ('admin', hashed_str))
                connection.commit()
                print("✅ User admin berhasil dibuat!")
            
            # Verifikasi
            cursor.execute("SELECT username FROM users")
            users = cursor.fetchall()
            print(f"\n📊 Total users di database: {len(users)}")
            for user in users:
                print(f"   - {user[0]}")
            
            print("\n" + "="*50)
            print("✅ SETUP SELESAI!")
            print("="*50)
            print("\n🔑 Kredensial Login:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n💡 Sekarang coba login ke aplikasi Streamlit")
            
            cursor.close()
            connection.close()
            
    except mysql.connector.Error as e:
        print(f"\n❌ Error MySQL: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Pastikan MySQL Server sudah running")
        print("   2. Cek file .env sudah benar (DB_HOST, DB_USER, DB_PASSWORD)")
        print("   3. Pastikan database 'fuzzy_tsukamoto' sudah dibuat")
        print("   4. Jalankan: Get-Content database_setup.sql | mysql -u root -p fuzzy_tsukamoto")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_login():
    """Test login credentials"""
    try:
        print("\n" + "="*50)
        print("🧪 TESTING LOGIN")
        print("="*50)
        
        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'fuzzy_tsukamoto'),
            port=os.getenv('DB_PORT', '3306')
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT password FROM users WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result:
            stored_hash = result['password'].encode('utf-8')
            test_password = "admin123".encode('utf-8')
            
            if bcrypt.checkpw(test_password, stored_hash):
                print("✅ Test login BERHASIL!")
                print("   Username 'admin' dengan password 'admin123' valid!")
            else:
                print("❌ Test login GAGAL!")
                print("   Password hash tidak cocok!")
        else:
            print("❌ User 'admin' tidak ditemukan di database!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error saat test: {e}")

if __name__ == "__main__":
    print("="*50)
    print("🚀 SETUP USER ADMIN - FUZZY TSUKAMOTO")
    print("="*50)
    
    setup_admin_user()
    test_login()
    
    print("\n" + "="*50)
    print("📝 Jika masih ada masalah:")
    print("   1. Cek file .env (DB_PASSWORD harus sesuai dengan MySQL)")
    print("   2. Restart aplikasi Streamlit")
    print("   3. Coba login lagi dengan admin/admin123")
    print("="*50)
