import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 1. LLAVES (REVISADAS)
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
genai.configure(api_key=API_KEY)

# Usamos el modelo Pro que es más estable para estas apps
model = genai.GenerativeModel('gemini-1.5-pro') 

# 2. INTERFAZ
st.set_page_config(page_title="Pino AI", page_icon="🎧")
st.title("🎧 Pino AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 3. LÓGICA
if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Instrucción fija para que no olvide quién sos
        contexto = "Sos el asistente de Omar, DJ con 20 años de exp. Su mujer es Romina. Tiene Aitana Eventos."
        response = model.generate_content(f"{contexto}\nUsuario: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Hubo un tema con la conexión: {e}")
