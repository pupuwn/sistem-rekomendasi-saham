# Sistem Rekomendasi Saham Low-Risk (Fuzzy Tsukamoto)

Sistem Pendukung Keputusan berbasis Fuzzy Tsukamoto untuk merekomendasikan saham berisiko rendah di Bursa Efek Indonesia (BEI) - Indeks LQ45.

## Fitur Utama

- 🔐 **Multi-User Authentication** dengan Role-Based Access Control
- 👑 **Admin**: Akses penuh ke semua fitur
- 👤 **User**: Akses terbatas (hanya Data Saham & Hasil)
- 📊 Manajemen Kriteria & Variabel Fuzzy
- 📋 Manajemen Aturan Fuzzy (Rule Base)
- 💹 Input & Kelola Data Saham
- 🧮 Perhitungan Otomatis Fuzzy Tsukamoto
- 📈 Dashboard Hasil & Ranking Saham

## Teknologi

- Python 3.8+
- Streamlit (Web Framework)
- MySQL (Database)
- Pandas & NumPy (Data Processing)

## Instalasi

1. Clone repository ini
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Setup database MySQL dan jalankan script `database_setup.sql`

4. Copy `.env.example` menjadi `.env` dan sesuaikan konfigurasi database

5. Jalankan aplikasi:

```bash
streamlit run app.py
```

## Kredensial Default

### Admin (Full Access)

- Username: `admin`
- Password: `admin123`

### User (Limited Access - Stocks Only)

- Username: `user`
- Password: `user123`

⚠️ **PENTING**: Ganti password default untuk keamanan!

## Multi-User Management

Gunakan script manajemen user:

```bash
python manage_users.py
```

Fitur:

- Tambah user baru
- Ubah role (admin/user)
- Hapus user
- Lihat daftar user

Dokumentasi lengkap: `MULTI_USER_GUIDE.md`

## Struktur Project

```
/tsukamoto
├── /models            # Modul logika fuzzy
│   ├── fuzzification.py
│   ├── inference.py
│   └── defuzzification.py
├── /data              # Dataset (optional)
├── app.py             # Main Streamlit App
├── db_connect.py      # Koneksi Database
├── database_setup.sql # Schema Database
└── requirements.txt
```

## Metodologi

Sistem ini menggunakan metode **Fuzzy Tsukamoto** dengan tahapan:

1. **Fuzzifikasi**: Mengubah nilai crisp menjadi derajat keanggotaan fuzzy
2. **Inferensi**: Evaluasi aturan IF-THEN dengan fungsi implikasi Tsukamoto
3. **Defuzzifikasi**: Menghitung nilai crisp dengan weighted average

## Kriteria Penilaian

- **Volatilitas** (dari Selisih Harga)
- **Volume** Transaksi
- **Frekuensi** Transaksi

## Output

Sistem menghasilkan **skor risiko** dan **kategori risiko**:

- Low Risk (Skor > 70)
- Medium Risk (Skor 40-70)
- High Risk (Skor < 40)
