import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Configuración de Página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard ENIGH - Desigualdad y Gasto en México",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard ENIGH: Desigualdad de Ingreso y Estructura de Gasto")
st.markdown("""
*Análisis relacional y econométrico basado en la Encuesta Nacional de Ingresos y Gastos de los Hogares (INEGI).*
---
""")

# ---------------------------------------------------------
# Carga de Datos (con Caché)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # Intentar cargar dataset local
        df = pd.read_csv("data/concentradohogar.csv")
    except Exception:
        try:
            df = pd.read_csv("concentradohogar.csv")
        except Exception:
            st.warning("⚠️ No se encontró el archivo 'concentradohogar.csv' en 'data/'. Mostrando datos demostrativos.")
            # Generar datos demostrativos
            np.random.seed(42)
            n = 5000
            ing = np.random.exponential(scale=25000, size=n) + 3000
            df = pd.DataFrame({
                'folioviv': np.random.randint(100000, 999999, size=n),
                'foliohog': 1,
                'ubica_geo': np.random.choice([14001, 9001, 15001, 19001], size=n),
                'factor': np.random.randint(100, 300, size=n),
                'ing_cor': ing,
                'gasto_mon': ing * np.random.uniform(0.5, 0.9, size=n),
                'alimentos': ing * np.random.uniform(0.2, 0.5, size=n),
                'educa_espa': ing * np.random.uniform(0.05, 0.2, size=n),
                'transporte': ing * np.random.uniform(0.1, 0.25, size=n),
                'salud': ing * np.random.uniform(0.02, 0.1, size=n)
            })
    
    # Asegurar columna entidad
    if 'entidad' not in df.columns and 'ubica_geo' in df.columns:
        df['entidad'] = (df['ubica_geo'] // 1000).astype(int)
    elif 'entidad' not in df.columns:
        df['entidad'] = 14
        
    return df

df_raw = load_data()

# ---------------------------------------------------------
# Funciones Econométricas
# ---------------------------------------------------------
def calculate_gini(income, weights):
    df_sorted = pd.DataFrame({'inc': income, 'w': weights}).dropna().sort_values('inc')
    cum_w = np.cumsum(df_sorted['w'])
    cum_inc_w = np.cumsum(df_sorted['inc'] * df_sorted['w'])
    
    total_w = cum_w.iloc[-1]
    total_inc = cum_inc_w.iloc[-1]
    
    p = cum_w / total_w
    l = cum_inc_w / total_inc
    
    gini = 1 - np.sum((p.values[1:] - p.values[:-1]) * (l.values[1:] + l.values[:-1]))
    return gini, p, l

# ---------------------------------------------------------
# Sidebar - Filtros
# ---------------------------------------------------------
st.sidebar.header("🔍 Filtros de Análisis")

region_filter = st.sidebar.selectbox(
    "Selecciona Entidad / Región:",
    ["Nacional (Todos)", "Jalisco (Entidad 14)", "Resto del País"]
)

if region_filter == "Jalisco (Entidad 14)":
    df_filtered = df_raw[df_raw['entidad'] == 14].copy()
elif region_filter == "Resto del País":
    df_filtered = df_raw[df_raw['entidad'] != 14].copy()
else:
    df_filtered = df_raw.copy()

# Asignación de Deciles
df_filtered = df_filtered.sort_values('ing_cor').reset_index(drop=True)
df_filtered['cum_factor'] = np.cumsum(df_filtered['factor'])
df_filtered['decil'] = pd.qcut(df_filtered['cum_factor'], q=10, labels=[f"D{i}" for i in range(1, 11)])

# ---------------------------------------------------------
# KPIs Principales
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_hogares = (df_filtered['factor']).sum()
ingreso_medio = (df_filtered['ing_cor'] * df_filtered['factor']).sum() / total_hogares
gasto_medio = (df_filtered['gasto_mon'] * df_filtered['factor']).sum() / total_hogares
gini_score, p_val, l_val = calculate_gini(df_filtered['ing_cor'], df_filtered['factor'])

with col1:
    st.metric("Hogares Representados", f"{total_hogares:,.0f}")
with col2:
    st.metric("Ingreso Trimestral Medio", f"${ingreso_medio:,.2f} MXN")
with col3:
    st.metric("Gasto Trimestral Medio", f"${gasto_medio:,.2f} MXN")
with col4:
    st.metric("Coeficiente de Gini", f"{gini_score:.4f}")

st.markdown("---")

# ---------------------------------------------------------
# Pestañas Analíticas
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📉 Desigualdad y Lorenz", "🍕 Ley de Engel (Gasto)", "🇲🇽 Comparativa Jalisco"])

with tab1:
    st.subheader("Curva de Lorenz e Ingreso por Decil")
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_lorenz = go.Figure()
        fig_lorenz.add_trace(go.Scatter(x=p_val, y=l_val, mode='lines', name=f'Curva de Lorenz (Gini={gini_score:.3f})', line=dict(color='#1f77b4', width=3)))
        fig_lorenz.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Igualdad Perfecta', line=dict(color='red', dash='dash')))
        fig_lorenz.update_layout(
            title="Curva de Lorenz",
            xaxis_title="Proporción Acumulada de Hogares",
            yaxis_title="Proporción Acumulada del Ingreso",
            template="plotly_white"
        )
        st.plotly_chart(fig_lorenz, use_container_width=True)
        
    with col_b:
        decil_summary = df_filtered.groupby('decil', observed=False).apply(
            lambda x: pd.Series({
                'Ingreso Promedio': (x['ing_cor'] * x['factor']).sum() / x['factor'].sum(),
                'Gasto Promedio': (x['gasto_mon'] * x['factor']).sum() / x['factor'].sum()
            })
        ).reset_index()
        
        fig_deciles = px.bar(
            decil_summary, x='decil', y=['Ingreso Promedio', 'Gasto Promedio'],
            barmode='group',
            title="Ingreso vs. Gasto Promedio por Decil (Trimestral)",
            labels={'value': 'Monto ($ MXN)', 'decil': 'Decil de Ingreso'},
            template="plotly_white"
        )
        st.plotly_chart(fig_deciles, use_container_width=True)

with tab2:
    st.subheader("Estructura del Gasto: Ley de Engel")
    st.write("Análisis de la proporción del gasto destinada a Alimentos Básicos vs. Educación y Esparcimiento por decil.")
    
    engel_summary = df_filtered.groupby('decil', observed=False).apply(
        lambda x: pd.Series({
            '% Alimentos': (x['alimentos'] * x['factor']).sum() / (x['gasto_mon'] * x['factor']).sum() * 100,
            '% Educación/Esparcimiento': (x['educa_espa'] * x['factor']).sum() / (x['gasto_mon'] * x['factor']).sum() * 100
        })
    ).reset_index()
    
    fig_engel = px.bar(
        engel_summary, x='decil', y=['% Alimentos', '% Educación/Esparcimiento'],
        barmode='group',
        color_discrete_sequence=['#d62728', '#2ca02c'],
        title="Proporción del Gasto por Decil (%)",
        labels={'value': 'Porcentaje del Gasto Total (%)', 'decil': 'Decil'},
        template="plotly_white"
    )
    st.plotly_chart(fig_engel, use_container_width=True)

with tab3:
    st.subheader("Jalisco vs. Promedio Nacional")
    
    df_raw['region_label'] = np.where(df_raw['entidad'] == 14, 'Jalisco', 'Resto del País')
    
    comp_summary = df_raw.groupby('region_label').apply(
        lambda x: pd.Series({
            'Ingreso Promedio': (x['ing_cor'] * x['factor']).sum() / x['factor'].sum(),
            'Gasto Promedio': (x['gasto_mon'] * x['factor']).sum() / x['factor'].sum(),
            '% Gasto Alimentos': (x['alimentos'] * x['factor']).sum() / (x['gasto_mon'] * x['factor']).sum() * 100
        })
    ).reset_index()
    
    col_c, col_d = st.columns(2)
    with col_c:
        fig_comp_ing = px.bar(
            comp_summary, x='region_label', y='Ingreso Promedio',
            color='region_label', text_auto='.2f',
            title="Ingreso Medio Trimestral ($ MXN)",
            template="plotly_white"
        )
        st.plotly_chart(fig_comp_ing, use_container_width=True)
        
    with col_d:
        fig_comp_food = px.bar(
            comp_summary, x='region_label', y='% Gasto Alimentos',
            color='region_label', text_auto='.2f',
            title="% del Gasto Destinado a Alimentos",
            template="plotly_white"
        )
        st.plotly_chart(fig_comp_food, use_container_width=True)
