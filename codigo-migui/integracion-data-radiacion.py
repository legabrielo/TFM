import pandas as pd
import numpy as np
import os

# Especificar la ruta de la carpeta
ruta_carpeta = "./codigo-migui/csv_eur"

# Lista para almacenar los DataFrames
dataframes = []

# Recorrer la carpeta y leer cada archivo CSV
for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".csv"):
        
        # Crear un DataFrame para el archivo CSV actual
        df = pd.read_csv(f"{ruta_carpeta}/{archivo}")
        
        df[["year", "month", "H(h)_m"]] = df["year\t\tmonth\t\tH(h)_m"].str.split("\\t\\t", expand=True)
        del df["year\t\tmonth\t\tH(h)_m"]
        
        # Asignar un nombre descriptivo al DataFrame (opcional)
        df.name = archivo[:-4]  # Eliminar la extensión .csv

        # Agregar el DataFrame a la lista
        dataframes.append(df)

df_combinado = pd.DataFrame()  # DataFrame vacío para almacenar el resultado final

month_num_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

longitud_df = 0

# Recorrer y combinar DataFrames
for df in dataframes:
    # Asegurar orden consistente de "year" y "month"
    if df["year"].name != "year" or df["month"].name != "month":
        df = df.rename(columns={"year": "year", "month": "month"})

    # Unificar columnas "year" y "month" con el DataFrame actual
    if df_combinado.empty:
        df_comun = df[["year", "month"]]
    else:
        df_comun = pd.concat([df_combinado, df[["year", "month"]]], ignore_index=True)

    # Agregar columna "H(h)_m" con el nombre del DataFrame actual
    longitud_df=len(df)
    df_comun[f"{df.name}"] = df["H(h)_m"]
    df_combinado = df_comun.head(longitud_df)

df_combinado.loc[:, "month"] = df_combinado["month"].map(month_num_map)

# Crear columna "Fecha"
df_combinado["Fecha"] = df_combinado.apply(lambda row: f"{row['year']}_{str(row['month']).zfill(2)}", axis=1)

# Mover "Fecha" a la primera posición
df_combinado = df_combinado[['Fecha'] + list(df_combinado.columns[2:-1])]

# Ordenar por Fecha
df_combinado = df_combinado.sort_values(by=['Fecha'])


df_combinado.to_excel("./datos/Radiacion.xlsx", index=False)  
print(df_combinado.head())  # Mostrar las primeras filas del DataFrame