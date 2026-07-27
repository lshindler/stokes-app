import streamlit as st
import numpy as np

st.set_page_config(page_title="Heritage-Air Manager", layout="wide")

# --- MAIN APP TITLE ---
st.title("🏛️ Heritage-Air Manager")
st.markdown("Data-driven decision support tool for cultural heritage dust management")

# --- SIDEBAR: ROOM GEOMETRY ---
st.sidebar.header("Room Geometry")
volume = st.sidebar.number_input("Room Volume (V) [m³]", value=2200)
superficie = st.sidebar.number_input("Storage Surface Area to Dust (S) [m²]", value=590, help="Total area of book spines or vertical surfaces requiring cleaning.")

if volume > 0:
    sv_ratio = superficie / volume
    st.sidebar.text(f"Calculated S/V Ratio: {sv_ratio:.2f} m⁻¹")

# --- MAIN SECTION: SHINDLER MODEL (DUST) ---
st.header("🧹 Shindler Model (Dusting Frequency)")
st.markdown("Calculate the exact cleaning interval based on indoor particulate matter accumulation.")

# Layout with two clean columns for inputs and outputs
col_input, col_output = st.columns(2)

with col_input:
    st.subheader("Model Inputs")
    cin_pm = st.number_input("Indoor PM2.5 Concentration (Cm) [µg/m³]", value=3.3)
    uvl_perc = st.slider("Unacceptable Visual Limit (UVL) [%]", 0.1, 1.0, 0.2)
    
    st.markdown("---")
    st.caption("**Model Physics Constants (Baseline values from paper)**")
    lambda_param = st.number_input(
        "Dose-Response Constant (λ) [m³/(µg·s)]", 
        value=3.0e-11, 
        format="%.1e",
        help="Average value derived from deposition velocity, particle density, and diameter."
    )

with col_output:
    st.subheader("Calculated Conservation Metrics")
    
    if cin_pm > 0 and lambda_param > 0:
        uvl_dec = uvl_perc / 100
        k_soiling = lambda_param * cin_pm
        
        # Exact paper formulas (sec -> hr -> days)
        df_seconds = -np.log(1 - uvl_dec) / k_soiling
        df_hours_limit = df_seconds / 3600
        df_days = df_hours_limit / 24
        
        # Main results display
        st.metric("Dusting Frequency (DF)", f"{int(df_days)} days")
        st.success(f"📅 Recommended Cleaning Interval: {round(df_days/30, 1)} months")
        st.caption(f"Calculated Soiling Constant (K): {k_soiling:.4e} s⁻¹")
    else:
        st.error("Please ensure both Concentration and Lambda are greater than 0")

# --- NEW SECTION: MAINTENANCE & STAFF PLANNING ---
st.divider()
st.header("📋 Maintenance & Staff Planning")
st.markdown("Estimate required resources and weekly schedules based on the calculated Dusting Frequency.")

if cin_pm > 0 and lambda_param > 0 and superficie > 0:
    col_staff_in, col_staff_out = st.columns(2)
    
    with col_staff_in:
        st.subheader("Cleaning Parameters")
        time_per_m2 = st.number_input("Average dusting time per m² [minutes]", value=3, min_value=1)
        hours_per_day = st.slider("Dusting allocation [hours/day]", 0.5, 8.0, 1.0, step=0.5)
        days_per_week = st.slider("Cleaning days per week", 1, 7, 4)
        
    with col_staff_out:
        st.subheader("Resource Estimation")
        
        # Calculations based on paper text logic
        total_minutes = superficie * time_per_m2
        total_hours_needed = total_minutes / 60
        
        weekly_allocated_hours = hours_per_day * days_per_week
        weeks_to_complete_cycle = total_hours_needed / weekly_allocated_hours if weekly_allocated_hours > 0 else 0
        
        # Maximum allowed gap check: the library must not be neglected more than DF
        required_hours_per_week_to_match_df = (total_hours_needed / df_days) * 7
        
        # Output Metrics
        st.metric("Total Cleaning Effort (Full Cycle)", f"{int(total_hours_needed)} hours")
        st.info(f"⏳ Time to complete one full library cycle with current schedule: **{round(weeks_to_complete_cycle, 1)} weeks**")
        
        # Operational warning/guidance based on your paper text
        if weekly_allocated_hours < required_hours_per_week_to_match_df:
            st.error(f"⚠️ **Warning**: The current cleaning rate ({weekly_allocated_hours} h/week) is too slow. To prevent exceeding the UVL threshold within {int(df_days)} days, staff must dedicate at least **{required_hours_per_week_to_match_df:.1f} hours per week** to dusting.")
        else:
            st.success(f"✅ **Safe Schedule**: This routine ensures the library will not be neglected for more than {round(df_days/30, 1)} months, meeting your conservation targets.")

# --- FOOTER & CONTACTS ---
st.sidebar.markdown("---")
st.sidebar.write("✉️ **Contact the Author**")
email_link = "mailto:shindler@sogin.it?subject=Inquiry regarding Shindler Dust Model"
st.sidebar.markdown(f'<a href="{email_link}" style="background-color: #3498db; color: white; padding: 10px; border-radius: 5px; text-decoration: none; display: block; text-align: center;">Send Email</a>', unsafe_allow_html=True)

st.divider()
st.caption("Model developed by: Shindler, L., & Fabbri, K. (2026). DOI: 10.1016/j.jobe.2024.110595")




