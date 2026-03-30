import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# --- 1. CONFIGURACIÓN DE CLAVES (OMAR) ---
API_KEY = "AIzaSyB-5gXfxDOskyIQJBseXLRWhJ6JohZzVuA"
SPOTIFY_ID = "f15fc7dd7ef846259de5381b0ebfd2e9"
SPOTIFY_SECRET = "508e9c33b093478da144c9c103f43332"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Configuración Spotify
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --- 2. INTERFAZ TIPO APP MÓVIL ---
st.set_page_config(page_title="Pino AI Assistant", page_icon="🎧")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; max-width: 500px; margin: 0 auto; }
    .stChatMessage { border-radius: 20px; border: 1px solid #1db954; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. EL CEREBRO (MEMORIA EVOLUTIVA) ---
if "memoria_adn" not in st.session_state:
    st.session_state.memoria_adn = "Usuario: Omar. Profesión: DJ (20 años exp). Negocios: Aitana Eventos y Pino Productions. Familia: Romina e hijos."

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🎧 Pino AI")
st.caption("Asistente Personal en Evolución")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. LÓGICA DE APRENDIZAJE ---
if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # El Prompt incluye lo que la IA "ya sabe" de vos para que no lo olvide
    instruccion = f"""
    Eres el asistente personal de Omar. 
    LO QUE SABES DE ÉL HASTA AHORA: {st.session_state.memoria_adn}
    
    Tu tarea es responderle y, si menciona algo nuevo sobre sus gustos, 
    trabajo en La Plata o su familia, intégralo a tu conocimiento.
    Si pregunta por música, usa tu conocimiento de DJ profesional.
    """

    with st.chat_message("assistant"):
        response = model.generate_content(f"{instruccion}\n\nChat: {prompt}")
        output = response.text
        st.markdown(output)
    
    st.session_state.messages.append({"role": "assistant", "content": output})

    # AUTO-EVOLUCIÓN: La IA actualiza su propia base de datos sobre Omar
    evolucion = model.generate_content(f"Resumí en una frase qué aprendiste de nuevo sobre Omar en este mensaje: '{prompt}'.")
    st.session_state.memoria_adn += f" | {evolucion.text}"