import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Demi AI", page_icon="🎓")

# Menghubungkan ke API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key belum terpasang!")

# 2. Desain Sederhana
st.markdown("<h1 style='text-align: center; color: #38BDF8;'>🎓 Demi AI</h1>", unsafe_allow_html=True)
st.divider()

# 3. Logika Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Proses Jawaban
if prompt := st.chat_input("Tanyakan materi pelajaran..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # JURUS PAMUNGKAS: Mencari model yang tersedia otomatis
            model_name = 'gemini-1.5-flash' # Coba ini dulu
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Jika gagal, coba model alternatif 'gemini-pro'
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Waduh, koneksi ke otak AI terputus. Coba klik 'Reboot' di menu Settings Streamlit ya!")
