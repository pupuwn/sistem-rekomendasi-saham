"""
Script untuk debug perhitungan UNVR
Membandingkan hasil sistem dengan Excel
"""

import sys
sys.path.append('c:\\laragon\\www\\tsukamoto')

from db_connect import get_db_connection
from models.fuzzification import FuzzificationEngine
from models.inference import InferenceEngine
from models.defuzzification import DefuzzificationEngine

# Data UNVR dari user
UNVR_DATA = {
    'stock_code': 'UNVR',
    'stock_name': 'Unilever Indonesia Tbk',
    'selisih': 35.0,  # Volatilitas
    'volume': 50952000.0,
    'frekuensi': 9231.0
}

print("=" * 80)
print("DEBUG PERHITUNGAN FUZZY TSUKAMOTO - UNVR")
print("=" * 80)
print(f"\nData Input:")
print(f"  Kode Saham    : {UNVR_DATA['stock_code']}")
print(f"  Nama Saham    : {UNVR_DATA['stock_name']}")
print(f"  Volatilitas   : {UNVR_DATA['selisih']}")
print(f"  Volume        : {UNVR_DATA['volume']:,.0f}")
print(f"  Frekuensi     : {UNVR_DATA['frekuensi']:,.0f}")

# Koneksi database
db = get_db_connection()
if not db:
    print("ERROR: Tidak bisa koneksi ke database!")
    sys.exit(1)

# Ambil konfigurasi fuzzy sets
def get_fuzzy_sets_config(db):
    config = {}
    variables = db.fetch_all("SELECT id, variable_name FROM fuzzy_variables")
    
    for var in variables:
        fuzzy_sets = db.fetch_all(
            "SELECT * FROM fuzzy_sets WHERE variable_id = %s",
            (var['id'],)
        )
        cleaned_sets = []
        for fs in fuzzy_sets:
            fs['min_value'] = float(fs['min_value'])
            fs['max_value'] = float(fs['max_value'])
            fs['peak_start'] = float(fs['peak_start'])
            fs['peak_end'] = float(fs['peak_end'])
            cleaned_sets.append(fs)
        config[var['variable_name']] = cleaned_sets
    
    return config

def get_output_sets_config(db):
    output_sets = db.fetch_all("SELECT * FROM fuzzy_output_sets")
    config = {}
    for item in output_sets:
        config[item['set_name']] = {
            'min_value': float(item['min_value']),
            'max_value': float(item['max_value'])
        }
    return config

fuzzy_sets_config = get_fuzzy_sets_config(db)
output_sets_config = get_output_sets_config(db)
rules = db.fetch_all("SELECT * FROM fuzzy_rules")

print("\n" + "=" * 80)
print("STEP 1: FUZZIFIKASI")
print("=" * 80)

# Inisialisasi engine
fuzz_engine = FuzzificationEngine()
fuzzy_inputs = fuzz_engine.fuzzify_all_inputs(
    UNVR_DATA['selisih'], 
    UNVR_DATA['volume'], 
    UNVR_DATA['frekuensi'], 
    fuzzy_sets_config
)

print("\nHasil Fuzzifikasi:")
for var_name, memberships in fuzzy_inputs.items():
    print(f"\n{var_name}:")
    for set_name, mu_value in memberships.items():
        bar = "#" * int(mu_value * 40)
        print(f"  {set_name:10} : mu = {mu_value:.4f}  {bar}")

print("\n" + "=" * 80)
print("STEP 2: INFERENSI")
print("=" * 80)

inference_engine = InferenceEngine(rules, output_sets_config)
inference_results = inference_engine.evaluate_all_rules(fuzzy_inputs)

# Filter hanya rules yang aktif
active_rules = [r for r in inference_results if r['alpha'] > 0]

print(f"\nTotal Rules di Database: {len(rules)}")
print(f"Rules yang Aktif (alpha > 0): {len(active_rules)}")

if active_rules:
    print("\nDetail Rules Aktif:")
    print(f"{'No':<4} {'Rule Name':<20} {'Alpha':<10} {'Z':<10} {'Output Set':<15}")
    print("-" * 80)
    for i, res in enumerate(active_rules, 1):
        print(f"{i:<4} {res['rule_name']:<20} {res['alpha']:<10.4f} {res['z']:<10.2f} {res['output_set']:<15}")
    
    # Tampilkan perhitungan detail
    print("\nPerhitungan Detail Weighted Average:")
    print(f"{'No':<4} {'Rule':<20} {'Alpha (ai)':<12} {'Z (zi)':<12} {'ai * zi':<15}")
    print("-" * 80)
    
    total_alpha = 0
    total_weighted = 0
    
    for i, res in enumerate(active_rules, 1):
        alpha_val = float(res['alpha'])
        z_val = float(res['z'])
        weighted = alpha_val * z_val
        
        total_alpha += alpha_val
        total_weighted += weighted
        
        print(f"{i:<4} {res['rule_name']:<20} {alpha_val:<12.4f} {z_val:<12.2f} {weighted:<15.2f}")
    
    print("-" * 80)
    print(f"{'TOTAL':<24} {total_alpha:<12.4f} {'':<12} {total_weighted:<15.2f}")
    
    # Defuzzifikasi
    defuzz_engine = DefuzzificationEngine()
    final_score = defuzz_engine.weighted_average(inference_results)
    risk_category = defuzz_engine.get_risk_category(final_score)
    
    print("\n" + "=" * 80)
    print("STEP 3: DEFUZZIFIKASI")
    print("=" * 80)
    
    print(f"\nFormula: Z* = (Sum ai * zi) / (Sum ai)")
    print(f"       Z* = {total_weighted:.2f} / {total_alpha:.4f}")
    print(f"       Z* = {final_score:.6f}")
    
    print(f"\n{'='*80}")
    print(f"HASIL AKHIR SISTEM:")
    print(f"{'='*80}")
    print(f"  Skor Akhir      : {final_score:.6f}")
    print(f"  Kategori Risiko : {risk_category}")
    
    print(f"\n{'='*80}")
    print(f"PERBANDINGAN DENGAN EXCEL:")
    print(f"{'='*80}")
    print(f"  Excel Skor      : 67.06592")
    print(f"  Excel Kategori  : Medium Risk")
    print(f"  Sistem Skor     : {final_score:.6f}")
    print(f"  Sistem Kategori : {risk_category}")
    print(f"  Selisih         : {abs(67.06592 - final_score):.6f}")
    
    # Threshold kategori
    print(f"\n{'='*80}")
    print(f"THRESHOLD KATEGORI RISIKO:")
    print(f"{'='*80}")
    print(f"  Low Risk    : >= 70")
    print(f"  Medium Risk : 40 - 69.99")
    print(f"  High Risk   : < 40")
    
    if final_score < 70 and final_score >= 69:
        print(f"\nCATATAN: Skor {final_score:.2f} sangat dekat dengan batas Low Risk (70).")
        print(f"         Hanya selisih {70 - final_score:.2f} dari kategori Low Risk.")
    
else:
    print("\nTIDAK ADA RULES YANG AKTIF!")

# Tampilkan konfigurasi output sets
print(f"\n{'='*80}")
print(f"KONFIGURASI OUTPUT SETS:")
print(f"{'='*80}")
for set_name, config in output_sets_config.items():
    print(f"{set_name:15} : [{config['min_value']:.2f}, {config['max_value']:.2f}]")

db.disconnect()
print("\n" + "=" * 80)
