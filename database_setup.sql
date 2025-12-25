-- =================================================================
-- FIXED FUZZY SETS SCHEMA - Disesuaikan dengan Data Real LQ45
-- =================================================================

USE fuzzy_tsukamoto;

-- STEP 1: Update range Fuzzy Variables
UPDATE fuzzy_variables 
SET min_value = 0, max_value = 300 
WHERE variable_name = 'Volatilitas';

UPDATE fuzzy_variables 
SET min_value = 0, max_value = 300000000 
WHERE variable_name = 'Volume';

UPDATE fuzzy_variables 
SET min_value = 0, max_value = 40000 
WHERE variable_name = 'Frekuensi';

-- STEP 2: Hapus fuzzy sets lama
DELETE FROM fuzzy_sets;

-- STEP 3: Insert fuzzy sets baru dengan range yang sesuai

-- =====================================================
-- VOLATILITAS (Selisih Harga): 0 - 300
-- =====================================================
-- Berdasarkan data Anda: BBRI=0, TLKM=50, UNVR=35, BBCA=100, ICBP=100
-- Range realistis: 0-150 (kebanyakan saham LQ45 volatilitas < 150)

INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES
-- Rendah: 0-60 (peak: 0-30)
(1, 'Rendah', 0, 60, 0, 30),

-- Sedang: 30-120 (peak: 60-90)
(1, 'Sedang', 30, 120, 60, 90),

-- Tinggi: 90-300 (peak: 150-300)
(1, 'Tinggi', 90, 300, 150, 300);

-- =====================================================
-- VOLUME TRANSAKSI: 0 - 300 juta
-- =====================================================
-- Berdasarkan data Anda: ICBP=2.3jt, ASII=46jt, UNVR=51jt, 
-- TLKM=96jt, BBCA=164jt, BBRI=226jt

INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES
-- Rendah: 0-50 juta (peak: 0-25 juta)
(2, 'Rendah', 0, 50000000, 0, 25000000),

-- Sedang: 30-120 juta (peak: 60-90 juta)
(2, 'Sedang', 30000000, 120000000, 60000000, 90000000),

-- Tinggi: 100-300 juta (peak: 150-300 juta)
(2, 'Tinggi', 100000000, 300000000, 150000000, 300000000);

-- =====================================================
-- FREKUENSI TRANSAKSI: 0 - 40,000
-- =====================================================
-- Berdasarkan data Anda: ICBP=2079, UNVR=9231, TLKM=9425,
-- ASII=13608, BBRI=28803, BBCA=29510

INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES
-- Rendah: 0-10,000 (peak: 0-5,000)
(3, 'Rendah', 0, 10000, 0, 5000),

-- Sedang: 6,000-20,000 (peak: 10,000-15,000)
(3, 'Sedang', 6000, 20000, 10000, 15000),

-- Tinggi: 15,000-40,000 (peak: 25,000-40,000)
(3, 'Tinggi', 15000, 40000, 25000, 40000);

-- =====================================================
-- VERIFIKASI DATA
-- =====================================================

-- Cek Fuzzy Variables yang sudah diupdate
SELECT * FROM fuzzy_variables;

-- Cek Fuzzy Sets yang baru
SELECT 
    fv.variable_name,
    fs.set_name,
    fs.min_value,
    fs.max_value,
    fs.peak_start,
    fs.peak_end
FROM fuzzy_sets fs
JOIN fuzzy_variables fv ON fs.variable_id = fv.id
ORDER BY fv.variable_name, fs.min_value;

-- =====================================================
-- CATATAN PENTING
-- =====================================================
-- Dengan range baru ini, data Anda seharusnya menghasilkan:
--
-- BBCA (Vol=100, Vol=164jt, Freq=29510):
--   Volatilitas: Tinggi (μ ≈ 0.2-0.5)
--   Volume: Tinggi (μ ≈ 1.0)
--   Frekuensi: Tinggi (μ ≈ 1.0)
--   Rule: R27 (Tinggi,Tinggi,Tinggi) → Low_Risk
--   Expected Score: 70-85
--
-- BBRI (Vol=0, Vol=226jt, Freq=28803):
--   Volatilitas: Rendah (μ = 1.0)
--   Volume: Tinggi (μ = 1.0)
--   Frekuensi: Tinggi (μ = 1.0)
--   Rule: R9 (Rendah,Tinggi,Tinggi) → Low_Risk
--   Expected Score: 85-95
--
-- ICBP (Vol=100, Vol=2.3jt, Freq=2079):
--   Volatilitas: Tinggi (μ ≈ 0.2-0.5)
--   Volume: Rendah (μ = 1.0)
--   Frekuensi: Rendah (μ ≈ 0.5)
--   Rule: R19 (Tinggi,Rendah,Rendah) → High_Risk
--   Expected Score: 20-35