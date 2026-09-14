import pandas as pd
import os

print("Procesando concentradohogar.csv para crear dataset liviano para Streamlit Cloud...")

# Intentar leer desde data/concentradohogar.csv o concentradohogar.csv
input_path = r"C:\Users\alda09\Downloads\inegi\data\concentradohogar.csv" if os.path.exists("data/concentradohogar.csv") else "concentradohogar.csv"

if not os.path.exists(input_path):
    print(f"Error: No se encontró {input_path}")
    exit(1)

df = pd.read_csv(input_path)

# Seleccionar solo las columnas necesarias para el dashboard
cols = ['folioviv', 'foliohog', 'ubica_geo', 'factor', 'ing_cor', 'gasto_mon', 'alimentos', 'educa_espa', 'transporte', 'salud']
cols_present = [c for c in cols if c in df.columns]

df_clean = df[cols_present].copy()
if 'ubica_geo' in df_clean.columns:
    df_clean['entidad'] = (df_clean['ubica_geo'] // 1000).astype(int)

os.makedirs("data", exist_ok=True)

# Guardar CSV liviano
clean_csv_path = "data/concentradohogar_clean.csv"
df_clean.to_csv(clean_csv_path, index=False)
print(f"Creado: {clean_csv_path} ({os.path.getsize(clean_csv_path) / (1024*1024):.2f} MB)")

# Guardar Parquet aún más liviano si pyarrow/fastparquet está instalado
try:
    parquet_path = "data/concentradohogar.parquet"
    df_clean.to_parquet(parquet_path, index=False)
    print(f"Creado: {parquet_path} ({os.path.getsize(parquet_path) / (1024*1024):.2f} MB)")
except Exception as e:
    print("Nota: Parquet no generado (puedes usar solo el CSV liviano).", e)
