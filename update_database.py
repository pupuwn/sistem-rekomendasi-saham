# update_database.py

import sys
from db_connect import get_db_connection

def execute_commands(db, commands):
    """Helper function to execute a list of SQL commands one by one."""
    for command in commands:
        try:
            db.execute_query(command)
        except Exception as e:
            # Abaikan error jika kolom sudah ada
            if "Duplicate column name" in str(e):
                print(f"ℹ️ Kolom 'stock_code' mungkin sudah ada, melanjutkan...")
                continue
            print(f"❌ Gagal menjalankan perintah: {command.strip()}")
            print(f"   Error: {e}")
            return False
    return True

def run_update():
    """Connects to the database and runs the update scripts."""
    db = get_db_connection()
    if not db:
        print("❌ Gagal terhubung ke database. Keluar.")
        sys.exit(1)

    print("✅ Berhasil terhubung ke database.")

    try:
        # --- 1. Ubah Skema Tabel fuzzy_rules ---
        # Tambahkan kolom stock_code untuk mengaitkan aturan dengan saham
        schema_update = [
            "ALTER TABLE fuzzy_rules ADD COLUMN stock_code VARCHAR(10) NULL"
        ]
        print("🔄 Memperbarui skema tabel fuzzy_rules (menambah kolom stock_code)...")
        if execute_commands(db, schema_update):
            print("✅ Skema tabel berhasil diperbarui.")

        # --- 2. Hapus Aturan Lama dan Masukkan 36 Aturan Baru ---
        # Data ini diambil langsung dari tabel evaluasi yang Anda berikan
        rules_update = [
            "DELETE FROM fuzzy_rules",
            
            # Rules untuk BBCA
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBCA_R1', 'BBCA', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk', 40.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBCA_R2', 'BBCA', 'Sedang', 'Tinggi', 'Tinggi', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBCA_R3', 'BBCA', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBCA_R4', 'BBCA', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBCA_R5', 'BBCA', 'Tinggi', 'Sedang', 'Sedang', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBCA_R6', 'BBCA', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk', 26.6667)",
            
            # Rules untuk BBRI
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBRI_R1', 'BBRI', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk', 40.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBRI_R2', 'BBRI', 'Sedang', 'Tinggi', 'Tinggi', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBRI_R3', 'BBRI', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBRI_R4', 'BBRI', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBRI_R5', 'BBRI', 'Tinggi', 'Sedang', 'Sedang', 'High_Risk', 92.5)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('BBRI_R6', 'BBRI', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk', 40.0)",
            
            # Rules untuk TLKM
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('TLKM_R1', 'TLKM', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk', 40.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('TLKM_R2', 'TLKM', 'Sedang', 'Tinggi', 'Tinggi', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('TLKM_R3', 'TLKM', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('TLKM_R4', 'TLKM', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('TLKM_R5', 'TLKM', 'Tinggi', 'Sedang', 'Sedang', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('TLKM_R6', 'TLKM', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk', 40.0)",
            
            # Rules untuk ASII
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ASII_R1', 'ASII', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk', 40.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ASII_R2', 'ASII', 'Sedang', 'Tinggi', 'Tinggi', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ASII_R3', 'ASII', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ASII_R4', 'ASII', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ASII_R5', 'ASII', 'Tinggi', 'Sedang', 'Sedang', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ASII_R6', 'ASII', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk', 40.0)",
            
            # Rules untuk UNVR
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('UNVR_R1', 'UNVR', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk', 40.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('UNVR_R2', 'UNVR', 'Sedang', 'Tinggi', 'Tinggi', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('UNVR_R3', 'UNVR', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('UNVR_R4', 'UNVR', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('UNVR_R5', 'UNVR', 'Tinggi', 'Sedang', 'Sedang', 'High_Risk', 95.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('UNVR_R6', 'UNVR', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk', 40.0)",
            
            # Rules untuk ICBP
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ICBP_R1', 'ICBP', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk', 40.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ICBP_R2', 'ICBP', 'Sedang', 'Tinggi', 'Tinggi', 'Medium_Risk', 70.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ICBP_R3', 'ICBP', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk', 55.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ICBP_R4', 'ICBP', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ICBP_R5', 'ICBP', 'Tinggi', 'Sedang', 'Sedang', 'High_Risk', 100.0)",
            "INSERT INTO fuzzy_rules (rule_name, stock_code, volatilitas_set, volume_set, frekuensi_set, output_set, z_value) VALUES ('ICBP_R6', 'ICBP', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk', 40.0)"
        ]
        print("🔄 Memperbarui fuzzy rules dengan 36 aturan spesifik per saham...")
        if execute_commands(db, rules_update):
            print("✅ Fuzzy rules berhasil diperbarui.")
        
        print("\n🎉 Pembaruan aturan fuzzy selesai dengan sukses!")

    except Exception as e:
        print(f"\n❌ Terjadi error selama pembaruan: {e}")
    finally:
        db.disconnect()
        print("🔌 Koneksi database ditutup.")

if __name__ == "__main__":
    run_update()