import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE OMAR
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
genai.configure(api_key=API_KEY)

# --- FUNCIÓN DE AUTO-DETECCIÓN (Para matar el error 404) ---
@st.cache_resource
def detectar_modelo():
    try:
        # Le pedimos a tu cuenta la lista de modelos que REALMENTE tenés
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Prioridad para los modelos más modernos de 2026
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro', 'models/gemini-1.0-pro']:
            if target in modelos_disponibles:
                return target
        return modelos_disponibles[0] # Si no están los de arriba, usa el primero que encuentre
    except Exception as e:
        return f"Error al listar: {e}"

modelo_final = detectar_modelo()
model = genai.GenerativeModel(modelo_final)

# --- INTERFAZ ESTILO DJ / AITANA ---
st.set_page_config(page_title="Pino AI", page_icon="🎧")
st.markdown("<style>.stApp { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

st.title("🎧 Pino AI")
st.caption(f"Modelo activo: {modelo_final}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- CEREBRO EVOLUTIVO ---
if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Tu ADN: Familia, Negocios y Trayectoria
        contexto = (
            "Eres el asistente personal de Omar, DJ con 20 años de trayectoria. "
            "Su mujer es Romina y tienen dos hijos (18 y 7 años). "
            "Maneja Aitana Eventos en La Plata y su marca Pino Productions. "
            "Tu misión es aprender de él y evolucionar en cada charla."
        )
        
        response = model.generate_content(f"{contexto}\n\nPregunta: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Se cortó el cable: {e}")
