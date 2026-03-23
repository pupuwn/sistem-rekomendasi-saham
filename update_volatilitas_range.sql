-- =================================================================
-- UPDATE RANGE VOLATILITAS UNTUK MENDUKUNG NILAI NEGATIF
-- =================================================================

USE fuzzy_tsukamoto;

-- STEP 1: Update range Fuzzy Variables untuk Volatilitas
-- Mengubah min_value dari 0 menjadi -50
UPDATE fuzzy_variables 
SET min_value = -50, max_value = 300 
WHERE variable_name = 'Volatilitas';

-- STEP 2: Hapus fuzzy sets lama untuk Volatilitas
DELETE FROM fuzzy_sets WHERE variable_id = 1;

-- STEP 3: Insert fuzzy sets baru dengan range yang mendukung nilai negatif
-- =====================================================
-- VOLATILITAS (Selisih Harga): -50 hingga 300
-- =====================================================
-- Range ini mencakup:
-- - Nilai negatif (penurunan): -50 hingga 0
-- - Nilai positif (kenaikan): 0 hingga 300

INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES
-- Rendah (Sangat Stabil): -50 hingga 60 (peak: -20 hingga 30)
-- Mencakup nilai negatif dan positif rendah
(1, 'Rendah', -50, 60, -20, 30),

-- Sedang (Volatilitas Normal): 20 hingga 120 (peak: 60 hingga 90)
(1, 'Sedang', 20, 120, 60, 90),

-- Tinggi (Volatilitas Tinggi): 90 hingga 300 (peak: 150 hingga 300)
(1, 'Tinggi', 90, 300, 150, 300);

-- =====================================================
-- VERIFIKASI DATA
-- =====================================================

-- Cek Fuzzy Variables yang sudah diupdate
SELECT * FROM fuzzy_variables WHERE variable_name = 'Volatilitas';

-- Cek Fuzzy Sets yang baru untuk Volatilitas
SELECT 
    fv.variable_name,
    fs.set_name,
    fs.min_value,
    fs.max_value,
    fs.peak_start,
    fs.peak_end
FROM fuzzy_sets fs
JOIN fuzzy_variables fv ON fs.variable_id = fv.id
WHERE fv.variable_name = 'Volatilitas'
ORDER BY fs.min_value;

-- =====================================================
-- CATATAN PENTING
-- =====================================================
-- Dengan range baru ini:
-- - Nilai -15 akan masuk ke kategori "Rendah" dengan derajat keanggotaan > 0
-- - Nilai negatif menunjukkan volatilitas yang sangat rendah/stabil
-- - Sistem sekarang dapat menghitung skor untuk semua nilai termasuk negatif
