import pandas as pd
import geopy.geocoders as geocoders
from geopy.location import Location
from geopy.distance import geodesic
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import streamlit as st

# Leer los datasets, crear un DataFrame y transformar los datos
df_subestaciones = pd.read_excel(f"./datos/df-final.xlsx")
df_kWh_euro = pd.read_excel(f"./datos/kWh_euro.xlsx")
df_radiacion = pd.read_excel(f"./datos/Radiacion.xlsx")
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

def analisis_lugar(lugar):
    '''
    Esta función hace una análisis de todas las centralitas cercanas a la ubicación dada y las ordena por cercanía.
    Devuelve un DataFrame con la información.
    
    Atributos:
        lugar (str): Ubicación a analizar.
    '''
    # Creamos un nuevo dataframe con la distancia entre la localidad selecionada y las subestaciones y la suma de kWh_euro de la provincia
    distancias = pd.DataFrame(columns=['Subestacion', 'Provincia', 'Distancia', 'kWh_euro_de_terreno'])

    for index, row in df_subestaciones.iterrows():
        latitud_subestacion = row['Latitud']
        longitud_subestacion = row['Longitud']
        distancia = geodesic((lugar.latitude, lugar.longitude), (latitud_subestacion, longitud_subestacion)).kilometers
        provincia = row['Provincia']
        kWh_euro = df_kWh_euro.loc[df_kWh_euro['Unnamed: 0'] == provincia].iloc[:, 1:].mean(axis=1).values[0]
        distancias = pd.concat([distancias, pd.DataFrame([{'Subestacion': row['Localidad'], 'Provincia': provincia, 'Distancia': distancia, 'kWh_euro_de_terreno': kWh_euro}])], ignore_index=True)
        
    # Hacer la normalización de los datos de distancia y kWh_euro_de_terreno
    # Cortar "distancias" a 50 filas y hacer la normalización
    # D_norm	E_norm	Puntaje
    distancias = distancias.sort_values(by='Distancia')
    return distancias.head(50)

def recomendacion_pasada(mejores_lugares, modo):
    '''
    Esta función calcula la puntuación de los mejores lugares donde se podría haber instalado una planta fotovoltáica.
    Devuelve un DataFrame con la información.
    
    Atributos:
        mejores_lugares (DataFrame): DataFrame con la infromación para realizar la recomendación.
        mode (str): Modo de recomendación, puede ser por 'Distancia' o 'Radiación'.
    '''
    D_min = mejores_lugares['Distancia'].min()
    D_max = mejores_lugares['Distancia'].max()
    E_min = mejores_lugares['kWh_euro_de_terreno'].min()
    E_max = mejores_lugares['kWh_euro_de_terreno'].max()

    for index, row in mejores_lugares.iterrows():
        mejores_lugares.loc[index, 'D_norm'] = (D_max - row['Distancia']) / (D_max - D_min)
        mejores_lugares.loc[index, 'E_norm'] = (row['kWh_euro_de_terreno'] - E_min) / (E_max - E_min)
        if modo == 'Distancia':
            mejores_lugares.at[index, 'Puntuacion'] = 0.7*(mejores_lugares.at[index, 'D_norm']) + 0.3*(mejores_lugares.at[index, 'E_norm'])
        elif modo == 'Radiación':
            mejores_lugares.at[index, 'Puntuacion'] = 0.3*(mejores_lugares.at[index, 'D_norm']) + 0.7*(mejores_lugares.at[index, 'E_norm'])
        else:
            mejores_lugares.at[index, 'Puntuacion'] = 0
    
    mejores_lugares.drop(['E_norm', 'D_norm'], axis=1, inplace=True)
    return mejores_lugares.head(10)

def radiacion_pasada(mejores_lugares, lugar):
    '''
    Devuele una gráfica de la radiación en el lugar seleccionado.
    
    Atributos:
        mejores_lugares (DataFrame): DataFrame con la infromación para realizar la recomendación.
        lugar (str): Ubicación para la gráfica.
    '''
    mejores_lugares = mejores_lugares[mejores_lugares['Subestacion'] == lugar]
    provincia = mejores_lugares['Provincia'].values[0]
    radiacion = df_radiacion[provincia]
    fechas = pd.date_range(start='2010-01-01', end='2023-12-01', freq='MS')
    df = pd.DataFrame({'Radacion': radiacion.values}, index=fechas)
    
    df.plot(kind='line', color='orange')
    plt.ylabel('Radiación')
    plt.title(f'Radiacion Pasada en {lugar}')
    plt.ylim(0)
    plt.grid(axis='y', linestyle='dashed')
    plt.show()
    return df

st.title("Análisis de Ubicaciones para Plantas Fotovoltaicas")

ubicacion = st.text_input("Indique la localidad que desea analizar:")

if st.button("Analizar"):
    geolocator = geocoders.Nominatim(user_agent="tu_aplicacion")
    lugar = geolocator.geocode(ubicacion)
    
    if lugar is not None:
        analisis = analisis_lugar(lugar)
        recomendacion = recomendacion_pasada(analisis, 'Radiación')
        st.write(recomendacion.sort_values('Puntuacion', ascending=False))
        
        lugar_seleccionado = st.selectbox("Seleccione una subestación:", recomendacion['Subestacion'].values)
        radiacion_pasada(recomendacion, lugar_seleccionado)
    else:
        st.write("No se pudo encontrar la ubicación. Por favor, intente nuevamente.")
            
