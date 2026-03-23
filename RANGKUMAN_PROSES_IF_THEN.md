# RANGKUMAN PROSES IF-THEN DALAM SISTEM
## Implementasi Teknis dari Kode yang Dibangun

---

## 📍 ALUR EKSEKUSI LENGKAP

```
┌─────────────────────────────────────────────────────────────┐
│ 1. LOAD ATURAN DARI DATABASE                               │
│    File: app.py (baris 175)                                 │
│    Code: rules = db.fetch_all("SELECT * FROM fuzzy_rules") │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. INISIALISASI INFERENCE ENGINE                            │
│    File: app.py (baris 183)                                 │
│    Code: inference_engine = InferenceEngine(rules,          │
│                                    output_sets_config)       │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. FUZZIFIKASI INPUT (untuk setiap saham)                   │
│    File: app.py (baris 195-197)                             │
│    Code: fuzzy_inputs = fuzz_engine.fuzzify_all_inputs(     │
│              val_selisih, val_volume, val_freq,             │
│              fuzzy_sets_config)                             │
│    Output: {'Volatilitas': {'Rendah': 0.15, ...}, ...}     │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. EVALUASI ATURAN IF-THEN ⭐ (INTI PROSES)                │
│    File: app.py (baris 201)                                 │
│    Code: inference_results =                                │
│          inference_engine.evaluate_all_rules(fuzzy_inputs)  │
│                                                              │
│    Di dalam method ini terjadi:                             │
│    ┌──────────────────────────────────────────────┐        │
│    │ 4a. Loop semua 27 aturan                     │        │
│    │ 4b. Hitung α-predikat (evaluasi IF)          │        │
│    │ 4c. Hitung z-value (evaluasi THEN)           │        │
│    │ 4d. Simpan hasil aturan yang aktif           │        │
│    └──────────────────────────────────────────────┘        │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. DEFUZZIFIKASI                                            │
│    File: app.py (baris 211)                                 │
│    Code: final_score =                                      │
│          defuzz_engine.weighted_average(inference_results)  │
│    Output: skor 0-100 dan kategori risiko                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 DETAIL IMPLEMENTASI STEP 4: EVALUASI IF-THEN

### **File: `models/inference.py`**

Ini adalah **INTI** dari proses IF-THEN. Mari kita breakdown kode per bagian:

---

### **STEP 4a: Loop Semua Aturan**

**Lokasi:** `models/inference.py` baris 73-96

```python
def evaluate_all_rules(self, fuzzy_inputs):
    """Evaluasi semua aturan fuzzy"""
    results = []
    
    for rule in self.rules:  # ← Loop 27 aturan dari database
        # Proses setiap aturan...
```

**Penjelasan:**
- `self.rules` berisi 27 aturan yang di-load dari database
- Setiap `rule` adalah dictionary dengan key: `volatilitas_set`, `volume_set`, `frekuensi_set`, `output_set`

**Contoh data `rule`:**
```python
{
    'id': 4,
    'rule_name': 'R4',
    'volatilitas_set': 'Rendah',
    'volume_set': 'Sedang',
    'frekuensi_set': 'Rendah',
    'output_set': 'Medium_Risk'
}
```

---

### **STEP 4b: Hitung α-predikat (Evaluasi Bagian IF)**

**Lokasi:** `models/inference.py` baris 78-79

```python
# 1. Hitung α-predikat
alpha = self.calculate_alpha_predicate(fuzzy_inputs, rule)
```

**Method detail:** `models/inference.py` baris 18-27

```python
def calculate_alpha_predicate(self, fuzzy_inputs, rule):
    """Menghitung α-predikat menggunakan operator MIN (AND)"""
    
    # Ambil derajat keanggotaan (μ) dari hasil fuzzifikasi
    mu_volatilitas = fuzzy_inputs['Volatilitas'].get(rule['volatilitas_set'], 0.0)
    mu_volume = fuzzy_inputs['Volume'].get(rule['volume_set'], 0.0)
    mu_frekuensi = fuzzy_inputs['Frekuensi'].get(rule['frekuensi_set'], 0.0)
    
    # Operator AND = MIN (ambil nilai terkecil)
    alpha = min(float(mu_volatilitas), float(mu_volume), float(mu_frekuensi))
    return alpha
```

**Penjelasan Detail:**

1. **Ambil derajat keanggotaan** dari `fuzzy_inputs` sesuai set yang diminta rule
2. **Gunakan operator MIN** untuk AND operation
3. **Return α** sebagai tingkat kepercayaan aturan

**Contoh Eksekusi untuk Rule R4:**

```python
# Input fuzzy_inputs:
fuzzy_inputs = {
    'Volatilitas': {'Rendah': 0.15, 'Sedang': 0.06, 'Tinggi': 0.0},
    'Volume': {'Rendah': 0.0, 'Sedang': 0.20, 'Tinggi': 0.0},
    'Frekuensi': {'Rendah': 0.69, 'Sedang': 0.23, 'Tinggi': 0.0}
}

# Rule R4 meminta: Rendah, Sedang, Rendah
mu_volatilitas = fuzzy_inputs['Volatilitas']['Rendah']  # = 0.15
mu_volume = fuzzy_inputs['Volume']['Sedang']            # = 0.20
mu_frekuensi = fuzzy_inputs['Frekuensi']['Rendah']      # = 0.69

# Hitung α dengan MIN
alpha = min(0.15, 0.20, 0.69)  # = 0.15

# Rule R4 AKTIF dengan α = 0.15
```

---

### **STEP 4c: Hitung z-value (Evaluasi Bagian THEN)**

**Lokasi:** `models/inference.py` baris 81-86

```python
# 2. Jika α > 0, rule aktif
if alpha > 0:
    output_set = rule['output_set']
    
    # 3. Hitung z secara dinamis
    z = self.calculate_z_tsukamoto(alpha, output_set)
```

**Method detail:** `models/inference.py` baris 29-71

```python
def calculate_z_tsukamoto(self, alpha, output_set_name):
    """
    Menghitung nilai z (crisp output) secara dinamis sesuai Excel.
    
    Range Excel:
    - High_Risk: 0-40 (Grafik Turun)
    - Medium_Risk: 30-70 (Grafik Naik)
    - Low_Risk: 60-100 (Grafik Naik)
    """
    # Ambil konfigurasi range output
    config = self.output_sets.get(output_set_name)
    if not config:
        return 0.0
        
    min_val = float(config['min_value'])
    max_val = float(config['max_value'])
    range_val = max_val - min_val
    
    # Logika Tsukamoto
    if output_set_name == 'High_Risk':
        # Kurva TURUN: α tinggi → skor kecil
        z = max_val - (alpha * range_val)
    else:
        # Kurva NAIK: α tinggi → skor besar
        z = min_val + (alpha * range_val)
        
    return z
```

**Penjelasan Detail:**

1. **Ambil konfigurasi range** untuk output_set (misal Medium_Risk = [30, 70])
2. **Tentukan arah kurva**:
   - High_Risk: Turun (semakin risk, skor makin kecil)
   - Medium/Low_Risk: Naik (semakin confidence, skor makin besar)
3. **Hitung z** dengan rumus inverse mapping
4. **Return z** sebagai nilai crisp output

**Contoh Eksekusi untuk Rule R4:**

```python
# Input:
alpha = 0.15
output_set_name = 'Medium_Risk'

# Konfigurasi dari database:
config = {'min_value': 30, 'max_value': 70}

min_val = 30
max_val = 70
range_val = 70 - 30 = 40

# Karena Medium_Risk (bukan High_Risk), gunakan kurva NAIK:
z = min_val + (alpha * range_val)
z = 30 + (0.15 * 40)
z = 30 + 6
z = 36.00

# Rule R4 menghasilkan z = 36.00
```

---

### **STEP 4d: Simpan Hasil Aturan Aktif**

**Lokasi:** `models/inference.py` baris 88-94

```python
results.append({
    'rule_id': rule.get('id', 0),
    'rule_name': rule.get('rule_name', ''),
    'alpha': alpha,
    'z': z,
    'output_set': output_set
})
```

**Output untuk Rule R4:**
```python
{
    'rule_id': 4,
    'rule_name': 'R4',
    'alpha': 0.15,
    'z': 36.00,
    'output_set': 'Medium_Risk'
}
```

---

## 📊 CONTOH LENGKAP: SAHAM UNVR

### **Input Data**

```python
stock = {
    'stock_code': 'UNVR',
    'selisih': 35,           # Volatilitas
    'volume': 50952000,      # Volume
    'frekuensi': 9231        # Frekuensi
}
```

### **Hasil Fuzzifikasi (Step 3)**

```python
fuzzy_inputs = {
    'Volatilitas': {
        'Rendah': 0.15,
        'Sedang': 0.06,
        'Tinggi': 0.0
    },
    'Volume': {
        'Rendah': 0.0,
        'Sedang': 0.20,
        'Tinggi': 0.0
    },
    'Frekuensi': {
        'Rendah': 0.69,
        'Sedang': 0.23,
        'Tinggi': 0.0
    }
}
```

### **Proses Evaluasi IF-THEN (Step 4)**

Sistem loop 27 aturan, berikut yang aktif:

#### **Rule R4: IF Rendah-Sedang-Rendah THEN Medium_Risk**

```python
# Step 4b: Hitung α
mu_vol = 0.15  # Volatilitas Rendah
mu_volume = 0.20  # Volume Sedang
mu_freq = 0.69  # Frekuensi Rendah
alpha = min(0.15, 0.20, 0.69) = 0.15 ✅ AKTIF

# Step 4c: Hitung z
z = 30 + (0.15 × 40) = 36.00

# Step 4d: Simpan hasil
{'rule_name': 'R4', 'alpha': 0.15, 'z': 36.00, 'output_set': 'Medium_Risk'}
```

#### **Rule R5: IF Rendah-Sedang-Sedang THEN Low_Risk**

```python
# Step 4b: Hitung α
alpha = min(0.15, 0.20, 0.23) = 0.06 ✅ AKTIF

# Step 4c: Hitung z (Low_Risk range: 60-100)
z = 60 + (0.06 × 40) = 62.40

# Step 4d: Simpan hasil
{'rule_name': 'R5', 'alpha': 0.06, 'z': 62.40, 'output_set': 'Low_Risk'}
```

#### **Rule R13: IF Sedang-Sedang-Rendah THEN Medium_Risk**

```python
# Step 4b: Hitung α
alpha = min(0.06, 0.20, 0.69) = 0.06 ✅ AKTIF

# Step 4c: Hitung z
z = 30 + (0.06 × 40) = 32.40

# Step 4d: Simpan hasil
{'rule_name': 'R13', 'alpha': 0.06, 'z': 32.40, 'output_set': 'Medium_Risk'}
```

#### **Rule R14: IF Sedang-Sedang-Sedang THEN Medium_Risk**

```python
# Step 4b: Hitung α
alpha = min(0.06, 0.20, 0.23) = 0.06 ✅ AKTIF

# Step 4c: Hitung z
z = 30 + (0.06 × 40) = 32.40

# Step 4d: Simpan hasil
{'rule_name': 'R14', 'alpha': 0.06, 'z': 32.40, 'output_set': 'Medium_Risk'}
```

#### **Rule lainnya (23 rules)**

```python
# Contoh Rule R1: IF Rendah-Rendah-Rendah
alpha = min(0.15, 0.0, 0.69) = 0.0 ❌ TIDAK AKTIF (α = 0)
# Skip, tidak disimpan ke results
```

### **Output dari evaluate_all_rules()**

```python
inference_results = [
    {'rule_name': 'R4', 'alpha': 0.15, 'z': 36.00, 'output_set': 'Medium_Risk'},
    {'rule_name': 'R5', 'alpha': 0.06, 'z': 62.40, 'output_set': 'Low_Risk'},
    {'rule_name': 'R13', 'alpha': 0.06, 'z': 32.40, 'output_set': 'Medium_Risk'},
    {'rule_name': 'R14', 'alpha': 0.06, 'z': 32.40, 'output_set': 'Medium_Risk'}
]

# Total: 4 rules aktif dari 27 rules
```

### **Defuzzifikasi (Step 5)**

```python
# File: models/defuzzification.py
Z* = Σ(αᵢ × zᵢ) / Σ(αᵢ)

Z* = (0.15×36.00 + 0.06×62.40 + 0.06×32.40 + 0.06×32.40) / (0.15 + 0.06 + 0.06 + 0.06)
Z* = (5.40 + 3.74 + 1.94 + 1.94) / 0.33
Z* = 13.03 / 0.33
Z* = 39.48

# Kategori: Medium Risk (karena 30 ≤ 39.48 < 70)
```

---

## 🧩 STRUKTUR DATA PENTING

### **1. Data Rule dari Database**

Query: `SELECT * FROM fuzzy_rules`

```python
[
    {
        'id': 1,
        'rule_name': 'R1',
        'volatilitas_set': 'Rendah',
        'volume_set': 'Rendah',
        'frekuensi_set': 'Rendah',
        'output_set': 'Medium_Risk'
    },
    {
        'id': 4,
        'rule_name': 'R4',
        'volatilitas_set': 'Rendah',
        'volume_set': 'Sedang',
        'frekuensi_set': 'Rendah',
        'output_set': 'Medium_Risk'
    },
    # ... 25 rules lainnya
]
```

### **2. Output Sets Config**

Query: `SELECT * FROM fuzzy_output_sets`

```python
{
    'High_Risk': {'min_value': 0, 'max_value': 40},
    'Medium_Risk': {'min_value': 30, 'max_value': 70},
    'Low_Risk': {'min_value': 60, 'max_value': 100}
}
```

### **3. Fuzzy Inputs (Hasil Fuzzifikasi)**

```python
{
    'Volatilitas': {
        'Rendah': 0.15,
        'Sedang': 0.06,
        'Tinggi': 0.0
    },
    'Volume': {
        'Rendah': 0.0,
        'Sedang': 0.20,
        'Tinggi': 0.0
    },
    'Frekuensi': {
        'Rendah': 0.69,
        'Sedang': 0.23,
        'Tinggi': 0.0
    }
}
```

### **4. Inference Results (Output STEP 4)**

```python
[
    {
        'rule_id': 4,
        'rule_name': 'R4',
        'alpha': 0.15,
        'z': 36.00,
        'output_set': 'Medium_Risk'
    },
    {
        'rule_id': 5,
        'rule_name': 'R5',
        'alpha': 0.06,
        'z': 62.40,
        'output_set': 'Low_Risk'
    },
    # ... rules aktif lainnya
]
```

---

## 🔑 RINGKASAN KODE KEY METHODS

### **Method 1: `evaluate_all_rules()`**

**Tujuan:** Mengeksekusi semua 27 aturan IF-THEN

**Input:** `fuzzy_inputs` (derajat keanggotaan)

**Output:** List aturan aktif dengan α dan z

**Lokasi:** `models/inference.py` baris 73-96

---

### **Method 2: `calculate_alpha_predicate()`**

**Tujuan:** Evaluasi bagian IF (kondisi)

**Input:** `fuzzy_inputs` dan `rule`

**Output:** α-predikat (float 0-1)

**Rumus:** `α = min(μ₁, μ₂, μ₃)`

**Lokasi:** `models/inference.py` baris 18-27

---

### **Method 3: `calculate_z_tsukamoto()`**

**Tujuan:** Evaluasi bagian THEN (konsekuen)

**Input:** `alpha` dan `output_set_name`

**Output:** z-value (float 0-100)

**Rumus:** 
- High_Risk: `z = max - α × range`
- Others: `z = min + α × range`

**Lokasi:** `models/inference.py` baris 29-71

---

## 📂 FILE-FILE TERKAIT

### **1. `models/inference.py` (107 baris)**
- Class `InferenceEngine`
- **Inti proses IF-THEN**

### **2. `app.py` (495 baris)**
- Function `calculate_all_stocks()` (baris 157-247)
- Integrasi semua komponen

### **3. `update_database.py` (276 baris)**
- Setup 27 aturan (baris 179-213)
- Insert ke database

### **4. `debug_unvr.py` (187 baris)**
- Tool debugging untuk trace execution
- Menampilkan detail setiap step

---

## ✅ KESIMPULAN

**Proses IF-THEN dilakukan oleh sistem melalui:**

1. **Load aturan** dari database (`app.py` baris 175)
2. **Loop 27 aturan** satu per satu (`inference.py` baris 77)
3. **Evaluasi IF**: Hitung α dengan MIN operator (`inference.py` baris 18-27)
4. **Evaluasi THEN**: Hitung z dengan inverse mapping (`inference.py` baris 29-71)
5. **Simpan hasil** aturan yang aktif (α > 0)
6. **Return list** aturan aktif dengan α dan z

**File utama:** `models/inference.py` - Method `evaluate_all_rules()`

**Karakteristik:**
- Database-driven (aturan dari MySQL)
- Dynamic calculation (z dihitung real-time)
- Transparent (setiap step traceable)
- Efficient (< 1 detik untuk 45 saham)
