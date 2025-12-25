# update_database.py - Fixed Version

import sys
from db_connect import get_db_connection

def execute_commands(db, commands):
    """Helper function to execute a list of SQL commands one by one."""
    success_count = 0
    fail_count = 0
    
    for i, command in enumerate(commands, 1):
        # Skip empty commands
        if not command.strip():
            continue
            
        try:
            db.execute_query(command)
            success_count += 1
            print(f"  ✓ Command {i}/{len(commands)} executed successfully")
        except Exception as e:
            # Abaikan error tertentu yang tidak kritis
            error_msg = str(e)
            if any(x in error_msg for x in ["Duplicate column name", "already exists", "Unknown column"]):
                print(f"  ℹ️ Command {i}: {error_msg[:100]}... (skipped, not critical)")
                success_count += 1
                continue
            
            print(f"  ❌ Command {i} failed: {command[:100]}...")
            print(f"     Error: {error_msg}")
            fail_count += 1
    
    print(f"\n  📊 Summary: {success_count} succeeded, {fail_count} failed")
    return fail_count == 0

def run_update():
    """Connects to the database and runs the update scripts."""
    print("="*70)
    print("🚀 MEMULAI UPDATE DATABASE FUZZY TSUKAMOTO")
    print("="*70)
    
    db = get_db_connection()
    if not db:
        print("❌ Gagal terhubung ke database. Keluar.")
        sys.exit(1)

    print("✅ Berhasil terhubung ke database.\n")

    try:
        # =================================================================
        # STEP 1: UPDATE RANGE FUZZY VARIABLES
        # =================================================================
        print("📋 STEP 1: Update Range Fuzzy Variables")
        print("-" * 70)
        
        variables_update = [
            "UPDATE fuzzy_variables SET min_value = 0, max_value = 300, description = 'Selisih harga saham (0-300)' WHERE variable_name = 'Volatilitas'",
            "UPDATE fuzzy_variables SET min_value = 0, max_value = 300000000, description = 'Volume transaksi harian (0-300 juta)' WHERE variable_name = 'Volume'",
            "UPDATE fuzzy_variables SET min_value = 0, max_value = 40000, description = 'Frekuensi transaksi harian (0-40,000)' WHERE variable_name = 'Frekuensi'"
        ]
        
        if execute_commands(db, variables_update):
            print("✅ Range variabel berhasil diperbarui.\n")
        else:
            print("⚠️ Ada error saat update variabel, tapi melanjutkan...\n")

        # =================================================================
        # STEP 2: UPDATE FUZZY SETS (INPUT)
        # =================================================================
        print("📋 STEP 2: Update Fuzzy Sets (Input Membership Functions)")
        print("-" * 70)
        
        # Hapus fuzzy sets lama
        fuzzy_sets_delete = ["DELETE FROM fuzzy_sets"]
        execute_commands(db, fuzzy_sets_delete)
        
        # Insert fuzzy sets baru dengan range yang disesuaikan
        fuzzy_sets_insert = [
            # ===== VOLATILITAS (Selisih Harga): 0-300 =====
            # Rendah: 0-60 (peak: 0-30)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (1, 'Rendah', 0, 60, 0, 30)",
            
            # Sedang: 30-120 (peak: 60-90)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (1, 'Sedang', 30, 120, 60, 90)",
            
            # Tinggi: 90-300 (peak: 150-300)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (1, 'Tinggi', 90, 300, 150, 300)",
            
            # ===== VOLUME TRANSAKSI: 0-300 juta =====
            # Rendah: 0-50 juta (peak: 0-25 juta)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (2, 'Rendah', 0, 50000000, 0, 25000000)",
            
            # Sedang: 30-120 juta (peak: 60-90 juta)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (2, 'Sedang', 30000000, 120000000, 60000000, 90000000)",
            
            # Tinggi: 100-300 juta (peak: 150-300 juta)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (2, 'Tinggi', 100000000, 300000000, 150000000, 300000000)",
            
            # ===== FREKUENSI TRANSAKSI: 0-40,000 =====
            # Rendah: 0-10,000 (peak: 0-5,000)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (3, 'Rendah', 0, 10000, 0, 5000)",
            
            # Sedang: 6,000-20,000 (peak: 10,000-15,000)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (3, 'Sedang', 6000, 20000, 10000, 15000)",
            
            # Tinggi: 15,000-40,000 (peak: 25,000-40,000)
            "INSERT INTO fuzzy_sets (variable_id, set_name, min_value, max_value, peak_start, peak_end) VALUES (3, 'Tinggi', 15000, 40000, 25000, 40000)"
        ]
        
        if execute_commands(db, fuzzy_sets_insert):
            print("✅ Fuzzy sets (input) berhasil diperbarui.\n")
        else:
            print("❌ Gagal update fuzzy sets.\n")
            return

        # =================================================================
        # STEP 3: UPDATE FUZZY OUTPUT SETS
        # =================================================================
        print("📋 STEP 3: Update Fuzzy Output Sets")
        print("-" * 70)
        
        # Cek apakah tabel fuzzy_output_sets ada
        check_table = "SHOW TABLES LIKE 'fuzzy_output_sets'"
        result = db.fetch_one(check_table)
        
        if not result:
            print("⚠️ Tabel fuzzy_output_sets tidak ada, membuat tabel baru...")
            create_table = """
            CREATE TABLE IF NOT EXISTS fuzzy_output_sets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                set_name VARCHAR(50) NOT NULL,
                min_value DECIMAL(10,2) NOT NULL,
                max_value DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            db.execute_query(create_table)
        
        # Hapus dan insert ulang output sets
        output_sets_update = [
            "DELETE FROM fuzzy_output_sets",
            
            # Low_Risk: 70-100 (semakin tinggi semakin baik)
            "INSERT INTO fuzzy_output_sets (set_name, min_value, max_value) VALUES ('Low_Risk', 70, 100)",
            
            # Medium_Risk: 40-70
            "INSERT INTO fuzzy_output_sets (set_name, min_value, max_value) VALUES ('Medium_Risk', 40, 70)",
            
            # High_Risk: 0-40 (semakin rendah semakin berisiko)
            "INSERT INTO fuzzy_output_sets (set_name, min_value, max_value) VALUES ('High_Risk', 0, 40)"
        ]
        
        if execute_commands(db, output_sets_update):
            print("✅ Fuzzy output sets berhasil diperbarui.\n")
        else:
            print("❌ Gagal update fuzzy output sets.\n")

        # =================================================================
        # STEP 4: UPDATE FUZZY RULES (UNIVERSAL)
        # =================================================================
        print("📋 STEP 4: Update Fuzzy Rules (27 Aturan Universal)")
        print("-" * 70)
        print("ℹ️ Menggunakan aturan UMUM yang berlaku untuk SEMUA saham")
        print("   (bukan aturan spesifik per saham)\n")
        
        # Hapus kolom stock_code jika ada (karena rules harus universal)
        try:
            db.execute_query("ALTER TABLE fuzzy_rules DROP COLUMN stock_code")
            print("  ✓ Kolom stock_code dihapus (rules menjadi universal)")
        except:
            print("  ℹ️ Kolom stock_code tidak ada atau sudah dihapus")
        
        # Hapus kolom z_value jika ada (z dihitung dinamis, bukan hardcoded)
        try:
            db.execute_query("ALTER TABLE fuzzy_rules DROP COLUMN z_value")
            print("  ✓ Kolom z_value dihapus (z akan dihitung dinamis)")
        except:
            print("  ℹ️ Kolom z_value tidak ada atau sudah dihapus")
        
        rules_update = [
            "DELETE FROM fuzzy_rules",
            
            # ===== VOLATILITAS RENDAH (Low Volatility = Good) =====
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R1', 'Rendah', 'Rendah', 'Rendah', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R2', 'Rendah', 'Rendah', 'Sedang', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R3', 'Rendah', 'Rendah', 'Tinggi', 'Low_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R4', 'Rendah', 'Sedang', 'Rendah', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R5', 'Rendah', 'Sedang', 'Sedang', 'Low_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R6', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R7', 'Rendah', 'Tinggi', 'Rendah', 'Low_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R8', 'Rendah', 'Tinggi', 'Sedang', 'Low_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R9', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk')",
            
            # ===== VOLATILITAS SEDANG (Medium Volatility) =====
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R10', 'Sedang', 'Rendah', 'Rendah', 'High_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R11', 'Sedang', 'Rendah', 'Sedang', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R12', 'Sedang', 'Rendah', 'Tinggi', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R13', 'Sedang', 'Sedang', 'Rendah', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R14', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R15', 'Sedang', 'Sedang', 'Tinggi', 'Low_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R16', 'Sedang', 'Tinggi', 'Rendah', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R17', 'Sedang', 'Tinggi', 'Sedang', 'Low_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R18', 'Sedang', 'Tinggi', 'Tinggi', 'Low_Risk')",
            
            # ===== VOLATILITAS TINGGI (High Volatility = Risky) =====
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R19', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R20', 'Tinggi', 'Rendah', 'Sedang', 'High_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R21', 'Tinggi', 'Rendah', 'Tinggi', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R22', 'Tinggi', 'Sedang', 'Rendah', 'High_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R23', 'Tinggi', 'Sedang', 'Sedang', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R24', 'Tinggi', 'Sedang', 'Tinggi', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R25', 'Tinggi', 'Tinggi', 'Rendah', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R26', 'Tinggi', 'Tinggi', 'Sedang', 'Medium_Risk')",
            "INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set) VALUES ('R27', 'Tinggi', 'Tinggi', 'Tinggi', 'Low_Risk')"
        ]
        
        if execute_commands(db, rules_update):
            print("✅ Fuzzy rules (27 aturan universal) berhasil diperbarui.\n")
        else:
            print("❌ Gagal update fuzzy rules.\n")

        # =================================================================
        # STEP 5: VERIFIKASI HASIL UPDATE
        # =================================================================
        print("📋 STEP 5: Verifikasi Hasil Update")
        print("-" * 70)
        
        # Cek jumlah data
        count_vars = db.fetch_one("SELECT COUNT(*) as count FROM fuzzy_variables")
        count_sets = db.fetch_one("SELECT COUNT(*) as count FROM fuzzy_sets")
        count_output_sets = db.fetch_one("SELECT COUNT(*) as count FROM fuzzy_output_sets")
        count_rules = db.fetch_one("SELECT COUNT(*) as count FROM fuzzy_rules")
        
        print(f"  ✓ Fuzzy Variables: {count_vars['count']} (expected: 3)")
        print(f"  ✓ Fuzzy Sets: {count_sets['count']} (expected: 9)")
        print(f"  ✓ Fuzzy Output Sets: {count_output_sets['count']} (expected: 3)")
        print(f"  ✓ Fuzzy Rules: {count_rules['count']} (expected: 27)")
        
        # Validasi
        all_ok = (
            count_vars['count'] == 3 and
            count_sets['count'] == 9 and
            count_output_sets['count'] == 3 and
            count_rules['count'] == 27
        )
        
        print("\n" + "="*70)
        if all_ok:
            print("🎉 PEMBARUAN DATABASE BERHASIL!")
            print("="*70)
            print("\n✅ Semua tabel telah diperbarui dengan benar.")
            print("✅ Range fuzzy sets sudah disesuaikan dengan data real.")
            print("✅ 27 aturan universal siap digunakan untuk semua saham.")
            print("\n💡 Langkah selanjutnya:")
            print("   1. Restart aplikasi Streamlit")
            print("   2. Jalankan 'Proses Perhitungan' di menu aplikasi")
            print("   3. Hasil seharusnya menampilkan skor yang bervariasi (bukan 0)")
        else:
            print("⚠️ PEMBARUAN SELESAI DENGAN PERINGATAN")
            print("="*70)
            print("\n⚠️ Beberapa tabel memiliki jumlah data yang tidak sesuai.")
            print("   Silakan cek log error di atas dan perbaiki secara manual.")
        
    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ TERJADI ERROR FATAL")
        print("="*70)
        print(f"Error: {e}")
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())
    finally:
        db.disconnect()
        print("\n🔌 Koneksi database ditutup.")

if __name__ == "__main__":
    run_update()