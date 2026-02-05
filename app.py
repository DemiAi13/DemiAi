import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman & Tema Ungu Meriah
st.set_page_config(page_title="Adel AI", page_icon="💜", layout="centered")

# CSS untuk tampilan "Purple Love" yang meriah
st.markdown("""
    <style>
    /* Background utama ungu gelap */
    .stApp {
        background: linear-gradient(to bottom, #1e1b4b, #4c1d95);
        color: white;
    }

    /* Dekorasi Love di pojok kiri dan kanan atas */
    .stApp::before {
        content: "💜";
        position: absolute;
        top: 10px;
        left: 20px;
        font-size: 40px;
    }
    .stApp::after {
        content: "💜";
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 40px;
    }
    
    /* Judul Utama yang bercahaya */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: #f5d0fe;
        text-shadow: 0 0 20px #a855f7, 0 0 30px #d8b4fe;
        margin-top: 20px;
    }

    /* Subtitle */
    .sub-title {
        text-align: center;
        color: #e9d5ff;
        font-style: italic;
        margin-bottom: 30px;
    }

    /* Kotak Chat yang lebih estetik */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        border: 1px solid #d8b4fe !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Tampilan Header
st.markdown('<h1 class="main-title">💜 Adel AI 💜</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Asisten Masa Depan Penuh Cinta</p>', unsafe_allow_html=True)
st.divider()

# 3. Konfigurasi Google AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 4. Logika Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Chat
if prompt := st.chat_input("Tanyakan sesuatu ke Adel..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Jalur paling stabil menggunakan gemini-pro
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Aduh, Adel lagi galau nih: {e}")
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Kita gunakan model yang paling stabil
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Jika error 404 muncul lagi, sistem akan mencoba model cadangan
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Adel sedang beristirahat sejenak. Coba lagi nanti ya!")
