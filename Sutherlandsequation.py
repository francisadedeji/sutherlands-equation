import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title and description
st.title("Sutherland's Equation Viscosity Calculator by Francis Adedeji")
st.markdown(
    """
    Calculate the dynamic viscosity of air based on temperature using Sutherland's formula.  
    Choose your preferred unit system (SI or USC) and input the temperature.  
    You can also plot viscosity vs. temperature from sea-level reference up to your input.
    """
)

# 1. Define Sutherland constants for each unit system
#    - t_ref: reference temperature
#    - s: Sutherland's constant
#    - v_ref: reference viscosity

# SI constants (Kelvin, kg/m·s)
T_REF_SI = 323.0
S_SI = 110.0
V_REF_SI = 1.716e-5

# USC constants (Rankine, slug/ft·s)
T_REF_USC = 518.67
S_USC = 198.72
V_REF_USC = 3.737e-7

# 2. Temperature conversion functions

def to_kelvin(value: float, unit: str) -> float:
    if unit == 'C':
        return value + 273.15
    elif unit == 'F':
        return (value - 32) * 5/9 + 273.15
    elif unit == 'K':
        return value
    elif unit == 'R':
        return value * 5/9
    else:
        raise ValueError(f"Unsupported unit: {unit}")


def to_rankine(value: float, unit: str) -> float:
    if unit == 'C':
        return (value * 9/5) + 491.67
    elif unit == 'F':
        return value + 459.67
    elif unit == 'K':
        return value * 9/5
    elif unit == 'R':
        return value
    else:
        raise ValueError(f"Unsupported unit: {unit}")

# 3. Viscosity calculation using Sutherland's formula

def sutherland_viscosity(temp: float, t_ref: float, s: float, v_ref: float) -> float:
    return v_ref * (temp / t_ref) ** 1.5 * (t_ref + s) / (temp + s)

# 4. Streamlit sidebar for user interaction
unit_system = st.sidebar.radio("Select unit system:", ("SI", "USC"))

# Choose temperature unit based on system
temp_unit = st.sidebar.selectbox(
    f"Temperature unit ({unit_system}):", ['C', 'F', 'K', 'R'],
    index=0 if unit_system=='SI' else 3
)

# Input temperature value
temp_input = st.sidebar.number_input(
    f"Enter temperature in {temp_unit} (°{temp_unit}):", format="%f", value=0.0
)

# Button to trigger calculation and plotting
if st.sidebar.button("Calculate"):
    # 5. Perform conversions and calculations
    if unit_system == "SI":
        T = to_kelvin(temp_input, temp_unit)
        base_temp = to_kelvin(15.0, 'C')  # sea-level reference 15°C
        viscosity = sutherland_viscosity(T, T_REF_SI, S_SI, V_REF_SI)
        unit_label = "K"
        ref = (T_REF_SI, S_SI, V_REF_SI)
    else:
        T = to_rankine(temp_input, temp_unit)
        base_temp = to_rankine(15.0, 'C')  # convert 15°C to R for USC
        viscosity = sutherland_viscosity(T, T_REF_USC, S_USC, V_REF_USC)
        unit_label = "R"
        ref = (T_REF_USC, S_USC, V_REF_USC)

    # Display results
    st.write(f"**Converted Temperature:** {T:.2f} {unit_label}")
    if unit_system == "SI":
        st.write(f"**Dynamic Viscosity (SI):** {viscosity:.6e} kg·m⁻¹·s⁻¹")
    else:
        st.write(f"**Dynamic Viscosity (USC):** {viscosity:.6e} slug·ft⁻¹·s⁻¹")

    # 6. Prepare data for plotting
    temps = np.linspace(base_temp, T, 100)
    mu = [sutherland_viscosity(t, ref[0], ref[1], ref[2]) for t in temps]

    # 7. Plot viscosity vs. temperature
    fig, ax = plt.subplots()
    ax.plot(temps, mu)
    ax.set_xlabel(f"Temperature ({unit_label})")
    ax.set_ylabel("Viscosity")
    ax.set_title("Viscosity vs. Temperature")
    ax.grid(True)
    st.pyplot(fig)

# 8. Help section
st.markdown("---")
st.markdown(
    "### How it works:\n"
    "1. Select unit system (SI or USC) and temperature unit.\n"
    "2. Enter your temperature.\n"
    "3. Click **Calculate** to see converted temperature, viscosity, and a plot from sea-level reference (15°C)."
)
