import pandas as pd
import numpy as np
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf, adfuller, kpss
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
        p = model.order[0]
        d = model.order[1]
        m = model.order[2]
        print(f'{df_provincia.name} \n  p: {p} d: {d} m: {m}')
        # model_fit = model.fit(y=df_provincia.iloc[:, 1])  # Pass 'y' explicitly

        # # Make predictions
        # provincia_predictions = model_fit.predict(n_periods=36)
        # predictions.append(provincia_predictions)
        # print(f'Predicciones para {df_provincia.name}:\n{provincia_predictions}')
        # break
    # Esto es una prueba, habría que ver que eficacia tiene el modelo...

def grafica_acf(provincia):
    for df_provincia in dfs:
        if df_provincia.name == provincia:
            plt.rcParams.update({'figure.figsize': (12, 15), 'figure.dpi':120})
            fig, axes = plt.subplots(nrows=2, ncols=2, sharex=False)
            fig.subplots_adjust(hspace=0.5)
            
            # Serie Original
            axes[0,0].plot(df_provincia.iloc[:, 1], color='r'); axes[0,0].set_title(f'{df_provincia.columns[1]} serie original')
            plot_acf(df_provincia.iloc[:, 1], ax=axes[0,1], color='r')
            
            # Primer Diferenciado
            axes[1,0].plot(df_provincia.iloc[:, 1].diff(), color='g'); axes[1,0].set_title(f'{df_provincia.columns[1]} Primera diferenciación')
            plot_acf(df_provincia.iloc[:, 1].diff().dropna(), ax=axes[1,1], color='g')
            
            plt.show()
            break

def grafica_pacf(provincia):
    for df_provincia in dfs:
        if df_provincia.name == provincia:
            plt.rcParams.update({'figure.figsize': (12, 15), 'figure.dpi':120})
            fig, axes = plt.subplots(nrows=2, ncols=2, sharex=False)
            fig.subplots_adjust(hspace=0.5)
            
            # Serie Original
            axes[0,0].plot(df_provincia.iloc[:, 1], color='r'); axes[0,0].set_title(f'{df_provincia.columns[1]} serie original')
            plot_pacf(df_provincia.iloc[:, 1], ax=axes[0,1], color='r')
            
            # Primer Diferenciado
            axes[1,0].plot(df_provincia.iloc[:, 1].diff(), color='g'); axes[1,0].set_title(f'{df_provincia.columns[1]} Primera diferenciación')
            plot_pacf(df_provincia.iloc[:, 1].diff().dropna(), ax=axes[1,1], color='g')
            
            plt.show()
            break
        
def grafica_acf_pacf(provincia):
    for df_provincia in dfs:
        if df_provincia.name == provincia:
            plt.rcParams.update({'figure.figsize': (12, 15), 'figure.dpi':120})
            fig, axes = plt.subplots(nrows=2, ncols=2, sharex=False)
            fig.subplots_adjust(hspace=0.5)
            
            # Serie Original
            plot_acf(df_provincia.iloc[:, 1], ax=axes[0,0], color='r')
            plot_pacf(df_provincia.iloc[:, 1], ax=axes[0,1], color='r')
            
            # Primer Diferenciado
            plot_acf(df_provincia.iloc[:, 1].diff().dropna(), ax=axes[1,0], color='g')
            plot_pacf(df_provincia.iloc[:, 1].diff().dropna(), ax=axes[1,1], color='g')
            
            plt.show()
            break

def comprobar_estacionariedad(df):
    result = adfuller(df)
    return result[1]  # p-valor

def determinar_d(df, max_diff=2, significance_level=0.05):
    """
    Determina el número de diferenciaciones necesarias para estacionarizar la serie.
    :param series: Serie temporal (pandas Series).
    :param max_diff: Número máximo de diferenciaciones a probar.
    :param significance_level: Nivel de significancia para la prueba de ADF.
    :return: Mejor valor de d.
    """
    d = 0
    p_value = comprobar_estacionariedad(df)
    
    while p_value > significance_level and d < max_diff:
        d += 1
        df = df.diff().dropna()
        p_value = comprobar_estacionariedad(df)
    
    return d

def determinar_p(df, max_diff=2, significance_level=0.05):
    pacf_values, conf_interval = pacf(df, nlags=max_diff, alpha=significance_level)
    i=0
    p=0
    signo_inicial="+" if pacf_values[0]>=0 else "-"
    for value in pacf_values:
        signo_actual="+" if pacf_values[i]>=0 else "-"
        if abs(value) < conf_interval[i][1] - value:
            p = i+1
            break
        elif signo_inicial != signo_actual:
            p = i+1
            break
        else:
            p=0
        i=i+1
    return p

def determinar_m(df, max_diff=2, significance_level=0.05):  
    return 0      
# Creamos un modelo ARIMA para cada provincia
def modelo_ARIMA(dfs):
    for df_provincia in dfs: 
        # Diferenciación   
        d = determinar_d(df_provincia.iloc[:, 1])
        
        # Autorregresión
        p = determinar_p(df_provincia.iloc[:, 1])

        # Medias móviles
        m = determinar_m(df_provincia.iloc[:, 1])
        
        print(f'{df_provincia.name} \n p: {p} d: {d} m: {m}')


# grafica_acf_pacf("Las Palmas")
# modelo_ARIMA(dfs)
# modelo_auto_ARIMA(dfs)










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
