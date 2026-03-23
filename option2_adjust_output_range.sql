-- =================================================================
-- OPSI 2: SESUAIKAN RANGE OUTPUT SETS DENGAN EXCEL
-- =================================================================
-- Kemungkinan Excel menggunakan range yang berbeda

USE fuzzy_tsukamoto;

-- Backup data lama (opsional, untuk referensi)
SELECT 'SEBELUM UPDATE:' as info, set_name, min_value, max_value FROM fuzzy_output_sets;

-- Update dengan range yang mungkin digunakan Excel
-- Biasanya Excel menggunakan range yang lebih proporsional:

-- ALTERNATIF 1: Range proposional (33.33% untuk masing-masing)
UPDATE fuzzy_output_sets SET min_value = 66.67, max_value = 100 WHERE set_name = 'Low_Risk';
UPDATE fuzzy_output_sets SET min_value = 33.33, max_value = 66.67 WHERE set_name = 'Medium_Risk';
UPDATE fuzzy_output_sets SET max_value = 33.33 WHERE set_name = 'High_Risk';

-- Verifikasi hasil
SELECT 'SETELAH UPDATE:' as info, set_name, min_value, max_value FROM fuzzy_output_sets ORDER BY min_value DESC;

-- =================================================================
-- CATATAN:
-- Dengan range baru:
-- - Low Risk: >= 66.67
-- - Medium Risk: 33.33 - 66.66
-- - High Risk: < 33.33
--
-- UNVR dengan skor 69.85 akan menjadi Low Risk
-- =================================================================
