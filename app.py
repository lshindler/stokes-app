import streamlit as st
import numpy as np

st.set_page_config(page_title="Heritage-Air Manager", layout="wide")

# --- MAIN APP TITLE ---
st.title("🏛️ Heritage-Air Manager")
st.markdown("Data-driven decision support tool for cultural heritage indoor conservation")

# --- SIDEBAR: ENVIRONMENTAL PARAMETERS ---
st.sidebar.header("Environmental Parameters")
ach = st.sidebar.slider("Air Changes per Hour (ACH) [h⁻¹]", 0.01, 2.0, 0.18)
volume = st.sidebar.number_input("Room Volume [m³]", value=2200)
superficie = st.sidebar.number_input("Storage Surface Area [m²]", value=590)

col1, col2 = st.columns(2)

# --- COLUMN 1: IMPACT MODEL (GAS) ---
with col1:
    st.header("🧪 IMPACT Model (Gas)")
    
    # Gas selection dropdown linked to standard Vdep values
    gas_scelto = st.selectbox(
        "Select Gas Pollutant",
        ["Custom", "Nitrogen Dioxide (NO₂)", "Ozone (O₃)", "Sulfur Dioxide (SO₂)", "Nitric Acid (HNO₃)"]
    )
    
    # Assigning default Vdep values based on literature
    default_vdep_gas = 0.020
    if gas_scelto == "Nitrogen Dioxide (NO₂)":
        default_vdep_gas = 0.020
    elif gas_scelto == "Ozone (O₃)":
        default_vdep_gas = 0.070
    elif gas_scelto == "Sulfur Dioxide (SO₂)":
        default_vdep_gas = 0.040
    elif gas_scelto == "Nitric Acid (HNO₃)":
        default_vdep_gas = 0.200

    v_dep_gas = st.slider("Deposition Velocity (Vdep) [m/hr]", 0.001, 0.5, default_vdep_gas, format="%.3f")
    cout_gas = st.number_input("Outdoor Gas Conc. [µg/m³]", value=40.0)
    
    # IMPACT model steady-state formula
    io_ratio = ach / (v_dep_gas * (superficie/volume) + ach)
    cin_gas = cout_gas * io_ratio
    
    # Results display
    st.metric("Penetration Factor (I/O Ratio)", f"{round(io_ratio * 100, 1)}%")
    st.metric("Estimated Indoor Gas Conc.", f"{cin_gas:.2f} µg/m³")
    
    st.info(f"💡 **Dynamic Info:** Given the room parameters, **{round(io_ratio * 100, 1)}%** of outdoor {gas_scelto if gas_scelto != 'Custom' else 'gas'} remains suspended indoors.")

# --- COLUMN 2: SHINDLER MODEL (DUST) ---
with col2:
    st.header("🧹 Shindler Model (Dust)")
    cin_pm = st.number_input("Indoor PM2.5 Conc. [µg/m³]", value=3.3)
    uvl_perc = st.slider("Unacceptable Visual Limit (UVL) [%]", 0.1, 1.0, 0.2)
    
    # Only Vdep as input, initialized with the paper's validated baseline (2.5e-5 m/s)
    vg_dust = st.slider("Dust Settling Velocity (vg) [m/s]", 1.0e-5, 5.0e-5, 2.5e-5, format="%.2e")
    
    if cin_pm > 0:
        uvl_dec = uvl_perc / 100
        
        # Calculate dynamic k factor scaled for days (Eq. 23 & mass conversion)
        # Baseline variables from paper: D = 1.75e-6 m, rho_p = 1000 kg/m³
        lambda_shindler = (3 * vg_dust) / (2 * 1.75e-6 * 1000)
        k_dynamic = lambda_shindler * 1e-9 * 86400
        
        df_days = -np.log(1 - uvl_dec) / (k_dynamic * cin_pm)
        
        # Results display
        st.metric("Dusting Frequency (DF)", f"{int(df_days)} days")
        st.success(f"📅 Cleaning Interval: {round(df_days/30, 1)} months")
        
        st.caption(f"Calculated Kinetic Soiling Constant (k): {k_dynamic:.4e}")
    else:
        st.error("Please enter a concentration value greater than 0")

# --- FOOTER & CONTACTS ---
st.sidebar.markdown("---")
st.sidebar.write("✉️ **Contact the Consultant**")
email_link = "mailto:luca@esempio.it?subject=Consulting Request - Shindler Model"
st.sidebar.markdown(f'<a href="{email_link}" style="background-color: #3498db; color: white; padding: 10px; border-radius: 5px; text-decoration: none; display: block; text-align: center;">Send Email</a>', unsafe_allow_html=True)

st.divider()
st.caption("Model based on: Shindler, L., & Fabbri, K. (2026). DOI: 10.1016/j.jobe.2024.110595")
