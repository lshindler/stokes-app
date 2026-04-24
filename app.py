import streamlit as st
import numpy as np

st.set_page_config(page_title="Heritage-Air Manager", layout="wide")

st.title("🏛️ Heritage-Air Manager")
st.markdown("Basato sul modello Shindler et al. (2026)")

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
    sv_ratio = superficie / volume
    io_ratio = ach / (v_dep_gas * sv_ratio + ach)
    cin_gas = cout_gas * io_ratio
    st.metric("Conc. Interna Gas", f"{cin_gas:.2f} µg/m3")
    st.write(f"Rapporto I/O: {io_ratio:.3f}")

with col2:
    st.header("🧹 Modello Shindler (Polvere)")
    cin_pm = st.number_input("Conc. Interna PM2.5 [µg/m3]", value=3.3)
    uvl_perc = st.slider("Limite Visivo (UVL) [%]", 0.1, 1.0, 0.2)
    
    # --- CALCOLO DF (DUSTING FREQUENCY) ---
    if cin_pm > 0:
        # Parametri dal tuo paper
        uvl_target = uvl_perc / 100
        vg = 0.000025  # m/s (velocità di deposizione fisica)
        k_const = 0.5  # parametro di contrasto
        # La formula inversa per il tempo t (in secondi)
        # t = UVL / (k * Cin * vg)
        # Usiamo Cin in kg/m3 (Cin * 1e-9)
        cin_kg_m3 = cin_pm * 1e-9
        
        t_seconds = uvl_target / (k_const * cin_kg_m3 * vg)
        df_days = t_seconds / 86400
        
        st.metric("Dusting Frequency (DF)", f"{int(df_days)} giorni")
        
        if df_days > 30:
            st.success(f"📅 Prossima pulizia tra circa {round(df_days/30, 1)} mesi")
        else:
            st.warning(f"⚠️ Pulizia necessaria entro {int(df_days)} giorni!")
    else:
        st.error("Inserisci una concentrazione maggiore di zero.")
