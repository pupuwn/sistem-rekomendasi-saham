# Multi-User & Role-Based Access Control

## 📋 Overview

Sistem sekarang mendukung **multi-user** dengan **role-based access control (RBAC)**:

### Roles:

1. **👑 Admin** - Akses penuh ke semua fitur
2. **👤 User** - Akses terbatas (hanya Data Saham & Hasil)

---

## 🔧 Setup Database

### 1. Jalankan Migration Script

```powershell
# Di PowerShell
Get-Content database_migration_roles.sql | mysql -u root -p fuzzy_tsukamoto
```

Atau login ke MySQL:

```sql
mysql -u root -p fuzzy_tsukamoto
source database_migration_roles.sql
```

### 2. Verifikasi

```sql
SELECT id, username, role, created_at FROM users;
```

Output:

```
+----+----------+-------+---------------------+
| id | username | role  | created_at          |
+----+----------+-------+---------------------+
|  1 | admin    | admin | 2024-01-01 10:00:00 |
|  2 | user     | user  | 2024-01-01 10:00:00 |
+----+----------+-------+---------------------+
```

---

## 👥 Default Users

| Username | Password | Role  | Akses                    |
| -------- | -------- | ----- | ------------------------ |
| `admin`  | admin123 | Admin | ✅ Semua fitur           |
| `user`   | user123  | User  | ⚠️ Terbatas (Saham only) |

---

## 🔐 Manajemen User

### Menggunakan Script Python

```powershell
python manage_users.py
```

Menu tersedia:

1. **Lihat semua user** - Tampilkan daftar user & role
2. **Tambah user baru** - Buat user admin/user
3. **Ubah role user** - Promote/demote user
4. **Hapus user** - Remove user dari sistem
5. **Keluar**

### Contoh Penggunaan:

#### Tambah User Baru

```
➤ Pilih menu (1-5): 2

➕ TAMBAH USER BARU
Username: investor1
Password: pass123
Role (admin/user) [default: user]: user

✅ User 'investor1' berhasil ditambahkan dengan role 'user'
```

#### Ubah Role User

```
➤ Pilih menu (1-5): 3

🔄 UBAH ROLE USER
Username: investor1
Role baru (admin/user): admin

✅ Role user 'investor1' berhasil diubah menjadi 'admin'
```

---

## 🎯 Hak Akses Berdasarkan Role

### 👑 Admin (Full Access)

✅ Dashboard - Lihat statistik sistem  
✅ Variabel Fuzzy - **Tambah/Edit/Hapus** variabel  
✅ Aturan Fuzzy - **Tambah/Edit/Hapus** rules  
✅ Data Saham - **Tambah/Edit/Hapus** data  
✅ Proses & Hasil - Jalankan kalkulasi & lihat hasil

### 👤 User (Limited Access)

✅ Dashboard - Lihat statistik sistem  
❌ Variabel Fuzzy - **TIDAK ADA AKSES**  
❌ Aturan Fuzzy - **TIDAK ADA AKSES**  
✅ Data Saham - **Tambah/Edit/Hapus** data (HANYA INI!)  
✅ Proses & Hasil - Jalankan kalkulasi & lihat hasil

---

## 🖥️ User Interface

### Login Page

- User masuk dengan username & password
- Sistem otomatis detect role dari database

### Sidebar

- Menampilkan **username** dan **role badge**:
  - 👑 Admin (badge biru)
  - 👤 User (badge hijau)
- **Menu dinamis** berdasarkan role:
  - Admin: Semua menu terlihat
  - User: Menu Variabel & Aturan **hidden**

### Access Control

- Jika User mencoba akses halaman admin:
  ```
  ⛔ Akses ditolak! Halaman ini hanya untuk Admin.
  💡 Anda login sebagai User biasa. Silakan hubungi Admin untuk akses penuh.
  ```

---

## 🔑 Password Hash

Sistem menggunakan **bcrypt** untuk keamanan password:

```python
import bcrypt

# Generate hash baru
password = "mypassword123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
print(hashed.decode('utf-8'))
```

**⚠️ JANGAN simpan password plain text di database!**

---

## 📁 Files yang Dimodifikasi

1. **database_migration_roles.sql** - Migration script untuk tambah kolom `role`
2. **manage_users.py** - Script manajemen user (CRUD operations)
3. **app.py** - Update dengan:
   - Session state untuk `role`
   - Fungsi `check_credentials()` return role
   - Fungsi `is_admin()` untuk cek role
   - Fungsi `require_admin()` untuk access control
   - Sidebar menampilkan role badge
   - Menu navigasi filter by role
   - Access control di setiap halaman

---

## 🧪 Testing

### Test Admin Login

1. Login dengan: `admin` / `admin123`
2. Pastikan badge menampilkan "👑 Admin"
3. Cek semua menu terlihat
4. Akses halaman Variabel & Aturan (harus bisa)

### Test User Login

1. Login dengan: `user` / `user123`
2. Pastikan badge menampilkan "👤 User"
3. Cek menu Variabel & Aturan **TIDAK terlihat**
4. Coba akses langsung (ganti page state) → harus blocked
5. Pastikan bisa akses Data Saham & Hasil

### Test Manajemen User

```powershell
python manage_users.py
```

1. Lihat daftar user (menu 1)
2. Tambah user baru (menu 2)
3. Login dengan user baru
4. Ubah role (menu 3)
5. Re-login, pastikan role berubah

---

## 🚀 Deployment

### Production Checklist

- [ ] Ganti semua default password
- [ ] Gunakan password yang kuat (min 12 karakter)
- [ ] Setup environment variable untuk credentials
- [ ] Enable HTTPS untuk production
- [ ] Backup database secara berkala
- [ ] Monitor login activity
- [ ] Setup rate limiting untuk login

---

## 🐛 Troubleshooting

### Error: "Kolom 'role' tidak ditemukan"

**Solusi:** Jalankan migration script:

```powershell
Get-Content database_migration_roles.sql | mysql -u root -p fuzzy_tsukamoto
```

### User tidak bisa login setelah migration

**Solusi:** Pastikan kolom `role` punya nilai:

```sql
UPDATE users SET role = 'user' WHERE role IS NULL;
```

### Menu masih muncul padahal User biasa

**Solusi:** Clear browser cache & restart Streamlit:

```powershell
# Ctrl+C di terminal Streamlit
streamlit run app.py --server.port 8501
```

### Lupa password admin

**Solusi:** Reset via MySQL:

```sql
-- Password baru: newpass123
UPDATE users
SET password = '$2b$12$example_hash_here'
WHERE username = 'admin';
```

Atau gunakan `manage_users.py`:

1. Hapus user lama (menu 4)
2. Buat user baru dengan password baru (menu 2)

---

## 📝 Future Enhancements

Fitur yang bisa ditambahkan:

- [ ] **Audit log** - Track semua user activity
- [ ] **Password reset** - Self-service password reset
- [ ] **Email notification** - Notify admin saat user baru register
- [ ] **Session timeout** - Auto logout setelah idle
- [ ] **Two-factor authentication (2FA)**
- [ ] **User permissions granular** - Custom permissions per user
- [ ] **User profile page** - Edit profile, change password
- [ ] **Admin dashboard** - Monitor user activity

---

## 📞 Support

Jika ada masalah dengan multi-user system:

1. Cek log error di terminal Streamlit
2. Verifikasi struktur database: `DESCRIBE users;`
3. Test koneksi database: `python -c "from db_connect import Database; db = Database(); print('OK' if db else 'FAIL')"`
4. Re-run migration script jika perlu

---

**Last Updated:** 2025-12-11  
**Version:** 2.0 - Multi-User Support
