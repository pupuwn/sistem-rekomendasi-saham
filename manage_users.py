"""
Setup Multi-User dengan Role
Script untuk menambahkan user baru dengan role admin atau user
"""

import bcrypt
from db_connect import Database
from dotenv import load_dotenv

load_dotenv()

def hash_password(password):
    """Generate bcrypt hash untuk password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def add_user(username, password, role='user'):
    """Tambah user baru ke database"""
    db = Database()
    
    # Check apakah username sudah ada
    check_query = "SELECT id FROM users WHERE username = %s"
    existing = db.fetch_one(check_query, (username,))
    
    if existing:
        print(f"❌ Username '{username}' sudah terdaftar!")
        db.disconnect()
        return False
    
    # Hash password
    hashed_pw = hash_password(password)
    
    # Insert user baru
    insert_query = """
    INSERT INTO users (username, password, role) 
    VALUES (%s, %s, %s)
    """
    
    result = db.execute_query(insert_query, (username, hashed_pw, role))
    db.disconnect()
    
    if result:
        print(f"✅ User '{username}' berhasil ditambahkan dengan role '{role}'")
        return True
    else:
        print(f"❌ Gagal menambahkan user '{username}'")
        return False

def list_users():
    """Tampilkan semua user yang terdaftar"""
    db = Database()
    
    query = "SELECT id, username, role, created_at FROM users ORDER BY role DESC, id"
    users = db.fetch_all(query)
    db.disconnect()
    
    if users:
        print("\n📋 DAFTAR USER:")
        print("-" * 70)
        print(f"{'ID':<5} {'Username':<20} {'Role':<10} {'Created At':<25}")
        print("-" * 70)
        
        for user in users:
            created = user['created_at'].strftime('%Y-%m-%d %H:%M:%S') if user['created_at'] else 'N/A'
            role_icon = "👑" if user['role'] == 'admin' else "👤"
            print(f"{user['id']:<5} {user['username']:<20} {role_icon} {user['role']:<8} {created:<25}")
        
        print("-" * 70)
    else:
        print("⚠️ Tidak ada user yang terdaftar")

def update_user_role(username, new_role):
    """Update role user"""
    if new_role not in ['admin', 'user']:
        print("❌ Role harus 'admin' atau 'user'")
        return False
    
    db = Database()
    
    update_query = "UPDATE users SET role = %s WHERE username = %s"
    result = db.execute_query(update_query, (new_role, username))
    db.disconnect()
    
    if result:
        print(f"✅ Role user '{username}' berhasil diubah menjadi '{new_role}'")
        return True
    else:
        print(f"❌ Gagal mengubah role user '{username}'")
        return False

def delete_user(username):
    """Hapus user dari database"""
    db = Database()
    
    # Check apakah user ada
    check_query = "SELECT id FROM users WHERE username = %s"
    existing = db.fetch_one(check_query, (username,))
    
    if not existing:
        print(f"❌ Username '{username}' tidak ditemukan!")
        db.disconnect()
        return False
    
    # Delete user
    delete_query = "DELETE FROM users WHERE username = %s"
    result = db.execute_query(delete_query, (username,))
    db.disconnect()
    
    if result:
        print(f"✅ User '{username}' berhasil dihapus")
        return True
    else:
        print(f"❌ Gagal menghapus user '{username}'")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔐 MANAJEMEN MULTI-USER - SISTEM FUZZY TSUKAMOTO")
    print("="*70)
    
    while True:
        print("\n📋 MENU:")
        print("1. Lihat semua user")
        print("2. Tambah user baru")
        print("3. Ubah role user")
        print("4. Hapus user")
        print("5. Keluar")
        
        choice = input("\n➤ Pilih menu (1-5): ").strip()
        
        if choice == '1':
            list_users()
        
        elif choice == '2':
            print("\n➕ TAMBAH USER BARU")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            role = input("Role (admin/user) [default: user]: ").strip().lower() or 'user'
            
            if role not in ['admin', 'user']:
                print("❌ Role harus 'admin' atau 'user'")
                continue
            
            if username and password:
                add_user(username, password, role)
            else:
                print("❌ Username dan password tidak boleh kosong!")
        
        elif choice == '3':
            print("\n🔄 UBAH ROLE USER")
            username = input("Username: ").strip()
            new_role = input("Role baru (admin/user): ").strip().lower()
            
            if username and new_role:
                update_user_role(username, new_role)
            else:
                print("❌ Input tidak valid!")
        
        elif choice == '4':
            print("\n🗑️ HAPUS USER")
            username = input("Username yang akan dihapus: ").strip()
            confirm = input(f"Yakin ingin menghapus user '{username}'? (y/n): ").strip().lower()
            
            if confirm == 'y':
                delete_user(username)
            else:
                print("❌ Penghapusan dibatalkan")
        
        elif choice == '5':
            print("\n👋 Terima kasih!")
            break
        
        else:
            print("❌ Pilihan tidak valid!")
