# app.py
import os
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
from services.sbif_client import fetch_dollar_month, latest_quote

st.set_page_config(page_title="Dólar SBIF – Consulta mensual", page_icon="💸", layout="centered")
st.title("💸 Dólar (SBIF) – Consulta mensual (SBIF)")
st.caption("Selecciona un período, consulta la API y grafica con Matplotlib.")

# --- Filtros de período ---
col1, col2 = st.columns(2)

with col1:
    years = list(range(2010, datetime.now().year + 1))[::-1]
    year = st.selectbox("Año", years, index=0)

with col2:
    month_labels = [
        "01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril",
        "05 - Mayo", "06 - Junio", "07 - Julio", "08 - Agosto",
        "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"
    ]

    month = st.selectbox("Mes", month_labels, index=datetime.now().month - 1)
    month_num = int(month.split(" - ")[0])

# --- API Key ---
default_key = st.secrets.get("SBIF_API_KEY", os.getenv("SBIF_API_KEY", ""))

api_key = st.text_input(
    "API Key SBIF",
    value=default_key,
    type="password",
    help="Se debe almacenar en .streamlit/secrets.toml (SBIF_API_KEY) o variable de entorno SBIF_API_KEY."
)

# --- Botón de acción ---
consultar = st.button("🔎 Consultar")

if consultar:
    if not api_key:
        st.error("Por favor ingresa tu **API Key**.")
        st.stop()

    with st.spinner("Consultando API SBIF..."):
        try:
            quotes = fetch_dollar_month(year, month_num, api_key)

            if not quotes:
                st.warning("No se encontraron datos para el período seleccionado.")
                st.stop()

            # Tabla
            st.subheader("Datos")
            st.dataframe(
                [{"Fecha": q.date.strftime("%Y-%m-%d"), "Dólar (CLP)": q.value} for q in quotes],
                use_container_width=True
            )

            # Gráfico con Matplotlib (sin estilos ni colores personalizados)
            st.subheader("Gráfico (Matplotlib)")

            fechas = [q.date for q in quotes]
            valores = [q.value for q in quotes]

            fig, ax = plt.subplots()

            ax.plot(fechas, valores, marker="o")
            ax.set_title(f"Dólar observado – {year}-{month_num:02d}")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Valor (CLP)")
            ax.grid(True, linestyle="--", alpha=0.5)

            st.pyplot(fig)

            # Último valor
            last = latest_quote(quotes)
            
            if last:
                st.success(f"Último valor del período ({last.date.strftime('%Y-%m-%d')}): **{last.value:.2f} CLP**")

        except Exception as e:
            st.error(f"Ocurrió un problema: {e}")
