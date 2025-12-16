# Panduan Instalasi & Penggunaan

## Prasyarat

1. **Python 3.8 atau lebih tinggi**

   - Download dari: https://www.python.org/downloads/
   - Pastikan menambahkan Python ke PATH saat instalasi

2. **MySQL Server**

   - Download dari: https://dev.mysql.com/downloads/mysql/
   - Atau gunakan XAMPP/WAMP yang sudah include MySQL

3. **Git** (opsional, untuk clone repository)

## Langkah Instalasi

### 1. Setup Project

```bash
# Clone atau download project
cd c:\Users\puanm\Downloads\tsukamoto

# Buat virtual environment (opsional tapi disarankan)
python -m venv venv

# Aktifkan virtual environment
# Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Database

1. Jalankan MySQL Server
2. Buat database:

```bash
# Login ke MySQL
mysql -u root -p

# Di MySQL prompt:
CREATE DATABASE fuzzy_tsukamoto;
exit;
```

3. Import schema database:

**Untuk PowerShell (Windows):**

```powershell
Get-Content database_setup.sql | mysql -u root -p fuzzy_tsukamoto
```

**Untuk Command Prompt (CMD):**

```cmd
mysql -u root -p fuzzy_tsukamoto < database_setup.sql
```

**Atau menggunakan SOURCE command:**

```powershell
# Login ke MySQL dulu
mysql -u root -p

# Di MySQL prompt, ketik:
USE fuzzy_tsukamoto;
SOURCE C:/Users/puanm/Downloads/tsukamoto/database_setup.sql;
exit;
```

**Atau cara manual:**

- Buka file `database_setup.sql`
- Copy semua isinya
- Paste di MySQL Workbench atau phpMyAdmin
- Execute

### 3. Konfigurasi Environment

1. Copy file `.env.example` menjadi `.env`:

```bash
copy .env.example .env
```

2. Edit file `.env` dan sesuaikan dengan konfigurasi MySQL Anda:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=fuzzy_tsukamoto
DB_PORT=3306
```

### 4. Test Koneksi Database

```bash
python db_connect.py
```

Jika berhasil akan muncul: `✓ Database connection successful!`

## Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

## Login

Kredensial default:

- **Username:** `admin`
- **Password:** `admin123`

## Cara Menggunakan Aplikasi

### 1. Dashboard

- Melihat statistik sistem
- Melihat hasil perhitungan terbaru

### 2. Manajemen Variabel

- Lihat variabel fuzzy yang ada (Volatilitas, Volume, Frekuensi)
- Tambah variabel baru jika diperlukan
- Edit himpunan fuzzy (Rendah, Sedang, Tinggi)

### 3. Manajemen Aturan

- Lihat aturan fuzzy (IF-THEN rules)
- Tambah aturan baru
- Export aturan ke CSV

### 4. Data Saham

- Input data saham baru
- Lihat data saham yang sudah ada
- Hapus data saham

### 5. Proses & Hasil

- Jalankan perhitungan Fuzzy Tsukamoto
- Lihat hasil rekomendasi dalam bentuk ranking
- Download hasil ke CSV

## Alur Penggunaan

1. **Login** dengan kredensial admin
2. **Cek Variabel & Aturan** - pastikan sudah ada (default sudah ter-setup)
3. **Input Data Saham** - tambahkan data saham yang ingin dianalisis
4. **Jalankan Perhitungan** - klik tombol "Jalankan Perhitungan"
5. **Lihat Hasil** - ranking saham berdasarkan risiko

## Troubleshooting

### Error: ModuleNotFoundError

```bash
pip install -r requirements.txt
```

### Error: Access denied for user

- Cek username dan password di file `.env`
- Pastikan MySQL Server sudah running

### Error: Can't connect to MySQL server

- Pastikan MySQL Server sudah berjalan
- Cek port (default: 3306)
- Cek firewall

### Error: Database does not exist

**PowerShell:**

```powershell
mysql -u root -p -e "CREATE DATABASE fuzzy_tsukamoto;"
Get-Content database_setup.sql | mysql -u root -p fuzzy_tsukamoto
```

**Command Prompt (CMD):**

```cmd
mysql -u root -p -e "CREATE DATABASE fuzzy_tsukamoto;"
mysql -u root -p fuzzy_tsukamoto < database_setup.sql
```

## Import Data Sample

Jika ingin import data sample:

```bash
# Login ke MySQL
mysql -u root -p fuzzy_tsukamoto

# Di MySQL prompt:
LOAD DATA LOCAL INFILE 'data/sample_stocks.csv'
INTO TABLE stock_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(stock_code, stock_name, selisih, volume, frekuensi, @input_date)
SET input_date = STR_TO_DATE(@input_date, '%Y-%m-%d');
```

## Testing Modul Fuzzy

Test modul fuzzifikasi:

```bash
python models/fuzzification.py
```

Test modul inferensi:

```bash
python models/inference.py
```

Test modul defuzzifikasi:

```bash
python models/defuzzification.py
```

## Mengganti Password Admin

```bash
# Login ke MySQL
mysql -u root -p fuzzy_tsukamoto

# Di MySQL prompt:
UPDATE users
SET password = '$2b$12$NEW_HASH_HERE'
WHERE username = 'admin';
```

Untuk generate password hash baru, gunakan Python:

```python
import bcrypt
password = "password_baru"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

## Support

Jika ada masalah atau pertanyaan:

1. Cek dokumentasi di README.md
2. Cek komentar di source code
3. Review PRD untuk memahami logika bisnis

## Struktur File

```
/tsukamoto
├── app.py                    # Main aplikasi Streamlit
├── db_connect.py             # Koneksi database
├── database_setup.sql        # Schema database
├── requirements.txt          # Dependencies
├── .env                      # Konfigurasi (jangan di-commit ke git!)
├── .env.example              # Template konfigurasi
├── README.md                 # Dokumentasi utama
├── INSTALLATION.md           # Panduan ini
├── /models                   # Modul fuzzy logic
│   ├── fuzzification.py
│   ├── inference.py
│   └── defuzzification.py
└── /data                     # Sample data
    └── sample_stocks.csv
```

## Next Steps

Setelah instalasi berhasil:

1. ✅ Familiarisasi dengan antarmuka
2. ✅ Test dengan data sample
3. ✅ Pahami alur perhitungan fuzzy
4. ✅ Customize aturan fuzzy sesuai kebutuhan
5. ✅ Input data real dari pasar saham

---

**Good luck! 🚀**
