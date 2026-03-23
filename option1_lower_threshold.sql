-- =================================================================
-- OPSI 1: TURUNKAN THRESHOLD LOW RISK DARI 70 MENJADI 69
-- =================================================================
-- Dengan perubahan ini, skor 69.85 akan masuk kategori Low Risk

USE fuzzy_tsukamoto;

-- Update output sets
UPDATE fuzzy_output_sets SET min_value = 69 WHERE set_name = 'Low_Risk';
UPDATE fuzzy_output_sets SET max_value = 69 WHERE set_name = 'Medium_Risk';

-- Verifikasi
SELECT * FROM fuzzy_output_sets ORDER BY min_value DESC;

-- =================================================================
-- CATATAN:
-- Dengan threshold baru:
-- - Low Risk: >= 69 (sebelumnya >= 70)
-- - Medium Risk: 40-68.99 (sebelumnya 40-69.99)
-- - High Risk: < 40
--
-- UNVR dengan skor 69.85 akan menjadi Low Risk
-- =================================================================
