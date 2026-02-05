import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfigurasi Halaman & Tema
st.set_page_config(page_title="Adel AI", page_icon="💜", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #1e1b4b, #4c1d95); color: white; }
    .stApp::before { content: "💜"; position: absolute; top: 10px; left: 20px; font-size: 40px; }
    .stApp::after { content: "💜"; position: absolute; top: 10px; right: 20px; font-size: 40px; }
    .main-title { font-size: 3.5rem; font-weight: 800; text-align: center; color: #f5d0fe; text-shadow: 0 0 20px #a855f7; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; border: 1px solid #d8b4fe !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💜 Adel AI 💜</h1>', unsafe_allow_html=True)
st.divider()

# 2. Inisialisasi API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Fitur Upload Gambar (Di Sidebar atau di atas chat)
with st.sidebar:
    st.title("📸 Fitur Mata Adel")
    uploaded_file = st.file_uploader("Kirim foto muka atau gambar ke Adel...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Gambar terunggah", use_container_width=True)

# 4. Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input Chat & Logika Vision
if prompt := st.chat_input("Tanyakan sesuatu tentang fotomu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Jika ada gambar, gunakan model flash (Vision), jika tidak pakai pro
            if uploaded_file:
                model = genai.GenerativeModel('gemini-1.5-flash')
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
            else:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Aduh, Adel sulit melihat: {e}")
