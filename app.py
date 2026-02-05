import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman & Tema Meriah
st.set_page_config(page_title="Adel AI", page_icon="💜", layout="centered")

# CSS untuk tampilan "Purple Love" (Tetap seperti permintaan sebelumnya)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #1e1b4b, #4c1d95);
        color: white;
    }
    .stApp::before { content: "💜"; position: absolute; top: 10px; left: 20px; font-size: 40px; }
    .stApp::after { content: "💜"; position: absolute; top: 10px; right: 20px; font-size: 40px; }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: #f5d0fe;
        text-shadow: 0 0 20px #a855f7, 0 0 30px #d8b4fe;
        margin-top: 20px;
    }
    .sub-title { text-align: center; color: #e9d5ff; font-style: italic; margin-bottom: 30px; }
    
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        border: 1px solid #d8b4fe !important;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Judul
st.markdown('<h1 class="main-title">💜 Adel AI 💜</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Asisten Pintar yang Selalu Ingat Pesanmu</p>', unsafe_allow_html=True)
st.divider()

# 3. Inisialisasi Memori Chat (Mirip Gemini)
# Ini berfungsi agar chat tersimpan selama sesi browser aktif
if "chat_session" not in st.session_state:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    # Memulai sesi chat baru
    st.session_state.chat_session = model.start_chat(history=[])

# 4. Menampilkan Riwayat Chat dari Sesi
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. Input Chat & Proses Jawaban
if prompt := st.chat_input("Tanyakan sesuatu ke Adel..."):
    # Menampilkan pesan user di layar
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mengirim pesan ke AI dan mendapatkan jawaban
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Adel sedang berpikir keras: {e}")
