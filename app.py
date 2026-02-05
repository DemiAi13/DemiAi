import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Demi AI - Teman Belajar",
    page_icon="🎓",
    layout="centered"
)

# 2. Desain Tampilan (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: white;
    }
    .main-title {
        text-align: center;
        color: #38BDF8;
        font-family: 'Helvetica';
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 class='main-title'>🎓 Demi AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Tanyakan apa saja, kita pelajari bersama.</p>", unsafe_allow_html=True)
st.divider()

# 4. Logika Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya Demi. Materi apa yang ingin kamu kuasai hari ini?"}
    ]

# Tampilkan chat yang sudah ada
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input User
if prompt := st.chat_input("Contoh: Jelaskan cara kerja fotosintesis"):
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon Demi (Simulasi AI)
    with st.chat_message("assistant"):
        response = f"Demi sedang berpikir tentang '{prompt}'... \n\n(Hubungkan API Key Gemini/OpenAI untuk jawaban asli)."
        st.markdown(response)
    
    # Simpan respon asisten
    st.session_state.messages.append({"role": "assistant", "content": response})
