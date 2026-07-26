import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Vietnam Port", layout="wide")

st.title(" Vietnam Port Operations")

st.caption(
    "Estimate emissions generated during cargo handling and terminal operations in Vietnam."
)

st.divider()

# ------------------------------------------------
# INPUTS
# ------------------------------------------------

left, right = st.columns(2)

with left:

    containers = st.number_input(
        "Containers Handled (TEU)",
        min_value=0,
        value=240,
        step=10
    )

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / TEU)",
        min_value=0.0,
        value=18.0,
        step=1.0
    )

with right:

    electric_equipment = st.slider(
        "Electric Equipment Usage (%)",
        0,
        100,
        20
    )

    renewable_energy = st.slider(
        "Renewable Electricity (%)",
        0,
        100,
        10
    )

# ------------------------------------------------
# CALCULATIONS
# ------------------------------------------------

base_emissions = containers * emission_factor

equipment_reduction = electric_equipment * 0.002

renewable_reduction = renewable_energy * 0.002

emissions = base_emissions * (
    1
    - equipment_reduction
    - renewable_reduction
)

TOTAL_SUPPLY_CHAIN = 34200

share = emissions / TOTAL_SUPPLY_CHAIN * 100

# ------------------------------------------------
# KPI CARDS
# ------------------------------------------------

st.divider()

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Port Emissions",
        f"{emissions:,.0f} kg CO₂e"
    )

with c2:

    st.metric(
        "Share of Total",
        f"{share:.1f}%"
    )

with c3:

    st.metric(
        "Containers",
        containers
    )

# ------------------------------------------------
# GAUGE
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
# INTERPRETATION
# ------------------------------------------------

st.subheader("Interpretation")

if share > 10:

    st.warning(
        """
Vietnam port operations are a moderate contributor
to the total carbon footprint.
"""
    )

else:

    st.success(
        """
Vietnam port operations contribute a relatively
small portion of total emissions.
"""
    )

# ------------------------------------------------
# REDUCTION STRATEGIES
# ------------------------------------------------

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### ⚡ Electrify Cargo Equipment

Replace diesel cranes and yard vehicles
with electric alternatives.

Expected reduction:

**10–25%**
""")

    st.info("""
### ☀ Renewable Electricity

Increase renewable energy for terminal operations.

Expected reduction:

**5–20%**
""")

with col2:

    st.info("""
### Reduce Vessel Waiting Time

Improve scheduling to minimize idling.

Expected reduction:

**3–10%**
""")

    st.info("""
### Terminal Optimization

Improve cargo movement efficiency.

Expected reduction:

**2–8%**
""")

# ------------------------------------------------
# EXECUTIVE SUMMARY
# ------------------------------------------------

st.divider()

st.subheader("Executive Summary")

st.write(f"""
Current estimated emissions from Vietnam Port Operations are **{emissions:,.0f} kg CO₂e**.

This represents approximately **{share:.1f}%** of the total supply chain emissions.

Electrification of cargo handling equipment and increasing renewable electricity are the two largest opportunities for reducing emissions at this stage.
""")