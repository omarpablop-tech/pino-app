import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN (OMAR)
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
genai.configure(api_key=API_KEY)

# Probamos con el nombre estándar que es el más compatible
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Pino AI", page_icon="🎧")

# Estilo Aitana Eventos
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

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 2. LÓGICA
if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Tu contexto de DJ y familia
        contexto = "Sos el asistente de Omar, DJ con 20 años de experiencia. Su mujer es Romina. Maneja Aitana Eventos y Pino Productions en La Plata."
        
        # Intentar generar respuesta
        response = model.generate_content(f"{contexto}\n\nPregunta: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error de API: {e}")
        st.info("Omar, si persiste el error, es probable que la API Key necesite un minuto para activarse.")
