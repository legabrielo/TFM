import pandas as pd
import geopy.geocoders as geocoders
from geopy.location import Location

# Leer los datasets y crear un DataFrame
df_subestaciones = pd.read_excel(f"./datos/df-final.xlsx")
df_precio_euro_m2 = pd.read_excel(f"./datos/Precio euro_m2.xlsx")
df_subestaciones['Localidad'] = df_subestaciones['Localidad'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

ubicacion = input("Indique la localidad que sea analizar: \n")
geolocator = geocoders.Nominatim(user_agent="tu_aplicacion")
lugar = geolocator.geocode(ubicacion)

# Si la búsqueda es exitosa, imprime las coordenadas
if lugar is not None:
    print(f"Coordenadas: {lugar.latitude}, {lugar.longitude}")
else:
    print("Ubicación no encontrada.")

