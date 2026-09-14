# 📊 Análisis Econométrico de Desigualdad y Estructura del Gasto en México (ENIGH - INEGI)

![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue?style=flat&logo=mysql)
![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat&logo=pandas)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)

##  Descripción del Proyecto

Este proyecto combina **econometría aplicada**, **consultas avanzadas en SQL** y **procesamiento de datos en Python** para analizar la desigualdad en la distribución del ingreso y la estructura del gasto en los hogares mexicanos. 

Utilizando los microdatos oficiales de la **Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH)** publicada por el **INEGI**, el análisis evalúa más de 91,000 registros de hogares que representan a **38.8 millones de hogares a nivel nacional** mediante sus respectivos factores de expansión (`factor`).

###  Objetivos de Negocio y Análisis Económico
1. **Medición de Desigualdad**: Cuantificar la brecha de ingresos mediante la estimación del **Coeficiente de Gini ponderado** y la construcción de la **Curva de Lorenz**.
2. **Estructura del Gasto y Ley de Engel**: Analizar cómo varía la proporción del gasto destinada a necesidades básicas (alimentos) frente a bienes de desarrollo (educación y esparcimiento) a lo largo de los deciles de ingreso.
3. **Análisis Comparativo Regional**: Evaluar el desempeño económico del estado de **Jalisco** frente al promedio nacional en términos de ingreso trimestral y gasto alimentario.
4. **Retorno al Nivel Educativo**: Cruzar relacionalmente los datos del hogar con las características sociodemográficas del jefe de familia para evaluar el impacto de la educación aprobada sobre los ingresos.

---

##  Estructura del Repositorio

```text
├── data/
│   ├── concentradohogar.csv   # Microdatos a nivel hogar (~91k registros)
│   └── poblacion.csv          # Microdatos a nivel integrante del hogar
├── sql/
│   ├── schema.sql             # Creación de base de datos e importación en MySQL
│   └── queries.sql            # Consultas analíticas avanzadas (CTEs, Window Functions, JOINs)
├── notebooks/
│   └── enigh_analysis.ipynb   # Extracción con SQLAlchemy, cálculo de Gini y gráficos
├── output/
│   ├── curva_lorenz_enigh.png # Gráfico de distribución e igualdad del ingreso
│   ├── ley_engel_deciles.png  # Gráfico comparativo de estructura de gasto (D1 vs D10)
│   └── comparativo_jalisco.png # Comparativa regional Jalisco vs. Resto de México
└── README.md                  # Documentación del proyecto
```

---

##  Tecnologías y Metodología

- **Base de Datos**: MySQL 8.0+
  - **Uso de SQL Avanzado**: Expresiones de Tabla Comunes (`WITH ... AS`), Funciones de Ventana (`NTILE(10)`, `SUM() OVER()`), Agregaciones Condicionales y `INNER JOIN` relacionales.
- **Lenguaje de Programación**: Python 3.10+
  - **Librerías principales**: `pandas`, `numpy`, `sqlalchemy`, `pymysql`, `matplotlib`, `seaborn`.
- **Econometría**: Integración numérica trapezoidal ponderada por el factor de expansión para el cálculo exacto del **Coeficiente de Gini** y la **Curva de Lorenz**.

---

##  Hallazgos Principales

1. **Coeficiente de Gini Ponderado**: El análisis sobre la muestra expandida refleja la marcada concentración del ingreso en México, confirmando la utilidad de utilizar ponderaciones muestrales para no subestimar la desigualdad.
2. **Evidencia Empírica de la Ley de Engel**: Los hogares del primer decil (**D1**, menores ingresos) destinan más del 50% de su gasto monetario exclusivamente a alimentos, mientras que en el decil superior (**D10**), esta proporción cae drásticamente, incrementando el presupuesto hacia educación y esparcimiento.
3. **Perspectiva Regional (Jalisco)**: Jalisco muestra un ingreso promedio trimestral superior a la media nacional, acompañado de un menor porcentaje relativo de gasto destinado a alimentos de primera necesidad.
4. **Retorno Educativo**: Existe una relación monotónica creciente entre el nivel de escolaridad del jefe de hogar y el ingreso corriente promedio, donde la educación superior y posgrado representan el mayor salto cuantitativo en ingresos.

---

##  Instrucciones de Reproducibilidad

### 1. Clonar el Repositorio
```bash
git clone https://github.com/jesus09001/enigh-desigualdad-sql-python.git
cd enigh-desigualdad-sql-python
```

### 2. Configurar la Base de Datos en MySQL
1. Crea la base de datos e importa los datos ejecutando el script `sql/schema.sql`.
2. Ejecuta las consultas analíticas en `sql/queries.sql`.

### 3. Ejecutar el Análisis en Python
1. Instala las dependencias:
   ```bash
   pip install pandas matplotlib seaborn sqlalchemy pymysql numpy
   ```
2. Ejecuta el cuaderno `notebooks/enigh_analysis.ipynb` ajustando las credenciales de tu servidor MySQL local.

---

##  Autor
Copado Crespo Jesus Adahir

**Economista & Científico de Datos**
- **Perfil**: Especializado en análisis econométrico, inteligencia de negocios, ingeniería de datos y desarrollo de soluciones analíticas de extremo a extremo.
- **LinkedIn**: www.linkedin.com/in/jesus-adahir-copado-crespo-251748294
- **GitHub**: https://github.com/jesus09001
