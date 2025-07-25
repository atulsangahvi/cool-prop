
import CoolProp.CoolProp as CP

def compressor_thermo_analysis():
    # Refrigerant and inputs
    refrigerant = 'R407C'
    mass_flow = 0.599  # kg/s
    power_input = 29.2  # kW
    eta_isen = 0.6797

    # Suction conditions
    T_suction = 20 + 273.15  # K
    T_evap = 10 + 273.15  # K
    P_suction = CP.PropsSI('P', 'T', T_evap, 'Q', 1, refrigerant)
    h1 = CP.PropsSI('H', 'P', P_suction, 'T', T_suction, refrigerant)
    s1 = CP.PropsSI('S', 'P', P_suction, 'T', T_suction, refrigerant)

    # Condensing pressure at dew point 57°C
    P_cond = CP.PropsSI('P', 'T', 57 + 273.15, 'Q', 1, refrigerant)
    h2s = CP.PropsSI('H', 'P', P_cond, 'S', s1, refrigerant)

    # Actual outlet enthalpy
    h2 = h1 + (h2s - h1) / eta_isen
    T_discharge = CP.PropsSI('T', 'P', P_cond, 'H', h2, refrigerant)
    actual_power = mass_flow * (h2 - h1) / 1000

    # Display results
    print(f"Suction Pressure: {P_suction / 1e5:.2f} bar")
    print(f"Condensing Pressure: {P_cond / 1e5:.2f} bar")
    print(f"Inlet Enthalpy: {h1 / 1000:.2f} kJ/kg")
    print(f"Isentropic Outlet Enthalpy: {h2s / 1000:.2f} kJ/kg")
    print(f"Actual Outlet Enthalpy: {h2 / 1000:.2f} kJ/kg")
    print(f"Discharge Temperature: {T_discharge - 273.15:.2f} °C")
    print(f"Calculated Compressor Power: {actual_power:.2f} kW")

if __name__ == "__main__":
    compressor_thermo_analysis()
