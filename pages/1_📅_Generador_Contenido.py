import streamlit as st

from utils.gemini_client import get_model, pedir_api_key_si_falta

st.set_page_config(page_title="Generador de Contenido | Pino AI", page_icon="📅", layout="wide")
st.title("📅 Generador de Contenido para Instagram")
st.caption("Pensado para @pino.productions.ar y @aitanaeventosok")

model = get_model()
if model is None:
    pedir_api_key_si_falta()

TIPOS_POST = [
    "Recap de evento (después de trabajar)",
    "Anuncio / promoción de fecha disponible",
    "Detrás de escena (armado de equipo, sonido, luces)",
    "Testimonio de cliente",
    "Combo Pino Productions + Salón Aitana",
    "Reel de tendencia adaptado al rubro",
    "Post educativo (tips para organizar un evento)",
    "Búsqueda de DJs/talento para el equipo",
]

HASHTAGS_BASE = (
    "#PinoProductions #DJLaPlata #BodasLaPlata #15AñosLaPlata #EventosPremium "
    "#DiaInternacionalDelDJ"
)

with st.form("form_contenido"):
    col1, col2 = st.columns(2)
    with col1:
        marca = st.selectbox("Marca", ["Pino Productions", "Aitana Eventos", "Combo (las dos)"])
        tipo_post = st.selectbox("Tipo de contenido", TIPOS_POST)
        tono = st.select_slider(
            "Tono",
            options=["Premium / elegante (el actual de la marca)", "Cercano", "Divertido / picante"],
            value="Premium / elegante (el actual de la marca)",
        )
    with col2:
        evento = st.text_input(
            "Detalles del evento o tema (opcional)",
            placeholder="Ej: cumple de 15 en el salón, tematica neón, 150 invitados",
        )
        cantidad = st.slider("Cantidad de variantes", 1, 5, 3)

    submitted = st.form_submit_button("Generar contenido", type="primary")

if submitted:
    prompt = f"""
Generá {cantidad} variantes de posteo para Instagram de la marca "{marca}".

Tipo de contenido: {tipo_post}
Tono: {tono}
Detalles del evento/tema: {evento or "no especificado, usá algo genérico y creíble para el rubro"}

Respetá la identidad ya establecida de Pino Productions: premium, elegante, minimalista.
Frases que ya usa la marca (usalas como referencia de estilo, no las repitas literal siempre):
"diseñamos atmósferas que perduran", "el arquitecto de los mejores momentos",
"la ingeniería del momento perfecto". Cubre Villa Elisa, City Bell y La Plata.

Para cada variante dame:
1. Un texto de caption (2 a 5 líneas, con emojis con moderación, que enganche en el primer renglón)
2. Una línea aparte con 12-15 hashtags: incluí siempre estos como base — {HASHTAGS_BASE} —
   y sumale 6-9 más relevantes para eventos, DJs y salones de fiestas en La Plata / Villa
   Elisa / City Bell, Buenos Aires, Argentina
3. Una idea de imagen o video corta para acompañar el post
4. Un prompt corto para generar esa imagen/video con una herramienta de IA (estilo Veo/Sora/
   generador de imágenes), listo para copiar y pegar

Separá cada variante con un título "Variante N" y una línea divisoria.
No inventes datos de contacto ni precios. Si hace falta un contacto, usá wa.me/5492215078765.
"""
    with st.spinner("Generando ideas..."):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"No se pudo generar el contenido: {e}")

st.divider()
st.subheader("Calendario semanal sugerido")
st.write(
    "Para no depender de la inspiración del momento, publicá con esta frecuencia base "
    "(ajustable según la temporada de eventos):"
)
st.table(
    {
        "Día": ["Lunes", "Miércoles", "Viernes", "Domingo"],
        "Contenido": [
            "Detrás de escena / armado de equipo",
            "Recap de evento reciente (foto o reel)",
            "Promoción de fecha disponible / combo",
            "Testimonio o video corto de la semana",
        ],
    }
)
