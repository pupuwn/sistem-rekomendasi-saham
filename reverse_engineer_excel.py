"""
Script untuk reverse-engineer konfigurasi fuzzy sets Excel
Berdasarkan nilai membership yang diketahui
"""

# DARI EXCEL UNVR (volatilitas = 35):
# mu_rendah = 0.8333
# mu_sedang = 0.16667

# Untuk trapezoid membership function:
# mu = (x - a) / (b - a)  [slope naik]
# mu = 1.0  [plateau]
# mu = (d - x) / (d - c)  [slope turun]

volatilitas = 35.0
mu_rendah = 0.8333
mu_sedang = 0.16667

print("=" * 80)
print("REVERSE ENGINEERING FUZZY SETS EXCEL - VOLATILITAS")
print("=" * 80)
print(f"\nData yang diketahui:")
print(f"  Volatilitas = {volatilitas}")
print(f"  mu_rendah = {mu_rendah}")
print(f"  mu_sedang = {mu_sedang}")

print("\n" + "=" * 80)
print("ANALISIS RENDAH:")
print("=" * 80)

# Untuk Rendah dengan mu = 0.8333
# Kemungkinan 1: Slope turun (c < x <= d)
# mu = (d - x) / (d - c)
# 0.8333 = (d - 35) / (d - c)

# Coba berbagai kombinasi
# Jika Rendah: [0, 0, 30, 60]
# mu = (60 - 35) / (60 - 30) = 25/30 = 0.8333 ✓

a_rendah, b_rendah, c_rendah, d_rendah = 0, 0, 30, 60
if c_rendah < volatilitas <= d_rendah:
    mu_calc = (d_rendah - volatilitas) / (d_rendah - c_rendah)
    print(f"\nRendah: [{a_rendah}, {b_rendah}, {c_rendah}, {d_rendah}]")
    print(f"Karena {volatilitas} berada di ({c_rendah}, {d_rendah}], slope turun:")
    print(f"mu = ({d_rendah} - {volatilitas}) / ({d_rendah} - {c_rendah})")
    print(f"mu = {mu_calc:.6f}")
    print(f"Expected: {mu_rendah}")
    print(f"Match: {abs(mu_calc - mu_rendah) < 0.001}")

print("\n" + "=" * 80)
print("ANALISIS SEDANG:")
print("=" * 80)

# Untuk Sedang dengan mu = 0.16667
# Kemungkinan: Slope naik (a <= x < b)
# mu = (x - a) / (b - a)
# 0.16667 = (35 - a) / (b - a)

# Coba berbagai kombinasi
# Jika Sedang: [30, 60, 90, 120]
# Untuk x=35, berada di [30, 60] (slope naik)
# mu = (35 - 30) / (60 - 30) = 5/30 = 0.16667 ✓

a_sedang, b_sedang, c_sedang, d_sedang = 30, 60, 90, 120
if a_sedang <= volatilitas < b_sedang:
    mu_calc = (volatilitas - a_sedang) / (b_sedang - a_sedang)
    print(f"\nSedang: [{a_sedang}, {b_sedang}, {c_sedang}, {d_sedang}]")
    print(f"Karena {volatilitas} berada di [{a_sedang}, {b_sedang}), slope naik:")
    print(f"mu = ({volatilitas} - {a_sedang}) / ({b_sedang} - {a_sedang})")
    print(f"mu = {mu_calc:.6f}")
    print(f"Expected: {mu_sedang}")
    print(f"Match: {abs(mu_calc - mu_sedang) < 0.001}")

print("\n" + "=" * 80)
print("KONFIGURASI FUZZY SETS EXCEL (VOLATILITAS):")
print("=" * 80)
print(f"  Rendah: [{a_rendah}, {b_rendah}, {c_rendah}, {d_rendah}]")
print(f"  Sedang: [{a_sedang}, {b_sedang}, {c_sedang}, {d_sedang}]")
print(f"  Tinggi: [90, 150, 300, 300] (asumsi)")

print("\n" + "=" * 80)
print("BANDINGKAN DENGAN SISTEM SAAT INI:")
print("=" * 80)
print("  Rendah: [-50, -20, 30, 60]")
print("  Sedang: [20, 60, 90, 120]")
print("  Tinggi: [90, 150, 300, 300]")

print("\n" + "=" * 80)
print("PERBEDAAN UTAMA:")
print("=" * 80)
print("  1. Excel Rendah: [0, 0, 30, 60] (segitiga)")
print("     Sistem Rendah: [-50, -20, 30, 60] (trapezoid)")
print("")
print("  2. Excel Sedang: [30, 60, 90, 120]")
print("     Sistem Sedang: [20, 60, 90, 120]")
print("")
print("  Untuk volatilitas=35:")
print("  - Excel: mu_sedang = (35-30)/(60-30) = 0.16667")
print("  - Sistem: mu_sedang = (35-20)/(60-20) = 0.375")
print("=" * 80)

# Verifikasi dengan sistem saat ini
print("\n" + "=" * 80)
print("VERIFIKASI DENGAN KONFIGURASI SISTEM:")
print("=" * 80)

# Sistem: Sedang [20, 60, 90, 120]
a_sys, b_sys, c_sys, d_sys = 20, 60, 90, 120
if a_sys <= volatilitas < b_sys:
    mu_sys = (volatilitas - a_sys) / (b_sys - a_sys)
    print(f"Sistem Sedang: [{a_sys}, {b_sys}, {c_sys}, {d_sys}]")
    print(f"mu_sedang = ({volatilitas} - {a_sys}) / ({b_sys} - {a_sys})")
    print(f"mu_sedang = {mu_sys:.6f}")
    print(f"Ini sesuai dengan hasil debug sebelumnya: 0.375")
