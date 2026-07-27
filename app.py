import streamlit as st
import numpy as np

st.set_page_config(page_title="Heritage-Air Manager", layout="wide")

# --- MAIN APP TITLE ---
st.title("🏛️ Heritage-Air Manager")
st.markdown("Data-driven decision support tool for cultural heritage dust management")

# --- SIDEBAR: ENVIRONMENTAL PARAMETERS ---
st.sidebar.header("Environmental Parameters")
volume = st.sidebar.number_input("Room Volume [m³]", value=2200)
superficie = st.sidebar.number_input("Storage Surface Area [m²]", value=590)

# Vg changed to number_input with high precision step and support for scientific notation
vg_dust = st.sidebar.number_input(
    "Dust Settling Velocity (vg) [m/s]", 
    value=2.5e-5, 
    format="%.6f", 
    step=1.0e-6
)

# --- MAIN SECTION: SHINDLER MODEL (DUST) ---
st.header("🧹 Shindler Model (Dusting Frequency)")
st.markdown("Calculate the exact cleaning interval based on indoor particulate matter accumulation.")

# Layout with two clean columns for inputs and outputs
col_input, col_output = st.columns(2)

with col_input:
    st.subheader("Model Inputs")
    cin_pm = st.number_input("Indoor PM2.5 Concentration [µg/m³]", value=3.3)
    uvl_perc = st.slider("Unacceptable Visual Limit (UVL) [%]", 0.1, 1.0, 0.2)

with col_output:
    st.subheader("Calculated Conservation Metrics")
    
    if cin_pm > 0:
        uvl_dec = uvl_perc / 100
        
        # Calculate dynamic k factor scaled for days (Eq. 23 & mass conversion from paper)
        # Constants: D = 1.75e-6 m, rho_p = 1000 kg/m³
        lambda_shindler = (3 * vg_dust) / (2 * 1.75e-6 * 1000)
        k_dynamic = lambda_shindler * 1e-9 * 86400
        
        df_days = -np.log(1 - uvl_dec) / (k_dynamic * cin_pm)
        
        # Main results display
        st.metric("Dusting Frequency (DF)", f"{int(df_days)} days")
        st.success(f"📅 Recommended Cleaning Interval: {round(df_days/30, 1)} months")
        
        # Technical transparency caption
        st.caption(f"Calculated Kinetic Soiling Constant (k): {k_dynamic:.4e}")
    else:
        st.error("Please enter an indoor concentration value greater than 0")

# --- FOOTER & CONTACTS ---
st.sidebar.markdown("---")
st.sidebar.write("✉️ **Contact the Author**")
email_link = "mailto:luca@esempio.it?subject=Inquiry regarding Shindler Dust Model"
st.sidebar.markdown(f'<a href="{email_link}" style="background-color: #3498db; color: white; padding: 10px; border-radius: 5px; text-decoration: none; display: block; text-align: center;">Send Email</a>', unsafe_allow_html=True)

st.divider()
st.caption("Model developed by: Shindler, L., & Fabbri, K. (2026). DOI: 10.1016/j.jobe.2024.110595")


