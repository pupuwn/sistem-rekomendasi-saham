-- Migration: Tambah Role-Based Access Control
-- Tanggal: 2025-12-11

USE fuzzy_tsukamoto;

-- Cek dan tambah kolom role ke tabel users (jika belum ada)
-- MySQL tidak support IF NOT EXISTS untuk ALTER COLUMN, jadi kita handle dengan procedure

DELIMITER $$

DROP PROCEDURE IF EXISTS add_role_column$$
CREATE PROCEDURE add_role_column()
BEGIN
    -- Cek apakah kolom 'role' sudah ada
    IF NOT EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = 'fuzzy_tsukamoto' 
        AND TABLE_NAME = 'users' 
        AND COLUMN_NAME = 'role'
    ) THEN
        ALTER TABLE users ADD COLUMN role ENUM('admin', 'user') DEFAULT 'user' AFTER password;
    END IF;
END$$

DELIMITER ;

-- Jalankan procedure
CALL add_role_column();

-- Hapus procedure setelah selesai
DROP PROCEDURE IF EXISTS add_role_column;

-- Update existing admin user
UPDATE users SET role = 'admin' WHERE username = 'admin';

-- Tambah sample user biasa (password: user123)
INSERT INTO users (username, password, role) VALUES 
('user', '$2b$12$rMKLw5hDGJ0yJzGx/XFsB.KZ0xVQGvqYJ8r6QMXH8k2LxPCJ3Fk2C', 'user')
ON DUPLICATE KEY UPDATE password = VALUES(password), role = VALUES(role);

-- Verifikasi
SELECT id, username, role, created_at FROM users ORDER BY role DESC, id;
