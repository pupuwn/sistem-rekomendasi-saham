import sys
from db_connect import get_db_connection

def run_fix():
    print("🚀 MEMULAI PERBAIKAN STRUKTUR & DATA DATABASE")
    db = get_db_connection()
    if not db:
        sys.exit("❌ Gagal koneksi database")

    try:
        # 1. PERBAIKI STRUKTUR TABEL (ALTER TABLE)
        # Ubah kolom menjadi DECIMAL(20,2) agar muat angka ratusan juta
        print("\n🔧 STEP 1: Memperbesar Kapasitas Kolom Database...")
        
        alter_commands = [
            # Perbesar kolom di fuzzy_variables
            "ALTER TABLE fuzzy_variables MODIFY min_value DECIMAL(20,2)",
            "ALTER TABLE fuzzy_variables MODIFY max_value DECIMAL(20,2)",
            
            # Perbesar kolom di fuzzy_sets
            "ALTER TABLE fuzzy_sets MODIFY min_value DECIMAL(20,2)",
            "ALTER TABLE fuzzy_sets MODIFY max_value DECIMAL(20,2)",
            "ALTER TABLE fuzzy_sets MODIFY peak_start DECIMAL(20,2)",
            "ALTER TABLE fuzzy_sets MODIFY peak_end DECIMAL(20,2)",

            # Perbesar kolom di fuzzy_output_sets
            "ALTER TABLE fuzzy_output_sets MODIFY min_value DECIMAL(20,2)",
            "ALTER TABLE fuzzy_output_sets MODIFY max_value DECIMAL(20,2)"
        ]
        
        for cmd in alter_commands:
            try:
                db.execute_query(cmd)
            except Exception as e:
                print(f"   Info: {e} (Lanjut)")

        # 2. RE-CREATE OUTPUT SETS (Untuk mengatasi error ID)
        print("🔧 STEP 2: Reset Tabel Output Sets...")
        db.execute_query("DROP TABLE IF EXISTS fuzzy_output_sets")
        db.execute_query("""
            CREATE TABLE fuzzy_output_sets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                set_name VARCHAR(50),
                min_value DECIMAL(20,2),
                max_value DECIMAL(20,2)
            )
        """)

        # 3. INSERT DATA BARU (Range Besar)
        print("📥 STEP 3: Insert Data Baru (Range Besar)...")
        
        # Bersihkan data lama
        db.execute_query("DELETE FROM fuzzy_variables")
        db.execute_query("DELETE FROM fuzzy_sets")
        db.execute_query("DELETE FROM fuzzy_rules")
        db.execute_query("DELETE FROM fuzzy_output_sets")

        # Insert Variables
        db.execute_query("INSERT INTO fuzzy_variables (id, variable_name, min_value, max_value) VALUES (1, 'Volatilitas', 0, 300)")
        db.execute_query("INSERT INTO fuzzy_variables (id, variable_name, min_value, max_value) VALUES (2, 'Volume', 0, 300000000)")
        db.execute_query("INSERT INTO fuzzy_variables (id, variable_name, min_value, max_value) VALUES (3, 'Frekuensi', 0, 40000)")

        # Insert Sets (Volatilitas)
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (1, 'Rendah', 0, 60, 0, 30)")
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (1, 'Sedang', 30, 120, 60, 90)")
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (1, 'Tinggi', 90, 300, 150, 300)")

        # Insert Sets (Volume - JUTAAN)
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (2, 'Rendah', 0, 50000000, 0, 25000000)")
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (2, 'Sedang', 30000000, 120000000, 60000000, 90000000)")
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (2, 'Tinggi', 100000000, 300000000, 150000000, 300000000)")

        # Insert Sets (Frekuensi)
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (3, 'Rendah', 0, 10000, 0, 5000)")
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (3, 'Sedang', 6000, 20000, 10000, 15000)")
        db.execute_query("INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (3, 'Tinggi', 15000, 40000, 25000, 40000)")

        # Insert Output Sets
        db.execute_query("INSERT INTO fuzzy_output_sets (set_name, min_value, max_value) VALUES ('Low_Risk', 70, 100)")
        db.execute_query("INSERT INTO fuzzy_output_sets (set_name, min_value, max_value) VALUES ('Medium_Risk', 40, 70)")
        db.execute_query("INSERT INTO fuzzy_output_sets (set_name, min_value, max_value) VALUES ('High_Risk', 0, 40)")

        # Insert Rules (Universal)
        rules = [
            # Rules Low Volatility
            ('R1', 'Rendah', 'Rendah', 'Rendah', 'Medium_Risk'), ('R2', 'Rendah', 'Rendah', 'Sedang', 'Medium_Risk'), ('R3', 'Rendah', 'Rendah', 'Tinggi', 'Low_Risk'),
            ('R4', 'Rendah', 'Sedang', 'Rendah', 'Medium_Risk'), ('R5', 'Rendah', 'Sedang', 'Sedang', 'Low_Risk'), ('R6', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk'),
            ('R7', 'Rendah', 'Tinggi', 'Rendah', 'Low_Risk'), ('R8', 'Rendah', 'Tinggi', 'Sedang', 'Low_Risk'), ('R9', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk'),
            # Rules Medium Volatility
            ('R10', 'Sedang', 'Rendah', 'Rendah', 'High_Risk'), ('R11', 'Sedang', 'Rendah', 'Sedang', 'Medium_Risk'), ('R12', 'Sedang', 'Rendah', 'Tinggi', 'Medium_Risk'),
            ('R13', 'Sedang', 'Sedang', 'Rendah', 'Medium_Risk'), ('R14', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk'), ('R15', 'Sedang', 'Sedang', 'Tinggi', 'Low_Risk'),
            ('R16', 'Sedang', 'Tinggi', 'Rendah', 'Medium_Risk'), ('R17', 'Sedang', 'Tinggi', 'Sedang', 'Low_Risk'), ('R18', 'Sedang', 'Tinggi', 'Tinggi', 'Low_Risk'),
            # Rules High Volatility
            ('R19', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk'), ('R20', 'Tinggi', 'Rendah', 'Sedang', 'High_Risk'), ('R21', 'Tinggi', 'Rendah', 'Tinggi', 'Medium_Risk'),
            ('R22', 'Tinggi', 'Sedang', 'Rendah', 'High_Risk'), ('R23', 'Tinggi', 'Sedang', 'Sedang', 'Medium_Risk'), ('R24', 'Tinggi', 'Sedang', 'Tinggi', 'Medium_Risk'),
            ('R25', 'Tinggi', 'Tinggi', 'Rendah', 'Medium_Risk'), ('R26', 'Tinggi', 'Tinggi', 'Sedang', 'Medium_Risk'), ('R27', 'Tinggi', 'Tinggi', 'Tinggi', 'Low_Risk')
        ]
        
        for r in rules:
            sql = f"INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
            db.execute_query(sql)

        print("\n✅ SELESAI! Database sudah di-upgrade untuk menampung angka ratusan juta.")
        
    except Exception as e:
        print(f"\n❌ Error Fatal: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    run_fix()