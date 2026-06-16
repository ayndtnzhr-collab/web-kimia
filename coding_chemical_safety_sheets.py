import streamlit as st
import random

# Setting Halaman Utama Web
st.set_page_config(page_title="Chemical Safety System", page_icon="🧪", layout="centered")

# Database Senyawa
chemicals = {
    "HCl": {"nama": "Asam Klorida", "kategori": "Inorganic Acid"},
    "H2SO4": {"nama": "Asam Sulfat", "kategori": "Inorganic Acid"},
    "HNO3": {"nama": "Asam Nitrat", "kategori": "Oxidizing Acid"},
    "NaOH": {"nama": "Natrium Hidroksida", "kategori": "Caustic Base"},
    "Al(OH)3": {"nama": "Aluminium Hidroksida", "kategori": "Base"},
    "KMnO4": {"nama": "Kalium Permanganat", "kategori": "Oxidizer"},
    "K2Cr2O7": {"nama": "Kalium Dikromat", "kategori": "Oxidizer"},
    "AgNO3": {"nama": "Perak Nitrat", "kategori": "Oxidizer"},
    "C2H5OH": {"nama": "Etanol", "kategori": "Flammable"},
    "KCN": {"nama": "Kalium Sianida", "kategori": "Toxic Cyanide"},
    "C2H2O4": {"nama": "Asam Oksalat", "kategori": "Organic Acid"},
    "NaCl": {"nama": "Natrium Klorida", "kategori": "General Salt"},
    "KCl": {"nama": "Kalium Klorida", "kategori": "General Salt"},
    "Li2SO4": {"nama": "Litium Sulfat", "kategori": "General Salt"},
    "CaCl2": {"nama": "Kalsium Klorida", "kategori": "General Salt"},
    "MgCl2": {"nama": "Magnesium Klorida", "kategori": "General Salt"},
    "BaCl2": {"nama": "Barium Klorida", "kategori": "Toxic Salt"},
    "Na2CO3": {"nama": "Natrium Karbonat", "kategori": "Carbonate"},
    "CaCO3": {"nama": "Kalsium Karbonat", "kategori": "Carbonate"},
    "H2O": {"nama": "Air", "kategori": "Water"}
}

# Aturan Kombinasi
rules = {
    ("Inorganic Acid", "Inorganic Acid"): ("PERLU PERHATIAN", 2, "Campuran tetap korosif"),
    ("Inorganic Acid", "Oxidizing Acid"): ("PERLU PERHATIAN", 3, "Asam oksidator dipisahkan dari asam biasa"),
    ("Inorganic Acid", "Caustic Base"): ("PERLU PERHATIAN", 3, "Reaksi netralisasi eksoterm"),
    ("Inorganic Acid", "Base"): ("PERLU PERHATIAN", 2, "Terjadi netralisasi"),
    ("Inorganic Acid", "Oxidizer"): ("PERLU PERHATIAN", 3, "Asam dan oksidator perlu segregasi"),
    ("Inorganic Acid", "Flammable"): ("PERLU PERHATIAN", 3, "Asam tidak disimpan bersama bahan mudah terbakar"),
    ("Inorganic Acid", "Organic Acid"): ("PERLU PERHATIAN", 2, "Hindari pencampuran asam berbeda"),
    ("Inorganic Acid", "General Salt"): ("PERLU PERHATIAN", 2, "Periksa reaktivitas ion"),
    ("Inorganic Acid", "Toxic Salt"): ("PERLU PERHATIAN", 2, "Perlu evaluasi pelepasan ion"),
    ("Inorganic Acid", "Carbonate"): ("PERLU PERHATIAN", 2, "Asam bereaksi dengan karbonat"),
    ("Inorganic Acid", "Toxic Cyanide"): ("PERLU PERHATIAN", 3, "Risiko pembentukan gas beracun"),
    ("Inorganic Acid", "Water"): ("PERLU PERHATIAN", 2, "Pengenceran asam menghasilkan panas"),
    ("Oxidizing Acid", "Caustic Base"): ("PERLU PERHATIAN", 3, "Tidak kompatibel"),
    ("Oxidizing Acid", "Flammable"): ("PERLU PERHATIAN", 3, "Dapat memicu oksidasi"),
    ("Oxidizing Acid", "Organic Acid"): ("PERLU PERHATIAN", 3, "Tidak kompatibel"),
    ("Oxidizing Acid", "Oxidizer"): ("PERLU PERHATIAN", 3, "Kelompok reaktif"),
    ("Oxidizing Acid", "General Salt"): ("PERLU PERHATIAN", 2, "Periksa reaktivitas"),
    ("Oxidizing Acid", "Carbonate"): ("PERLU PERHATIAN", 2, "Potensi pelepasan gas"),
    ("Oxidizing Acid", "Toxic Cyanide"): ("PERLU PERHATIAN", 3, "Sangat tidak kompatibel"),
    ("Oxidizing Acid", "Water"): ("PERLU PERHATIAN", 2, "Pengenceran menghasilkan panas"),
    ("Caustic Base", "Caustic Base"): ("PERLU PERHATIAN", 2, "Campuran sangat basa"),
    ("Caustic Base", "Base"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("Caustic Base", "Oxidizer"): ("PERLU PERHATIAN", 2, "Periksa kompatibilitas"),
    ("Caustic Base", "Flammable"): ("PERLU PERHATIAN", 2, "Tidak disimpan bersama"),
    ("Caustic Base", "General Salt"): ("AMAN", 1, "Umumnya kompatibel"),
    ("Caustic Base", "Toxic Salt"): ("PERLU PERHATIAN", 2, "Periksa kestabilan"),
    ("Caustic Base", "Carbonate"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("Caustic Base", "Toxic Cyanide"): ("PERLU PERHATIAN", 2, "Kendalikan paparan"),
    ("Caustic Base", "Water"): ("PERLU PERHATIAN", 2, "Pelarutan basa menghasilkan panas"),
    ("Oxidizer", "Oxidizer"): ("PERLU PERHATIAN", 3, "Jangan campur oksidator"),
    ("Oxidizer", "Flammable"): ("PERLU PERHATIAN", 3, "Risiko kebakaran"),
    ("Oxidizer", "Organic Acid"): ("PERLU PERHATIAN", 3, "Potensi reaksi oksidasi"),
    ("Oxidizer", "General Salt"): ("PERLU PERHATIAN", 2, "Evaluasi kompatibilitas"),
    ("Oxidizer", "Toxic Salt"): ("PERLU PERHATIAN", 2, "Periksa kestabilan"),
    ("Oxidizer", "Carbonate"): ("PERLU PERHATIAN", 2, "Periksa reaktivitas"),
    ("Oxidizer", "Toxic Cyanide"): ("PERLU PERHATIAN", 3, "Tidak kompatibel"),
    ("Oxidizer", "Water"): ("AMAN", 1, "Umumnya stabil"),
    ("Flammable", "Flammable"): ("PERLU PERHATIAN", 2, "Risiko kebakaran"),
    ("Flammable", "General Salt"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("Flammable", "Toxic Salt"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("Flammable", "Carbonate"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("Flammable", "Water"): ("AMAN", 1, "Tergantung kelarutan"),
    ("Toxic Cyanide", "Water"): ("PERLU PERHATIAN", 2, "Ikuti prosedur keselamatan"),
    ("Toxic Cyanide", "General Salt"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("Toxic Cyanide", "Toxic Salt"): ("PERLU PERHATIAN", 2, "Periksa kompatibilitas"),
    ("General Salt", "General Salt"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("General Salt", "Toxic Salt"): ("PERLU PERHATIAN", 2, "Perhatikan toksisitas"),
    ("General Salt", "Carbonate"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("General Salt", "Water"): ("AMAN", 1, "Umumnya larut"),
    ("Carbonate", "Carbonate"): ("AMAN", 1, "Tidak ada incompatibility utama"),
    ("Carbonate", "Water"): ("AMAN", 1, "Umumnya stabil"),
    ("Water", "Water"): ("AMAN", 1, "Tidak ada incompatibility utama")
}

# Aturan Default
default_rules = {
    "Water": ("AMAN", 1, "Tidak ada incompatibility utama"),
    "General Salt": ("AMAN", 1, "Tidak ada incompatibility utama"),
    "Carbonate": ("AMAN", 1, "Tidak ada incompatibility utama"),
    "Base": ("AMAN", 1, "Tidak ada incompatibility utama"),
    "Caustic Base": ("PERLU PERHATIAN", 2, "Periksa kondisi pencampuran"),
    "Inorganic Acid": ("PERLU PERHATIAN", 2, "Asam memerlukan evaluasi kompatibilitas"),
    "Organic Acid": ("PERLU PERHATIAN", 2, "Asam memerlukan evaluasi kompatibilitas"),
    "Oxidizer": ("PERLU PERHATIAN", 2, "Oksidator memerlukan segregasi"),
    "Oxidizing Acid": ("PERLU PERHATIAN", 3, "Asam oksidator memerlukan segregasi"),
    "Flammable": ("PERLU PERHATIAN", 2, "Bahan mudah terbakar perlu perhatian"),
    "Toxic Salt": ("PERLU PERHATIAN", 2, "Perhatikan toksisitas"),
    "Toxic Cyanide": ("PERLU PERHATIAN", 3, "Sianida memerlukan prosedur keselamatan")
}

# Fungsi Utama Kompatibilitas
def cek_kompatibilitas(bahan1, bahan2):
    kategori1 = chemicals[bahan1]["kategori"]
    kategori2 = chemicals[bahan2]["kategori"]

    if (kategori1, kategori2) in rules:
        return rules[(kategori1, kategori2)]
    elif (kategori2, kategori1) in rules:
        return rules[(kategori2, kategori1)]
    else:
        prioritas = [kategori1, kategori2]
        for k in prioritas:
            if k in default_rules:
                return default_rules[k]
        return ("PERLU PERHATIAN", 2, "Perlu evaluasi kompatibilitas")

# Fungsi Bank Soal Game
def buat_bank_soal():
    bank = []
    for b1 in chemicals:
        for b2 in chemicals:
            if b1 != b2:
                bank.append((b1, b2))
    return bank

# Desain Interface Web
st.title("🧪 CHEMICAL SAFETY SYSTEM")
st.write("Selamat datang! Kelola keamanan laboratorium kimia Anda secara interaktif.")

# Menu Sidebar Navigasi
menu = st.sidebar.radio("PILIH MENU SISTEM:", ["1. Cek Kompatibilitas Bahan", "2. Chemical Safety Game", "3. Database Senyawa"])

if menu == "3. Database Senyawa":
    st.header("📋 Database Senyawa Kimia")
    data_tabel = [{"Rumus": k, "Nama Senyawa": v["nama"], "Kategori": v["kategori"]} for k, v in chemicals.items()]
    st.table(data_tabel)

elif menu == "1. Cek Kompatibilitas Bahan":
    st.header("🔍 Cek Kompatibilitas Bahan Kimia")
    st.write("Pilih dua bahan kimia di bawah ini untuk menganalisis risiko pencampuran.")
    
    opsi_bahan = list(chemicals.keys())
    bahan1 = st.selectbox("Pilih Bahan Pertama:", opsi_bahan, key="b1")
    bahan2 = st.selectbox("Pilih Bahan Kedua:", opsi_bahan, key="b2")
    
    if st.button("Analisis Kompatibilitas", key="btn_analisis"):
        hasil = cek_kompatibilitas(bahan1, bahan2)
        
        st.subheader("📊 Hasil Analisis")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Bahan 1:** {bahan1} ({chemicals[bahan1]['nama']})")
        with col2:
            st.info(f"**Bahan 2:** {bahan2} ({chemicals[bahan2]['nama']})")
            
        if hasil[0] == "AMAN":
            st.success(f"🟢 **Status:** {hasil[0]}")
        else:
            st.error(f"🔴 **Status:** {hasil[0]}")
            
        st.warning(f"⚠️ **Tingkat Risiko:** Level {hasil[1]}")
        st.markdown(f"ℹ️ **Keterangan:** {hasil[2]}")

elif menu == "2. Chemical Safety Game":
    st.header("🎮 Chemical Safety Challenge")
    st.write("Uji pengetahuan laboratoriummu! Tebak apakah campuran bahan berikut **AMAN** atau **BERBAHAYA**.")
    
    # Inisialisasi State (Hanya ditulis 1 kali saja)
    if "game_active" not in st.session_state:
        st.session_state.game_active = False
        st.session_state.skor = 0
        st.session_state.nyawa = 5
        st.session_state.level = 1
        st.session_state.answered = False
        st.session_state.bank_soal = []

    # Tombol Mulai Game (Hanya ditulis 1 kali saja)
    if st.button("Mulai / Reset Game Baru", key="btn_start_game"):
        st.session_state.skor = 0
        st.session_state.nyawa = 5
        st.session_state.level = 1
        st.session_state.bank_soal = buat_bank_soal()
        random.shuffle(st.session_state.bank_soal)
        st.session_state.current_question = st.session_state.bank_soal.pop()
        st.session_state.game_active = True
        st.session_state.answered = False
        st.session_state.scored_this_round = False

    if st.session_state.game_active:
        if st.session_state.nyawa > 0 and len(st.session_state.bank_soal) > 0:
            b1, b2 = st.session_state.current_question
            hasil_real = cek_kompatibilitas(b1, b2)
            jawaban_benar = "AMAN" if hasil_real[0] == "AMAN" else "BERBAHAYA / PERLU PERHATIAN"
            
            st.markdown(f"### LEVEL {st.session_state.level}")
            c1, c2 = st.columns(2)
            c1.metric(label="Skor Kamu 🏆", value=st.session_state.skor)
            c2.metric(label="Sisa Nyawa ❤️", value=st.session_state.nyawa)
            
            st.info(f"Apakah campuran ini aman? {b1} ({chemicals[b1]['nama']}) + {b2} ({chemicals[b2]['nama']})")
            
            # Key menggunakan sisa panjang bank soal agar selalu unik tiap soal berganti
            q_id = len(st.session_state.bank_soal)
            col_ans1, col_ans2 = st.columns(2)
            pilih_aman = col_ans1.button("🟢 AMAN", disabled=st.session_state.answered, key=f"aman_{q_id}")
            pilih_bahaya = col_ans2.button("🔴 BERBAHAYA", disabled=st.session_state.answered, key=f"bahaya_{q_id}")
            
            user_choice = None
            if pilih_aman:
                user_choice = "AMAN"
            if pilih_bahaya:
                user_choice = "BERBAHAYA / PERLU PERHATIAN"
                
            if user_choice is not None:
                st.session_state.answered = True
                st.session_state.user_choice = user_choice
                
            if st.session_state.answered:
                if st.session_state.user_choice == jawaban_benar:
                    st.success("✅ BENAR! Kamu mendapatkan +10 poin.")
                    if "scored_this_round" not in st.session_state or not st.session_state.scored_this_round:
                        st.session_state.skor += 10
                        st.session_state.scored_this_round = True
                else:
                    st.error("❌ SALAH!")
                    st.markdown(f"Status Sebenarnya: {hasil_real[0]}")
                    st.markdown(f"Alasan: {hasil_real[2]}")
                    if "scored_this_round" not in st.session_state or not st.session_state.scored_this_round:
                        st.session_state.nyawa -= 1
                        st.session_state.scored_this_round = True
                        
                if st.button("Lanjut ke Soal Berikutnya ➡️", key=f"next_{q_id}"):
                    if st.session_state.nyawa > 0 and len(st.session_state.bank_soal) > 0:
                        st.session_state.current_question = st.session_state.bank_soal.pop()
                        st.session_state.level += 1
                        st.session_state.answered = False
                        st.session_state.scored_this_round = False
                    st.rerun()
        else:
            st.error("💀 GAME OVER!")
            st.metric(label="Skor Akhir Kamu", value=st.session_state.skor)
            st.session_state.game_active = False
