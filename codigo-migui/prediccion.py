import pandas as pd
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
# Leer el archivo Excel y cargarlo en un DataFrame
df = pd.read_excel(f"./datos/Radiacion.xlsx")

# Crear un DataFrame con las columnas "Fecha" y "Provincia" por cada porvincia
fechas=pd.date_range(start='1/1/2010', end='12/1/2023', freq='MS')

dfs = []
for column in df.columns[1:]:
    radiacion = df[column]
    df_provincia = pd.DataFrame({
        'Fecha': fechas,
        f'{column}': radiacion
    })
    df_provincia.name = column
    dfs.append(df_provincia)
    
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

def ad_fuller(df):
    result = adfuller(df)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])

def predicciones_auto_ARIMA(dfs, año):
    predictions = []
    num_pred = (año-2023)*12    
    for df_provincia in dfs:
        model = auto_arima(df_provincia.iloc[:, 1], m=12, seasonal=True, trace=False, suppress_warnings=True, error_action="ignore")
        model = model.fit(y=df_provincia.iloc[:, 1])  # Pass 'y' explicitly
        
        # Make predictions
        provincia_predictions = model.predict(n_periods=num_pred)
        predictions.append(provincia_predictions)
        print(f'Predicciones para {df_provincia.name}:\n{provincia_predictions}')
        
        # Falta volcarlo el otro excel, juntarlo...
        # Nos centramos en justificar el modelo, en redactar vaya
        break

def resumen_modelo(provincia):
    for df_provincia in dfs:
        if df_provincia.name == provincia:
            model = auto_arima(df_provincia.iloc[:, 1], m=12, seasonal=True, trace=False, suppress_warnings=True, error_action="ignore")
            print(model.summary())

def prediccion(provincia, año):
    num_pred = (año-2021)*12
    fechas_pred=pd.date_range(start='1/1/2022', end=f'12/1/{año}', freq='MS')
    for df_provincia in dfs:
        if df_provincia.name == provincia:
            train, test=df_provincia[:-24],df_provincia[-24:]
            model = auto_arima(train.iloc[:, 1], m=12, seasonal=True, trace=False, suppress_warnings=True, error_action="ignore")
            model = model.fit(y=train.iloc[:, 1])  # Pass 'y' explicitly
            provincia_predictions = model.predict(n_periods=num_pred, freq='M')   
            predicciones = pd.DataFrame({
                'Fecha': fechas_pred,
                f'{column}': provincia_predictions
            })
            plt.plot(train['Fecha'], train.iloc[:, 1], label='Train')
            plt.plot(test['Fecha'], test.iloc[:, 1], label='Valid')   
            plt.plot(predicciones['Fecha'], predicciones.iloc[:, 1], label='Prediction')
            plt.legend()
            plt.show()

def residuos(provincia):
    for df_provincia in dfs:
        if df_provincia.name == provincia:
            model = auto_arima(df_provincia.iloc[:, 1], m=12, seasonal=True, trace=False, suppress_warnings=True, error_action="ignore")
            residuos = model.resid()
            plt.plot(residuos)
            plt.title('Residuos')
            plt.show()

# predicciones_auto_ARIMA(dfs, 2030)
# resumen_modelo('Almeria')
residuos('Malaga')
# prediccion('Jaen',2023)

