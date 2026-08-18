import streamlit as st

from utils.gemini_client import get_model, pedir_api_key_si_falta

st.set_page_config(page_title="Pino AI", page_icon="🎧", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #d4af37; background-color: #1a1c23; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎧 Pino AI")
st.caption("Asistente central — Pino Productions & Aitana Eventos | Omar, Villa Elisa")

with st.sidebar:
    st.header("Pino Productions")
    st.write(
        "Usá el menú de arriba para pasar a:\n\n"
        "- **Generador de Contenido**: posts e ideas para Instagram\n"
        "- **Cotizador**: presupuestos automáticos para eventos\n"
        "- **CRM Clientes**: seguimiento de consultas y clientes\n\n"
        "El plan de negocio completo está en `BUSINESS_PLAN.md`."
    )

model = get_model()
if model is None:
    pedir_api_key_si_falta()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("¿Qué armamos hoy, Omar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error en la mezcla: {e}")
