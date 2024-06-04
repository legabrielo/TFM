import pandas as pd
import numpy as np
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
# Leer el archivo Excel y cargarlo en un DataFrame
df = pd.read_excel(f"./datos/Radiacion.xlsx")

# Crear un DataFrame con las columnas "Fecha" y "Provincia" por cada porvincia
dfs = []
for column in df.columns[1:]:
    df_provincia = df[['Fecha', column]]
    df_provincia.name = column
    dfs.append(df_provincia)
 
# Crear un modelo Auto-ARIMA para cada provincia
predictions = []   
def modelo_auto_ARIMA(dfs):
    for df_provincia in dfs:
        model = auto_arima(df_provincia.iloc[:, 1], seasonal=False, suppress_warnings=True)
        model_fit = model.fit(y=df_provincia.iloc[:, 1])  # Pass 'y' explicitly

        # Make predictions
        provincia_predictions = model_fit.predict(n_periods=36)
        predictions.append(provincia_predictions)
        print(f'Predicciones para {df_provincia.name}:\n{provincia_predictions}')
        break
    # Esto es una prueba, habría que ver que eficacia tiene el modelo...

def comparacion_diferenciacion(provincia):
    for df_provincia in dfs:
        if df_provincia.name == provincia:
            plt.rcParams.update({'figure.figsize': (12, 15), 'figure.dpi':120})
            fig, axes = plt.subplots(nrows=2, ncols=2, sharex=False)
            fig.subplots_adjust(hspace=0.5)
            
            # Serie Original
            axes[0,0].plot(df_provincia.iloc[:, 1], color='r'); axes[0,0].set_title(f'{df_provincia.columns[1]} Serie Original')
            plot_acf(df_provincia.iloc[:, 1], ax=axes[0,1], color='r')
            
            # Primer Diferenciado
            axes[1,0].plot(df_provincia.iloc[:, 1].diff(), color='g'); axes[1,0].set_title(f'{df_provincia.columns[1]} Primer Diferenciado')
            plot_acf(df_provincia.iloc[:, 1].diff().dropna(), ax=axes[1,1], color='g')
            
            plt.show()
            break
    
# Creamos un modelo ARIMA para cada provincia
def modelo_ARIMA(dfs):
    for df_provincia in dfs: 
        #Diferenciación   
        result = adfuller(df_provincia.iloc[:, 1]) #Usando la prueba de Dickey-Fuller, documenta!
        d = 0
        # print(f'{df_provincia.name}')
        # print('Serie Original - AD Statistic: %f' % result[0])
        # print('Serie Original - p-value: %f' % result[1]) #Como es menor a 0.05, podemos rechazar la hipotesis nula. Es estacionaria.
        if result[1] > 0.05:
            result1 = adfuller(df_provincia.iloc[:, 1].diff().dropna())
            d = 1 if result1[1] < 0.05 else d
            # print('Primera diferenciación - AD Statistic: %f' % result1[0])
            # print('Primera diferenciación - p-value: %f' % result1[1]) #Como es menor a 0.05, podemos rechazar la hipotesis nula. Es estacionaria.
        print(f'Diferenciación de {df_provincia.name} es {d}')
            
            #Auto-Correlación
            
    

modelo_ARIMA(dfs)










# # Usar el modelo ARIMA para predecir la radiación solar para cada provincia
# predictions = []

# # Creamos una serie de tiempo con fechas desde 2021-01 hasta 2023-12, esto cambiara de 2024-01 a 2026-12
# meses = []
# for año in range(2010, 2027):
#     # Iterate through months (1 to 12)
#     for mes in range(1, 13):
#         # Create the month string in the desired format
#         mes_str = f"{año}_{mes:02d}"
#         meses.append(mes_str)
        
# tiempo = pd.Series(meses)
