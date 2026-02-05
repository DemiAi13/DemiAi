import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi
st.set_page_config(page_title="Adel AI", page_icon="♥️")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Fungsi untuk mencari model yang aktif otomatis
@st.cache_resource
def get_working_model():
    # Mencari semua model yang mendukung 'generateContent'
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return "gemini-1.5-flash" # fallback

st.title("♥️ Adel Ai")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanyakan materi pelajaran..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Memanggil model yang terdeteksi aktif
            active_model_name = get_working_model()
            model = genai.GenerativeModel(active_model_name)

            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error sistem: {e}")
            st.info("Saran: Pastikan API Key di Secrets sudah benar tanpa spasi.")
