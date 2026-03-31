import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE OMAR
# Tu clave está perfecta, no la toques
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
genai.configure(api_key=API_KEY)

# USAMOS EL MODELO ESTÁNDAR "GEMINI-PRO" (EL MÁS COMPATIBLE)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Pino AI", page_icon="🎧")

# Estilo Aitana Eventos / Pino Productions
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 Pino AI")
st.caption("Asistente de Omar | DJ & Eventos")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 2. LÓGICA DE RESPUESTA
if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Contexto Maestro (Tu ADN de usuario)
        contexto = "Sos el asistente de Omar, DJ con 20 años de experiencia. Su mujer es Romina. Maneja Aitana Eventos y Pino Productions en La Plata."
        
        # Generar respuesta con el modelo Pro
        response = model.generate_content(f"{contexto}\n\nPregunta: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error detectado: {e}")
        st.info("Omar, si dice 'Model not found', probá cambiar 'gemini-pro' por 'gemini-1.0-pro' en el código.")
