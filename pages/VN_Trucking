import streamlit as st
import plotly.graph_objects as go

st.title("🚚 Vietnam Trucking")

st.caption(
    "Factory-to-port trucking emissions in Vietnam."
)

st.divider()

left, right = st.columns(2)

with left:

    distance = st.number_input(
        "Distance (km)",
        min_value=0.0,
        value=120.0,
        step=10.0
    )

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / ton-km)",
        min_value=0.0,
        value=0.12,
        step=0.01
    )

with right:

    cargo_weight = st.number_input(
        "Cargo Weight (tons)",
        min_value=0.0,
        value=5000.0,
        step=100.0
    )

    load_factor = st.slider(
        "Truck Utilization (%)",
        50,
        100,
        80
    )

# ------------------------------------------------
# Calculation
# ------------------------------------------------

base = distance * cargo_weight * emission_factor

utilization_reduction = (load_factor - 50) * 0.004

emissions = base * (1 - utilization_reduction)

TOTAL_SUPPLY_CHAIN = 34200

share = emissions / TOTAL_SUPPLY_CHAIN * 100

# ------------------------------------------------
# Metrics
# ------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "VN Truck Emissions",
        f"{emissions:,.0f} kg CO₂e"
    )

with c2:
    st.metric(
        "Share of Total",
        f"{share:.1f}%"
    )

with c3:
    st.metric(
        "Truck Utilization",
        f"{load_factor}%"
    )

st.divider()

# ------------------------------------------------
# Gauge
# ------------------------------------------------

fig = go.Figure(go.Indicator(

    mode="gauge+number",

    value=share,

    number={"suffix":"%"},

    gauge={

        "axis":{"range":[0,100]},

        "bar":{"color":"green"},

        "steps":[

            {"range":[0,20],"color":"#14532d"},
            {"range":[20,40],"color":"#166534"},
            {"range":[40,60],"color":"#facc15"},
            {"range":[60,80],"color":"#f97316"},
            {"range":[80,100],"color":"#dc2626"}

        ]

    }

))

fig.update_layout(
    paper_bgcolor="#0f172a",
    font_color="white",
    height=350
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------------------------------
# Interpretation
# ------------------------------------------------

st.subheader("Interpretation")

if share > 25:

    st.error(
        "Vietnam trucking is a major contributor to emissions."
    )

elif share > 10:

    st.warning(
        "Vietnam trucking contributes a moderate amount of emissions."
    )

else:

    st.success(
        "Vietnam trucking is a relatively small contributor."
    )

# ------------------------------------------------
# Reduction Opportunities
# ------------------------------------------------

st.subheader("Emission Reduction Opportunities")

st.info(
"""
### 🚛 Increase Load Factor

Higher truck utilization means fewer trips are required.

Expected reduction:

**5–20%**
"""
)

st.info(
"""
### 🛣 Route Optimization

Shorter routes directly reduce fuel consumption.

Expected reduction:

**3–15%**
"""
)

st.info(
"""
### ⚡ Alternative Fuel Trucks

Use lower-carbon fuel options where available.

Expected reduction:

**10–30%**
"""
)