"""
Fix User Password - Generate dan update password hash yang benar
"""

import bcrypt
from db_connect import DatabaseConnection
from dotenv import load_dotenv

load_dotenv()

def fix_user_password():
    """Generate hash baru untuk user dan update database"""
    
    # Generate hash untuk user123
    password = "user123"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_str = hashed.decode('utf-8')
    
    print("=" * 70)
    print("🔧 FIX USER PASSWORD")
    print("=" * 70)
    print(f"\n📝 Password: {password}")
    print(f"🔐 Hash: {hashed_str}\n")
    
    # Connect ke database
    db = DatabaseConnection()
    db.connect()
    
    # Update atau insert user
    query = """
    INSERT INTO users (username, password, role) 
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        password = VALUES(password),
        role = VALUES(role)
    """
    
    result = db.execute_query(query, ('user', hashed_str, 'user'))
    
    if result:
        print("✅ Password untuk user 'user' berhasil diupdate!")
    else:
        print("❌ Gagal update password!")
        db.disconnect()
        return
    
    # Test login
    print("\n" + "=" * 70)
    print("🧪 TEST LOGIN")
    print("=" * 70)
    
    check_query = "SELECT username, password, role FROM users WHERE username = %s"
    user_data = db.fetch_one(check_query, ('user',))
    
    if user_data:
        print(f"\n✓ Username: {user_data['username']}")
        print(f"✓ Role: {user_data['role']}")
        print(f"✓ Hash di DB: {user_data['password'][:50]}...")
        
        # Test password
        stored_hash = user_data['password'].encode('utf-8')
        is_match = bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        
        if is_match:
            print(f"\n✅ TEST LOGIN BERHASIL!")
            print(f"   Username: user")
            print(f"   Password: user123")
        else:
            print(f"\n❌ TEST LOGIN GAGAL! Hash tidak cocok.")
    else:
        print("\n❌ User tidak ditemukan di database!")
    
    # Tampilkan semua user
    print("\n" + "=" * 70)
    print("📋 DAFTAR SEMUA USER")
    print("=" * 70)
    
    all_users = db.fetch_all("SELECT id, username, role, created_at FROM users")
    
    if all_users:
        for u in all_users:
            role_icon = "👑" if u['role'] == 'admin' else "👤"
            print(f"{role_icon} ID:{u['id']} | {u['username']} | {u['role']}")
    
    db.disconnect()
    print("\n" + "=" * 70)

if __name__ == "__main__":
    fix_user_password()
