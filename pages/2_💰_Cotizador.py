import json
from pathlib import Path

import streamlit as st

from utils.gemini_client import get_model

st.set_page_config(page_title="Cotizador | Pino AI", page_icon="💰", layout="wide")
st.title("💰 Cotizador de Eventos")

PRECIOS_PATH = Path(__file__).resolve().parent.parent / "config" / "precios.json"


def ar_money(valor: float) -> str:
    """Formatea un número como pesos argentinos: $150.000"""
    return f"${valor:,.0f}".replace(",", ".")


@st.cache_data
def cargar_precios():
    with open(PRECIOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


precios = cargar_precios()
st.info(precios["nota"])

servicios = precios["servicios"]

with st.form("form_cotizacion"):
    st.subheader("Datos del cliente")
    col1, col2 = st.columns(2)
    with col1:
        nombre_cliente = st.text_input("Nombre del cliente")
        tipo_evento = st.text_input("Tipo de evento", placeholder="Ej: cumpleaños 15, casamiento, corporativo")
    with col2:
        fecha_evento = st.date_input("Fecha del evento")
        invitados = st.number_input("Cantidad de invitados (aprox.)", min_value=0, step=10)

    st.subheader("Servicios")
    seleccion = {}
    for key, s in servicios.items():
        if key == "hora_extra":
            continue
        seleccion[key] = st.checkbox(f"{s['nombre']} — {ar_money(s['precio_base'])} ({s['unidad']})")

    horas_extra = st.number_input(
        f"Horas extra ({ar_money(servicios['hora_extra']['precio_base'])} c/u)",
        min_value=0,
        step=1,
    )

    submitted = st.form_submit_button("Calcular presupuesto", type="primary")

if submitted:
    items = []
    total = 0
    for key, incluido in seleccion.items():
        if incluido:
            precio = servicios[key]["precio_base"]
            items.append((servicios[key]["nombre"], precio))
            total += precio

    if horas_extra:
        precio_horas = horas_extra * servicios["hora_extra"]["precio_base"]
        items.append((f"{horas_extra} hora(s) extra", precio_horas))
        total += precio_horas

    combo = len(items) >= 2
    descuento = 0
    if combo:
        descuento = round(total * precios["combo_descuento_pct"] / 100)

    total_final = total - descuento

    st.subheader("Resumen del presupuesto")
    if not items:
        st.warning("No seleccionaste ningún servicio.")
    else:
        for nombre, precio in items:
            st.write(f"- {nombre}: {ar_money(precio)}")
        if descuento:
            st.write(
                f"- Descuento combo ({precios['combo_descuento_pct']}%): -{ar_money(descuento)}"
            )
        st.markdown(f"### Total: {ar_money(total_final)}")

        model = get_model()
        if model is not None:
            with st.spinner("Redactando mensaje para el cliente..."):
                lineas_servicios = chr(10).join(f"- {n}: {ar_money(p)}" for n, p in items)
                linea_descuento = (
                    f"Descuento combo aplicado: {ar_money(descuento)}" if descuento else ""
                )
                prompt = f"""
Redactá un mensaje corto de WhatsApp para enviarle a un cliente llamado
"{nombre_cliente or 'el cliente'}" con el presupuesto de su evento
"{tipo_evento or 'evento'}" el {fecha_evento} para aprox. {invitados} invitados.

Servicios incluidos:
{lineas_servicios}
{linea_descuento}
Total: {ar_money(total_final)}

Tono cercano, profesional, cerrando con una pregunta para avanzar con la reserva
(seña / fecha). No inventes datos de contacto ni condiciones que no te di.
"""
                try:
                    response = model.generate_content(prompt)
                    st.subheader("Mensaje sugerido para WhatsApp")
                    st.code(response.text, language=None)
                except Exception as e:
                    st.error(f"No se pudo generar el mensaje: {e}")
