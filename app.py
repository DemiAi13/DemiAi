import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman & Styling
st.set_page_config(page_title="Adel AI", page_icon="❤️", layout="centered")

# CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    /* Mengubah warna background utama */
    .stApp {
        background: linear-gradient(to bottom, #0f172a, #1e293b);
        color: white;
    }
    
    /* Mempercantik kotak input chat */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* Membuat header bercahaya */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* Styling untuk balon chat */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Judul dengan Gaya Baru
st.markdown('<h1 class="main-title">❤️ Adel AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Asisten Masa Depan Anda</p>", unsafe_allow_html=True)
st.divider()

# 3. Koneksi API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 4. Logika Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Chat
if prompt := st.chat_input("Apa yang bisa Adel bantu hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
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
