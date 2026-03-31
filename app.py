import streamlit as st
import google.generativeai as genai

# 1. LLAVE Y CONFIGURACIÓN (OMAR)
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
genai.configure(api_key=API_KEY)

# NOMBRE DEL MODELO CORREGIDO PARA V1BETA
model = genai.GenerativeModel('gemini-1.5-flash-latest') 

st.set_page_config(page_title="Pino AI", page_icon="🎧")
st.title("🎧 Pino AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 2. LÓGICA DE INTERACCIÓN
if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Contexto Maestro: Aquí vive la "memoria" de quién sos
        contexto = "Sos el asistente de Omar, DJ con 20 años de exp. Su mujer es Romina. Tiene Aitana Eventos en La Plata y Pino Productions."
        
        # Generar respuesta
        response = model.generate_content(f"{contexto}\n\nChat actual: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.info("Probá actualizar la página en un momento.")
