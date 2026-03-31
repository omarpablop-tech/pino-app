import streamlit as st
import google.generativeai as genai

# 1. EL "ADN" DE PINO PRODUCTIONS
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
genai.configure(api_key=API_KEY)

# Aquí está el truco: sin el 'models/' adelante para que no tire error de formato
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Pino AI", page_icon="🎧", layout="centered")

# Estilo Aitana Eventos (Dorado y Negro)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d4af37; background-color: #1a1c23; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 Pino AI")
st.subheader("Asistente Personal de Omar")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Historial de la charla
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 2. LÓGICA DE APRENDIZAJE
if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Tu contexto Maestro: Esto es lo que la IA "sabe" de vos
        contexto = (
            "Actúa como el asistente personal de Omar, DJ con 20 años de experiencia. "
            "Su mujer es Romina. Tienen dos hijos (uno de 18 y una de 7). "
            "Es dueño de Aitana Eventos en La Plata y de la productora Pino Productions. "
            "Él es de Villa Elisa. Sé profesional, creativo y recordá sus gustos musicales."
        )
        
        # Petición limpia a la IA
        full_query = f"{contexto}\n\nChat histórico:\n{st.session_state.messages}\n\nNueva pregunta: {prompt}"
        response = model.generate_content(full_query)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error("Hubo un salto en el disco (Error de conexión).")
        st.info(f"Detalle técnico para Omar: {e}")
