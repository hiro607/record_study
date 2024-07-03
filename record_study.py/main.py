import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['Date', 'Heures d\'Études', 'Contenu', 'Remarques'])
        df.to_csv(file_path, index=False)
        return df
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Heures d\'Études', 'Contenu', 'Remarques'])

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

file_path = 'study_records_st.csv'
if 'data' not in st.session_state:
    st.session_state.data = load_data(file_path)

st.title('Application de Suivi d\'Études en japonais')

with st.form('Formulaire de suivi d\'études'):
    date = st.date_input('Date')
    heures_d_etude = st.number_input('Heures d\'étude (heures)', 
                                     min_value=0.0, max_value=24.0, step=0.5)
    contenu = st.text_input('Contenu')
    remarques = st.text_area('Remarques')
    submitted = st.form_submit_button('Enregistrer')

    if submitted:
        new_row = pd.DataFrame({'Date':[date],'Heures d\'étude':[heures_d_etude],
                                'Contenu':[contenu],'Remarques':[remarques],})
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        save_data(st.session_state.data, file_path)
        st.success('Enregistrement de l\'étude sauvegardé!')
    
st.subheader('Liste des enregistrements d\'études')
st.dataframe(st.session_state.data)

st.subheader('Temps d\'Étude quotidien')
if not st.session_state.data.empty:
    daily_study_time = st.session_state.data.groupby('Date')['Heures d\'étude'].sum()
    total_study_time = st.session_state.data['Heures d\'étude'].sum()
    average_study_time = st.session_state.data['Heures d\'étude'].mean()
    st.subheader(f'Temps d\'étude total: {total_study_time:.2f} heures')
    st.subheader(f'Temps d\'étude moyen: {average_study_time:.2f} heures/jour')

else:
    st.info('Aucun enregistrement d\'étude disponible.')
