
import streamlit as st
import CoolProp.CoolProp as CP

st.set_page_config(page_title="R407C Compressor Analysis", layout="centered")

st.title("🧊 R407C Compressor Thermodynamic Analysis")
st.markdown("This app calculates discharge temperature, enthalpy, and compressor power for a scroll compressor using R407C.")

# User Inputs
mass_flow = st.number_input("Mass Flow Rate (kg/s)", value=0.599, step=0.01)
power_input = st.number_input("Power Input (kW)", value=29.2, step=0.1)
eta_isen = st.slider("Isentropic Efficiency (%)", min_value=40, max_value=90, value=68) / 100
T_suction_C = st.number_input("Suction Gas Temperature (°C)", value=20.0, step=1.0)
T_evap_C = st.number_input("Evaporating Temperature (°C)", value=10.0, step=1.0)
T_cond_C = st.number_input("Condensing Dew Point Temperature (°C)", value=57.0, step=1.0)

# Thermodynamic Calculations
refrigerant = "R407C"
T_suction = T_suction_C + 273.15
T_evap = T_evap_C + 273.15
T_cond = T_cond_C + 273.15

try:
    P_suction = CP.PropsSI('P', 'T', T_evap, 'Q', 1, refrigerant)
    h1 = CP.PropsSI('H', 'P', P_suction, 'T', T_suction, refrigerant)
    s1 = CP.PropsSI('S', 'P', P_suction, 'T', T_suction, refrigerant)
    P_cond = CP.PropsSI('P', 'T', T_cond, 'Q', 1, refrigerant)
    h2s = CP.PropsSI('H', 'P', P_cond, 'S', s1, refrigerant)
    h2 = h1 + (h2s - h1) / eta_isen
    T_discharge = CP.PropsSI('T', 'P', P_cond, 'H', h2, refrigerant)
    calculated_power = mass_flow * (h2 - h1) / 1000  # kW

    # Output
    st.subheader("🔍 Results")
    st.write(f"**Suction Pressure:** {P_suction/1e5:.2f} bar abs")
    st.write(f"**Condensing Pressure:** {P_cond/1e5:.2f} bar abs")
    st.write(f"**Inlet Enthalpy:** {h1/1000:.2f} kJ/kg")
    st.write(f"**Isentropic Outlet Enthalpy:** {h2s/1000:.2f} kJ/kg")
    st.write(f"**Actual Outlet Enthalpy:** {h2/1000:.2f} kJ/kg")
    st.write(f"**Discharge Temperature:** {T_discharge - 273.15:.2f} °C")
    st.write(f"**Calculated Compressor Power:** {calculated_power:.2f} kW")

except Exception as e:
    st.error(f"Calculation failed: {e}")
