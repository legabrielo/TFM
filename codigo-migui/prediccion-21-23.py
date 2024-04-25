import pandas as pd
from pmdarima import auto_arima

# Leer el archivo Excel y cargarlo en un DataFrame
df = pd.read_excel(f"./datos/Radiacion2020.xlsx")

# Crear un DataFrame con las columnas "Fecha" y "Provincia" por cada porvincia
df_ceuta = df[['Fecha', 'Ceuta']]
df_melilla = df[['Fecha', 'Melilla']]
df_las_palmas = df[['Fecha', 'Las Palmas']]
df_gerona = df[['Fecha', 'Gerona']]
df_lerida = df[['Fecha', 'Lerida']]
df_tarragona = df[['Fecha', 'Tarragona']]
df_barcelona = df[['Fecha', 'Barcelona']]
df_vizcaya = df[['Fecha', 'Vizcaya']]
df_guipuzcoa = df[['Fecha', 'Guipuzcoa']]
df_asturias = df[['Fecha', 'Asturias']]

dfs = [df_ceuta, df_melilla, df_las_palmas, df_gerona, df_lerida, df_tarragona, df_barcelona, df_vizcaya, df_guipuzcoa, df_asturias]

# Creamos una serie de tiempo con fechas desde 2021-01-01 hasta 2023-12-31
meses = []

# Iterate through years from 2010 to 2023
for año in range(2010, 2024):
    # Iterate through months (1 to 12)
    for mes in range(1, 13):
        # Create the month string in the desired format
        mes_str = f"{año}_{mes:02d}"
        meses.append(mes_str)
        
tiempo = pd.Series(meses)

# Fit the ARIMA model using auto_arima
predictions = []

for df_provincia in dfs:
    model = auto_arima(df_provincia.iloc[:, 1], seasonal=False, suppress_warnings=True)
    model_fit = model.fit(y=df_provincia.iloc[:, 1])  # Pass 'y' explicitly

    # Make predictions
    provincia_predictions = model_fit.predict(n_periods=36)
    predictions.append(provincia_predictions)

# Falta esto 
# Create a DataFrame with the predictions for Melilla
df_23_melilla = pd.DataFrame({'Fecha': tiempo, 'Melilla': predictions[1]}).dropna()

# Print the predictions
print(df_23_melilla)

