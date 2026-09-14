"""
Ejemplo de dashboard Streamlit para el proyecto ENIGH.
Estructura base: conecta a MySQL, filtra, grafica con Plotly.
Ejecutar con: streamlit run dashboard_enigh_ejemplo.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# --- Configuración de página ---
st.set_page_config(page_title="ENIGH 2024 - Análisis de Ingreso y Gasto", layout="wide")
st.title("Distribución de Ingreso y Gasto en México (ENIGH 2024)")
st.caption("Fuente: INEGI, microdatos ENIGH 2024. ~91,414 hogares.")

# --- Conexión a datos ---
@st.cache_data
def cargar_datos():
    conn = mysql.connector.connect(
        host="localhost",
        user="tu_usuario",
        password="tu_password",
        database="enigh_db"
    )
    query = """
        SELECT ch.folioviv, ch.foliohog, ch.ing_cor, ch.gasto_mon,
               ch.est_dis, p.edad, p.sexo, p.nivelaprob
        FROM concentradohogar ch
        JOIN poblacion p ON ch.folioviv = p.folioviv AND ch.foliohog = p.foliohog
        WHERE p.parentesco = 101  -- jefe de hogar
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Deciles de ingreso
    df["decil_ingreso"] = pd.qcut(df["ing_cor"], 10, labels=range(1, 11))
    return df

df = cargar_datos()

# --- Filtros en barra lateral ---
st.sidebar.header("Filtros")

estados = st.sidebar.multiselect(
    "Estado", options=sorted(df["est_dis"].unique()), default=None
)
nivel_edu = st.sidebar.multiselect(
    "Nivel educativo del jefe de hogar", options=sorted(df["nivelaprob"].dropna().unique())
)

df_filtrado = df.copy()
if estados:
    df_filtrado = df_filtrado[df_filtrado["est_dis"].isin(estados)]
if nivel_edu:
    df_filtrado = df_filtrado[df_filtrado["nivelaprob"].isin(nivel_edu)]

# --- KPIs principales ---
col1, col2, col3 = st.columns(3)
col1.metric("Hogares analizados", f"{len(df_filtrado):,}")
col2.metric("Ingreso corriente promedio", f"${df_filtrado['ing_cor'].mean():,.0f}")
col3.metric("Gasto monetario promedio", f"${df_filtrado['gasto_mon'].mean():,.0f}")

# --- Gráfico 1: Ingreso promedio por decil ---
ingreso_decil = df_filtrado.groupby("decil_ingreso", observed=True)["ing_cor"].mean().reset_index()
fig1 = px.bar(
    ingreso_decil, x="decil_ingreso", y="ing_cor",
    title="Ingreso corriente promedio por decil",
    labels={"decil_ingreso": "Decil", "ing_cor": "Ingreso corriente promedio ($)"}
)
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico 2: Participación del gasto por decil ---
gasto_decil = df_filtrado.groupby("decil_ingreso", observed=True)["gasto_mon"].sum().reset_index()
gasto_decil["participacion_%"] = 100 * gasto_decil["gasto_mon"] / gasto_decil["gasto_mon"].sum()
fig2 = px.pie(
    gasto_decil, names="decil_ingreso", values="participacion_%",
    title="Participación del gasto total por decil de ingreso"
)
st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: Ingreso vs nivel educativo ---
fig3 = px.box(
    df_filtrado, x="nivelaprob", y="ing_cor",
    title="Ingreso corriente por nivel educativo del jefe de hogar",
    labels={"nivelaprob": "Nivel educativo (código INEGI)", "ing_cor": "Ingreso corriente ($)"}
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.caption("Proyecto de portafolio | Datos: INEGI ENIGH 2024 | Autor: Jesús Copado")
