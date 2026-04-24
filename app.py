import streamlit as st
import numpy as np

st.set_page_config(page_title="Heritage-Air Manager", layout="wide")
st.title("🏛️ Heritage-Air Manager")

# --- SIDEBAR ---
st.sidebar.header("Parametri Ambientali")
ach = st.sidebar.slider("Ricambio d'aria (ACH) [h-1]", 0.01, 2.0, 0.18)
volume = st.sidebar.number_input("Volume stanza [m3]", value=2200)
superficie = st.sidebar.number_input("Superficie deposito [m2]", value=590)

col1, col2 = st.columns(2)

with col1:
    st.header("🧪 Modello Gas")
    v_dep_gas = st.slider("Vdep Gas [m/hr]", 0.001, 0.1, 0.02)
    cout_gas = st.number_input("Conc. Esterna Gas [µg/m3]", value=40.0)
    io_ratio = ach / (v_dep_gas * (superficie/volume) + ach)
    st.metric("Conc. Interna Gas", f"{(cout_gas * io_ratio):.2f} µg/m3")

with col2:
    st.header("🧹 Modello Polvere")
    cin_pm = st.number_input("Conc. Interna PM2.5 [µg/m3]", value=3.3)
    uvl_perc = st.slider("Limite Visivo (UVL) [%]", 0.1, 1.0, 0.2)
    
    if cin_pm > 0:
        # Calibrazione manuale basata sui risultati del paper:
        # Cin = 3.3, UVL = 0.2% -> DF = 230 giorni
        # Usiamo una costante K che sintetizza (lambda * vg)
        
        uvl_dec = uvl_perc / 100
        # Questa costante K è calibrata per restituire 230 con 3.3 e 0.002
        k_shindler = 2.63e-06 
        
        # t_giorni = -ln(1 - UVL) / (K * Cin)
        df_days = -np.log(1 - uvl_dec) / (k_shindler * cin_pm)
        
        st.metric("Dusting Frequency (DF)", f"{int(df_days)} giorni")
        st.success(f"📅 Intervallo: {round(df_days/30, 1)} mesi")
    else:
        st.error("Inserisci una concentrazione > 0")
