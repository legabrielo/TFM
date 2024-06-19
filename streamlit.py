'''
Propuesta front-end de cara al TFM
'''

import streamlit as st
import pandas as pd
import numpy as np
import os 
from sklearn.cluster import KMeans
import pickle 


model_path = r'C:\Users\Gabriel Castillo\Desktop\Cosas Gabriel\Máster\kmeans_model.pkl'
res = pd.read_csv(r'total_df.csv')

def load_model(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

model = load_model(model_path)

def dar_prediccion(selected_provincia, selected_value):
    filtered_df = res[res['Provincia'] == selected_provincia]
    filtered_df['Adjusted Value'] = filtered_df['rad-media'] * selected_value
    sorted_df = filtered_df.sort_values(by='Adjusted Value', ascending=False)
    
    return sorted_df


def main():
    st.title('Recomendador de suelos para construcción de parque fotovoltaicos')

    selected_provincia = st.selectbox("Seleccione Provincia", res['Provincia'].unique().astype(str))
    selected_value = st.selectbox("Seleccione un valor", [50000, 1000000, 150000, 200000])


    if st.button("Obtener predicción"):
        sorted_df = dar_prediccion(selected_provincia, selected_value)
        st.write(f"Predicción para {selected_provincia} con valor {selected_value}")
        st.dataframe(sorted_df)

if __name__ == "__main__":
    main()




        # print('This is filtered res:' '\n', filtered_res)
    # # Añadir aquí un buclque para que primero pono ponga nada (done)

    # if filtered_res.empty:
    #     if st.button("Obtener Terrenos"):
    #         st.write('No hay recomendación todavía')
    # else:
    #     if st.button("Obtener Terrenos"):
    #         dar_prediccion(filtered_res)
