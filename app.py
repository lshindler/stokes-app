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
    st.header("🧪 Modello IMPACT (Gas)")
    v_dep_gas = st.slider("Vdep Gas [m/hr]", 0.001, 0.1, 0.02)
    cout_gas = st.number_input("Conc. Esterna Gas [µg/m3]", value=40.0)
    io_ratio = ach / (v_dep_gas * (superficie/volume) + ach)
    st.metric("Conc. Interna Gas", f"{(cout_gas * io_ratio):.2f} µg/m3")

with col2:
    st.header("🧹 Modello Shindler (Polvere)")
    cin_pm = st.number_input("Conc. Interna PM2.5 [µg/m3]", value=3.3)
    uvl_perc = st.slider("Limite Visivo (UVL) [%]", 0.1, 1.0, 0.2)
    
    if cin_pm > 0:
        # --- CALIBRAZIONE ESATTA PAPER SHINDLER ---
        # vg = 2.5e-5 m/s
        vg = 0.000025 
        # Cin convertita in kg/m3 (3.3 ug/m3 = 3.3e-9 kg/m3)
        cin_kg_m3 = cin_pm * 1e-9
        # costante lambda dal paper = 106000 m2/kg
        lambda_const = 106000 
        # UVL decimale (0.2% = 0.002)
        uvl_dec = uvl_perc / 100
        
        # Formula: UVL = 1 - exp(-lambda * Cin * vg * t)
        # t = -ln(1 - UVL) / (lambda * Cin * vg)
        t_seconds = -np.log(1 - uvl_dec) / (lambda_const * cin_kg_m3 * vg)
        df_days = t_seconds / 86400
        
        st.metric("Dusting Frequency (DF)", f"{int(df_days)} giorni")
        st.success(f"📅 Intervallo: {round(df_days/30, 1)} mesi")
    else:
        st.error("Inserisci una concentrazione > 0")
