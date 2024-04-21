import pandas as pd
import numpy as np
import os

df_20 = pd.read_excel(f"./datos/Radiacion.xlsx")
ruta_carpeta="./datos/2020-2023"

dataframes = []

month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

# Recorrer la carpeta y leer cada archivo CSV
for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".csv"):
        
        # Crear un DataFrame para el archivo CSV actual
        df = pd.read_csv(f"{ruta_carpeta}/{archivo}", sep=";", encoding="latin-1")  # Replace with the appropriate encoding
        
        # Eliminamos las columnas que no nos influyen y establecemos tipo de dato
        df.drop(columns=["IdProvincia", "IdEstacion"], inplace=True)
        df.drop(columns=["Fecha"], inplace=True)
        df['Año'] = df['Año'].astype(int)
        df['Mes'] = df['Mes'].astype(int)
        
        df['Radiación (MJ/m2)'] = df['Radiación (MJ/m2)'].str.replace(',', '.')
        df['Radiación (MJ/m2)'] = df['Radiación (MJ/m2)'].astype(float)
        
        # Pasamos de MJ/m2 diarios a MJ
        for month, days in month_days.items():
            df.loc[df['Mes'] == month, 'Radiación (MJ/m2)'] = round(df.loc[df['Mes'] == month, 'Radiación (MJ/m2)'] * days * 0.27777778 , 2)
            
        # Crear columna "Fecha"
        df["Fecha"] = df.apply(lambda row: f"{row['Año']}_{str(row['Mes']).zfill(2)}", axis=1)
        df["Fecha"] = df.apply(lambda row: f"{row['Año']}_{str(row['Mes']).zfill(2)}", axis=1)

        # Mover "Fecha" a la primera posición
        df = df[['Fecha'] + list(df.columns[2:-1])]

        # Asignar un nombre descriptivo al DataFrame (opcional)
        df.name = archivo[:-4]  # Eliminar la extensión .csv

        # Agregar el DataFrame a la lista
        dataframes.append(df)

print(dataframes[1])