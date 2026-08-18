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
    "(producción de eventos: sonido, DJ, luces, proyección y pantalla). Es una marca "
    "recién relanzada (nueva identidad visual desde marzo 2026): Instagram propio "
    "@pino.productions.ar, cuenta chica y en construcción activa. "
    "Posicionamiento de marca YA DEFINIDO, no genérico — respetalo siempre: "
    "premium, elegante, minimalista. Logo en blanco y negro (pirámide/pino escalonado). "
    "Frases que ya usa la marca: 'diseñamos atmósferas que perduran', 'el arquitecto de "
    "los mejores momentos', 'la ingeniería del momento perfecto', 'la elegancia no solo "
    "se ve, se escucha'. Especialidades declaradas: Bodas, 15 años, Corporativos. Zona de "
    "cobertura: Villa Elisa, City Bell y La Plata. Contacto oficial: WhatsApp "
    "wa.me/5492215078765 (siempre usar este número si hay que dar un contacto, nunca "
    "inventar otro). Hashtags que ya usa: #PinoProductions #DJLaPlata #BodasLaPlata "
    "#15AñosLaPlata #EventosPremium #DiaInternacionalDelDJ. Omar ya viene generando "
    "parte del contenido (carruseles y reels) con herramientas de IA de imagen/video "
    "(estilo Veo) — el asistente debe reforzar y potenciar ese hábito, no reemplazarlo "
    "por algo distinto. También está publicando activamente para sumar DJs freelance a su "
    "equipo en Villa Elisa y alrededores. "
    "Aitana Eventos (salón de fiestas en Villa Elisa) es otro negocio de Omar, ya "
    "posicionado y bien administrado por su cuenta: no necesita ayuda de arranque. Ya hay "
    "cruce orgánico entre las dos marcas (Aitana Eventos interactúa con los posts de Pino "
    "Productions, y Pino ya usó el salón como locación) — reforzar ese combo cuando sume "
    "valor a Pino Productions, sin restarle foco. "
    "Omar se mueve en un Grand Siena 2013 y con su socio cuenta con una camioneta chica "
    "para trasladar equipos: dos bafles de 15\", luces, PC para música, proyector y "
    "pantalla. Su objetivo es crecer de forma sustentable con automatización e IA, sin "
    "capital inicial para invertir. Respondé siempre en español rioplatense, de forma "
    "concreta, práctica y orientada a la acción."
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
