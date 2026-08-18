import pandas as pd
import streamlit as st

from utils.crm_db import (
    ESTADOS,
    actualizar_estado,
    agregar_lead,
    borrar_lead,
    init_db,
    listar_leads,
)

st.set_page_config(page_title="CRM Clientes | Pino AI", page_icon="📋", layout="wide")
st.title("📋 CRM de Clientes y Consultas")

init_db()

with st.expander("➕ Agregar nueva consulta / lead", expanded=False):
    with st.form("form_lead", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del cliente *")
            telefono = st.text_input("Teléfono / WhatsApp")
            marca = st.selectbox("Marca de interés", ["Pino Productions", "Aitana Eventos", "Combo"])
        with col2:
            tipo_evento = st.text_input("Tipo de evento")
            fecha_evento = st.date_input("Fecha tentativa del evento")
            estado = st.selectbox("Estado inicial", ESTADOS, index=0)
        notas = st.text_area("Notas")

        if st.form_submit_button("Guardar", type="primary"):
            if not nombre:
                st.warning("El nombre es obligatorio.")
            else:
                agregar_lead(nombre, telefono, tipo_evento, fecha_evento, marca, notas)
                st.success(f"Lead '{nombre}' guardado.")
                st.rerun()

st.divider()

leads = listar_leads()

if not leads:
    st.info("Todavía no cargaste ningún cliente. Usá el formulario de arriba.")
else:
    df = pd.DataFrame([dict(row) for row in leads])

    col1, col2 = st.columns(2)
    with col1:
        filtro_marca = st.multiselect("Filtrar por marca", sorted(df["marca"].dropna().unique()))
    with col2:
        filtro_estado = st.multiselect("Filtrar por estado", ESTADOS)

    df_filtrado = df.copy()
    if filtro_marca:
        df_filtrado = df_filtrado[df_filtrado["marca"].isin(filtro_marca)]
    if filtro_estado:
        df_filtrado = df_filtrado[df_filtrado["estado"].isin(filtro_estado)]

    st.subheader(f"Clientes ({len(df_filtrado)})")
    st.dataframe(
        df_filtrado[
            ["id", "nombre", "telefono", "marca", "tipo_evento", "fecha_evento", "estado", "notas"]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇️ Exportar a CSV",
        df_filtrado.to_csv(index=False).encode("utf-8"),
        file_name="clientes_pino_productions.csv",
        mime="text/csv",
    )

    st.divider()
    st.subheader("Actualizar estado de un cliente")
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        lead_id = st.selectbox(
            "Cliente",
            df["id"],
            format_func=lambda i: f"#{i} - {df.loc[df['id'] == i, 'nombre'].values[0]}",
        )
    with col2:
        nuevo_estado = st.selectbox("Nuevo estado", ESTADOS, key="nuevo_estado")
    with col3:
        st.write("")
        st.write("")
        if st.button("Actualizar"):
            actualizar_estado(lead_id, nuevo_estado)
            st.success("Estado actualizado.")
            st.rerun()

    with st.expander("🗑️ Borrar un cliente"):
        lead_a_borrar = st.selectbox(
            "Elegí el cliente a borrar",
            df["id"],
            format_func=lambda i: f"#{i} - {df.loc[df['id'] == i, 'nombre'].values[0]}",
            key="lead_borrar",
        )
        if st.button("Borrar definitivamente", type="secondary"):
            borrar_lead(lead_a_borrar)
            st.success("Cliente borrado.")
            st.rerun()

    st.divider()
    st.subheader("Resumen del embudo")
    resumen = df["estado"].value_counts().reindex(ESTADOS, fill_value=0)
    st.bar_chart(resumen)
