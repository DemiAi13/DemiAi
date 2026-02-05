import streamlit as st
import google.generativeai as genai

# Konfigurasi API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎓 Demi AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanyakan sesuatu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Menggunakan model 'gemini-1.5-flash' tanpa embel-embel 'models/'
        model = genai.GenerativeModel('gemini-1.5-flash')
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Gagal memanggil AI: {e}")
