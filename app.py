import streamlit as st
import pandas as pd
import bcrypt
import traceback
from datetime import datetime
from db_connect import get_db_connection
from models.fuzzification import FuzzificationEngine
from models.inference import InferenceEngine
from models.defuzzification import DefuzzificationEngine

# ==========================================
# KONFIGURASI HALAMAN & CSS
# ==========================================
st.set_page_config(
    page_title="Fuzzy Tsukamoto - Rekomendasi Saham Low-Risk",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #31333F;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================
# Inisialisasi session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0  # Counter untuk reset form

# Auto-restore session dari query params (untuk persistent login)
try:
    query_params = st.query_params
    if not st.session_state.logged_in and 'session_user' in query_params:
        stored_username = query_params.get('session_user')
        stored_role = query_params.get('session_role', 'user')
        if stored_username:
            st.session_state.logged_in = True
            st.session_state.username = stored_username
            st.session_state.role = stored_role
except:
    pass

# ==========================================
# DATA ATURAN HARDCODED
# ==========================================
def get_hardcoded_rules():
    """
    Mengembalikan daftar 27 aturan Fuzzy Tsukamoto secara hardcoded.
    Ini menggantikan fungsi pengambilan data dari database untuk menjaga integritas logika.
    """
    return [
        # --- Aturan Volatilitas RENDAH ---
        {'id': 1, 'rule_name': 'R1', 'volatilitas_set': 'Rendah', 'volume_set': 'Rendah', 'frekuensi_set': 'Rendah', 'output_set': 'Medium_Risk'},
        {'id': 2, 'rule_name': 'R2', 'volatilitas_set': 'Rendah', 'volume_set': 'Rendah', 'frekuensi_set': 'Sedang', 'output_set': 'Medium_Risk'},
        {'id': 3, 'rule_name': 'R3', 'volatilitas_set': 'Rendah', 'volume_set': 'Rendah', 'frekuensi_set': 'Tinggi', 'output_set': 'Low_Risk'},
        {'id': 4, 'rule_name': 'R4', 'volatilitas_set': 'Rendah', 'volume_set': 'Sedang', 'frekuensi_set': 'Rendah', 'output_set': 'Medium_Risk'},
        {'id': 5, 'rule_name': 'R5', 'volatilitas_set': 'Rendah', 'volume_set': 'Sedang', 'frekuensi_set': 'Sedang', 'output_set': 'Low_Risk'},
        {'id': 6, 'rule_name': 'R6', 'volatilitas_set': 'Rendah', 'volume_set': 'Sedang', 'frekuensi_set': 'Tinggi', 'output_set': 'Low_Risk'},
        {'id': 7, 'rule_name': 'R7', 'volatilitas_set': 'Rendah', 'volume_set': 'Tinggi', 'frekuensi_set': 'Rendah', 'output_set': 'Low_Risk'},
        {'id': 8, 'rule_name': 'R8', 'volatilitas_set': 'Rendah', 'volume_set': 'Tinggi', 'frekuensi_set': 'Sedang', 'output_set': 'Low_Risk'},
        {'id': 9, 'rule_name': 'R9', 'volatilitas_set': 'Rendah', 'volume_set': 'Tinggi', 'frekuensi_set': 'Tinggi', 'output_set': 'Low_Risk'},

        # --- Aturan Volatilitas SEDANG ---
        {'id': 10, 'rule_name': 'R10', 'volatilitas_set': 'Sedang', 'volume_set': 'Rendah', 'frekuensi_set': 'Rendah', 'output_set': 'High_Risk'},
        {'id': 11, 'rule_name': 'R11', 'volatilitas_set': 'Sedang', 'volume_set': 'Rendah', 'frekuensi_set': 'Sedang', 'output_set': 'Medium_Risk'},
        {'id': 12, 'rule_name': 'R12', 'volatilitas_set': 'Sedang', 'volume_set': 'Rendah', 'frekuensi_set': 'Tinggi', 'output_set': 'Medium_Risk'},
        {'id': 13, 'rule_name': 'R13', 'volatilitas_set': 'Sedang', 'volume_set': 'Sedang', 'frekuensi_set': 'Rendah', 'output_set': 'Medium_Risk'},
        {'id': 14, 'rule_name': 'R14', 'volatilitas_set': 'Sedang', 'volume_set': 'Sedang', 'frekuensi_set': 'Sedang', 'output_set': 'Medium_Risk'},
        {'id': 15, 'rule_name': 'R15', 'volatilitas_set': 'Sedang', 'volume_set': 'Sedang', 'frekuensi_set': 'Tinggi', 'output_set': 'Low_Risk'},
        {'id': 16, 'rule_name': 'R16', 'volatilitas_set': 'Sedang', 'volume_set': 'Tinggi', 'frekuensi_set': 'Rendah', 'output_set': 'Medium_Risk'},
        {'id': 17, 'rule_name': 'R17', 'volatilitas_set': 'Sedang', 'volume_set': 'Tinggi', 'frekuensi_set': 'Sedang', 'output_set': 'Low_Risk'},
        {'id': 18, 'rule_name': 'R18', 'volatilitas_set': 'Sedang', 'volume_set': 'Tinggi', 'frekuensi_set': 'Tinggi', 'output_set': 'Low_Risk'},

        # --- Aturan Volatilitas TINGGI ---
        {'id': 19, 'rule_name': 'R19', 'volatilitas_set': 'Tinggi', 'volume_set': 'Rendah', 'frekuensi_set': 'Rendah', 'output_set': 'High_Risk'},
        {'id': 20, 'rule_name': 'R20', 'volatilitas_set': 'Tinggi', 'volume_set': 'Rendah', 'frekuensi_set': 'Sedang', 'output_set': 'High_Risk'},
        {'id': 21, 'rule_name': 'R21', 'volatilitas_set': 'Tinggi', 'volume_set': 'Rendah', 'frekuensi_set': 'Tinggi', 'output_set': 'Medium_Risk'},
        {'id': 22, 'rule_name': 'R22', 'volatilitas_set': 'Tinggi', 'volume_set': 'Sedang', 'frekuensi_set': 'Rendah', 'output_set': 'High_Risk'},
        {'id': 23, 'rule_name': 'R23', 'volatilitas_set': 'Tinggi', 'volume_set': 'Sedang', 'frekuensi_set': 'Sedang', 'output_set': 'Medium_Risk'},
        {'id': 24, 'rule_name': 'R24', 'volatilitas_set': 'Tinggi', 'volume_set': 'Sedang', 'frekuensi_set': 'Tinggi', 'output_set': 'Medium_Risk'},
        {'id': 25, 'rule_name': 'R25', 'volatilitas_set': 'Tinggi', 'volume_set': 'Tinggi', 'frekuensi_set': 'Rendah', 'output_set': 'Medium_Risk'},
        {'id': 26, 'rule_name': 'R26', 'volatilitas_set': 'Tinggi', 'volume_set': 'Tinggi', 'frekuensi_set': 'Sedang', 'output_set': 'Medium_Risk'},
        {'id': 27, 'rule_name': 'R27', 'volatilitas_set': 'Tinggi', 'volume_set': 'Tinggi', 'frekuensi_set': 'Tinggi', 'output_set': 'Low_Risk'},
    ]

# ==========================================
# FUNGSI HELPER & AUTENTIKASI
# ==========================================
def check_credentials(username, password):
    """Verifikasi username dan password"""
    db = get_db_connection()
    if not db:
        return False, None
    
    query = "SELECT password, role FROM users WHERE username = %s"
    result = db.fetch_one(query, (username,))
    db.disconnect()
    
    if result:
        # Note: Dalam produksi, password harus di-hash. 
        # Untuk demo ini kita anggap password di DB sudah hash bcrypt atau plain text (tergantung setup awal)
        try:
            stored_hash = result['password'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return True, result.get('role', 'user')
        except:
            # Fallback jika password di DB masih plain text (untuk development)
            if result['password'] == password:
                return True, result.get('role', 'user')
                
    return False, None

def is_admin():
    return st.session_state.get('role') == 'admin'

def require_admin():
    if not is_admin():
        st.error("⛔ Akses ditolak! Halaman ini hanya untuk Admin.")
        st.info("💡 Anda login sebagai User biasa.")
        st.stop()

def get_fuzzy_sets_config(db):
    """Mengambil konfigurasi fuzzy sets dari database dengan konversi float"""
    config = {}
    variables = db.fetch_all("SELECT id, variable_name FROM fuzzy_variables")
    
    for var in variables:
        fuzzy_sets = db.fetch_all(
            "SELECT * FROM fuzzy_sets WHERE variable_id = %s",
            (var['id'],)
        )
        # Pastikan nilai numerik dikonversi ke float
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
    """Mengambil konfigurasi output fuzzy sets dari database dengan konversi float"""
    output_sets = db.fetch_all("SELECT * FROM fuzzy_output_sets")
    
    config = {}
    for item in output_sets:
        # PENTING: Konversi Decimal ke Float agar Engine tidak error
        config[item['set_name']] = {
            'min_value': float(item['min_value']),
            'max_value': float(item['max_value'])
        }
    
    return config

def calculate_all_stocks(db):
    """Fungsi UTAMA: Menghitung Fuzzy Tsukamoto untuk semua saham"""
    try:
        # 1. Ambil data saham
        stocks = db.fetch_all("SELECT * FROM stock_data")
        if not stocks:
            st.warning("⚠️ Tidak ada data saham untuk diproses!")
            return
        
        # 2. Persiapan Data Configuration (Sekali saja di luar loop)
        print("\n" + "="*60)
        print("🚀 MEMULAI PROSES PERHITUNGAN FUZZY TSUKAMOTO")
        print("="*60)
        
        fuzzy_sets_config = get_fuzzy_sets_config(db)
        output_sets_config = get_output_sets_config(db) # Return format: {'Low_Risk': {'min':70.0, ...}}
        
        # 3. Ambil Rules (HARDCODED RULES)
        # rules = db.fetch_all("SELECT * FROM fuzzy_rules")  <-- KODE LAMA (DATABASE)
        rules = get_hardcoded_rules()  # <-- KODE BARU (HARDCODED)
        
        if not rules:
            st.error("❌ Error: Tidak ada aturan fuzzy yang dimuat.")
            return

        # 4. Inisialisasi Engine
        fuzz_engine = FuzzificationEngine()
        inference_engine = InferenceEngine(rules, output_sets_config)
        defuzz_engine = DefuzzificationEngine()
        
        # 5. Reset Hasil Lama
        db.execute_query("DELETE FROM calculation_results")
        insert_query = "INSERT INTO calculation_results (stock_id, final_score, risk_category) VALUES (%s, %s, %s)"
        
        # 6. Loop Proses Setiap Saham
        success_count = 0
        
        for stock in stocks:
            print(f"\n🏷️  SAHAM: {stock['stock_code']} ({stock['stock_name']})")
            print("-" * 50)
            
            # --- STEP 1: FUZZIFIKASI ---
            # Pastikan input float
            val_selisih = float(stock['selisih'])
            val_volume = float(stock['volume'])
            val_freq = float(stock['frekuensi'])
            
            fuzzy_inputs = fuzz_engine.fuzzify_all_inputs(
                val_selisih, val_volume, val_freq, fuzzy_sets_config
            )
            
            print(f"   Input: Selisih={val_selisih}, Vol={val_volume}, Freq={val_freq}")
            
            # --- STEP 2: INFERENSI ---
            inference_results = inference_engine.evaluate_all_rules(fuzzy_inputs)
            
            # Debugging Rules yang aktif
            active_rules = [r for r in inference_results if r['alpha'] > 0]
            if active_rules:
                print(f"   ✅ {len(active_rules)} Aturan Aktif:")
                for res in active_rules:
                    a_val = float(res['alpha'])
                    z_val = float(res['z'])
                    print(f"      - {res['rule_name']}: α={a_val:.3f}, z={z_val:.2f}, Output={res['output_set']}")
            else:
                print("   ⚠️ Tidak ada aturan yang aktif (Skor 0)")

            # --- STEP 3: DEFUZZIFIKASI ---
            if inference_results:
                final_score = defuzz_engine.weighted_average(inference_results)
                risk_category = defuzz_engine.get_risk_category(final_score)
            else:
                final_score = 0.0
                risk_category = "High Risk"
            
            print(f"   🎯 HASIL: Skor={final_score:.2f} -> {risk_category}")
            
            # Simpan ke Database
            db.execute_query(insert_query, (stock['id'], final_score, risk_category))
            success_count += 1
            
        print("\n" + "="*60)
        print(f"✅ SELESAI. Berhasil memproses {success_count} saham.")
        print("="*60)
        
        st.success(f"✅ Berhasil menghitung {success_count} data saham! Cek tab 'Proses & Hasil'.")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Terjadi Error: {str(e)}")
        print("❌ ERROR TRACEBACK:")
        print(traceback.format_exc())

# ==========================================
# HALAMAN - HALAMAN
# ==========================================
def login_page():
    st.markdown('<div class="main-header">🔐 SISTEM REKOMENDASI SAHAM LOW-RISK</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Login Admin")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Masuk", use_container_width=True)
            
            if submit:
                if username and password:
                    is_valid, user_role = check_credentials(username, password)
                    if is_valid:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = user_role
                        # Set query params untuk persistent login
                        st.query_params['session_user'] = username
                        st.query_params['session_role'] = user_role
                        st.rerun()
                    else:
                        st.error("❌ Username atau password salah!")
                else:
                    st.warning("⚠️ Mohon isi username dan password!")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = 'dashboard'
    # Clear query params
    st.query_params.clear()
    st.rerun()

def show_dashboard():
    st.markdown('<div class="main-header">DASHBOARD</div>', unsafe_allow_html=True)
    db = get_db_connection()
    if not db: return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Total Saham", db.fetch_one("SELECT COUNT(*) as c FROM stock_data")['c'])
    with col2:
        # Menampilkan info rules (sekarang hardcoded 27)
        st.metric("⚙️ Total Rules", len(get_hardcoded_rules()))
    with col3:
        st.metric("📋 Variabel", db.fetch_one("SELECT COUNT(*) as c FROM fuzzy_variables")['c'])
    with col4:
        st.metric("🧮 Hasil Hitung", db.fetch_one("SELECT COUNT(*) as c FROM calculation_results")['c'])
    
    st.markdown("---")
    st.subheader("🕒 10 Hasil Terakhir")
    query = """
    SELECT sd.stock_code, sd.stock_name, cr.final_score, cr.risk_category, cr.calculation_date
    FROM calculation_results cr JOIN stock_data sd ON cr.stock_id = sd.id
    ORDER BY cr.calculation_date DESC LIMIT 10
    """
    results = db.fetch_all(query)
    if results:
        df = pd.DataFrame(results)
        df['final_score'] = df['final_score'].astype(float).round(2) # Format float
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada data perhitungan.")
    db.disconnect()

def show_variables_management():
    require_admin()
    st.markdown('<div class="main-header">📊 MANAJEMEN VARIABEL</div>', unsafe_allow_html=True)
    db = get_db_connection()
    if not db: return

    vars = db.fetch_all("SELECT * FROM fuzzy_variables")
    for var in vars:
        with st.expander(f"📌 {var['variable_name']} (Range: {float(var['min_value']):,.0f} - {float(var['max_value']):,.0f})"):
            sets = db.fetch_all("SELECT * FROM fuzzy_sets WHERE variable_id=%s ORDER BY min_value", (var['id'],))
            if sets:
                df = pd.DataFrame(sets)
                # Format float columns
                cols = ['min_value', 'max_value', 'peak_start', 'peak_end']
                for c in cols: df[c] = df[c].astype(float)
                st.dataframe(df[['set_name'] + cols], hide_index=True, use_container_width=True)
    db.disconnect()

def show_rules_management():
    require_admin()
    st.markdown('<div class="main-header">⚙️ MANAJEMEN ATURAN</div>', unsafe_allow_html=True)

    # Menampilkan aturan hardcoded
    rules = get_hardcoded_rules()
    df = pd.DataFrame(rules)
    st.dataframe(df, use_container_width=True, hide_index=True)

def show_stocks_management():
    st.markdown('<div class="main-header">💹 MANAJEMEN SAHAM</div>', unsafe_allow_html=True)
    db = get_db_connection()
    if not db: return
    
    tab1, tab2 = st.tabs(["List Data", "Tambah Data"])
    with tab1:
        stocks = db.fetch_all("SELECT * FROM stock_data ORDER BY input_date DESC")
        if stocks:
            df = pd.DataFrame(stocks)
            # Format angka besar
            df['volume'] = df['volume'].astype(float).apply(lambda x: f"{x:,.0f}")
            df['frekuensi'] = df['frekuensi'].astype(float).apply(lambda x: f"{x:,.0f}")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if st.button("🗑️ Hapus Semua Data Saham"):
                db.execute_query("DELETE FROM stock_data")
                st.success("Semua data saham dihapus.")
                st.rerun()
                
    with tab2:
        # Gunakan key yang unik untuk reset form setelah submit
        form_key = f"add_stock_{st.session_state.form_key}"
        with st.form(form_key):
        # Gunakan key yang unik untuk reset form setelah submit
        form_key = f"add_stock_{st.session_state.form_key}"
        with st.form(form_key):
            code = st.text_input("Kode Saham (Contoh: BBCA)")
            name = st.text_input("Nama Saham")
            selisih = st.number_input("Volatilitas (Selisih)")
            selisih = st.number_input("Volatilitas (Selisih)")
            volume = st.number_input("Volume", min_value=0.0, step=1000.0)
            freq = st.number_input("Frekuensi", min_value=0.0, step=100.0)
            if st.form_submit_button("Simpan"):
                if code and name:  # Validasi input minimal
                    db.execute_query(
                        "INSERT INTO stock_data (stock_code, stock_name, selisih, volume, frekuensi, input_date) VALUES (%s,%s,%s,%s,%s, NOW())",
                        (code, name, selisih, volume, freq)
                    )
                    st.success("✅ Data tersimpan!")
                    # Increment form key untuk reset form
                    st.session_state.form_key += 1
                    st.rerun()
                else:
                    st.error("❌ Kode Saham dan Nama Saham harus diisi!")
                if code and name:  # Validasi input minimal
                    db.execute_query(
                        "INSERT INTO stock_data (stock_code, stock_name, selisih, volume, frekuensi, input_date) VALUES (%s,%s,%s,%s,%s, NOW())",
                        (code, name, selisih, volume, freq)
                    )
                    st.success("✅ Data tersimpan!")
                    # Increment form key untuk reset form
                    st.session_state.form_key += 1
                    st.rerun()
                else:
                    st.error("❌ Kode Saham dan Nama Saham harus diisi!")
    db.disconnect()

def show_calculation_page():
    st.markdown('<div class="main-header">🧮 HASIL PERHITUNGAN</div>', unsafe_allow_html=True)
    db = get_db_connection()
    if not db: return
    
    if st.button("🚀 Jalankan Perhitungan", use_container_width=True):
        with st.spinner("Sedang menghitung..."):
            calculate_all_stocks(db)
            
    # Tampilkan Hasil
    query = """
    SELECT sd.stock_code, sd.stock_name, sd.selisih, sd.volume, sd.frekuensi, cr.final_score, cr.risk_category
    FROM calculation_results cr JOIN stock_data sd ON cr.stock_id = sd.id
    ORDER BY cr.final_score DESC
    """
    results = db.fetch_all(query)
    if results:
        df = pd.DataFrame(results)
        df.insert(0, 'Rank', range(1, len(df) + 1))
        
        # Styling
        def color_risk(val):
            if val == 'Low Risk': return 'background-color: #d4edda; color: #155724'
            elif val == 'Medium Risk': return 'background-color: #fff3cd; color: #856404'
            return 'background-color: #f8d7da; color: #721c24'

        st.dataframe(df.style.map(color_risk, subset=['risk_category']), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada hasil. Klik tombol di atas.")
    db.disconnect()

# ==========================================
# MAIN APP ROUTER
# ==========================================
def main_app():
    with st.sidebar:
        st.title("Navigasi")
        st.write(f"User: {st.session_state.username}")
        if st.button("Dashboard", use_container_width=True): st.session_state.page = 'dashboard'
        # Menu tambahan untuk User Management (Admin Only)
        if st.session_state.role == 'admin':
            if st.button("User", use_container_width=True): st.session_state.page = 'users'
        if st.button("Variabel", use_container_width=True): st.session_state.page = 'variables'
        if st.button("Rules", use_container_width=True): st.session_state.page = 'rules'
        if st.button("Data Saham", use_container_width=True): st.session_state.page = 'stocks'
        if st.button("Proses & Hasil", use_container_width=True): st.session_state.page = 'calculation'
        st.markdown("---")
        if st.button("Logout", use_container_width=True): logout()

    if st.session_state.page == 'dashboard': show_dashboard()
    elif st.session_state.page == 'variables': show_variables_management()
    elif st.session_state.page == 'rules': show_rules_management()
    elif st.session_state.page == 'stocks': show_stocks_management()
    elif st.session_state.page == 'calculation': show_calculation_page()
    elif st.session_state.page == 'users': show_user_management()

def show_user_management():
    require_admin()
    st.markdown('<div class="main-header">👥 MANAJEMEN USER</div>', unsafe_allow_html=True)
    db = get_db_connection()
    if not db: return

    tab1, tab2 = st.tabs(["List User", "Tambah User"])
    
    with tab1:
        # Menampilkan daftar user (tanpa password)
        users = db.fetch_all("SELECT id, username, role FROM users ORDER BY username")
        if users:
            st.dataframe(pd.DataFrame(users), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data user user.")

    with tab2:
        st.subheader("Tambah User Baru")
        with st.form("add_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["user", "admin"])
            
            if st.form_submit_button("Simpan User Baru"):
                if new_username and new_password:
                    # Cek apakah username sudah ada
                    existing = db.fetch_one("SELECT id FROM users WHERE username = %s", (new_username,))
                    if existing:
                        st.error("❌ Username sudah digunakan!")
                    else:
                        try:
                            # Hash password dengan bcrypt
                            hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                            
                            query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                            db.execute_query(query, (new_username, hashed_pw, new_role))
                            
                            st.success(f"✅ User '{new_username}' berhasil ditambahkan!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Gagal menyimpan: {str(e)}")
                else:
                    st.warning("⚠️ Mohon lengkapi username dan password!")
    
    db.disconnect()

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()