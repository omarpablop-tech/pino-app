"""Cliente compartido de Gemini para todas las páginas de Pino AI."""
import os

import google.generativeai as genai
import streamlit as st

MODELOS_PREFERIDOS = [
    "models/gemini-2.0-flash",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-1.0-pro",
]

CONTEXTO_MARCA = (
    "Sos el asistente de IA de Omar, DJ con 20 años de experiencia en Villa Elisa, "
    "La Plata, Argentina. La prioridad número uno es hacer crecer 'Pino Productions' "
    "(producción de eventos, sonido, DJ, luces, proyección y pantalla), que recién está "
    "arrancando como empresa formal aunque ya tiene marca, logo, equipo e Instagram "
    "propio (@pino.productions.ar) — ahí va la mayor parte de la energía. Aitana Eventos "
    "(salón de fiestas en Villa Elisa) es otro negocio de Omar, ya posicionado y bien "
    "administrado por su cuenta: no necesita ayuda de arranque, solo se menciona como "
    "posible combo cuando sume valor a Pino Productions, sin restarle foco. Omar se mueve "
    "en un Grand Siena 2013 y con su socio cuenta con una camioneta chica para trasladar "
    "equipos: dos bafles de 15\", luces, PC para música, proyector y pantalla. Su objetivo "
    "es crecer de forma sustentable con automatización e IA, sin capital inicial para "
    "invertir. Respondé siempre en español rioplatense, de forma concreta, práctica y "
    "orientada a la acción."
)


def obtener_api_key() -> str | None:
    """Busca la API key en st.secrets primero, después en variables de entorno."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY")


@st.cache_resource
def obtener_modelo_vivo(api_key: str):
    genai.configure(api_key=api_key)
    try:
        modelos = [
            m.name
            for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        for target in MODELOS_PREFERIDOS:
            if target in modelos:
                return target
        return modelos[0] if modelos else MODELOS_PREFERIDOS[0]
    except Exception:
        return MODELOS_PREFERIDOS[0]


def get_model():
    """Devuelve una instancia de GenerativeModel lista para usar, o None si falta la key."""
    api_key = obtener_api_key()
    if not api_key:
        return None
    modelo_seleccionado = obtener_modelo_vivo(api_key)
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(modelo_seleccionado, system_instruction=CONTEXTO_MARCA)


def pedir_api_key_si_falta():
    """Muestra un aviso claro en la UI si no hay API key configurada."""
    st.error(
        "⚠️ Falta configurar la API key de Gemini.\n\n"
        "1. Conseguí una gratis en https://aistudio.google.com/apikey\n"
        "2. Local: copiá `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml` "
        "y pegá tu key ahí.\n"
        "3. En Streamlit Community Cloud: Settings → Secrets → agregá "
        "`GEMINI_API_KEY = \"tu-key\"`."
    )
    st.stop()
