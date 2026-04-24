import streamlit as st
import numpy as np

st.set_page_config(page_title="Heritage-Air Manager (IMPACT + Shindler Model)", layout="wide")

st.title("🏛️ Heritage-Air Manager")
st.markdown("Strumento integrato per la conservazione preventiva: Gas Reattivi e Spolveramento")

# --- SIDEBAR: PARAMETRI AMBIENTALI COMUNI ---
st.sidebar.header("Parametri Ambientali")
ach = st.sidebar.slider("Ricambio d'aria (ACH) [h-1]", 0.05, 2.0, 0.18)
volume = st.sidebar.number_input("Volume della stanza [m3]", value=2200)
superficie = st.sidebar.number_input("Superficie di deposito [m2]", value=590)
sv_ratio = superficie / volume

# --- LAYOUT A DUE COLONNE ---
col1, col2 = st.columns(2)

with col1:
    st.header("🧪 Modello Gas (IMPACT)")
    gas_type = st.selectbox("Seleziona Gas", ["NO2", "SO2", "O3"])
    # Velocità di deposizione chimica media (m/hr) - Valori tipici IMPACT
    v_dep_gas = st.slider("Vdep Chimica [m/hr]", 0.001, 0.1, 0.02)
    cout_gas = st.number_input(f"Conc. Esterna {gas_type} [µg/m3]", value=40.0)
    
    # Formula IMPACT: I/O = ach / (v_dep * (S/V) + ach)
    io_ratio = ach / (v_dep_gas * sv_ratio + ach)
    cin_gas = cout_gas * io_ratio
    
    st.metric(label=f"Conc. Interna Stimata {gas_type}", value=f"{cin_gas:.2f} µg/m3")
    st.write(f"Rapporto I/O: **{io_ratio:.3f}**")

with col2:
    st.header("🧹 Modello Polvere (Shindler)")
    metodo_pm = st.radio("Sorgente dati PM", ["Inserimento Manuale Cin", "Stima da Outdoor (Cout)"])
    
    if metodo_pm == "Inserimento Manuale Cin":
        cin_pm = st.number_input("Conc. Interna PM2.5 misurata [µg/m3]", value=3.3)
    else:
        cout_pm = st.number_input("Conc. Esterna PM2.5 [µg/m3]", value=15.0)
        p_coeff = st.slider("Coeff. Penetrazione (P)", 0.0, 1.0, 0.8)
        # Qui usiamo la tua v_g di Stokes per calcolare I/O del particolato
        v_g_stokes_hr = 0.000025 * 3600 # m/s -> m/hr (dal tuo paper)
        cin_pm = (ach * p_coeff * cout_pm) / (v_g_stokes_hr * sv_ratio + ach)

    uvl = st.slider("Unacceptable Visual Limit (UVL) [%]", 0.1, 1.0, 0.2) / 100
    
    # Calcolo Dusting Frequency (Formula 23 del tuo paper)
    # Nota: λ e K dipendono dai tuoi parametri del paper
    lambda_const = 1.06e05 # Esempio valore medio dal tuo paper
    df = np.log(1 - uvl) / (-lambda_const * (cin_pm * 1e-9) * 86400) # s -> giorni
    
    st.metric(label="Dusting Frequency (DF)", value=f"{int(df)} giorni")
    st.write(f"Prossima pulizia tra: **{int(df/30)} mesi**")

st.divider()
st.info("Questo strumento integra il modello di bilancio di massa (IMPACT) con la fisica di Stokes-Cunningham per lo spolveramento (Shindler & Fabbri, 2026).")
