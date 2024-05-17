'''
Propuesta front-end de cara al TFM
'''

import streamlit as st
import pandas as pd
import numpy as np
import os 
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.neighbors import NearestNeighbors
import pickle 


features = pd.read_csv(r'features.csv')
res = pd.read_csv(r'total_df.csv')

modelo = pickle.load(open('Modelo_Radiacion.pkl', 'rb'))

def dar_prediccion(filtered_res):
            liked_PALCE = filtered_res.iloc[0]
            print(liked_PALCE)
            num_recom = 8
            _, ind = modelo.kneighbors(features.iloc[[liked_PALCE.name]])
        
            st.subheader('Recommended Restaurants')
            rec_indices = ind[0][0:num_recom]
            rec_resta = res.iloc[rec_indices, :]
            st.write(rec_resta)

    

def main():
    st.title('Recomendador de suelos para construcción de parque fotovolataícos')

    selected_provincia = st.selectbox("Seleccione Provincia",res['Provincia'].unique().astype(str))
    selected_rad = st.selectbox("Seleccione Radiacion",res['rad-media'].unique().astype(str))

    filtered_res = res[
        (res['Provincia'] == selected_provincia) &
        (res['rad-media'] == selected_rad) 
    ]
    print('This is filtered res:' '\n', filtered_res)
    # Añadir aquí un buclque para que primero pono ponga nada (done)

    if filtered_res.empty:
        if st.button("Obtener Terrenos"):
            st.write('No hay recomendación todavía')
    else:
        if st.button("Obtener Terrenos"):
            dar_prediccion(filtered_res)


if __name__ =="__main__":
    main()