import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE OMAR (PINO PRODUCTIONS)
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
genai.configure(api_key=API_KEY)

# ESTE ES EL MODELO MÁS COMPATIBLE EN 2026
model = genai.GenerativeModel('gemini-1.5-flash-8b')

st.set_page_config(page_title="Pino AI", page_icon="🎧")

# Estilo Aitana Eventos / Pino Productions
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 Pino AI")
st.caption("Asistente de Omar | Villa Elisa, La Plata")

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
        # Tu contexto de DJ y familia (Memoria de ADN)
        contexto = (
            "Sos el asistente personal de Omar. Omar es un DJ con 20 años de trayectoria. "
            "Su mujer es Romina. Tienen dos hijos (18 y 7 años). "
            "Es dueño de Aitana Eventos en La Plata y Pino Productions. "
            "Respondé siempre de forma profesional pero cercana, como un colega."
        )
        
        # Generar respuesta
        response = model.generate_content(f"{contexto}\n\nPregunta de Omar: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error detectado: {e}")
        st.info("Omar, si sigue el 404, cambiá 'gemini-1.5-flash-8b' por 'gemini-1.5-flash' a secas.")
