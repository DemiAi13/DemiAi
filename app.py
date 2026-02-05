import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Demi AI - Teman Belajar", page_icon="🎓")

# Menghubungkan ke API Key dari Secrets Streamlit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key belum terpasang di Secrets!")

# 2. Desain Tampilan (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: white; }
    .main-title { text-align: center; color: #38BDF8; font-family: 'Helvetica'; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🤪 Demi AI</h1>", unsafe_allow_html=True)
st.divider()

# 3. Logika Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Proses Jawaban AI
if prompt := st.chat_input("Tanyakan materi pelajaran..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-pro")
            # Instruksi agar AI menjadi teman belajar yang ramah
            full_prompt = f"Kamu adalah Demi AI, asisten belajar yang ramah untuk siswa. Jawablah pertanyaan ini: {prompt}"
            response = model.generate_content(full_prompt)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Ada kendala: {e}")
