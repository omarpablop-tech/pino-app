import streamlit as st
import google.generativeai as genai

# 1. CONEXIÓN DE OMAR (PINO PRODUCTIONS)
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
genai.configure(api_key=API_KEY)

# --- ESCANEO AUTOMÁTICO DE MODELOS ---
@st.cache_resource
def obtener_modelo_vivo():
    try:
        # Listamos los modelos que Google le da a tu cuenta
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Prioridad 2026: Buscamos los más modernos
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-2.0-flash', 'models/gemini-1.0-pro']:
            if target in modelos:
                return target
        return modelos[0] # Si no encuentra los de arriba, agarra el primero que haya
    except Exception:
        return "gemini-1.5-flash" # Fallback por si falla el escaneo

modelo_seleccionado = obtener_modelo_vivo()
model = genai.GenerativeModel(modelo_seleccionado)

# --- INTERFAZ ESTILO DJ / AITANA EVENTOS ---
st.set_page_config(page_title="Pino AI", page_icon="🎧")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d4af37; background-color: #1a1c23; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 Pino AI")
st.caption(f"Conectado con: {modelo_seleccionado} | Omar - Villa Elisa")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- LÓGICA DE APRENDIZAJE ---
if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Contexto Maestro (Tu identidad)
        contexto = (
            "Sos el asistente de Omar, DJ con 20 años de exp. Su mujer es Romina. "
            "Tienen dos hijos (18 y 7 años). Maneja Aitana Eventos y Pino Productions en La Plata. "
            "Aprendé de esta charla y ayudalo con sus eventos y música."
        )
        
        response = model.generate_content(f"{contexto}\n\nPregunta: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error en la mezcla: {e}")
