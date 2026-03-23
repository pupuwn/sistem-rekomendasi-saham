-- =================================================================
-- UPDATE FUZZY SETS AGAR SESUAI DENGAN EXCEL
-- =================================================================
-- Berdasarkan reverse engineering dari data Excel UNVR

USE fuzzy_tsukamoto;

-- Backup: Tampilkan konfigurasi lama
SELECT 'KONFIGURASI LAMA - VOLATILITAS:' as info;
SELECT fv.variable_name, fs.set_name, fs.min_value, fs.max_value, fs.peak_start, fs.peak_end
FROM fuzzy_sets fs
JOIN fuzzy_variables fv ON fs.variable_id = fv.id
WHERE fv.variable_name = 'Volatilitas'
ORDER BY fs.min_value;

-- Update range Volatilitas variable (kembali ke 0-300, bukan -50-300)
UPDATE fuzzy_variables 
SET min_value = 0, max_value = 300 
WHERE variable_name = 'Volatilitas';

-- Hapus fuzzy sets lama untuk Volatilitas
DELETE FROM fuzzy_sets WHERE variable_id = 1;

-- Insert fuzzy sets baru SESUAI DENGAN EXCEL
-- =================================================================
-- VOLATILITAS - KONFIGURASI EXCEL
-- =================================================================

-- Rendah: [0, 0, 30, 60] (SEGITIGA, bukan trapezoid)
-- Ini adalah segitiga karena peak_start = peak_end = 0 (atau min_value = peak_start)
INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) 
VALUES (1, 'Rendah', 0, 60, 0, 30);

-- Sedang: [30, 60, 90, 120] (TRAPEZOID)
-- Perbedaan dengan sistem lama: min_value = 30 (bukan 20)
INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) 
VALUES (1, 'Sedang', 30, 120, 60, 90);

-- Tinggi: [90, 150, 300, 300] (TRAPEZOID dengan plateau di atas)
-- Sama seperti sebelumnya
INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) 
VALUES (1, 'Tinggi', 90, 300, 150, 300);

-- Verifikasi hasil update
SELECT 'KONFIGURASI BARU - VOLATILITAS:' as info;
SELECT fv.variable_name, fs.set_name, fs.min_value, fs.max_value, fs.peak_start, fs.peak_end
FROM fuzzy_sets fs
JOIN fuzzy_variables fv ON fs.variable_id = fv.id
WHERE fv.variable_name = 'Volatilitas'
ORDER BY fs.min_value;

-- =================================================================
-- PENJELASAN PERUBAHAN:
-- =================================================================
-- SEBELUM:
--   Rendah: [-50, -20, 30, 60] --> Mendukung nilai negatif
--   Sedang: [20, 60, 90, 120]
--
-- SESUDAH (SESUAI EXCEL):
--   Rendah: [0, 0, 30, 60] --> Tidak mendukung nilai negatif
--   Sedang: [30, 60, 90, 120] --> Min dimulai dari 30, bukan 20
--
-- DAMPAK UNTUK VOLATILITAS = 35:
--   SEBELUM: mu_sedang = (35-20)/(60-20) = 0.375
--   SESUDAH: mu_sedang = (35-30)/(60-30) = 0.16667 ✓ (SAMA DENGAN EXCEL)
--
-- CATATAN:
-- Dengan perubahan ini, sistem TIDAK BISA menerima volatilitas negatif!
-- Jika Anda ingin input negatif, gunakan konfigurasi yang berbeda dari Excel.
-- =================================================================
