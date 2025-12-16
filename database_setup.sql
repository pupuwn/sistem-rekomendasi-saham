-- Database Schema untuk Sistem Rekomendasi Saham Fuzzy Tsukamoto
-- Versi: 1.0

CREATE DATABASE IF NOT EXISTS fuzzy_tsukamoto;
USE fuzzy_tsukamoto;

-- Tabel User untuk Autentikasi Admin
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (password: admin123)
-- Password hash menggunakan bcrypt
INSERT INTO users (username, password) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYCkPKn6jZ6');

-- Tabel Variabel Fuzzy (Kriteria Input)
CREATE TABLE IF NOT EXISTS fuzzy_variables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    variable_name VARCHAR(50) NOT NULL,
    min_value DECIMAL(10,2) NOT NULL,
    max_value DECIMAL(10,2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default variables: Volatilitas, Volume, Frekuensi
INSERT INTO fuzzy_variables (variable_name, min_value, max_value, description) VALUES
('Volatilitas', 0, 1000, 'Selisih harga saham (indikator volatilitas)'),
('Volume', 0, 10000000, 'Volume transaksi saham'),
('Frekuensi', 0, 5000, 'Frekuensi transaksi saham');

-- Tabel Himpunan Fuzzy (Membership Functions)
CREATE TABLE IF NOT EXISTS fuzzy_sets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    variable_id INT NOT NULL,
    set_name VARCHAR(50) NOT NULL, -- Rendah, Sedang, Tinggi
    min_value DECIMAL(10,2) NOT NULL,
    max_value DECIMAL(10,2) NOT NULL,
    peak_start DECIMAL(10,2), -- untuk trapezoid
    peak_end DECIMAL(10,2),   -- untuk trapezoid
    FOREIGN KEY (variable_id) REFERENCES fuzzy_variables(id) ON DELETE CASCADE
);

-- Insert default fuzzy sets untuk Volatilitas (0-1000)
INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES
(1, 'Rendah', 0, 500, 0, 200),
(1, 'Sedang', 200, 800, 400, 600),
(1, 'Tinggi', 600, 1000, 800, 1000);

-- Insert default fuzzy sets untuk Volume (0-10M)
INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES
(2, 'Rendah', 0, 5000000, 0, 2000000),
(2, 'Sedang', 2000000, 8000000, 4000000, 6000000),
(2, 'Tinggi', 6000000, 10000000, 8000000, 10000000);

-- Insert default fuzzy sets untuk Frekuensi (0-5000)
INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES
(3, 'Rendah', 0, 2500, 0, 1000),
(3, 'Sedang', 1000, 4000, 2000, 3000),
(3, 'Tinggi', 3000, 5000, 4000, 5000);

-- Tabel Output Fuzzy (Kategori Risiko)
CREATE TABLE IF NOT EXISTS fuzzy_outputs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    output_name VARCHAR(50) NOT NULL,
    min_value DECIMAL(10,2) NOT NULL,
    max_value DECIMAL(10,2) NOT NULL,
    description TEXT
);

-- Insert output variable: Risk Score (0-100)
INSERT INTO fuzzy_outputs (output_name, min_value, max_value, description) VALUES
('Risk_Score', 0, 100, 'Skor risiko saham (0=High Risk, 100=Low Risk)');

-- Tabel Himpunan Output Fuzzy
CREATE TABLE IF NOT EXISTS fuzzy_output_sets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    output_id INT NOT NULL,
    set_name VARCHAR(50) NOT NULL, -- Low_Risk, Medium_Risk, High_Risk
    min_value DECIMAL(10,2) NOT NULL,
    max_value DECIMAL(10,2) NOT NULL,
    peak_start DECIMAL(10,2),
    peak_end DECIMAL(10,2),
    FOREIGN KEY (output_id) REFERENCES fuzzy_outputs(id) ON DELETE CASCADE
);

-- Insert default output fuzzy sets
INSERT INTO fuzzy_output_sets (output_id, set_name, min_value, max_value, peak_start, peak_end) VALUES
(1, 'High_Risk', 0, 50, 0, 30),
(1, 'Medium_Risk', 30, 70, 45, 55),
(1, 'Low_Risk', 50, 100, 70, 100);

-- Tabel Aturan Fuzzy (Rule Base)
CREATE TABLE IF NOT EXISTS fuzzy_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    volatilitas_set VARCHAR(50) NOT NULL, -- Rendah/Sedang/Tinggi
    volume_set VARCHAR(50) NOT NULL,
    frekuensi_set VARCHAR(50) NOT NULL,
    output_set VARCHAR(50) NOT NULL, -- Low_Risk/Medium_Risk/High_Risk
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default fuzzy rules (27 kombinasi: 3x3x3)
-- Logika: Volatilitas Rendah & Volume Tinggi & Frekuensi Tinggi = Low Risk
INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES
('R1', 'Rendah', 'Rendah', 'Rendah', 'Medium_Risk'),
('R2', 'Rendah', 'Rendah', 'Sedang', 'Medium_Risk'),
('R3', 'Rendah', 'Rendah', 'Tinggi', 'Low_Risk'),
('R4', 'Rendah', 'Sedang', 'Rendah', 'Medium_Risk'),
('R5', 'Rendah', 'Sedang', 'Sedang', 'Low_Risk'),
('R6', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk'),
('R7', 'Rendah', 'Tinggi', 'Rendah', 'Low_Risk'),
('R8', 'Rendah', 'Tinggi', 'Sedang', 'Low_Risk'),
('R9', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk'),

('R10', 'Sedang', 'Rendah', 'Rendah', 'High_Risk'),
('R11', 'Sedang', 'Rendah', 'Sedang', 'Medium_Risk'),
('R12', 'Sedang', 'Rendah', 'Tinggi', 'Medium_Risk'),
('R13', 'Sedang', 'Sedang', 'Rendah', 'Medium_Risk'),
('R14', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk'),
('R15', 'Sedang', 'Sedang', 'Tinggi', 'Low_Risk'),
('R16', 'Sedang', 'Tinggi', 'Rendah', 'Medium_Risk'),
('R17', 'Sedang', 'Tinggi', 'Sedang', 'Low_Risk'),
('R18', 'Sedang', 'Tinggi', 'Tinggi', 'Low_Risk'),

('R19', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk'),
('R20', 'Tinggi', 'Rendah', 'Sedang', 'High_Risk'),
('R21', 'Tinggi', 'Rendah', 'Tinggi', 'Medium_Risk'),
('R22', 'Tinggi', 'Sedang', 'Rendah', 'High_Risk'),
('R23', 'Tinggi', 'Sedang', 'Sedang', 'Medium_Risk'),
('R24', 'Tinggi', 'Sedang', 'Tinggi', 'Medium_Risk'),
('R25', 'Tinggi', 'Tinggi', 'Rendah', 'Medium_Risk'),
('R26', 'Tinggi', 'Tinggi', 'Sedang', 'Medium_Risk'),
('R27', 'Tinggi', 'Tinggi', 'Tinggi', 'Low_Risk');

-- Tabel Data Saham (Alternatif)
CREATE TABLE IF NOT EXISTS stock_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(10) NOT NULL,
    stock_name VARCHAR(100),
    selisih DECIMAL(10,2) NOT NULL, -- Volatilitas (selisih harga)
    volume BIGINT NOT NULL,
    frekuensi INT NOT NULL,
    input_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data (contoh dari skripsi)
INSERT INTO stock_data (stock_code, stock_name, selisih, volume, frekuensi, input_date) VALUES
('BBRI', 'Bank Rakyat Indonesia', 450, 3000000, 900, '2025-01-15'),
('BBCA', 'Bank Central Asia', 120, 7000000, 1800, '2025-01-15'),
('UNVR', 'Unilever Indonesia', 200, 5000000, 1200, '2025-01-15'),
('ICBP', 'Indofood CBP', 500, 4000000, 1500, '2025-01-15');

-- Tabel Hasil Perhitungan
CREATE TABLE IF NOT EXISTS calculation_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    final_score DECIMAL(10,2) NOT NULL,
    risk_category VARCHAR(50) NOT NULL, -- Low Risk/Medium Risk/High Risk
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stock_data(id) ON DELETE CASCADE
);

-- Create indexes untuk performa
CREATE INDEX idx_stock_code ON stock_data(stock_code);
CREATE INDEX idx_input_date ON stock_data(input_date);
CREATE INDEX idx_calculation_date ON calculation_results(calculation_date);
