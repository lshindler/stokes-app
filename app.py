import streamlit as st
import numpy as np

st.set_page_config(page_title="Heritage-Air Manager", layout="wide")

# --- LOGIN ---
st.sidebar.title("🔐 Accesso Riservato")
pwd = st.sidebar.text_input("Password Progetto", type="password")

if pwd != "Angelica2026": # CAMBIA QUI LA TUA PASSWORD
    st.title("🏛️ Heritage-Air Manager")
    st.info("Benvenuto. Inserisci la password nella sidebar per accedere ai calcoli del modello Fabbri/Shindler.")
    st.stop()

# --- APP PRINCIPALE (Se la password è corretta) ---
st.title("🏛️ Heritage-Air Manager")
st.markdown("Strumento di supporto alle decisioni per la manutenzione dei Beni Culturali")

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
        uvl_dec = uvl_perc / 100
        k_shindler = 2.63e-06 
        df_days = -np.log(1 - uvl_dec) / (k_shindler * cin_pm)
        st.metric("Dusting Frequency (DF)", f"{int(df_days)} giorni")
        st.success(f"📅 Intervallo: {round(df_days/30, 1)} mesi")
    else:
        st.error("Inserisci una concentrazione > 0")

# --- FOOTER E CONTATTI ---
st.sidebar.markdown("---")
st.sidebar.write("✉️ **Contatta il Consulente**")
email_link = "mailto:luca@esempio.it?subject=Richiesta Consulenza Shindler Model"
st.sidebar.markdown(f'<a href="{email_link}" style="background-color: #3498db; color: white; padding: 10px; border-radius: 5px; text-decoration: none; display: block; text-align: center;">Invia Email</a>', unsafe_allow_html=True)

st.divider()
st.caption("Modello basato su: Shindler, L., & Fabbri, K. (2026). DOI: 10.1016/j.jobe.2024.110595")
