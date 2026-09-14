# 📊 Análisis Econométrico y Dashboard de Desigualdad en México (ENIGH - INEGI)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enigh-desigualdad-sql-python-j3zetuydc9ejumv5uatjij.streamlit.app/)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue?style=flat&logo=mysql)
![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=flat&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)

> 🌐 **Dashboard Interactivo en Vivo**: [Haz clic aquí para interactuar con la aplicación web en Streamlit](https://enigh-desigualdad-sql-python-j3zetuydc9ejumv5uatjij.streamlit.app/)

---

## 📌 Descripción del Proyecto

Este proyecto combina **econometría aplicada**, **consultas avanzadas en SQL**, **procesamiento de datos en Python** y un **Dashboard interactivo en Streamlit** para analizar la desigualdad en la distribución del ingreso y la estructura del gasto en los hogares mexicanos.

Utilizando los microdatos oficiales de la **Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH)** publicada por el **INEGI**, el análisis evalúa más de 91,000 registros de hogares que representan a **38.8 millones de hogares a nivel nacional** mediante sus respectivos factores de expansión (`factor`).

### 🎯 Objetivos de Negocio y Análisis Económico
1. **Medición de Desigualdad**: Cuantificar la brecha de ingresos mediante la estimación del **Coeficiente de Gini ponderado** y la construcción interactiva de la **Curva de Lorenz**.
2. **Estructura del Gasto y Ley de Engel**: Analizar cómo varía la proporción del gasto destinada a necesidades básicas (alimentos) frente a bienes de desarrollo (educación y esparcimiento) a lo largo de los deciles de ingreso.
3. **Análisis Comparativo Regional**: Evaluar el desempeño económico del estado de **Jalisco** frente al promedio nacional en términos de ingreso trimestral y gasto alimentario.
4. **Retorno al Nivel Educativo**: Cruzar relacionalmente los datos del hogar con las características sociodemográficas del jefe de familia para evaluar el impacto de la educación aprobada sobre los ingresos.

---

## 📂 Estructura del Repositorio

```text
├── data/                            # Subcarpeta para microdatos (.csv / .parquet)
├── output/                          # Visualizaciones estáticas exportadas (.png)
├── schema.sql                       # Creación de base de datos e importación en MySQL
├── queries.sql                      # Consultas analíticas avanzadas (CTEs, Window Functions, JOINs)
├── analisis_enigh_econometria.ipynb # Notebook interactivo con análisis econométrico y Gini
├── app.py                           # Aplicación web interactiva en Streamlit + Plotly
├── prepare_data.py                  # Script para optimización y preparación del dataset
├── requirements.txt                 # Dependencias para despliegue en la nube
├── .gitignore                       # Reglas de exclusión para datos y caché
└── README.md                        # Documentación ejecutiva del proyecto
```

---

## 🛠️ Tecnologías y Metodología

- **Base de Datos & SQL**: MySQL 8.0+
  - Expresiones de Tabla Comunes (`WITH ... AS`), Funciones de Ventana (`NTILE(10)`, `SUM() OVER()`), Agregaciones Condicionales y `INNER JOIN` relacionales.
- **Procesamiento y Econometría en Python**: Python 3.10+
  - `pandas`, `numpy`, `sqlalchemy`, `pymysql`, `matplotlib`, `seaborn`.
  - Integración numérica trapezoidal ponderada por el factor de expansión para el cálculo del **Coeficiente de Gini** y la **Curva de Lorenz**.
- **Visualización & Web App**: Streamlit + Plotly Express
  - Filtros dinámicos por estado (destacando **Jalisco**), cálculo reactivo de métricas (KPIs) y gráficos interactivos desplegados en **Streamlit Community Cloud**.

---

## 💡 Hallazgos Principales

1. **Coeficiente de Gini Ponderado**: El análisis sobre la muestra expandida refleja la marcada concentración del ingreso en México, confirmando la necesidad de utilizar ponderaciones muestrales para no subestimar la desigualdad.
2. **Evidencia Empírica de la Ley de Engel**: Los hogares del primer decil (**D1**, menores ingresos) destinan más del 50% de su gasto monetario exclusivamente a alimentos, mientras que en el decil superior (**D10**), esta proporción cae drásticamente, liberando presupuesto hacia educación y esparcimiento.
3. **Perspectiva Regional (Jalisco)**: Jalisco muestra un ingreso promedio trimestral superior a la media nacional, acompañado de un menor porcentaje relativo de gasto destinado a alimentos de primera necesidad.
4. **Retorno Educativo**: Existe una relación monotónica creciente entre el nivel de escolaridad del jefe de hogar y el ingreso corriente promedio, donde la educación superior y posgrado representan el mayor salto cuantitativo.

---

## 🚀 Instrucciones de Reproducibilidad y Ejecución

### 1. Clonar el Repositorio
```bash
git clone https://github.com/jesus09001/enigh-desigualdad-sql-python.git
cd enigh-desigualdad-sql-python
```

### 2. Configuración y Ejecución del Dashboard en Streamlit
```bash
# Instalar dependencias
pip install -r requirements.txt

# Preparar datos optimizados
python prepare_data.py

# Iniciar la aplicación web
streamlit run app.py
```

---

## 👨‍💻 Autor

**Copado Crespo Jesus Adahir**
- **Perfil**: Economista y Científico de Datos especializado en análisis econométrico, inteligencia de negocios, ingeniería de datos y soluciones analíticas end-to-end.
- **LinkedIn**: [Jesus Adahir Copado Crespo](https://www.linkedin.com/in/jesus-adahir-copado-crespo-251748294)
- **GitHub**: [jesus09001](https://github.com/jesus09001)
- **Dashboard en Vivo**: [Ver App Web en Streamlit](https://enigh-desigualdad-sql-python-nfd2hisxed9eyezuyxx2oz.streamlit.app/)
