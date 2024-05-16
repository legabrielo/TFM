import pandas as pd
import geopy.geocoders as geocoders
from geopy.location import Location
from geopy.distance import geodesic
from sklearn.linear_model import LinearRegression

# Leer los datasets y crear un DataFrame
df_subestaciones = pd.read_excel(f"./datos/df-final.xlsx")
df_kWh_euro = pd.read_excel(f"./datos/kWh_euro.xlsx")
df_subestaciones['Localidad'] = df_subestaciones['Localidad'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_subestaciones['Provincia'] = df_subestaciones['Provincia'].replace(
    {'Jaén': 'Jaen',
     'Córdoba': 'Cordoba',
     'Almería': 'Almeria',
     'Málaga': 'Malaga',
     'Huelva\n': 'Huelva',
     'Cádiz': 'Cadiz',
     'Cáceres': 'Caceres',
     'Murcia (Región de)': 'Murcia',
     'Alicante/Alacant': 'Alicante',
     'Alicante\n': 'Alicante',
     'Valencia/València': 'Valencia',
     'Valencia\n': 'Valencia',
     'Castellón/Castelló': 'Castellon',
     'Balears (Illes)': 'Baleares',
     'Islas Baleares': 'Baleares',
     'Palmas (Las)': 'Las Palmas',
     'Madrid (Comunidad de)': 'Madrid',
     'León': 'Leon',
     'Girona': 'Gerona',
     'Lleida': 'Lerida',
     'Navarra (Comunidad Foral de)': 'Navarra',
     'Rioja (La)': 'La Rioja',
     'Álava': 'Alava',
     'Guipúzcoa': 'Guipuzcoa',
     'Gipuzcoa': 'Guipuzcoa',
     'Asturias (Principado de )': 'Asturias',
     'Coruña (A)': 'La Coruña',
     'La Coruña\n': 'La Coruña',
     'Ourense': 'Orense',
     'Galicia': 'Lugo',
     }).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').replace({'La Coruna':'La Coruña'})

ubicacion = input("Indique la localidad que sea analizar: \n")
geolocator = geocoders.Nominatim(user_agent="tu_aplicacion")
lugar = geolocator.geocode(ubicacion)

distancias = pd.DataFrame(columns=['Subestacion', 'Distancia', 'kWh_euro'])

for index, row in df_subestaciones.iterrows():
    latitud_subestacion = row['Latitud']
    longitud_subestacion = row['Longitud']
    distancia = geodesic((lugar.latitude, lugar.longitude), (latitud_subestacion, longitud_subestacion)).kilometers
    provincia = row['Provincia']
    kWh_euro = df_kWh_euro.loc[df_kWh_euro['Unnamed: 0'] == provincia].iloc[:, 1:].sum(axis=1).values[0]
    distancias = pd.concat([distancias, pd.DataFrame([{'Subestacion': row['Localidad'], 'Distancia': distancia, 'kWh_euro': kWh_euro}])], ignore_index=True)

# Crear el modelo de regresión lineal
modelo = LinearRegression()

# Entrenar el modelo con las columnas 'Distancia' y 'kWh_euro'
X = distancias[['Distancia', 'kWh_euro']]
y = distancias['Subestacion']
modelo.fit(X, y)

# Predecir las subestaciones en función del modelo
distancias['Prediccion'] = modelo.predict(X)

# Ordenar el DataFrame en función de la columna 'Prediccion'
distancias = distancias.sort_values(by='Prediccion')

print(distancias.head(10))

# print(distancias.sort_values(by='Distancia').head(10))