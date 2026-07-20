"""
Teman Jaga Kesehatan — versi Python (Streamlit)

Cara menjalankan:
    pip install streamlit
    streamlit run teman_sehat.py
"""

import datetime
import streamlit as st

# ---------- Data statis ----------
TIPS = [
    "Minum segelas air putih segera setelah bangun tidur bisa membantu tubuhmu 'menyala' lebih cepat.",
    "Jalan kaki 10 menit setelah makan membantu pencernaan dan menstabilkan gula darah.",
    "Tidur di jam yang sama tiap malam membuat tubuh punya ritme yang lebih sehat.",
    "Sarapan dengan protein (telur, tahu, kacang) bikin kenyang lebih lama dan energi lebih stabil.",
    "Sesekali berhenti sejenak, tarik napas dalam 4 hitungan, tahan 4 hitungan, lalu hembuskan pelan.",
    "Peregangan leher dan bahu setiap 1 jam kerja bisa mencegah pegal menumpuk.",
    "Kurangi cahaya layar 30 menit sebelum tidur agar lebih mudah terlelap.",
]

MOODS = ["😄 Semangat", "🙂 Baik", "😐 Biasa", "😔 Lelah", "😣 Kurang enak badan"]

ACTIVITY_ITEMS = {
    "olahraga": "Bergerak / olahraga ringan",
    "sayur_buah": "Makan sayur atau buah",
    "tidur_cukup": "Tidur cukup semalam",
    "peregangan": "Peregangan / istirahat mata",
}


def tip_hari_ini() -> str:
    hari = datetime.date.today().day
    return TIPS[hari % len(TIPS)]


def kategori_bmi(bmi: float):
    if bmi < 18.5:
        return "Berat badan kurang", "info"
    if bmi < 25:
        return "Berat badan normal", "success"
    if bmi < 30:
        return "Berat badan berlebih", "warning"
    return "Obesitas — sebaiknya konsultasi ke dokter", "error"


st.set_page_config(page_title="Teman Jaga Kesehatan", page_icon="🌿", layout="centered")

st.markdown(
    """
    <style>
    .main { background-color: #F6F3EC; }
    h1, h2, h3 { color: #4E6E5B; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align:center;'>🌿 Teman Jaga Kesehatan</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#5B6B62;'>Langkah kecil, konsisten setiap hari — itu yang penting.</p>",
    unsafe_allow_html=True,
)

st.info(f"**Tips hari ini:** {tip_hari_ini()}")

st.subheader("Bagaimana perasaanmu hari ini?")
mood = st.radio("Pilih mood", MOODS, horizontal=True, label_visibility="collapsed")

st.subheader("Air putih hari ini")
if "air" not in st.session_state:
    st.session_state.air = 0

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("➖ Kurangi"):
        st.session_state.air = max(0, st.session_state.air - 1)
with col2:
    if st.button("➕ Tambah"):
        st.session_state.air += 1
with col3:
    st.write("💧" * st.session_state.air if st.session_state.air else "🥛 Belum minum")

st.progress(min(st.session_state.air / 8, 1.0))
st.caption(f"{st.session_state.air} dari target 8 gelas")

st.subheader("Checklist aktivitas hari ini")
selesai = 0
for key, label in ACTIVITY_ITEMS.items():
    checked = st.checkbox(label, key=key)
    if checked:
        selesai += 1
st.caption(f"{selesai}/{len(ACTIVITY_ITEMS)} selesai")

st.subheader("Kalkulator BMI")
c1, c2 = st.columns(2)
with c1:
    tinggi = st.number_input("Tinggi badan (cm)", min_value=0.0, step=0.5, value=0.0)
with c2:
    berat = st.number_input("Berat badan (kg)", min_value=0.0, step=0.5, value=0.0)

if tinggi > 0 and berat > 0:
    bmi = berat / ((tinggi / 100) ** 2)
    label, tone = kategori_bmi(bmi)
    getattr(st, tone)(f"BMI kamu: **{bmi:.1f}** — {label}")

st.caption("Catatan hanya tersimpan selama sesi ini berjalan.")