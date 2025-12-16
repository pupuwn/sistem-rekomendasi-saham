import streamlit as st
import pandas as pd
import bcrypt
from datetime import datetime
from db_connect import get_db_connection
from models.fuzzification import FuzzificationEngine
from models.inference import InferenceEngine
from models.defuzzification import DefuzzificationEngine

# Konfigurasi halaman
st.set_page_config(
    page_title="Fuzzy Tsukamoto - Rekomendasi Saham Low-Risk",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Fungsi Autentikasi
def check_credentials(username, password):
    """Verifikasi username dan password"""
    db = get_db_connection()
    if not db:
        return False, None
    
    query = "SELECT password, role FROM users WHERE username = %s"
    result = db.fetch_one(query, (username,))
    db.disconnect()
    
    if result:
        stored_hash = result['password'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True, result.get('role', 'user')
    return False, None

def is_admin():
    """Check apakah user saat ini adalah admin"""
    return st.session_state.get('role') == 'admin'

def require_admin():
    """Decorator/helper untuk halaman yang butuh akses admin"""
    if not is_admin():
        st.error("⛔ Akses ditolak! Halaman ini hanya untuk Admin.")
        st.info("💡 Anda login sebagai User biasa. Silakan hubungi Admin untuk akses penuh.")
        st.stop()

def login_page():
    """Halaman Login"""
    st.markdown('<div class="main-header">🔐 SISTEM REKOMENDASI SAHAM LOW-RISK</div>', unsafe_allow_html=True)
    # st.markdown('<div class="sub-header">Fuzzy Tsukamoto Method - Bursa Efek Indonesia</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Login Admin")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            submit = st.form_submit_button("Masuk", use_container_width=True)
            
            if submit:
                if username and password:
                    is_valid, user_role = check_credentials(username, password)
                    if is_valid:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = user_role
                        st.rerun()
                    else:
                        st.error("❌ Username atau password salah!")
                else:
                    st.warning("⚠️ Mohon isi username dan password!")
        
        st.markdown("---")
        st.info("💡 **Kredensial Default:**\n- Username: `admin`\n- Password: `admin123`")
        st.caption("© 2025 Fuzzy Tsukamoto System v1.0")

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = 'dashboard'
    st.rerun()

# Layout Utama (setelah login)
def main_app():
    """Aplikasi utama setelah login"""
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### MENU NAVIGASI")
        st.markdown(f"**User:** {st.session_state.username}")
        st.markdown("---")
        
        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
        
        if st.button("Manajemen Variabel", use_container_width=True):
            st.session_state.page = 'variables'
        
        if st.button("Manajemen Aturan", use_container_width=True):
            st.session_state.page = 'rules'
        
        if st.button("Data Saham", use_container_width=True):
            st.session_state.page = 'stocks'
        
        if st.button("Proses & Hasil", use_container_width=True):
            st.session_state.page = 'calculation'
        
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            logout()
        
        st.markdown("---")
        st.caption("© 2025 Fuzzy Tsukamoto v1.0")
    
    # Content berdasarkan page yang dipilih
    if st.session_state.page == 'dashboard':
        show_dashboard()
    elif st.session_state.page == 'variables':
        show_variables_management()
    elif st.session_state.page == 'rules':
        show_rules_management()
    elif st.session_state.page == 'stocks':
        show_stocks_management()
    elif st.session_state.page == 'calculation':
        show_calculation_page()

def show_dashboard():
    """Halaman Dashboard"""
    st.markdown('<div class="main-header">DASHBOARD</div>', unsafe_allow_html=True)
    
    db = get_db_connection()
    if not db:
        st.error("❌ Koneksi database gagal!")
        return
    
    # Statistik
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_stocks = db.fetch_one("SELECT COUNT(*) as count FROM stock_data")
        st.metric("📈 Total Data Saham", total_stocks['count'] if total_stocks else 0)
    
    with col2:
        total_rules = db.fetch_one("SELECT COUNT(*) as count FROM fuzzy_rules")
        st.metric("⚙️ Total Aturan Fuzzy", total_rules['count'] if total_rules else 0)
    
    with col3:
        total_variables = db.fetch_one("SELECT COUNT(*) as count FROM fuzzy_variables")
        st.metric("📋 Total Variabel", total_variables['count'] if total_variables else 0)
    
    with col4:
        total_results = db.fetch_one("SELECT COUNT(*) as count FROM calculation_results")
        st.metric("🧮 Total Hasil Kalkulasi", total_results['count'] if total_results else 0)
    
    st.markdown("---")
    
    # Recent calculations
    st.subheader("🕒 Hasil Perhitungan Terbaru")
    
    query = """
    SELECT 
        sd.stock_code,
        sd.stock_name,
        cr.final_score,
        cr.risk_category,
        cr.calculation_date
    FROM calculation_results cr
    JOIN stock_data sd ON cr.stock_id = sd.id
    ORDER BY cr.calculation_date DESC
    LIMIT 10
    """
    
    recent_results = db.fetch_all(query)
    
    if recent_results:
        df = pd.DataFrame(recent_results)
        df['calculation_date'] = pd.to_datetime(df['calculation_date']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Format display
        df_display = df.rename(columns={
            'stock_code': 'Kode Saham',
            'stock_name': 'Nama Saham',
            'final_score': 'Skor',
            'risk_category': 'Kategori',
            'calculation_date': 'Tanggal'
        })
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("💡 Belum ada hasil perhitungan. Silakan input data saham dan jalankan proses kalkulasi.")
    
    db.disconnect()
    
    # Informasi Sistem
    st.markdown("---")
    st.subheader("ℹ️ Tentang Sistem")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Metode:** Fuzzy Tsukamoto
        
        **Kriteria Penilaian:**
        - 📊 Volatilitas (Selisih Harga)
        - 📈 Volume Transaksi
        - 🔄 Frekuensi Transaksi
        
        **Output:**
        - 🟢 Low Risk (Skor ≥ 70)
        - 🟡 Medium Risk (Skor 40-70)
        - 🔴 High Risk (Skor < 40)
        """)
    
    with col2:
        st.markdown("""
        **Tahapan Proses:**
        1. **Fuzzifikasi**: Konversi nilai crisp → fuzzy
        2. **Inferensi**: Evaluasi aturan IF-THEN
        3. **Defuzzifikasi**: Konversi fuzzy → crisp (weighted average)
        
        **Target:** Investor pemula yang mencari saham berisiko rendah di indeks LQ45
        """)

def show_variables_management():
    """Halaman Manajemen Variabel dan Himpunan Fuzzy"""
    require_admin()  # Hanya admin yang bisa akses
    
    st.markdown('<div class="main-header">📊 MANAJEMEN VARIABEL</div>', unsafe_allow_html=True)
    
    db = get_db_connection()
    if not db:
        st.error("❌ Koneksi database gagal!")
        return
    
    tab1, tab2 = st.tabs(["📊 Lihat Variabel", "➕ Tambah/Edit Variabel"])
    
    with tab1:
        # Tampilkan variabel yang ada
        variables = db.fetch_all("SELECT * FROM fuzzy_variables")
        
        if variables:
            for var in variables:
                with st.expander(f"📌 {var['variable_name']} (Range: {var['min_value']} - {var['max_value']})"):
                    st.write(f"**Deskripsi:** {var['description']}")
                    
                    # Tampilkan himpunan fuzzy untuk variabel ini
                    fuzzy_sets = db.fetch_all(
                        "SELECT * FROM fuzzy_sets WHERE variable_id = %s ORDER BY min_value",
                        (var['id'],)
                    )
                    
                    if fuzzy_sets:
                        st.markdown("**Himpunan Fuzzy:**")
                        df = pd.DataFrame(fuzzy_sets)
                        df_display = df[['set_name', 'min_value', 'max_value', 'peak_start', 'peak_end']]
                        df_display.columns = ['Himpunan', 'Min', 'Max', 'Peak Start', 'Peak End']
                        st.dataframe(df_display, hide_index=True, use_container_width=True)
        else:
            st.info("💡 Belum ada variabel yang terdaftar.")
    
    with tab2:
        st.subheader("➕ Tambah Variabel Baru")
        
        with st.form("add_variable_form"):
            var_name = st.text_input("Nama Variabel", placeholder="Contoh: Volatilitas")
            col1, col2 = st.columns(2)
            with col1:
                min_val = st.number_input("Nilai Minimum", value=0.0)
            with col2:
                max_val = st.number_input("Nilai Maximum", value=100.0)
            
            description = st.text_area("Deskripsi", placeholder="Deskripsi variabel...")
            
            submit = st.form_submit_button("💾 Simpan Variabel")
            
            if submit:
                if var_name and max_val > min_val:
                    query = """
                    INSERT INTO fuzzy_variables (variable_name, min_value, max_value, description)
                    VALUES (%s, %s, %s, %s)
                    """
                    result = db.execute_query(query, (var_name, min_val, max_val, description))
                    
                    if result:
                        st.success(f"✅ Variabel '{var_name}' berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menambahkan variabel!")
                else:
                    st.error("❌ Mohon isi semua field dengan benar!")
    
    db.disconnect()

def show_rules_management():
    """Halaman Manajemen Aturan Fuzzy"""
    require_admin()  # Hanya admin yang bisa akses
    
    st.markdown('<div class="main-header">⚙️ MANAJEMEN ATURAN</div>', unsafe_allow_html=True)
    
    db = get_db_connection()
    if not db:
        st.error("❌ Koneksi database gagal!")
        return
    
    tab1, tab2 = st.tabs(["📜 Lihat Aturan", "➕ Tambah Aturan"])
    
    with tab1:
        rules = db.fetch_all("SELECT * FROM fuzzy_rules ORDER BY id")
        
        if rules:
            st.write(f"**Total Aturan:** {len(rules)}")
            
            df = pd.DataFrame(rules)
            df_display = df[['rule_name', 'volatilitas_set', 'volume_set', 'frekuensi_set', 'output_set']]
            df_display.columns = ['Rule', 'Volatilitas', 'Volume', 'Frekuensi', 'Output']
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Export rules
            if st.button("📥 Export Rules ke CSV"):
                csv = df_display.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="fuzzy_rules.csv",
                    mime="text/csv"
                )
        else:
            st.info("💡 Belum ada aturan fuzzy yang terdaftar.")
    
    with tab2:
        st.subheader("➕ Tambah Aturan Baru")
        
        with st.form("add_rule_form"):
            rule_name = st.text_input("Nama Aturan", placeholder="Contoh: R28")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                vol_set = st.selectbox("Volatilitas", ["Rendah", "Sedang", "Tinggi"])
            with col2:
                volume_set = st.selectbox("Volume", ["Rendah", "Sedang", "Tinggi"])
            with col3:
                freq_set = st.selectbox("Frekuensi", ["Rendah", "Sedang", "Tinggi"])
            
            output_set = st.selectbox("Output (Risiko)", ["Low_Risk", "Medium_Risk", "High_Risk"])
            
            submit = st.form_submit_button("💾 Simpan Aturan")
            
            if submit:
                if rule_name:
                    query = """
                    INSERT INTO fuzzy_rules (rule_name, volatilitas_set, volume_set, frekuensi_set, output_set)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    result = db.execute_query(query, (rule_name, vol_set, volume_set, freq_set, output_set))
                    
                    if result:
                        st.success(f"✅ Aturan '{rule_name}' berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menambahkan aturan!")
                else:
                    st.error("❌ Nama aturan tidak boleh kosong!")
    
    db.disconnect()

def show_stocks_management():
    """Halaman Manajemen Data Saham"""
    st.markdown('<div class="main-header">💹 MANAJEMEN DATA SAHAM</div>', unsafe_allow_html=True)
    
    db = get_db_connection()
    if not db:
        st.error("❌ Koneksi database gagal!")
        return
    
    tab1, tab2 = st.tabs(["📊 Lihat Data Saham", "➕ Tambah Data Saham"])
    
    with tab1:
        stocks = db.fetch_all("SELECT * FROM stock_data ORDER BY input_date DESC")
        
        if stocks:
            st.write(f"**Total Data:** {len(stocks)}")
            
            df = pd.DataFrame(stocks)
            df_display = df[['stock_code', 'stock_name', 'selisih', 'volume', 'frekuensi', 'input_date']]
            df_display.columns = ['Kode', 'Nama Saham', 'Selisih (Volatilitas)', 'Volume', 'Frekuensi', 'Tanggal Input']
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Delete functionality
            st.markdown("---")
            st.subheader("🗑️ Hapus Data Saham")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                stock_to_delete = st.selectbox(
                    "Pilih saham yang akan dihapus",
                    options=[f"{s['stock_code']} - {s['stock_name']}" for s in stocks]
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("🗑️ Hapus", use_container_width=True):
                    stock_code = stock_to_delete.split(' - ')[0]
                    delete_query = "DELETE FROM stock_data WHERE stock_code = %s"
                    db.execute_query(delete_query, (stock_code,))
                    st.success(f"✅ Data saham {stock_code} berhasil dihapus!")
                    st.rerun()
        else:
            st.info("💡 Belum ada data saham yang terdaftar.")
    
    with tab2:
        st.subheader("➕ Tambah Data Saham Baru")
        
        with st.form("add_stock_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                stock_code = st.text_input("Kode Saham", placeholder="Contoh: BBRI")
                stock_name = st.text_input("Nama Saham", placeholder="Contoh: Bank Rakyat Indonesia")
            
            with col2:
                selisih = st.number_input("Selisih Harga (Volatilitas)", min_value=0.0, value=0.0, step=10.0)
                volume = st.number_input("Volume Transaksi", min_value=0, value=0, step=100000)
            
            frekuensi = st.number_input("Frekuensi Transaksi", min_value=0, value=0, step=10)
            input_date = st.date_input("Tanggal Input", value=datetime.now())
            
            submit = st.form_submit_button("💾 Simpan Data Saham")
            
            if submit:
                if stock_code and stock_name:
                    query = """
                    INSERT INTO stock_data (stock_code, stock_name, selisih, volume, frekuensi, input_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    result = db.execute_query(query, (stock_code, stock_name, selisih, volume, frekuensi, input_date))
                    
                    if result:
                        st.success(f"✅ Data saham '{stock_code}' berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menambahkan data saham!")
                else:
                    st.error("❌ Kode dan nama saham harus diisi!")
    
    db.disconnect()

def show_calculation_page():
    """Halaman Proses Perhitungan dan Hasil"""
    st.markdown('<div class="main-header">🧮 PROSES PERHITUNGAN & HASIL REKOMENDASI</div>', unsafe_allow_html=True)
    
    db = get_db_connection()
    if not db:
        st.error("❌ Koneksi database gagal!")
        return
    
    # Tombol untuk menjalankan perhitungan
    if st.button("🚀 Jalankan Perhitungan Fuzzy Tsukamoto", use_container_width=True):
        with st.spinner("⏳ Memproses data..."):
            calculate_all_stocks(db)
    
    st.markdown("---")
    
    # Tampilkan hasil
    st.subheader("Hasil Rekomendasi Saham (Ranking)")
    
    query = """
    SELECT 
        sd.stock_code,
        sd.stock_name,
        sd.selisih,
        sd.volume,
        sd.frekuensi,
        cr.final_score,
        cr.risk_category
    FROM calculation_results cr
    JOIN stock_data sd ON cr.stock_id = sd.id
    ORDER BY cr.final_score DESC
    """
    
    results = db.fetch_all(query)
    
    if results:
        df = pd.DataFrame(results)
        
        # Tambahkan ranking
        df.insert(0, 'Ranking', range(1, len(df) + 1))
        
        # Format display
        df_display = df.rename(columns={
            'stock_code': 'Kode Saham',
            'stock_name': 'Nama Saham',
            'selisih': 'Volatilitas',
            'volume': 'Volume',
            'frekuensi': 'Frekuensi',
            'final_score': 'Skor Akhir',
            'risk_category': 'Kategori Risiko'
        })
        
        # Color coding untuk kategori
        def color_risk(val):
            if val == 'Low Risk':
                return 'background-color: #d4edda; color: #155724'
            elif val == 'Medium Risk':
                return 'background-color: #fff3cd; color: #856404'
            else:
                return 'background-color: #f8d7da; color: #721c24'
        
        styled_df = df_display.style.applymap(color_risk, subset=['Kategori Risiko'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Download hasil
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="📥 Download Hasil (CSV)",
                data=csv,
                file_name=f"rekomendasi_saham_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Statistik
        st.markdown("---")
        st.subheader("📈 Statistik Hasil")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            low_risk = len(df[df['risk_category'] == 'Low Risk'])
            st.metric("🟢 Low Risk", low_risk)
        
        with col2:
            medium_risk = len(df[df['risk_category'] == 'Medium Risk'])
            st.metric("🟡 Medium Risk", medium_risk)
        
        with col3:
            high_risk = len(df[df['risk_category'] == 'High Risk'])
            st.metric("🔴 High Risk", high_risk)
        
    else:
        st.info("💡 Belum ada hasil perhitungan. Klik tombol 'Jalankan Perhitungan' untuk memproses data saham.")
    
    db.disconnect()

def calculate_all_stocks(db):
    """Fungsi untuk menghitung semua data saham dengan detail debugging"""
    try:
        # Ambil data saham
        stocks = db.fetch_all("SELECT * FROM stock_data")
        
        if not stocks:
            st.warning("⚠️ Tidak ada data saham untuk diproses!")
            return
        
        # Ambil konfigurasi fuzzy sets (ini bisa di luar loop karena sama untuk semua saham)
        fuzzy_sets_config = get_fuzzy_sets_config(db)
        
        # Ambil output sets (ini juga bisa di luar loop)
        output_sets = get_output_sets_config(db)
        
        # Inisialisasi engine yang tidak bergantung pada aturan (bisa di luar loop)
        fuzz_engine = FuzzificationEngine()
        defuzz_engine = DefuzzificationEngine()
        
        # Hapus hasil perhitungan lama
        db.execute_query("DELETE FROM calculation_results")
        
        # Proses setiap saham
        for stock in stocks:
            print(f"\n{'='*50}")
            print(f"MEMPROSES SAHAM: {stock['stock_code']} ({stock['stock_name']})")
            print(f"{'='*50}")
            
            # --- TAHAP 1: FUZZIFIKASI ---
            print("\n--- TAHAP 1: FUZZIFIKASI ---")
            fuzzy_inputs = fuzz_engine.fuzzify_all_inputs(
                stock['selisih'],
                stock['volume'],
                stock['frekuensi'],
                fuzzy_sets_config
            )
            
            print(f"Input Crisp: Selisih={stock['selisih']}, Volume={stock['volume']}, Frekuensi={stock['frekuensi']}")
            print("Hasil Fuzzifikasi (Derajat Keanggotaan):")
            for var_name, sets in fuzzy_inputs.items():
                for set_name, mu_value in sets.items():
                    print(f"  mu_{var_name.lower()}_{set_name.lower()}: {mu_value:.4f}")

            # --- TAHAP 2: INFERENSI ---
            print("\n--- TAHAP 2: INFERENSI (EVALUASI ATURAN) ---")
            
            # 1. Ambil aturan yang spesifik untuk saham ini
            rules = db.fetch_all("SELECT * FROM fuzzy_rules WHERE stock_code = %s", (stock['stock_code'],))
            
            # 2. Inisialisasi InferenceEngine dengan aturan untuk saham ini
            #    INILAH YANG DIPERBAIKI: Inisialisasi dipindahkan ke dalam loop
            inference_engine = InferenceEngine(rules)
            
            inference_results = inference_engine.evaluate_all_rules(fuzzy_inputs)
            
            print("Hasil Evaluasi Aturan:")
            if not inference_results:
                print("  Tidak ada aturan yang aktif (fired).")
            else:
                for res in inference_results:
                    print(f"  Rule {res['rule_name']}: α = {res['alpha']:.4f}, z = {res['z']:.2f}, α*z = {res['alpha'] * res['z']:.4f}")

            # --- TAHAP 3: DEFUZZIFIKASI ---
            print("\n--- TAHAP 3: DEFUZZIFIKASI ---")
            if inference_results:
                final_score = defuzz_engine.weighted_average(inference_results)
                risk_category = defuzz_engine.get_risk_category(final_score)
                
                print(f"Skor Akhir (Z*): {final_score:.2f}")
                print(f"Kategori Risiko: {risk_category}")
                
                # Simpan hasil
                insert_query = """
                INSERT INTO calculation_results (stock_id, final_score, risk_category)
                VALUES (%s, %s, %s)
                """
                db.execute_query(insert_query, (stock['id'], final_score, risk_category))
            else:
                print("Skor Akhir (Z*): 0.00 (karena tidak ada aturan yang aktif)")
                print("Kategori Risiko: High Risk (default)")
                # Simpan hasil 0 jika tidak ada aturan yang aktif
                final_score = 0
                risk_category = "High Risk"
                db.execute_query(insert_query, (stock['id'], final_score, risk_category))

        
        st.success(f"✅ Berhasil memproses {len(stocks)} data saham! Detail perhitungan telah dicetak ke console.")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def get_fuzzy_sets_config(db):
    """Mengambil konfigurasi fuzzy sets dari database"""
    config = {}
    
    # Ambil ID variabel
    variables = db.fetch_all("SELECT id, variable_name FROM fuzzy_variables")
    
    for var in variables:
        fuzzy_sets = db.fetch_all(
            "SELECT * FROM fuzzy_sets WHERE variable_id = %s",
            (var['id'],)
        )
        config[var['variable_name']] = fuzzy_sets
    
    return config

def get_output_sets_config(db):
    """Mengambil konfigurasi output fuzzy sets dari database"""
    output_sets = db.fetch_all("SELECT * FROM fuzzy_output_sets")
    
    config = {}
    for output_set in output_sets:
        config[output_set['set_name']] = output_set
    
    return config

# Main Application Flow
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()
