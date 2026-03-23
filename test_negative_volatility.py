"""
Script untuk testing fuzzification dengan nilai negatif
Memverifikasi bahwa nilai volatilitas -15 sekarang menghasilkan derajat keanggotaan > 0
"""

import sys
sys.path.append('c:\\laragon\\www\\tsukamoto')

from models.fuzzification import FuzzificationEngine

# Konfigurasi Fuzzy Sets untuk Volatilitas (setelah update)
fuzzy_sets_volatilitas = [
    {
        'set_name': 'Rendah',
        'min_value': -50.0,
        'max_value': 60.0,
        'peak_start': -20.0,
        'peak_end': 30.0
    },
    {
        'set_name': 'Sedang',
        'min_value': 20.0,
        'max_value': 120.0,
        'peak_start': 60.0,
        'peak_end': 90.0
    },
    {
        'set_name': 'Tinggi',
        'min_value': 90.0,
        'max_value': 300.0,
        'peak_start': 150.0,
        'peak_end': 300.0
    }
]

# Test dengan nilai -15
fuzz_engine = FuzzificationEngine()
volatilitas_value = -15

print("=" * 60)
print("TESTING FUZZIFICATION UNTUK VOLATILITAS = -15")
print("=" * 60)
print(f"\nNilai Input: {volatilitas_value}")
print("\nFuzzy Sets Configuration:")
for fs in fuzzy_sets_volatilitas:
    print(f"  {fs['set_name']:10} : [{fs['min_value']:6}, {fs['peak_start']:6}, {fs['peak_end']:6}, {fs['max_value']:6}]")

print("\n" + "-" * 60)
print("HASIL FUZZIFICATION:")
print("-" * 60)

result = fuzz_engine.fuzzify_value(volatilitas_value, fuzzy_sets_volatilitas)

for set_name, membership_value in result.items():
    bar = "#" * int(membership_value * 30)
    print(f"{set_name:10} : mu = {membership_value:.4f} {bar}")

print("\n" + "=" * 60)

# Penjelasan
print("\nPENJELASAN:")
print("-" * 60)
if result['Rendah'] > 0:
    print("BERHASIL! Nilai -15 menghasilkan derajat keanggotaan > 0")
    print(f"   Nilai -15 masuk kategori 'Rendah' dengan mu = {result['Rendah']:.4f}")
    print("   Ini berarti sistem sekarang dapat menghitung skor fuzzy.")
else:
    print("GAGAL! Nilai -15 masih menghasilkan derajat keanggotaan = 0")
    print("   Perlu update range fuzzy sets lagi.")

# Hitung dengan trapezoid untuk Rendah (-50, -20, 30, 60)
# Untuk x = -15:
# x berada di range [-50, -20] (slope naik)
# μ = (x - a) / (b - a) = (-15 - (-50)) / (-20 - (-50)) = 35 / 30 = 1.167 (> 1, jadi di-cap ke 1)
# ATAU x berada di range [-20, 30] (plateau/flat) = 1.0
# Seharusnya μ ≈ 1.0 atau mendekati 1.0

print("\nEXPECTED:")
print("-" * 60)
a, b, c, d = -50, -20, 30, 60
x = -15
if a <= x < b:
    expected_mu = (x - a) / (b - a)
    print(f"Karena {x} berada di [{a}, {b}), slope naik:")
    print(f"mu = ({x} - {a}) / ({b} - {a}) = {expected_mu:.4f}")
elif b <= x <= c:
    expected_mu = 1.0
    print(f"Karena {x} berada di [{b}, {c}], pada puncak trapezoid:")
    print(f"mu = 1.0")
elif c < x <= d:
    expected_mu = (d - x) / (d - c)
    print(f"Karena {x} berada di ({c}, {d}], slope turun:")
    print(f"mu = ({d} - {x}) / ({d} - {c}) = {expected_mu:.4f}")
else:
    expected_mu = 0.0
    print(f"Karena {x} di luar range [{a}, {d}]:")
    print(f"mu = 0.0")

print(f"\nNilai yang diharapkan: mu = {expected_mu:.4f}")
print("=" * 60)
