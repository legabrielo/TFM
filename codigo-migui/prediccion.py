import pandas as pd
from pmdarima import auto_arima

# Leer el archivo Excel y cargarlo en un DataFrame
df = pd.read_excel(f"./datos/Radiacion2020.xlsx")

# Crear un DataFrame con las columnas "Fecha" y "Provincia" por cada porvincia
dfs = []

for column in df.columns[1:]:
    df_provincia = df[['Fecha', column]]
    df_provincia.name = column
    dfs.append(df_provincia)
    
# Creamos una serie de tiempo con fechas desde 2021-01 hasta 2023-12, esto cambiara de 2024-01 a 2026-12
meses = []
for año in range(2010, 2027):
    # Iterate through months (1 to 12)
    for mes in range(1, 13):
        # Create the month string in the desired format
        mes_str = f"{año}_{mes:02d}"
        meses.append(mes_str)
        
tiempo = pd.Series(meses)

# Usar el modelo ARIMA para predecir la radiación solar para cada provincia
predictions = []

for df_provincia in dfs:
    model = auto_arima(df_provincia.iloc[:, 1], seasonal=False, suppress_warnings=True)
    model_fit = model.fit(y=df_provincia.iloc[:, 1])  # Pass 'y' explicitly

    # Make predictions
    provincia_predictions = model_fit.predict(n_periods=36)
    predictions.append(provincia_predictions)
    
## Falta guardar las predicciones en un archivo Excel
