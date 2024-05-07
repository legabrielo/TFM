import pandas as pd
import warnings

# Leer el primer archivo de Excel y crear un DataFrame
df_radiacion = pd.read_excel(f"./datos/Radiacion.xlsx")
df_radiacion.drop(columns=['Ceuta','Melilla'], inplace=True)

# Leer el segundo archivo de Excel y crear un DataFrame
df_precio_euro_m2 = pd.read_excel("./datos/Precio euro_m2.xlsx")

# Transponer el DataFrame df_radiacion
df_radiacion_transpuesto = df_radiacion.transpose()

# Change certain names in the first column of df_precio_euro_m2
df_precio_euro_m2['Lugar'] = df_precio_euro_m2['Lugar'].replace(
    {'Jaén': 'Jaen',
     'Córdoba': 'Cordoba',
     'Almería': 'Almeria',
     'Málaga': 'Malaga',
     'Cádiz': 'Cadiz',
     'Cáceres': 'Caceres',
     'Murcia (Región de)': 'Murcia',
     'Alicante/Alacant': 'Alicante',
     'Valencia/València': 'Valencia',
     'Castellón/Castelló': 'Castellon',
     'Balears (Illes)': 'Baleares',
     'Palmas (Las)': 'Las Palmas',
     'Madrid (Comunidad de)': 'Madrid',
     'León': 'Leon',
     'Girona': 'Gerona',
     'Lleida': 'Lerida',
     'Navarra (Comunidad Foral de)': 'Navarra',
     'Rioja (La)': 'La Rioja',
     'Álava': 'Alava',
     'Guipúzcoa': 'Guipuzcoa',
     'Asturias (Principado de )': 'Asturias',
     'Coruña (A)': 'La Coruña',
     'Ourense': 'Orense'
     }).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').replace({'La Coruna':'La Coruña'})

# Cuadrar índice y cortar las columnas 2004 a 2009 del DataFrame df_precio_euro_m2
df_precio_euro_m2.index = df_precio_euro_m2['Lugar']
df_precio_euro_m2 = df_precio_euro_m2.iloc[:, 7:]
df_precio_euro_m2.index.name = None

# Crear el nuevo DataFrame df_kWh_euros
df_kWh_euros = df_radiacion_transpuesto

# Cuadrar el índice de df_kWh_euros
df_kWh_euros.columns = df_kWh_euros.iloc[0]
df_kWh_euros = df_kWh_euros[1:]
df_kWh_euros.columns.name = None

# Trasformar el DataFrame df_kWh_euros a kWh/m2

warnings.filterwarnings("ignore")

for column in df_precio_euro_m2.columns:
    for i in range(12):
        if i < 9:
            new_column_name = f"{column}_0{i+1}"
        else:
            new_column_name = f"{column}_{i+1}"
        df_precio_euro_m2[new_column_name] = round(df_precio_euro_m2[column],2)
    df_precio_euro_m2.drop(columns=column, inplace=True)

df_kWh_euros = df_kWh_euros.apply(lambda x: x/df_precio_euro_m2.loc[x.name, x.index], axis=1)

print(df_kWh_euros)

df_kWh_euros.to_excel("./datos/kWh_euro.xlsx", index=True)
