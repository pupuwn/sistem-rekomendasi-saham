-- =================================================================
-- UPDATE FUZZY OUTPUT RANGES SESUAI FILE EXCEL
-- =================================================================
-- Rentang baru:
-- - High Risk: 0-40 (Grafik Turun)
-- - Medium Risk: 30-70 (Grafik Segitiga)
-- - Low Risk: 60-100 (Grafik Naik)
-- =================================================================

USE fuzzy_tsukamoto;

-- Backup data lama untuk referensi
SELECT '=== SEBELUM UPDATE ===' as info;
SELECT set_name, min_value, max_value 
FROM fuzzy_output_sets 
ORDER BY min_value;

-- Update ranges sesuai Excel
UPDATE fuzzy_output_sets SET min_value = 0, max_value = 40 WHERE set_name = 'High_Risk';
UPDATE fuzzy_output_sets SET min_value = 30, max_value = 70 WHERE set_name = 'Medium_Risk';
UPDATE fuzzy_output_sets SET min_value = 60, max_value = 100 WHERE set_name = 'Low_Risk';

-- Verify new values
SELECT '=== SETELAH UPDATE ===' as info;
SELECT set_name, min_value, max_value 
FROM fuzzy_output_sets 
ORDER BY min_value DESC;

-- =================================================================
-- CATATAN:
-- Dengan range baru:
-- - Low Risk: 60-100 (risiko rendah, bagus untuk investasi)
-- - Medium Risk: 30-70 (risiko sedang, perlu pertimbangan)
-- - High Risk: 0-40 (risiko tinggi, hindari)
--
-- Ada overlap yang wajar:
-- - High-Medium overlap: 30-40
-- - Medium-Low overlap: 60-70
-- =================================================================
